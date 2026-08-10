from __future__ import annotations

import json
import re
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
    table_borders: str,
    table_zebra: bool,
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
                "md2tex-table-zebra": table_zebra,
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
    fragment = (
        process.stdout
        .replace(r"\st{", r"\sout{")
        .replace(r"\raggedright", r"\RaggedRight")
    )
    return apply_table_borders(fragment, table_borders)


LONGTABLE_RE = re.compile(
    r"(?P<start>\\begin\{longtable\}\[\]\{)(?P<spec>.*?)(?P<rules>\n\\toprule\\noalign\{\}.*?\\end\{longtable\})",
    re.DOTALL,
)


def apply_table_borders(fragment: str, mode: str) -> str:
    """Aplica contornos às tabelas longtable emitidas pelo Pandoc."""
    if mode == "none":
        return fragment

    def format_table(match: re.Match[str]) -> str:
        spec = match.group("spec")
        rules = match.group("rules")
        if spec.startswith("@{}"):
            spec = "|" + spec[3:]
        if spec.endswith("@{}}"):
            spec = spec[:-4] + "|}"
        elif spec.endswith("@{}"):
            spec = spec[:-3] + "|"
        if mode == "grid":
            spec = re.sub(r"(\})\n(\s*>\{)", r"\1|\n\2", spec)
            rules = rules.replace(r"\toprule\noalign{}", r"\hline")
            rules = rules.replace(r"\midrule\noalign{}", r"\hline")
            rules = rules.replace(r"\bottomrule\noalign{}", r"\hline")
            head, separator, body = rules.partition("\\endlastfoot\n")
            if separator:
                body = re.sub(
                    r"\\\\\n(?!(?:\\hline|\\end\{longtable\}))",
                    lambda _: "\\\\" + r"\hline" + "\n",
                    body,
                )
                body = body.replace(r"\end{longtable}", r"\hline" + "\n" + r"\end{longtable}")
                rules = head + separator + body
        return match.group("start") + spec + rules

    return LONGTABLE_RE.sub(format_table, fragment)
