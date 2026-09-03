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
        ({}, "", "Cliente/Projeto"),
        ({"client": "Cliente", "author": "Produtor", "date": "2026-08-31", "period": {"start": "09:00"}}, "", "Período — fim"),
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
    assert all(path in "\n".join(message.message for message in _meeting_minutes_messages({}, "")) for path in ("Cliente/Projeto", "author", "date", "Período — início", "Período — fim", "Objetivos da Reunião", "Tópicos Abordados", "Considerações Gerais e Definições", "Pendências"))



def test_meeting_minutes_validator_accepts_no_pendency_and_rejects_incomplete_table():
    raw, body = parse_frontmatter((MEETING_MINUTES_FIXTURES / "no-pendency.md").read_text(encoding="utf-8"))
    assert _meeting_minutes_messages(raw, body) == []
    invalid_body = body.replace("Sem pendências", "| Pendência | Responsável | Prazo para Solução |\n|---|---|---|\n| Ação | | 2026-09-01 |")
    assert any("Pendências[1].Responsável" in message.message for message in _meeting_minutes_messages(raw, invalid_body))

@pytest.mark.parametrize(
    ("period", "expected_label"),
    [
        ({"end": "10:00"}, "Período — início"),
        ({"start": "09:00"}, "Período — fim"),
        (None, "Período — início"),
    ],
)
def test_meeting_minutes_validator_uses_public_period_labels(period, expected_label):
    raw = {
        "client": "Cliente",
        "author": "Produtor",
        "date": "2026-08-31",
    }
    if period is not None:
        raw["period"] = period
    messages = _meeting_minutes_messages(raw, "")
    rendered = "\n".join(message.message for message in messages)
    assert expected_label in rendered
    assert "period.start" not in rendered
    assert "period.end" not in rendered


def test_meeting_minutes_validator_preserves_non_period_diagnostics():
    rendered = "\n".join(message.message for message in _meeting_minutes_messages({}, ""))
    assert "Cliente/Projeto" in rendered
    assert "Objetivos da Reunião" in rendered
    assert "Período — início" in rendered
    assert "Período — fim" in rendered


def _configured_requirements():
    from md2tex.models import DocumentRequirement, ProfileRequirements

    return {
        "meeting-minutes": ProfileRequirements(
            fields=[
                DocumentRequirement("client", "Cliente/Projeto", True, "Informe o cliente.", 'client: "Cliente"'),
                DocumentRequirement("period.start", "Período — início", True, "Informe o início.", 'period:\n  start: "09:00"'),
                DocumentRequirement("author", "Produtor/a", False, "Informe o produtor.", 'author: "Nome"'),
            ],
            sections=[
                DocumentRequirement("Objetivos da Reunião", "Objetivos", True, "Adicione objetivos.", "# Objetivos da Reunião\n\nDescreva os objetivos."),
            ],
        )
    }


def test_configured_requirements_validate_nested_fields_sections_and_optional_items():
    from md2tex.validator import validate_document_requirements

    messages = validate_document_requirements(
        _configured_requirements(), "meeting-minutes", {"period": {}}, "# Outro título\n\nTexto"
    )
    rendered = "\n".join(message.message for message in messages)
    assert "Cliente/Projeto" in rendered
    assert "Período — início" in rendered
    assert "Objetivos" in rendered
    assert "Produtor/a" not in rendered


def test_configured_requirements_are_isolated_by_profile():
    from md2tex.validator import validate_document_requirements

    assert validate_document_requirements(_configured_requirements(), "report", {}, "") == []


def test_configured_message_includes_instruction_and_multiline_example():
    from md2tex.validator import validate_document_requirements

    message = validate_document_requirements(_configured_requirements(), "meeting-minutes", {}, "")[0].message
    assert "Como preencher: Informe o cliente." in message
    assert 'client: "Cliente"' in message
