from pathlib import Path
import shutil
import time

import pytest

from md2tex.converter import convert
from md2tex.models import ConversionOptions


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
            style_path="netra-letterhead",
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
            style_path="netra-letterhead",
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
            style_path="netra-letterhead",
            force=True,
        )
    )
    content = output.read_text(encoding="utf-8")
    assert "\\usepackage{adjustbox}" in content
    assert "max width=0.9500\\linewidth" in content
    assert "max height=0.7800\\textheight" in content
    assert "\\includegraphics{\\detokenize{diagram.png}}" in content
    assert "\\caption{Arquitetura}" in content
