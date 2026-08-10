from importlib.resources import files
from pathlib import Path

from click.testing import CliRunner

from md2tex.cli import main
from md2tex.models import ConversionResult


def test_cli_forwards_subtitle_and_lists_option(tmp_path: Path, monkeypatch):
    document = tmp_path / "documento.md"
    document.write_text("# Documento\n", encoding="utf-8")
    config = tmp_path / "config.yaml"
    config.write_text(
        files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    captured = {}

    def fake_convert(options):
        captured["subtitle"] = options.subtitle
        return ConversionResult(tex_path=options.output_path, pdf_path=None, messages=[])

    monkeypatch.setattr("md2tex.cli.convert", fake_convert)

    result = CliRunner().invoke(
        main, [str(document), "--config", str(config), "--subtitle", "Guia da CLI"]
    )

    assert result.exit_code == 0
    assert captured["subtitle"] == "Guia da CLI"
    assert "--subtitle TEXT" in CliRunner().invoke(main, ["--help"]).output
