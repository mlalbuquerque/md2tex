from md2tex.frontmatter import parse_frontmatter


def test_parse_frontmatter():
    metadata, body = parse_frontmatter("---\ntitle: Teste\nversion: 1.0\n---\n\n# Corpo\n")
    assert metadata["title"] == "Teste"
    assert "# Corpo" in body
