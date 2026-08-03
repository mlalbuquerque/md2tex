from __future__ import annotations

import tempfile
from importlib.resources import files
from pathlib import Path

from .compiler import clean_latex_auxiliary_files, compile_pdf
from .errors import ValidationError
from .frontmatter import parse_frontmatter
from .mermaid import render_mermaid_blocks
from .metadata import build_metadata
from .models import ConversionOptions, ConversionResult, ValidationMessage
from .pandoc import markdown_to_latex_fragment
from .profiles import get_profile
from .templates import render_template
from .utils import ensure_parent, normalize_heading_levels, strip_manual_heading_numbering
from .validator import has_errors, validate_markdown, validate_metadata, validate_tex


def convert(options: ConversionOptions) -> ConversionResult:
    if not options.input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {options.input_path}")
    if options.output_path.exists() and not options.force:
        raise FileExistsError(
            f"Arquivo de saída já existe: {options.output_path}. Use --force para sobrescrever."
        )

    source_dir = options.input_path.parent.resolve()
    original = options.input_path.read_text(encoding="utf-8")
    raw_metadata, markdown = parse_frontmatter(original)
    metadata, markdown = build_metadata(raw_metadata, markdown, options)
    markdown = strip_manual_heading_numbering(markdown)
    markdown = normalize_heading_levels(markdown)

    messages: list[ValidationMessage] = []
    if options.validate:
        messages.extend(validate_metadata(metadata, options.profile))
        messages.extend(validate_markdown(markdown, source_dir))

    figures_dir = options.figures_dir
    mermaid_result = render_mermaid_blocks(
        markdown,
        source_dir=source_dir,
        figures_dir=figures_dir,
        output_format=options.mermaid_format,
        enabled=options.mermaid,
        strict=options.strict,
        verbose=options.verbose,
    )
    markdown = mermaid_result.markdown
    messages.extend(mermaid_result.messages)

    package_root = Path(str(files("md2tex")))
    lua_filter = package_root / "filters" / "netra.lua"
    profile = get_profile(options.profile)
    template_path = options.template_path or package_root / "templates" / profile["template"]

    temp_context = tempfile.TemporaryDirectory(prefix="md2tex-")
    build_dir = Path(temp_context.name)
    preprocessed_path = build_dir / "preprocessed.md"
    preprocessed_path.write_text(markdown, encoding="utf-8")

    fragment = markdown_to_latex_fragment(
        preprocessed_path,
        lua_filter=lua_filter,
        landscape_tables=options.landscape_tables,
        table_font=options.table_font,
        table_width=options.table_width,
        source_dir=source_dir,
        verbose=options.verbose,
    )

    tex = render_template(
        Path(template_path),
        metadata=metadata,
        body=fragment,
        style_path=options.style_path,
        user_config=options.user_config,
        toc=options.toc,
        engine=options.engine,
        used_svg=mermaid_result.used_svg,
        source_dir=source_dir,
    )

    if options.validate:
        messages.extend(validate_tex(tex))
    if options.strict and has_errors(messages):
        temp_context.cleanup()
        errors = "\n".join(f"- {m.message}" for m in messages if m.level == "error")
        raise ValidationError(f"Validação interrompeu a geração:\n{errors}")

    ensure_parent(options.output_path)
    options.output_path.write_text(tex, encoding="utf-8")

    pdf_path: Path | None = None
    if options.generate_pdf:
        pdf_path, compile_messages = compile_pdf(
            options.output_path,
            engine=options.engine,
            shell_escape=options.shell_escape or mermaid_result.used_svg,
            verbose=options.verbose,
        )
        messages.extend(compile_messages)


    if options.clean or options.clean_all:
        removed = clean_latex_auxiliary_files(
            options.output_path, include_toc=options.clean_all
        )
        mode = "--clean-all" if options.clean_all else "--clean"
        messages.append(
            ValidationMessage(
                "info",
                f"{mode}: {len(removed)} arquivo(s) auxiliar(es) removido(s).",
                "latex-clean",
            )
        )

    retained_build_dir: Path | None = None
    if options.keep_build:
        retained_build_dir = options.output_path.parent / f".{options.output_path.stem}-build"
        retained_build_dir.mkdir(parents=True, exist_ok=True)
        (retained_build_dir / "preprocessed.md").write_text(markdown, encoding="utf-8")
        (retained_build_dir / "fragment.tex").write_text(fragment, encoding="utf-8")

    temp_context.cleanup()
    return ConversionResult(options.output_path, pdf_path, messages, retained_build_dir)
