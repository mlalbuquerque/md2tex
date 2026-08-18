from md2tex.validator import (
    extract_headings,
    has_errors,
    missing_required_topics,
    validate_log,
    validate_tex,
)


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
