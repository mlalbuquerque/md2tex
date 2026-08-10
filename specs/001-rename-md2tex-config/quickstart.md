# Quickstart: md2tex 2.2.0

```bash
md2tex init
md2tex documento.md --pdf
```

Para projeto específico:

```bash
md2tex init --config ./md2tex.yaml
md2tex documento.md --config ./md2tex.yaml --style ./estilos/empresa.sty
```

Resultados esperados:

1. `init` cria um YAML válido e informa o caminho.
2. Executar `init` novamente falha sem `--force`.
3. Uma conversão sem YAML falha e recomenda `md2tex init`.
4. Alterações de `typography`, `style_packages` e `preamble_includes` aparecem no TEX gerado.

## Tabelas

Defina `tables.borders: grid` e `tables.zebra: true` para grade completa e zebrado. Para um estilo que fornece as macros `mdtexStartTable`/`mdtexEndTable`, o zebrado é aplicado automaticamente. Use `--table-borders grid --table-zebra` para sobrescrever uma execução.
