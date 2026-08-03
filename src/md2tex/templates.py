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
    style_path: str | None = None,
    user_config: UserConfig | None = None,
    toc: bool = True,
    engine: str = "pdflatex",
    used_svg: bool = False,
    source_dir: Path,
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
        style_path=style_path,
        user_config=user_config,
        toc=toc,
        engine=engine,
        used_svg=used_svg,
        source_dir=source_dir.as_posix().rstrip("/") + "/",
    )
