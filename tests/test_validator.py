from md2tex.validator import has_errors, validate_tex, validate_log


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

