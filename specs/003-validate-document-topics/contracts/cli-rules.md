# CLI Contract: regras de tópicos

```text
md2tex [OPTIONS] INPUT_FILE
md2tex init [--config PATH] [--force]
md2tex rules init [--rules PATH] [--force]
```

`rules init` cria `~/.config/md2tex/rules.yaml` sem `--rules`; cria diretórios pai e recusa substituir um arquivo existente sem `--force`.

| Opção | Contrato |
|---|---|
| `--rules PATH` | Usa este YAML em vez do padrão. Arquivo explícito ausente, ilegível ou inválido encerra antes de escrever saída. |
| `--validate` / `--no-validate` | Controla pendências; `--no-validate` não suprime erro de `--rules` explícito inválido. |
| `--strict` | Pendências impedem criar ou substituir TEX. |

Em modo normal: `AVISO [topics]: Tópico obrigatório ausente para o tipo 'adr': 'Decisão'.`

Com `--strict`: `Erro: Validação interrompeu a geração:` e cada pendência; a saída permanece intacta.

O modelo traz exemplos completos, comentados e inativos para `default`, `report`, `meeting-minutes`, `adr` e `technical-plan`; remover comentários e adaptar habilita cada perfil.
