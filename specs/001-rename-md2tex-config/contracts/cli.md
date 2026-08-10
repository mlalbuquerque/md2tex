# CLI Contract: md2tex 2.2.0

## Synopsis

```text
md2tex [OPTIONS] INPUT_FILE
md2tex init [--config PATH] [--force]
```

## Relevant options

| Flag | Short | Description |
|---|---|---|
| `--config` | `-c` | YAML explícito; padrão é o caminho do usuário |
| `--style` | `-s` | Substitui `style_packages`; pode repetir para informar todos os pacotes |
| `--engine` | `-e` | Sobrescreve o engine do YAML |
| `--setup` | | Assistente de dependências |
| `--check-deps` | | Relatório de dependências |
| `--force` | | Sobrescreve TEX de saída ou YAML em `init` |
| `--table-borders` | | Sobrescreve `tables.borders` |
| `--table-zebra` / `--no-table-zebra` | | Sobrescreve `tables.zebra` |
| `--verbose` | `-v` | Mostra comandos externos |
| `--version` | | Exibe versão |

## Exit codes

- `0`: sucesso.
- `1`: erro de configuração ou conversão tratado pela aplicação.
- `2`: uso inválido da CLI detectado pelo Click.
