from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .models import ValidationMessage
from .utils import executable, run_command


MERMAID_RE = re.compile(
    r"(?ms)^```mermaid(?:\s+\{(?P<attrs>[^}]*)\})?\s*\n"
    r"(?P<code>.*?)\n```\s*$"
)

ATTR_RE = re.compile(r"(?P<key>[\w-]+)=(?:\"(?P<quoted>[^\"]*)\"|'(?P<single>[^']*)'|(?P<bare>\S+))")


@dataclass(slots=True)
class MermaidResult:
    markdown: str
    messages: list[ValidationMessage]
    used_svg: bool = False


def render_mermaid_blocks(
    markdown: str,
    *,
    source_dir: Path,
    figures_dir: Path,
    output_format: str,
    enabled: bool,
    strict: bool,
    verbose: bool,
) -> MermaidResult:
    messages: list[ValidationMessage] = []
    if not enabled or "```mermaid" not in markdown:
        return MermaidResult(markdown, messages)

    mmdc = executable("mmdc")
    if not mmdc:
        message = (
            "Mermaid CLI (mmdc) não encontrado; os blocos Mermaid foram mantidos como código. "
            "Instale com: npm install -g @mermaid-js/mermaid-cli"
        )
        level = "error" if strict else "warning"
        messages.append(ValidationMessage(level, message, "mermaid"))
        return MermaidResult(markdown, messages)

    absolute_figures = figures_dir if figures_dir.is_absolute() else source_dir / figures_dir
    absolute_figures.mkdir(parents=True, exist_ok=True)
    used_svg = False

    def replace(match: re.Match[str]) -> str:
        nonlocal used_svg
        attrs = _parse_attrs(match.group("attrs") or "")
        code = match.group("code").strip() + "\n"
        digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]
        basename = attrs.get("name") or attrs.get("id") or f"diagram-{digest}"
        basename = re.sub(r"[^A-Za-z0-9_.-]", "-", basename).strip("-") or f"diagram-{digest}"
        target = absolute_figures / f"{basename}.{output_format}"
        source = absolute_figures / f".{basename}.mmd"
        source.write_text(code, encoding="utf-8")
        command = [mmdc, "-i", str(source), "-o", str(target), "-b", "transparent"]
        process = run_command(command, cwd=source_dir, verbose=verbose, check=False)
        try:
            source.unlink(missing_ok=True)
        except OSError:
            pass
        if process.returncode != 0:
            text = process.stderr.strip() or process.stdout.strip()
            messages.append(
                ValidationMessage(
                    "error" if strict else "warning",
                    f"Falha ao renderizar Mermaid: {text}",
                    basename,
                )
            )
            return match.group(0)

        caption = attrs.get("caption") or attrs.get("title") or "Diagrama"
        width = attrs.get("width", "95%")
        height = attrs.get("height", "78%")
        relative = target.relative_to(source_dir) if target.is_relative_to(source_dir) else target
        if output_format == "svg":
            used_svg = True
        return (
            f"![{caption}]({relative.as_posix()})"
            f"{{width={width} height={height}}}"
        )

    converted = MERMAID_RE.sub(replace, markdown)
    return MermaidResult(converted, messages, used_svg)


def _parse_attrs(raw: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for match in ATTR_RE.finditer(raw):
        attrs[match.group("key")] = (
            match.group("quoted") or match.group("single") or match.group("bare") or ""
        )
    return attrs
