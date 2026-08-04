from __future__ import annotations

import json
from pathlib import Path

from .errors import DependencyError, Md2TexError
from .utils import executable, run_command


PANDOC_FROM = (
    "markdown"
    "+yaml_metadata_block"
    "+fenced_divs"
    "+pipe_tables"
    "+grid_tables"
    "+footnotes"
    "+strikeout"
    "+task_lists"
    "+link_attributes"
    "+fenced_code_attributes"
    "+raw_tex"
)


def markdown_to_latex_fragment(
    markdown_path: Path,
    *,
    lua_filter: Path,
    landscape_tables: str,
    table_font: str,
    table_width: str,
    source_dir: Path,
    verbose: bool,
) -> str:
    pandoc = executable("pandoc")
    if not pandoc:
        raise DependencyError(
            "Pandoc não encontrado. Instale com: sudo apt install pandoc"
        )

    metadata_file = markdown_path.parent / "pandoc-metadata.json"
    metadata_file.write_text(
        json.dumps(
            {
                "md2tex-landscape-tables": landscape_tables,
                "md2tex-wrap-tables": True,
                "md2tex-table-font": table_font,
                "md2tex-table-width": table_width,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    command = [
        pandoc,
        str(markdown_path),
        "--from",
        PANDOC_FROM,
        "--to",
        "latex",
        "--wrap=none",
        "--no-highlight",
        "--top-level-division=section",
        "--lua-filter",
        str(lua_filter),
        "--metadata-file",
        str(metadata_file),
        "--resource-path",
        str(source_dir),
    ]
    process = run_command(command, cwd=source_dir, verbose=verbose, check=False)
    if process.returncode != 0:
        details = process.stderr.strip() or process.stdout.strip()
        raise Md2TexError(f"Pandoc falhou ao converter o Markdown:\n{details}")
    return (
        process.stdout
        .replace(r"\st{", r"\sout{")
        .replace(r"\raggedright", r"\RaggedRight")
    )
