from __future__ import annotations

import shutil
from pathlib import Path

from .errors import CompilationError, DependencyError
from .models import ValidationMessage
from .utils import executable, run_command
from .validator import validate_log


def compile_pdf(
    tex_path: Path,
    *,
    engine: str,
    shell_escape: bool,
    verbose: bool,
) -> tuple[Path, list[ValidationMessage]]:
    messages: list[ValidationMessage] = []
    output_dir = tex_path.parent
    latexmk = executable("latexmk")

    if latexmk:
        engine_flag = {
            "xelatex": "-xelatex",
            "lualatex": "-lualatex",
            "pdflatex": "-pdf",
        }[engine]
        command = [
            latexmk,
            engine_flag,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output_dir}",
        ]
        if shell_escape:
            command.append("-shell-escape")
        command.append(str(tex_path))
        process = run_command(command, cwd=output_dir, verbose=verbose, check=False)
    else:
        binary = executable(engine)
        if not binary:
            raise DependencyError(
                f"Nem latexmk nem {engine} foram encontrados. Instale TeX Live/XeLaTeX."
            )
        command = [binary, "-interaction=nonstopmode", "-halt-on-error"]
        if shell_escape:
            command.append("-shell-escape")
        command.append(str(tex_path.name))
        process = run_command(command, cwd=output_dir, verbose=verbose, check=False)
        if process.returncode == 0:
            process = run_command(command, cwd=output_dir, verbose=verbose, check=False)

    log_path = tex_path.with_suffix(".log")
    if log_path.exists():
        messages.extend(validate_log(log_path.read_text(encoding="utf-8", errors="replace")))

    pdf_path = tex_path.with_suffix(".pdf")
    if process.returncode != 0 or not pdf_path.exists():
        details = process.stderr.strip() or process.stdout.strip()
        log_errors = [m.message for m in messages if m.level == "error"]
        if log_errors:
            error_details = "\n".join(f"- {e}" for e in log_errors)
            raise CompilationError(
                f"Falha ao compilar PDF:\n{error_details}\n\nDetalhes do latexmk:\n{details}"
            )
        raise CompilationError(f"Falha ao compilar PDF:\n{details}")
    return pdf_path, messages


def clean_latex_auxiliary_files(tex_path: Path, *, include_toc: bool = False) -> list[Path]:
    """Remove arquivos auxiliares do LaTeX.

    Com ``include_toc=False``, preserva o arquivo ``.toc`` para acelerar
    recompilações e manter o sumário disponível durante a edição.
    """
    suffixes = [
        ".aux",
        ".fdb_latexmk",
        ".fls",
        ".log",
        ".out",
        ".lof",
        ".lot",
        ".synctex.gz",
        ".xdv",
        ".bbl",
        ".blg",
        ".bcf",
        ".run.xml",
        ".nav",
        ".snm",
        ".vrb",
    ]
    if include_toc:
        suffixes.append(".toc")

    removed: list[Path] = []
    for suffix in suffixes:
        candidate = tex_path.with_suffix(suffix)
        try:
            if candidate.exists():
                candidate.unlink()
                removed.append(candidate)
        except OSError:
            pass

    minted = tex_path.parent / f"_minted-{tex_path.stem}"
    if minted.exists():
        shutil.rmtree(minted, ignore_errors=True)
        removed.append(minted)
    return removed
