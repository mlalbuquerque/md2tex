# Contrato da CLI: `--subtitle`

## Interface pública

```text
md2tex INPUT_FILE [--subtitle TEXT]
```

| Aspecto | Contrato |
| --- | --- |
| Ajuda | Informa que a opção sobrescreve o subtítulo do documento. |
| Precedência | Opção fornecida vence `subtitle` do front matter. |
| Omissão | Conserva `subtitle` do front matter, se houver. |
| Valor vazio | Remove o subtítulo efetivo; a capa não mostra linha de subtítulo. |

## Exemplos

```bash
md2tex documento.md --subtitle "Guia de referência"
md2tex documento.md --subtitle ""
```

