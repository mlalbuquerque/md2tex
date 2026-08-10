# Configuration Contract: md2tex 2.2.0

O YAML exige todas as chaves de topo: `document_class`, `class_options`, `style_packages`, `page_geometry`, `typography`, `preamble_includes` e `compiler_options` e `tables`.

`typography.fontsize` é obrigatório. As chaves permitidas em `typography` são `language`, `fontsize`, `mainfont` e `line_spacing`. `compiler_options` contém exclusivamente `engine`, com valor `pdflatex`, `xelatex` ou `lualatex`.

Use `md2tex init` para obter o modelo completo e válido.

## Tables

```yaml
tables:
  landscape: auto # auto | always | never
  font: small # normalsize | small | footnotesize | scriptsize
  width: auto # auto | equal | natural
  borders: none # none | outer | grid
  zebra: false
```
