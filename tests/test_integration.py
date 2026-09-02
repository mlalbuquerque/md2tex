import shutil
import time
from importlib.resources import files
from pathlib import Path

import pytest

from md2tex.config import load_config
from md2tex.converter import convert
from md2tex.errors import ConfigError, ValidationError
from md2tex.models import ConversionOptions

MEETING_MINUTES_FIXTURES = Path(__file__).parent / "fixtures" / "meeting_minutes"

def config_for(tmp_path: Path):
    path = tmp_path / "config.yaml"
    path.write_text(files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return load_config(path)

def test_complete_meeting_minutes_renders_identification_participants_and_pendencies(
    tmp_path: Path, monkeypatch
):
    source = tmp_path / "meeting-minutes.md"
    source.write_text(
        (MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "letterhead.sty").write_text("% user-owned letterhead\n", encoding="utf-8")
    config = config_for(tmp_path)
    config.style_packages.append("letterhead.sty")
    monkeypatch.setattr(
        "md2tex.converter.markdown_to_latex_fragment",
        lambda *args, **kwargs: (
            "\\section{Pendências}\n"
            "\\begin{longtable}{lll}\n"
            "Enviar proposta revisada & Bruno Netra & 2026-09-05\\\\\n"
            "Validar orçamento & Ana Cliente & 2026-09-08\\\\\n"
            "\\end{longtable}"
        ),
    )
    output = tmp_path / "meeting-minutes.tex"
    result = convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            config_path=tmp_path / "config.yaml",
            user_config=config,
            profile="meeting-minutes",
            mermaid=False,
            force=True,
        )
    )

    assert not [message for message in result.messages if message.source == "meeting-minutes"]
    content = output.read_text(encoding="utf-8")
    for expected in (
        "\\usepackage{letterhead}",
        "\\section*{Identificação da Reunião}",
        "Cliente Aurora / Projeto Aurora (NEP-001)",
        "09:00 -- 10:30",
        "\\subsection*{Participantes do Cliente}",
        "Ana Cliente & Gerente de Produto",
        "\\subsection*{Participantes da Netra}",
        "Bruno Netra & Diretor de Projetos",
        "Enviar proposta revisada & Bruno Netra & 2026-09-05",
        "Validar orçamento & Ana Cliente & 2026-09-08",
    ):
        assert expected in content


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_conversion_performance_under_one_second(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text(
        "---\ntitle: Performance Test\n---\n\n# Header 1\n\nTexto de teste de conversão.\n",
        encoding="utf-8",
    )
    output = tmp_path / "doc.tex"
    start_time = time.perf_counter()
    result = convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            force=True,
        )
    )
    elapsed = time.perf_counter() - start_time
    assert result.tex_path.exists()
    assert elapsed < 1.0, f"Tempo de conversão ({elapsed:.3f}s) excedeu o limite de 1.0s"


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_generates_tex(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text(
        "---\ntitle: Documento\n---\n\n## 1. Objetivo\n\nTexto **forte** e *ênfase*.\n",
        encoding="utf-8",
    )
    output = tmp_path / "doc.tex"
    result = convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            force=True,
        )
    )
    assert result.tex_path.exists()
    content = output.read_text(encoding="utf-8")
    assert "\\section{Objetivo}" in content
    assert "\\textbf{forte}" in content
    assert "@@PH" not in content

@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_inline_code_wrap_and_table_options(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text(
        """---
title: Teste de Código
---

Caminho: `/home/usuario/uma/pasta/muito/longa/arquivo-com-nome-grande.conf`.

URL: `https://example.com/um/caminho/muito/longo?parametro=valor`.

Comando: `git push --follow-tags origin main`.

Código curto: `status`.

| A | B |
|---|---|
| Um | Dois |
""",
        encoding="utf-8",
    )
    output = tmp_path / "doc.tex"
    convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            landscape_tables="never",
            table_font="scriptsize",
            table_width="equal",
            force=True,
        )
    )
    content = output.read_text(encoding="utf-8")
    assert "\\protect\\path|/home/usuario/" in content
    assert "\\protect\\url|https://example.com/" in content
    assert "\\protect\\lstinline|git push --follow-tags origin main|" in content
    assert "\\robustify\\url" in content
    assert "\\texttt{status}" in content
    assert "\\scriptsize" in content
    assert "\\begin{landscape}" not in content


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_textual_control_escape_is_not_emitted_as_latex_command(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text(
        """---
title: Escapes de controle
---

| Regra |
|---|
| Rejeitar nova linha (\\r\\n). |
""",
        encoding="utf-8",
    )
    output = tmp_path / "doc.tex"
    convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            force=True,
        )
    )
    content = output.read_text(encoding="utf-8")
    assert "\\textbackslash{}r\\textbackslash{}n" in content
    assert "(\\r\\n)" not in content

