from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentMetadata, ValidationMessage


PLACEHOLDER_RE = re.compile(r"@@PH\d+@@")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+", re.MULTILINE)


def validate_markdown(markdown: str, source_dir: Path) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []

    previous_level: int | None = None
    for match in HEADING_RE.finditer(markdown):
        level = len(match.group(1))
        if previous_level is not None and level > previous_level + 1:
            messages.append(
                ValidationMessage(
                    "warning",
                    f"Nível de título salta de H{previous_level} para H{level}.",
                    "markdown",
                )
            )
        previous_level = level

    for image in IMAGE_RE.findall(markdown):
        if image.startswith(("http://", "https://", "data:")):
            continue
        path = (source_dir / image).resolve()
        if not path.exists():
            messages.append(
                ValidationMessage("warning", f"Imagem não encontrada: {image}", "markdown")
            )

    return messages


def validate_metadata(metadata: DocumentMetadata, profile: str) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []
    if not metadata.title.strip():
        messages.append(ValidationMessage("error", "O documento não possui título.", "metadata"))
    if profile == "meeting-minutes" and not metadata.date.strip():
        messages.append(
            ValidationMessage("warning", "Memória de reunião sem data.", "metadata")
        )
    if profile in {"report", "technical-plan"} and not metadata.version.strip():
        messages.append(
            ValidationMessage("warning", "Documento sem versão.", "metadata")
        )
    return messages


def validate_tex(tex: str) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []
    placeholders = sorted(set(PLACEHOLDER_RE.findall(tex)))
    if placeholders:
        messages.append(
            ValidationMessage(
                "error",
                "Placeholders internos não resolvidos: " + ", ".join(placeholders),
                "tex",
            )
        )
    if "\\begin{document}" not in tex or "\\end{document}" not in tex:
        messages.append(
            ValidationMessage("error", "Documento TEX incompleto.", "tex")
        )
    return messages


def validate_log(log_text: str) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []
    latex_errors = re.findall(r"^!(?:[^\n]+\n?){1,3}", log_text, re.MULTILINE)
    if latex_errors:
        for err in latex_errors[:5]:
            cleaned_err = " ".join(err.strip().splitlines())
            messages.append(ValidationMessage("error", f"Erro LaTeX: {cleaned_err}", "latex"))
    elif re.search(r"^! LaTeX Error:", log_text, re.MULTILINE):
        messages.append(ValidationMessage("error", "O log contém erro LaTeX.", "latex"))

    if "There were undefined references" in log_text:
        messages.append(
            ValidationMessage("warning", "Há referências internas não resolvidas.", "latex")
        )
    if "There were undefined citations" in log_text:
        messages.append(
            ValidationMessage("warning", "Há citações não resolvidas.", "latex")
        )
    overfull = len(re.findall(r"Overfull \\hbox", log_text))
    if overfull:
        messages.append(
            ValidationMessage(
                "warning", f"Foram encontrados {overfull} avisos de Overfull \\hbox.", "latex"
            )
        )
    return messages


def has_errors(messages: list[ValidationMessage]) -> bool:
    return any(message.level == "error" for message in messages)
