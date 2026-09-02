from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .models import DocumentMetadata, UserConfig


def latex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def render_template(
    template_path: Path,
    *,
    metadata: DocumentMetadata,
    body: str,
    user_config: UserConfig,
    toc: bool = True,
    engine: str,
    used_svg: bool,
    source_dir: Path,
    meeting_minutes: object | None = None,
) -> str:
    environment = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        variable_start_string="((*",
        variable_end_string="*))",
        block_start_string="((%",
        block_end_string="%))",
        comment_start_string="((#",
        comment_end_string="#))",
    )
    environment.filters["latex"] = latex_escape
    template = environment.get_template(template_path.name)
    return template.render(
        metadata=metadata,
        body=body,
        user_config=user_config,
        toc=toc,
        engine=engine,
        meeting_minutes=meeting_minutes,
        used_svg=used_svg,
        source_dir=source_dir.as_posix().rstrip("/") + "/",
    )