@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_block_image_uses_max_dimensions_without_distortion(tmp_path: Path):
    source = tmp_path / "doc.md"
    image = tmp_path / "diagram.png"
    image.write_bytes(b"not-a-real-png-needed-for-pandoc")
    source.write_text(
        "---\ntitle: Imagem\n---\n\n![Arquitetura](diagram.png){width=95% height=78%}\n",
        encoding="utf-8",
    )
    output = tmp_path / "doc.tex"
    convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            force=True,
        )
    )
    content = output.read_text(encoding="utf-8")
    assert "\\usepackage{adjustbox}" in content
    assert "max width=0.9500\\linewidth" in content
    assert "max height=0.7800\\textheight" in content
    assert "\\includegraphics{\\detokenize{diagram.png}}" in content
    assert "\\caption{Arquitetura}" in content


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="Pandoc não instalado")
def test_table_fragment_requires_calc_from_configuration(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text("| A | B |\n|---|---|\n| Um | Dois |\n", encoding="utf-8")
    config = config_for(tmp_path)
    config.style_packages.remove("calc")
    with pytest.raises(ConfigError, match="calc"):
        convert(
            ConversionOptions(
                input_path=source,
                output_path=tmp_path / "doc.tex",
                user_config=config,
                config_path=tmp_path / "config.yaml",
                force=True,
            )
        )


def _convert_with_topics(tmp_path: Path, monkeypatch, rules: str, profile: str, markdown: str):
    source = tmp_path / "doc.md"
    source.write_text(f"---\ntitle: Documento\n---\n\n{markdown}", encoding="utf-8")
    rules_path = tmp_path / "rules.yaml"
    rules_path.write_text(rules, encoding="utf-8")
    monkeypatch.setattr("md2tex.converter.markdown_to_latex_fragment", lambda *args, **kwargs: "Texto")
    output = tmp_path / "doc.tex"
    result = convert(
        ConversionOptions(
            input_path=source,
            output_path=output,
            user_config=config_for(tmp_path),
            rules_path=rules_path,
            profile=profile,
            mermaid=False,
            force=True,
        )
    )
    assert output.exists()
    return result


def test_topic_rules_accept_satisfied_and_duplicate_headings(tmp_path: Path, monkeypatch):
    result = _convert_with_topics(
        tmp_path,
        monkeypatch,
        "rules:\n  adr:\n    - Decisão\n",
        "adr",
        "# decisão\n\n## DECISÃO\n",
    )
    assert not [message for message in result.messages if message.source == "topics"]


def test_topic_rules_warn_for_each_missing_original_topic(tmp_path: Path, monkeypatch):
    result = _convert_with_topics(
        tmp_path,
        monkeypatch,
        "rules:\n  adr:\n    - Contexto\n    - Decisão\n",
        "adr",
        "# Contexto\n",
    )
    warnings = [message for message in result.messages if message.source == "topics"]
    assert [message.message for message in warnings] == [
        "Tópico obrigatório ausente para o tipo 'adr': 'Decisão'."
    ]


def test_topic_rules_only_apply_to_selected_profile(tmp_path: Path, monkeypatch):
    result = _convert_with_topics(
        tmp_path,
        monkeypatch,
        "rules:\n  adr:\n    - Decisão\n  report:\n    - Conclusão\n",
        "report",
        "# Conclusão\n",
    )
    assert not [message for message in result.messages if message.source == "topics"]


def _strict_topic_options(tmp_path: Path, output: Path) -> ConversionOptions:
    source = tmp_path / "doc.md"
    source.write_text("---\ntitle: Documento\n---\n\n# Contexto\n", encoding="utf-8")
    rules_path = tmp_path / "rules.yaml"
    rules_path.write_text("rules:\n  adr:\n    - Decisão\n", encoding="utf-8")
    return ConversionOptions(
        input_path=source,
        output_path=output,
        user_config=config_for(tmp_path),
        rules_path=rules_path,
        profile="adr",
        strict=True,
        force=True,
    )


def test_strict_topics_does_not_create_output_or_run_mermaid(tmp_path: Path, monkeypatch):
    output = tmp_path / "doc.tex"
    monkeypatch.setattr(
        "md2tex.converter.render_mermaid_blocks",
        lambda *args, **kwargs: pytest.fail("Mermaid não deve executar no gate estrito"),
    )
    with pytest.raises(ValidationError, match="Decisão"):
        convert(_strict_topic_options(tmp_path, output))
    assert not output.exists()


def test_strict_topics_preserves_existing_output(tmp_path: Path):
    output = tmp_path / "doc.tex"
    output.write_bytes(b"conteudo existente")
    with pytest.raises(ValidationError, match="Validação interrompeu"):
        convert(_strict_topic_options(tmp_path, output))
    assert output.read_bytes() == b"conteudo existente"


@pytest.mark.parametrize("existing", [False, True])
def test_strict_invalid_meeting_minutes_stops_before_external_work(tmp_path: Path, monkeypatch, existing: bool):
    source = tmp_path / "invalid-meeting-minutes.md"
    source.write_text((MEETING_MINUTES_FIXTURES / "complete.md").read_text(encoding="utf-8").replace("client: Cliente Aurora / Projeto Aurora (NEP-001)\n", ""), encoding="utf-8")
    output = tmp_path / "meeting-minutes.tex"
    expected = b"conteudo existente"
    if existing: output.write_bytes(expected)
    monkeypatch.setattr("md2tex.converter.render_mermaid_blocks", lambda *args, **kwargs: pytest.fail("Mermaid não deve executar"))
    monkeypatch.setattr("md2tex.converter.markdown_to_latex_fragment", lambda *args, **kwargs: pytest.fail("Pandoc não deve executar"))
    with pytest.raises(ValidationError, match="client"):
        convert(ConversionOptions(input_path=source, output_path=output, user_config=config_for(tmp_path), profile="meeting-minutes", strict=True, force=True))
    if existing:
        assert output.read_bytes() == expected
    else:
        assert not output.exists()
