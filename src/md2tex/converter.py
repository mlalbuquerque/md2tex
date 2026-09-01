from __future__ import annotations

import tempfile
from importlib.resources import files
from pathlib import Path

from .compiler import clean_latex_auxiliary_files, compile_pdf
from .config import available_style_packages
from .errors import ConfigError, ValidationError
from .frontmatter import parse_frontmatter
from .mermaid import render_mermaid_blocks
from .metadata import build_metadata
from .models import ConversionOptions, ConversionResult, ValidationMessage
from .pandoc import markdown_to_latex_fragment
from .profiles import get_profile
from .rules import load_rules
from .templates import render_template
from .utils import ensure_parent, normalize_heading_levels, strip_manual_heading_numbering
from .validator import (
    has_errors,
    missing_required_topics,
    validate_markdown,
    validate_meeting_minutes,
    validate_metadata,
    validate_tex,
)


def convert(options: ConversionOptions) -> ConversionResult:
    if options.user_config is None:
        raise ConfigError("Uma configuração válida é obrigatória. Execute 'md2tex init' ou use --config.")
    if not options.input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {options.input_path}")
    if options.output_path.exists() and not options.force:
        raise FileExistsError(
            f"Arquivo de saída já existe: {options.output_path}. Use --force para sobrescrever."
        )

    source_dir = options.input_path.parent.resolve()
    original = options.input_path.read_text(encoding="utf-8")
    raw_metadata, markdown = parse_frontmatter(original)
    headings_markdown = normalize_heading_levels(strip_manual_heading_numbering(markdown))
    metadata, markdown = build_metadata(raw_metadata, markdown, options)
    markdown = strip_manual_heading_numbering(markdown)
    markdown = normalize_heading_levels(markdown)

    messages: list[ValidationMessage] = []
    try:
        rules = load_rules(options.rules_path)
    except ConfigError as exc:
        if options.rules_path is not None:
            raise
        rules = {}
        messages.append(ValidationMessage("warning", str(exc), "rules"))

    if options.validate:
        messages.extend(validate_metadata(metadata, options.profile))
        if options.profile == "meeting-minutes":
            effective_raw_metadata = dict(raw_metadata)
            for key, value in (
                ("client", options.client),
                ("author", options.author),
                ("date", options.date),
            ):
                if value is not None:
                    effective_raw_metadata[key] = value
            messages.extend(validate_meeting_minutes(effective_raw_metadata, markdown))
        messages.extend(validate_markdown(markdown, source_dir))
        for topic in missing_required_topics(headings_markdown, rules.get(options.profile, [])):
            messages.append(
                ValidationMessage(
                    "warning",
                    f"Tópico obrigatório ausente para o tipo '{options.profile}': '{topic}'.",
                    "topics",
                )
            )

    topic_pendencies = [message for message in messages if message.source == "topics"]
    if options.strict and topic_pendencies:
        errors = "\n".join(f"- {message.message}" for message in topic_pendencies)
        raise ValidationError(f"Validação interrompeu a geração:\n{errors}")

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
    lua_filter = package_root / "filters" / "md2tex.lua"
    profile = get_profile(options.profile)
    template_path = options.template_path or package_root / "templates" / profile["template"]

    temp_context = tempfile.TemporaryDirectory(prefix="md2tex-")
    build_dir = Path(temp_context.name)
    preprocessed_path = build_dir / "preprocessed.md"
    preprocessed_path.write_text(markdown, encoding="utf-8")

    fragment = markdown_to_latex_fragment(
        preprocessed_path,
        lua_filter=lua_filter,
        landscape_tables=options.landscape_tables or str(options.user_config.tables["landscape"]),
        table_font=options.table_font or str(options.user_config.tables["font"]),
        table_width=options.table_width or str(options.user_config.tables["width"]),
        table_borders=options.table_borders or str(options.user_config.tables["borders"]),
        table_zebra=options.table_zebra if options.table_zebra is not None else bool(options.user_config.tables["zebra"]),
        source_dir=source_dir,
        verbose=options.verbose,
    )

    required_packages = {
        "calc": r"\real{" in fragment,
        "array": r"\arraybackslash" in fragment,
        "ragged2e": r"\RaggedRight" in fragment,
        "ulem": r"\sout{" in fragment,
    }
    configured_packages = available_style_packages(
        options.user_config.style_packages,
        base_dir=options.config_path.parent if options.config_path else None,
    )
    missing_packages = sorted(
        package for package, required in required_packages.items()
        if required and package not in configured_packages
    )
    if missing_packages:
        raise ConfigError(
            "A conversão gerada requer o(s) pacote(s) LaTeX "
            + ", ".join(missing_packages)
            + ". Adicione-os a style_packages, a menos que um .sty local os carregue."
        )

    tex = render_template(
        Path(template_path),
        metadata=metadata,
        body=fragment,
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
