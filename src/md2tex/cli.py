from __future__ import annotations

from pathlib import Path
import sys

import click

from . import __version__
from .config import DEFAULT_CONFIG_PATH, load_config
from .converter import convert
from .errors import ConfigError, Md2TexError
from .models import ConversionOptions, UserConfig
from .setup import print_dependency_report, run_interactive_setup


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_file", type=click.Path(path_type=Path, dir_okay=False, exists=True), required=False)
@click.option("-o", "--output", type=click.Path(path_type=Path, dir_okay=False), help="Arquivo de saída (.tex ou .pdf).")
@click.option("-c", "--config", "config_path", type=click.Path(path_type=Path, dir_okay=False), help="Caminho do arquivo de configuração YAML.")
@click.option("-s", "--style", "style_packages", multiple=True, help="Pacote de estilo .sty adicional.")
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
    default="auto",
    show_default=True,
    help="Coloca tabelas largas em páginas paisagem.",
)
@click.option(
    "--table-font",
    type=click.Choice(["normalsize", "small", "footnotesize", "scriptsize"]),
    default="small",
    show_default=True,
    help="Tamanho da fonte usado dentro das tabelas.",
)
@click.option(
    "--table-width",
    type=click.Choice(["auto", "equal", "natural"]),
    default="auto",
    show_default=True,
    help="Estratégia de largura das colunas.",
)
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
    style_packages: tuple[str, ...],
    check_deps: bool,
    run_setup: bool,
    profile: str,
    title: str | None,
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
    table_width: str,
    shell_escape: bool,
    keep_build: bool,
    clean: bool,
    clean_all: bool,
    force: bool,
    verbose: bool,
) -> None:
    """Converte INPUT_FILE Markdown para um documento LaTeX/PDF genérico."""
    if check_deps:
        print_dependency_report()
        return

    if run_setup:
        run_interactive_setup()
        return

    if not input_file:
        raise click.UsageError("É necessário fornecer um INPUT_FILE (ou usar --check-deps / --setup).")
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
    effective_engine = engine or (user_config.compiler_options.get("engine") if user_config else "pdflatex")
    merged_styles = list(user_config.style_packages) if user_config else []
    if style_packages:
        for s in style_packages:
            if s not in merged_styles:
                merged_styles.append(s)

    if user_config:
        user_config.style_packages = merged_styles

    output_path = output or input_file.with_suffix(".tex")
    options = ConversionOptions(
        input_path=input_file.resolve(),
        output_path=output_path.resolve(),
        config_path=config_path.resolve() if config_path else DEFAULT_CONFIG_PATH,
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
        landscape_tables=landscape_tables,
        table_font=table_font,
        table_width=table_width,
        keep_build=keep_build,
        force=force,
        verbose=verbose,
        title=title,
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
