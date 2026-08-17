from pathlib import Path

import pytest

from md2tex.metadata import build_metadata
from md2tex.models import ConversionOptions


@pytest.mark.parametrize(
    ("cli_subtitle", "expected"),
    [
        (None, "Subtítulo do front matter"),
        ("Subtítulo da CLI", "Subtítulo da CLI"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_subtitle_cli_precedence_and_empty_values(cli_subtitle: str | None, expected: str):
    metadata, _ = build_metadata(
        {"subtitle": "Subtítulo do front matter"},
        "# Documento\n",
        ConversionOptions(
            input_path=Path("documento.md"),
            output_path=Path("documento.tex"),
            subtitle=cli_subtitle,
        ),
    )

    assert metadata.subtitle == expected


@pytest.mark.parametrize(
    ("front_matter_subtitle", "cli_subtitle", "expected"),
    [
        ("Subtítulo do front matter", "  Subtítulo da CLI  ", "  Subtítulo da CLI  "),
        ("  Subtítulo do front matter  ", None, "  Subtítulo do front matter  "),
    ],
)
def test_subtitle_preserves_surrounding_whitespace(
    front_matter_subtitle: str, cli_subtitle: str | None, expected: str
):
    metadata, _ = build_metadata(
        {"subtitle": front_matter_subtitle},
        "# Documento\n",
        ConversionOptions(
            input_path=Path("documento.md"),
            output_path=Path("documento.tex"),
            subtitle=cli_subtitle,
        ),
    )

    assert metadata.subtitle == expected


@pytest.mark.parametrize(
    "template_name",
    [
        "base.tex.j2",
        "report.tex.j2",
        "meeting-minutes.tex.j2",
        "adr.tex.j2",
        "technical-plan.tex.j2",
    ],
)
def test_cover_templates_group_document_type_with_identification(template_name: str):
    template = (
        Path(__file__).parents[1] / "src" / "md2tex" / "templates" / template_name
    ).read_text(encoding="utf-8")

    assert template.index("metadata.document_type") > template.index("\\vfill")
    assert template.index("metadata.document_type") < template.rindex("metadata.author")
    assert template.index("metadata.document_type") > template.index("metadata.subtitle")
