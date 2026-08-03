from pathlib import Path

from md2tex.compiler import clean_latex_auxiliary_files


def _create_aux_files(tex: Path) -> None:
    tex.write_text("tex", encoding="utf-8")
    for suffix in [".aux", ".log", ".out", ".toc", ".synctex.gz", ".xdv"]:
        tex.with_suffix(suffix).write_text("aux", encoding="utf-8")


def test_clean_preserves_toc(tmp_path: Path):
    tex = tmp_path / "doc.tex"
    _create_aux_files(tex)
    clean_latex_auxiliary_files(tex, include_toc=False)
    assert tex.with_suffix(".toc").exists()
    assert not tex.with_suffix(".aux").exists()
    assert not tex.with_suffix(".synctex.gz").exists()


def test_clean_all_removes_toc(tmp_path: Path):
    tex = tmp_path / "doc.tex"
    _create_aux_files(tex)
    clean_latex_auxiliary_files(tex, include_toc=True)
    assert not tex.with_suffix(".toc").exists()
    assert tex.exists()
