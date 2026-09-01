from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .models import DocumentMetadata, ValidationMessage

PLACEHOLDER_RE = re.compile(r"@@PH\d+@@")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
ATX_HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
SETEXT_UNDERLINE_RE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def extract_headings(markdown: str) -> set[str]:
    """Retorna títulos ATX/Setext normalizados, ignorando blocos fenced."""
    headings: set[str] = set()
    in_fence: str | None = None
    previous_line: str | None = None
    for line in markdown.splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if in_fence is None:
                in_fence = marker[0]
            elif marker[0] == in_fence:
                in_fence = None
            previous_line = None
            continue
        if in_fence is not None:
            continue
        atx = ATX_HEADING_RE.match(line)
        if atx:
            headings.add(atx.group(1).strip().casefold())
            previous_line = None
            continue
        if SETEXT_UNDERLINE_RE.match(line) and previous_line and previous_line.strip():
            headings.add(previous_line.strip().casefold())
            previous_line = None
            continue
        previous_line = line
    return headings


def missing_required_topics(markdown: str, required_topics: list[str]) -> list[str]:
    """Preserva o texto configurado para cada tópico obrigatório ausente."""
    headings = extract_headings(markdown)
    return [topic for topic in required_topics if topic.strip().casefold() not in headings]


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


MEETING_MINUTES_SECTIONS = (
    "Objetivos da Reunião",
    "Tópicos Abordados",
    "Considerações Gerais e Definições",
    "Pendências",
)
PENDENCY_COLUMNS = ("Pendência", "Responsável", "Prazo para Solução")


def validate_meeting_minutes(raw: dict[str, Any], body: str) -> list[ValidationMessage]:
    """Valida o contrato de entrada do perfil ``meeting-minutes``."""
    messages: list[ValidationMessage] = []
    for field in ("client", "author", "date"):
        if not _non_empty_text(raw.get(field)):
            messages.append(_meeting_message(field))

    period = raw.get("period")
    if not isinstance(period, dict):
        messages.extend([_meeting_message("period.start"), _meeting_message("period.end")])
    else:
        for field in ("start", "end"):
            if not _non_empty_text(period.get(field)):
                messages.append(_meeting_message(f"period.{field}"))

    messages.extend(_validate_participants(raw.get("participants")))
    sections = _meeting_sections(body)
    for section in MEETING_MINUTES_SECTIONS:
        if not sections.get(section.casefold(), "").strip():
            messages.append(_meeting_message(section))

    pending_content = sections.get("pendências", "")
    if pending_content.strip():
        messages.extend(_validate_pendencies(pending_content))
    return messages


def _validate_participants(value: Any) -> list[ValidationMessage]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [_meeting_message("participants")]

    messages: list[ValidationMessage] = []
    for group, participants in value.items():
        path = f"participants.{group}"
        if group not in {"client", "netra"} or not isinstance(participants, list):
            messages.append(_meeting_message(path))
            continue
        for index, participant in enumerate(participants):
            item_path = f"{path}[{index}]"
            if not isinstance(participant, dict):
                messages.append(_meeting_message(item_path))
                continue
            for field in ("name", "role"):
                if not _non_empty_text(participant.get(field)):
                    messages.append(_meeting_message(f"{item_path}.{field}"))
            for field in participant.keys() - {"name", "role"}:
                messages.append(_meeting_message(f"{item_path}.{field}"))
    return messages


def _meeting_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", body, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1).strip().casefold()] = body[match.end():end].strip()
    return sections


def _validate_pendencies(content: str) -> list[ValidationMessage]:
    if content.strip() == "Sem pendências":
        return []
    rows = [line.strip() for line in content.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return [_meeting_message("Pendências")]
    headers = _table_cells(rows[0])
    if tuple(headers) != PENDENCY_COLUMNS:
        return [_meeting_message("Pendências")]
    messages: list[ValidationMessage] = []
    for row_number, row in enumerate(rows[2:], start=1):
        cells = _table_cells(row)
        if len(cells) != len(PENDENCY_COLUMNS):
            messages.append(_meeting_message(f"Pendências[{row_number}]"))
            continue
        for column, value in zip(PENDENCY_COLUMNS, cells):
            if not value.strip():
                messages.append(_meeting_message(f"Pendências[{row_number}].{column}"))
    return messages


def _table_cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _non_empty_text(value: Any) -> bool:
    return value is not None and not isinstance(value, (dict, list, tuple, set)) and bool(str(value).strip())


def _meeting_message(path: str) -> ValidationMessage:
    return ValidationMessage("warning", f"Memória de reunião: campo ou seção inválida: {path}.", "meeting-minutes")


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
    option_clash = re.search(r"^! LaTeX Error: Option clash for package ([^.]+)\.", log_text, re.MULTILINE)
    if option_clash:
        package = option_clash.group(1)
        messages.append(
            ValidationMessage(
                "error",
                f"Configuração: conflito de opções no pacote {package}. Um arquivo .sty pode já carregá-lo; "
                "remova o pacote duplicado de style_packages. Para geometry, use page_geometry: {} quando o .sty definir as margens.",
                "latex",
            )
        )
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
