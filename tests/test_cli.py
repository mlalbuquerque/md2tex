from importlib.resources import files
from pathlib import Path

from click.testing import CliRunner

from md2tex.cli import main
from md2tex.models import ConversionResult


def write_valid_config(path: Path) -> Path:
    path.write_text(files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return path


def test_cli_version_identity():
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "md2tex, version 2.3.0" in result.output


def test_cli_help_identity():
    result = CliRunner().invoke(main, ["--help"], prog_name="md2tex")
    assert result.exit_code == 0
    assert "md2tex init" in result.output
    assert "-v, --verbose" in result.output


def test_cli_init_creates_config_and_refuses_overwrite():
    runner = CliRunner()
    with runner.isolated_filesystem():
        target = Path("config.yaml")
        result = runner.invoke(main, ["init", "--config", str(target)])
        assert result.exit_code == 0
        assert target.exists()
        assert "Configuração criada" in result.output
        assert runner.invoke(main, ["init", "--config", str(target)]).exit_code == 1


def test_cli_check_deps():
    result = CliRunner().invoke(main, ["--check-deps"])
    assert result.exit_code == 0
    assert "Relatório de Dependências" in result.output


def test_cli_missing_config_fails(tmp_path: Path):
    doc = tmp_path / "input.md"
    doc.write_text("# Título\n", encoding="utf-8")
    result = CliRunner().invoke(main, [str(doc), "-c", str(tmp_path / "missing.yaml")])
    assert result.exit_code == 1
    assert "md2tex init" in result.output


def test_cli_precedence_over_config(tmp_path: Path):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento de Teste\nTexto simples.\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "custom_config.yaml")
    output_tex = tmp_path / "output.tex"
    result = CliRunner().invoke(
        main,
        [
            str(doc), "-o", str(output_tex), "-c", str(config_file),
            "-s", "calc", "-s", "extra_style.sty", "-e", "xelatex", "--force",
        ],
    )
    assert result.exit_code == 0
    content = output_tex.read_text(encoding="utf-8")
    assert "\\usepackage{extra_style}" in content
    assert "\\usepackage{calc}" in content
    assert "\\usepackage{fontspec}" not in content
    assert "\\documentclass[11pt,a4paper]{article}" in content


def test_cli_engine_override_takes_precedence(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    config_file.write_text(
        config_file.read_text(encoding="utf-8").replace("engine: xelatex", "engine: pdflatex"),
        encoding="utf-8",
    )
    captured = {}

    def fake_convert(options):
        captured["engine"] = options.engine
        return ConversionResult(tex_path=options.output_path, pdf_path=None, messages=[])

    monkeypatch.setattr("md2tex.cli.convert", fake_convert)
    result = CliRunner().invoke(main, [str(doc), "-c", str(config_file), "-e", "xelatex"])

    assert result.exit_code == 0
    assert captured["engine"] == "xelatex"


def test_cli_pdf_output_uses_a_tex_intermediate_path(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    captured = {}

    def fake_convert(options):
        captured["output_path"] = options.output_path
        return ConversionResult(
            tex_path=options.output_path,
            pdf_path=options.output_path.with_suffix(".pdf"),
            messages=[],
        )

    monkeypatch.setattr("md2tex.cli.convert", fake_convert)
    result = CliRunner().invoke(
        main,
        [str(doc), "-c", str(config_file), "--pdf", "-o", str(tmp_path / "output.pdf")],
    )

    assert result.exit_code == 0
    assert captured["output_path"] == tmp_path / "output.tex"
