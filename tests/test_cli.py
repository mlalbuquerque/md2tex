from importlib.resources import files
from pathlib import Path

import pytest
from click.testing import CliRunner

from md2tex.cli import main
from md2tex.models import ConversionResult

MEETING_MINUTES_FIXTURES = Path(__file__).parent / "fixtures" / "meeting_minutes"

def write_valid_config(path: Path) -> Path:
    path.write_text(files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8"), encoding="utf-8")

    return path


def test_cli_version_identity():
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "md2tex, version 2.6.0" in result.output


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


def test_cli_rules_init_creates_explicit_destination_and_requires_force(tmp_path: Path):
    runner = CliRunner()
    target = tmp_path / "nested" / "rules.yaml"
    result = runner.invoke(main, ["rules", "init", "--rules", str(target)])
    assert result.exit_code == 0
    assert target.exists()
    assert "Regras criadas" in result.output

    original = target.read_bytes()
    repeated = runner.invoke(main, ["rules", "init", "--rules", str(target)])
    assert repeated.exit_code == 1
    assert "já existe" in repeated.output
    assert target.read_bytes() == original

    forced = runner.invoke(main, ["rules", "init", "--rules", str(target), "--force"])
    assert forced.exit_code == 0
    assert target.read_text(encoding="utf-8").startswith("# Regras de tópicos")


def test_cli_rules_init_uses_default_destination(tmp_path: Path, monkeypatch):
    target = tmp_path / "config" / "rules.yaml"
    monkeypatch.setattr("md2tex.rules.DEFAULT_RULES_PATH", target)

    result = CliRunner().invoke(main, ["rules", "init"])

    assert result.exit_code == 0
    assert target.exists()
    assert str(target.resolve()) in result.output


def test_cli_rules_requires_init_subcommand():
    result = CliRunner().invoke(main, ["rules"])
    assert result.exit_code == 2
    assert "md2tex rules init" in result.output


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


def test_cli_forwards_explicit_rules_path(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text("rules: {}\n", encoding="utf-8")
    captured = {}

    def fake_convert(options):
        captured["rules_path"] = options.rules_path
        return ConversionResult(tex_path=options.output_path, pdf_path=None, messages=[])

    monkeypatch.setattr("md2tex.cli.convert", fake_convert)
    result = CliRunner().invoke(
        main, [str(doc), "-c", str(config_file), "--rules", str(rules_file)]
    )

    assert result.exit_code == 0
    assert captured["rules_path"] == rules_file.resolve()


def test_cli_converts_when_default_rules_file_is_absent(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    monkeypatch.setattr("md2tex.rules.DEFAULT_RULES_PATH", tmp_path / "missing-rules.yaml")
    monkeypatch.setattr(
        "md2tex.converter.markdown_to_latex_fragment", lambda *args, **kwargs: "Texto"
    )

    result = CliRunner().invoke(main, [str(doc), "-c", str(config_file)])

    assert result.exit_code == 0
    assert (tmp_path / "input.tex").exists()
    assert "[rules]" not in result.output


def test_cli_explicit_missing_or_invalid_rules_fail_before_conversion(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("# Documento\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    called = False

    def fake_convert(options):
        nonlocal called
        called = True
        from md2tex.rules import load_rules

        load_rules(options.rules_path)
        return ConversionResult(tex_path=options.output_path, pdf_path=None, messages=[])

    monkeypatch.setattr("md2tex.cli.convert", fake_convert)
    missing = CliRunner().invoke(
        main,
        [str(doc), "-c", str(config_file), "--rules", str(tmp_path / "missing.yaml"), "--no-validate"],
    )
    invalid_path = tmp_path / "invalid.yaml"
    invalid_path.write_text("not-rules: {}\n", encoding="utf-8")
    invalid = CliRunner().invoke(
        main, [str(doc), "-c", str(config_file), "--rules", str(invalid_path), "--no-validate"]
    )

    assert missing.exit_code == 1
    assert invalid.exit_code == 1
    assert "Arquivo de regras não encontrado" in missing.output
    assert "Regras inválidas" in invalid.output
    assert called


def test_cli_strict_topics_reports_error_and_no_validate_suppresses_check(tmp_path: Path, monkeypatch):
    doc = tmp_path / "input.md"
    doc.write_text("---\ntitle: Documento\n---\n\n# Contexto\n", encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text("rules:\n  adr:\n    - Decisão\n", encoding="utf-8")
    output = tmp_path / "output.tex"

    strict = CliRunner().invoke(
        main,
        [str(doc), "-c", str(config_file), "--rules", str(rules_file), "--type", "adr", "--strict", "-o", str(output)],
    )
    assert strict.exit_code == 1
    assert "Validação interrompeu a geração" in strict.output
    assert "Decisão" in strict.output
    assert not output.exists()

    monkeypatch.setattr("md2tex.converter.markdown_to_latex_fragment", lambda *args, **kwargs: "Texto")
    no_validate = CliRunner().invoke(
        main,
        [str(doc), "-c", str(config_file), "--rules", str(rules_file), "--type", "adr", "--strict", "--no-validate", "-o", str(output)],
    )
    assert no_validate.exit_code == 0
    assert output.exists()

def test_cli_meeting_minutes_uses_front_matter_configured_style_and_cli_precedence(
    tmp_path: Path, monkeypatch
):
    source = tmp_path / "meeting-minutes.md"
    source.write_text(
        MEETING_MINUTES_FIXTURES.joinpath("complete.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    config_file = write_valid_config(tmp_path / "config.yaml")
    config_file.write_text(
        config_file.read_text(encoding="utf-8").replace(
            "style_packages:\n", "style_packages:\n  - letterhead.sty\n"
        ),
        encoding="utf-8",
    )
    (tmp_path / "letterhead.sty").write_text("% user-owned letterhead\n", encoding="utf-8")
    monkeypatch.setattr("md2tex.converter.markdown_to_latex_fragment", lambda *args, **kwargs: "Corpo")
    output = tmp_path / "meeting-minutes.tex"

    result = CliRunner().invoke(
        main,
        [
            str(source), "--type", "meeting-minutes", "-c", str(config_file),
            "-o", str(output), "--client", "Cliente via CLI", "--author", "Autor via CLI",
            "--date", "2026-09-01", "--no-mermaid", "--force",
        ],
    )

    assert result.exit_code == 0, result.output
    content = output.read_text(encoding="utf-8")
    assert "\\usepackage{letterhead}" in content
    assert "Cliente via CLI" in content
    assert "Autor via CLI" in content
    assert "2026-09-01" in content
    assert "09:00 -- 10:30" in content


def test_cli_strict_reports_invalid_meeting_minutes_and_does_not_create_output(tmp_path: Path):
    source = tmp_path / "invalid-meeting-minutes.md"
    source.write_text((MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8").replace("client: Cliente Aurora / Projeto Aurora (NEP-001)\n", ""), encoding="utf-8")
    config_file = write_valid_config(tmp_path / "config.yaml")
    output = tmp_path / "meeting-minutes.tex"
    result = CliRunner().invoke(main, [str(source), "--type", "meeting-minutes", "-c", str(config_file), "-o", str(output), "--strict", "--no-mermaid", "--force"])
    assert result.exit_code == 1
    assert "Cliente/Projeto" in result.output
    assert not output.exists()

@pytest.mark.parametrize(
    ("removed_line", "expected_label"),
    [
        ('  start: "09:00"\n', "Período — início"),
        ('  end: "10:30"\n', "Período — fim"),
    ],
)
def test_cli_strict_uses_public_period_diagnostics(tmp_path: Path, removed_line: str, expected_label: str):
    source = tmp_path / "invalid-period.md"
    source.write_text(
        (MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8").replace(removed_line, ""),
        encoding="utf-8",
    )
    config_file = write_valid_config(tmp_path / "config.yaml")
    output = tmp_path / "meeting-minutes.tex"
    result = CliRunner().invoke(
        main,
        [str(source), "--type", "meeting-minutes", "-c", str(config_file), "-o", str(output), "--strict", "--no-mermaid", "--force"],
    )
    assert result.exit_code == 1
    assert expected_label in result.output
    assert "period.start" not in result.output
    assert "period.end" not in result.output
    assert not output.exists()
