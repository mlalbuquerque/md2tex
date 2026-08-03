from pathlib import Path
from click.testing import CliRunner

from md2tex.cli import main


def test_cli_version_identity():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "md2tex" in result.output
    assert "2.0.0" in result.output


def test_cli_help_identity():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"], prog_name="md2tex")
    assert result.exit_code == 0
    assert "md2tex" in result.output
    assert "Converte INPUT_FILE Markdown" in result.output


def test_cli_check_deps():
    runner = CliRunner()
    result = runner.invoke(main, ["--check-deps"])
    assert result.exit_code == 0
    assert "Relatório de Dependências" in result.output
    assert "Pandoc" in result.output


def test_cli_missing_config_fails(tmp_path: Path):
    doc = tmp_path / "input.md"
    doc.write_text("# Título\n", encoding="utf-8")
    missing_config = tmp_path / "missing.yaml"

    runner = CliRunner()
    result = runner.invoke(main, [str(doc), "-c", str(missing_config)])
    assert result.exit_code == 1
    assert "Erro de Configuração" in result.output or "não encontrado" in result.output


def test_cli_precedence_over_config(tmp_path: Path):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento de Teste\nTexto simples.\n", encoding="utf-8")
    config_file = tmp_path / "custom_config.yaml"
    config_file.write_text(
        """
document_class: article
style_packages:
  - graphicx
compiler_options:
  engine: pdflatex
""",
        encoding="utf-8",
    )
    output_tex = tmp_path / "output.tex"

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            str(doc),
            "-o",
            str(output_tex),
            "-c",
            str(config_file),
            "-s",
            "extra_style.sty",
            "-e",
            "xelatex",
            "--force",
        ],
    )
    assert result.exit_code == 0
    assert output_tex.exists()
    content = output_tex.read_text(encoding="utf-8")
    assert "\\usepackage{graphicx}" in content
    assert "\\usepackage{extra_style}" in content
