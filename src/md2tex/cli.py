from __future__ import annotations

import sys
from pathlib import Path

import click

from . import __version__
from .config import (
    DEFAULT_CONFIG_PATH,
    initialize_config,
    load_config,
    validate_style_configuration,
    validate_style_paths,
)
from .converter import convert
from .errors import ConfigError, Md2TexError
from .models import ConversionOptions, UserConfig
from .setup import print_dependency_report, run_interactive_setup


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_file", type=str, required=False)
@click.option("-o", "--output", type=click.Path(path_type=Path, dir_okay=False), help="Arquivo de saída (.tex ou .pdf).")
@click.option("-c", "--config", "config_path", type=click.Path(path_type=Path, dir_okay=False), help="Caminho do arquivo de configuração YAML.")
@click.option("--rules", "rules_path", type=click.Path(path_type=Path, dir_okay=False), help="Caminho do arquivo YAML de regras de tópicos.")
@click.option("-s", "--style", "style_packages", multiple=True, help="Substitui os pacotes de estilo definidos no YAML; pode repetir.")
@click.option("--check-deps", is_flag=True, help="Verifica o relatório de dependências instaladas no sistema e sai.")
@click.option("--setup", "run_setup", is_flag=True, help="Executa o assistente interativo de configuração de dependências.")
@click.option(
    "--type",
    "profile",
    type=click.Choice(["report", "meeting-minutes", "adr", "technical-plan", "default"]),
    default="default",
    show_default=True,
    help="Perfil documental aplicado ao documento.",
)
@click.option("--title", help="Sobrescreve o título do documento.")
@click.option("--subtitle", help="Sobrescreve o subtítulo do documento.")
@click.option("--author", help="Sobrescreve o autor.")
@click.option("--date", help="Sobrescreve a data do documento.")
@click.option("--document-version", help="Sobrescreve a versão documental.")
@click.option("--client", help="Sobrescreve o cliente/projeto.")
@click.option(
    "--figures",
    "figures_dir",
    type=click.Path(path_type=Path, file_okay=False),
    default=Path("figures"),
    show_default=True,
    help="Diretório das imagens e diagramas.",
)
@click.option(
    "--template",
    "template_path",
    type=click.Path(path_type=Path, dir_okay=False, exists=True),
    help="Template Jinja2 TEX personalizado.",
)
@click.option("--pdf/--no-pdf", "generate_pdf", default=False, help="Compila o TEX para PDF.")
@click.option("--validate/--no-validate", default=True, help="Executa validações antes/depois da conversão.")
@click.option("--strict", is_flag=True, help="Interrompe a execução em caso de erros de validação.")
@click.option("--toc/--no-toc", default=True, help="Inclui ou remove o sumário.")
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["pdflatex", "xelatex", "lualatex"]),
    default=None,
    help="Motor LaTeX usado com --pdf.",
)
@click.option("--mermaid/--no-mermaid", default=True, help="Renderiza blocos fenced mermaid.")
@click.option(
    "--mermaid-format",
    type=click.Choice(["png", "pdf", "svg"]),
    default="png",
    show_default=True,
    help="Formato de saída dos diagramas Mermaid.",
)
@click.option(
    "--landscape-tables",
    type=click.Choice(["auto", "always", "never"]),
    default=None,
    help="Sobrescreve tables.landscape da configuração.",
)
@click.option(
    "--table-font",
    type=click.Choice(["normalsize", "small", "footnotesize", "scriptsize"]),
    default=None,
    help="Sobrescreve tables.font da configuração.",
)
@click.option(
    "--table-width",
    type=click.Choice(["auto", "equal", "natural"]),
    default=None,
    help="Sobrescreve tables.width da configuração.",
)
@click.option("--table-borders", type=click.Choice(["none", "outer", "grid"]), default=None, help="Sobrescreve tables.borders da configuração.")
@click.option("--table-zebra/--no-table-zebra", default=None, help="Sobrescreve tables.zebra da configuração.")
@click.option("--shell-escape", is_flag=True, help="Habilita shell-escape na compilação LaTeX.")
@click.option("--keep-build", is_flag=True, help="Mantém Markdown pré-processado e fragmento TEX.")
@click.option("--clean", is_flag=True, help="Remove auxiliares LaTeX após execução, preservando .toc.")
@click.option("--clean-all", is_flag=True, help="Remove todos os auxiliares LaTeX, inclusive .toc.")
@click.option("--force", is_flag=True, help="Sobrescreve o arquivo de saída existente.")
@click.option("-v", "--verbose", is_flag=True, help="Mostra os comandos externos executados.")
@click.version_option(__version__, "--version", prog_name="md2tex")
def main(
    input_file: Path | None,
    output: Path | None,
    config_path: Path | None,
    rules_path: Path | None,
    style_packages: tuple[str, ...],
    check_deps: bool,
    run_setup: bool,
    profile: str,
    title: str | None,
    subtitle: str | None,
    author: str | None,
    date: str | None,
    document_version: str | None,
    client: str | None,
    figures_dir: Path,
    template_path: Path | None,
    generate_pdf: bool,
    validate: bool,
    strict: bool,
    toc: bool,
    engine: str | None,
    mermaid: bool,
    mermaid_format: str,
    landscape_tables: str,
    table_font: str,
    table_width: str | None,
    table_borders: str | None,
    table_zebra: bool | None,
    shell_escape: bool,
    keep_build: bool,
    clean: bool,
    clean_all: bool,
    force: bool,
    verbose: bool,
) -> None:
    """Converte INPUT_FILE Markdown para LaTeX/PDF; use `md2tex init` para criar a configuração."""
    if check_deps:
        print_dependency_report()
        return

    if run_setup:
        run_interactive_setup()
        return

    if input_file == "init":
        try:
            config_target = initialize_config(config_path, force=force)
        except ConfigError as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(f"Configuração criada: {config_target}")
        return

    if not input_file:
        raise click.UsageError("É necessário fornecer um INPUT_FILE (ou usar init / --check-deps / --setup).")
    input_path = Path(input_file)
    if not input_path.is_file():
        raise click.UsageError(f"INPUT_FILE não encontrado ou não é um arquivo: {input_file}")
    if clean and clean_all:
        raise click.UsageError("Use apenas uma das opções: --clean ou --clean-all.")

    # Carrega arquivo de configuração do usuário (ou customizado via --config)
    user_config: UserConfig | None = None
    try:
        user_config = load_config(config_path)
    except ConfigError as exc:
        click.echo(f"Erro de Configuração: {exc}", err=True)
        sys.exit(1)

    # Resolução de precedência (CLI sobre UserConfig)
    effective_landscape = landscape_tables or user_config.tables["landscape"]
    effective_table_font = table_font or user_config.tables["font"]
    effective_table_width = table_width or user_config.tables["width"]
    effective_table_borders = table_borders or user_config.tables["borders"]
    effective_table_zebra = user_config.tables["zebra"] if table_zebra is None else table_zebra
    effective_engine = engine or user_config.compiler_options["engine"]
    effective_styles = list(style_packages) if style_packages else user_config.style_packages

    user_config.style_packages = effective_styles
    try:
        config_base_dir = (config_path or DEFAULT_CONFIG_PATH).expanduser().resolve().parent
        validate_style_paths(user_config.style_packages, base_dir=config_base_dir)
        validate_style_configuration(user_config, base_dir=config_base_dir)
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc

    output_path = output or input_path.with_suffix(".tex")
    if generate_pdf and output_path.suffix.lower() == ".pdf":
        output_path = output_path.with_suffix(".tex")
    options = ConversionOptions(
        input_path=input_path.resolve(),
        output_path=output_path.resolve(),
        config_path=config_path.resolve() if config_path else DEFAULT_CONFIG_PATH,
        rules_path=rules_path.expanduser().resolve() if rules_path else None,
        user_config=user_config,
        profile=profile,
        figures_dir=figures_dir,
        template_path=template_path.resolve() if template_path else None,
        generate_pdf=generate_pdf,
        validate=validate,
        strict=strict,
        toc=toc,
        engine=effective_engine,
        mermaid=mermaid,
        mermaid_format=mermaid_format,
        landscape_tables=effective_landscape,
        table_font=effective_table_font,
        table_width=effective_table_width,
        table_borders=effective_table_borders,
        table_zebra=effective_table_zebra,
        keep_build=keep_build,
        force=force,
        verbose=verbose,
        title=title,
        subtitle=subtitle,
        author=author,
        date=date,
        document_version=document_version,
        client=client,
        shell_escape=shell_escape,
        clean=clean,
        clean_all=clean_all,
    )

    try:
        result = convert(options)
    except (OSError, Md2TexError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"TEX: {result.tex_path}")
    if result.pdf_path:
        click.echo(f"PDF: {result.pdf_path}")
    if result.build_dir:
        click.echo(f"Build: {result.build_dir}")

    for message in result.messages:
        prefix = {"error": "ERRO", "warning": "AVISO", "info": "INFO"}.get(
            message.level, message.level.upper()
        )
        source = f" [{message.source}]" if message.source else ""
        click.echo(f"{prefix}{source}: {message.message}", err=message.level == "error")

    if strict and any(message.level == "error" for message in result.messages):
        sys.exit(2)


if __name__ == "__main__":
    main()
