from pathlib import Path

import pytest

from md2tex.frontmatter import parse_frontmatter
from md2tex.validator import (
    extract_headings,
    has_errors,
    missing_required_topics,
    validate_log,
    validate_tex,
)

MEETING_MINUTES_FIXTURES = Path(__file__).parent / "fixtures" / "meeting_minutes"


def _meeting_minutes_messages(raw: dict, body: str):
    """Contrato de validação a ser implementado em T006."""
    from md2tex.validator import validate_meeting_minutes

    return validate_meeting_minutes(raw, body)


def test_extract_headings_handles_atx_setext_and_fenced_code():
    markdown = "# Objetivo #\n\nConclusão\n---------\n\n```md\n# Ignorado\n```\n"
    assert extract_headings(markdown) == {"objetivo", "conclusão"}


def test_missing_required_topics_normalizes_spaces_and_case():
    missing = missing_required_topics("##  DECISÃO  \n", ["Decisão", "Contexto"])
    assert missing == ["Contexto"]


def test_detects_unresolved_placeholder():
    messages = validate_tex("\\begin{document}@@PH0@@\\end{document}")
    assert has_errors(messages)
    assert "@@PH0@@" in messages[0].message


def test_accepts_complete_document():
    messages = validate_tex("\\begin{document}Texto\\end{document}")
    assert not has_errors(messages)


def test_validate_log_extracts_latex_errors():

    log_sample = "! Undefined control sequence.\nl.15 \\invalidcommand\n"
    messages = validate_log(log_sample)
    assert has_errors(messages)
    assert "Undefined control sequence" in messages[0].message



def test_validate_log_explains_package_option_clash():
    messages = validate_log("! LaTeX Error: Option clash for package geometry.\n")
    assert any("page_geometry: {}" in message.message for message in messages)


def test_meeting_minutes_validator_accepts_the_canonical_complete_fixture():
    raw, body = parse_frontmatter(
        (MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8")
    )

    assert _meeting_minutes_messages(raw, body) == []


@pytest.mark.parametrize(
    ("raw", "body", "expected_path"),
    [
        ({}, "", "client"),
        ({"client": "Cliente", "author": "Produtor", "date": "2026-08-31", "period": {"start": "09:00"}}, "", "period.end"),
        ({"client": "Cliente", "author": "Produtor", "date": "2026-08-31", "period": {"start": "09:00", "end": "10:00"}}, "# Pendências\n\nSem pendências\n", "Objetivos da Reunião"),
    ],
)
def test_meeting_minutes_validator_names_missing_metadata_and_sections(
    raw: dict, body: str, expected_path: str
):
    assert any(expected_path in message.message for message in _meeting_minutes_messages(raw, body))


@pytest.mark.parametrize(
    ("raw", "body", "expected_path"),
    [
        (
            {
                "client": "Cliente",
                "author": "Produtor",
                "date": "2026-08-31",
                "period": {"start": "09:00", "end": "10:00"},
                "participants": {"netra": [{"name": "Pessoa"}]},
            },
            "# Objetivos da Reunião\n\nOK\n# Tópicos Abordados\n\nOK\n# Considerações Gerais e Definições\n\nOK\n# Pendências\n\nSem pendências\n",
            "participants.netra[0].role",
        ),
        (
            {
                "client": "Cliente",
                "author": "Produtor",
                "date": "2026-08-31",
                "period": {"start": "09:00", "end": "10:00"},
            },
            "# Objetivos da Reunião\n\nOK\n# Tópicos Abordados\n\nOK\n# Considerações Gerais e Definições\n\nOK\n# Pendências\n\n| Pendência | Responsável | Prazo para Solução |\n|---|---|---|\n| Enviar proposta |  | 2026-09-05 |\n",
            "Pendências[1].Responsável",
        ),
    ],
)
def test_meeting_minutes_validator_names_invalid_participants_and_pendency_rows(
    raw: dict, body: str, expected_path: str
):
    assert any(expected_path in message.message for message in _meeting_minutes_messages(raw, body))

def test_meeting_minutes_validator_names_every_required_value():
    assert all(path in "\n".join(message.message for message in _meeting_minutes_messages({}, "")) for path in ("client", "author", "date", "period.start", "period.end", "Objetivos da Reunião", "Tópicos Abordados", "Considerações Gerais e Definições", "Pendências"))



def test_meeting_minutes_validator_accepts_no_pendency_and_rejects_incomplete_table():
    raw, body = parse_frontmatter((MEETING_MINUTES_FIXTURES / "no-pendency.md").read_text(encoding="utf-8"))
    assert _meeting_minutes_messages(raw, body) == []
    invalid_body = body.replace("Sem pendências", "| Pendência | Responsável | Prazo para Solução |\n|---|---|---|\n| Ação | | 2026-09-01 |")
    assert any("Pendências[1].Responsável" in message.message for message in _meeting_minutes_messages(raw, invalid_body))
