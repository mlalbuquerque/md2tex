from md2tex.pandoc import apply_table_borders

TABLE = r"""\begin{longtable}[]{@{}
  >{\RaggedRight\arraybackslash}p{0.4\columnwidth}
  >{\RaggedRight\arraybackslash}p{0.6\columnwidth}@{}}
\toprule\noalign{}
A & B \\
\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Um & Dois \\
Três & Quatro \\
\end{longtable}"""


def test_grid_borders_adds_full_table_contours():
    rendered = apply_table_borders(TABLE, "grid")
    assert r"\begin{longtable}[]{|" in rendered
    assert r"p{0.4\columnwidth}|" in rendered
    assert r"p{0.6\columnwidth}|}" in rendered
    assert r"\toprule" not in rendered
    assert rendered.count(r"\hline") >= 5


def test_outer_borders_preserves_booktabs_rules():
    rendered = apply_table_borders(TABLE, "outer")
    assert r"\begin{longtable}[]{|" in rendered
    assert r"p{0.6\columnwidth}|}" in rendered
    assert r"\toprule" in rendered
