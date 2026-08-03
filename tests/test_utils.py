from md2tex.utils import extract_title, normalize_heading_levels, strip_manual_heading_numbering


def test_remove_manual_numbering():
    source = "## 1. Objetivo\n### 1.1 Contexto\n"
    result = strip_manual_heading_numbering(source)
    assert "## Objetivo" in result
    assert "### Contexto" in result


def test_does_not_change_fenced_code():
    source = "```md\n## 1. Não alterar\n```\n"
    assert strip_manual_heading_numbering(source) == source


def test_extract_first_h1():
    title, body = extract_title("# Meu título\n\n## Seção\n")
    assert title == "Meu título"
    assert body.startswith("## Seção")


def test_normalize_heading_levels():
    source = "## Objetivo\n### Contexto\n"
    result = normalize_heading_levels(source)
    assert result.startswith("# Objetivo")
    assert "## Contexto" in result
