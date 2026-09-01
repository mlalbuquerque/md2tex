from pathlib import Path

import pytest

from md2tex.frontmatter import parse_frontmatter
from md2tex.metadata import build_metadata
from md2tex.models import ConversionOptions

MEETING_MINUTES_FIXTURES = Path(__file__).parent / "fixtures" / "meeting_minutes"


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


def test_complete_meeting_minutes_front_matter_keeps_structured_profile_metadata():
    raw, body = parse_frontmatter(
        (MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8")
    )

    metadata, body_without_title = build_metadata(
        raw,
        body,
        ConversionOptions(
            input_path=Path("meeting-minutes.md"),
            output_path=Path("meeting-minutes.tex"),
            profile="meeting-minutes",
        ),
    )

    assert metadata.document_type == "Memória de Reunião"
    assert metadata.client == "Cliente Aurora / Projeto Aurora (NEP-001)"
    assert metadata.author == "Marina Silva"
    assert metadata.date == "2026-08-31"
    assert metadata.extra["period"] == {"start": "09:00", "end": "10:30"}
    assert metadata.extra["participants"]["client"][0]["role"] == "Gerente de Produto"
    assert metadata.extra["participants"]["netra"][0]["name"] == "Bruno Netra"
    assert metadata.meeting_minutes is not None
    assert metadata.meeting_minutes.period_start == "09:00"
    assert metadata.meeting_minutes.netra_participants[0].group == "netra"
    assert "Alinhar o escopo e os próximos marcos do Projeto Aurora." in body_without_title


def test_no_pendency_meeting_minutes_allows_omitted_participant_groups_in_front_matter():
    raw, body = parse_frontmatter(
        (MEETING_MINUTES_FIXTURES / "no-pendency.md").read_text(encoding="utf-8")
    )

    metadata, body_without_title = build_metadata(
        raw,
        body,
        ConversionOptions(
            input_path=Path("meeting-minutes.md"),
            output_path=Path("meeting-minutes.tex"),
            profile="meeting-minutes",
        ),
    )

    assert "participants" not in metadata.extra
    assert "Sem pendências" in body_without_title
