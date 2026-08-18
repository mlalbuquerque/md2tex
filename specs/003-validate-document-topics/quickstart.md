# Quickstart: validação de tópicos

```bash
pip install -e ".[dev]"
md2tex init
md2tex rules init
```

Edite `~/.config/md2tex/rules.yaml`, descomentando e adaptando somente os perfis desejados. Para usar regras de projeto:

```bash
md2tex rules init --rules ./md2tex-rules.yaml
```

A segunda criação no mesmo destino falha sem modificá-lo, salvo com `--force`.

```bash
md2tex decisao.md --type adr --rules ./md2tex-rules.yaml --config ./config.yaml
```

Com `Decisão` faltante, há `AVISO [topics]` e o TEX é criado. Com `--strict`, a execução falha antes da escrita e não altera saída existente:

```bash
md2tex decisao.md --type adr --rules ./md2tex-rules.yaml --config ./config.yaml --strict -o decisao.tex
pytest -q tests/test_rules.py tests/test_validator.py tests/test_cli.py tests/test_integration.py
```
