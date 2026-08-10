# Quickstart: validar o subtítulo pela CLI

## Pré-requisitos

- Python 3.10 ou superior e dependências de desenvolvimento instaladas.
- Uma configuração válida do md2tex, criada por `md2tex init` ou fornecida por `--config`.

Consulte o [contrato da CLI](contracts/cli-subtitle.md) e o [modelo de dados](data-model.md) para as regras de precedência.

## 1. Executar os testes automatizados

```bash
pytest -q
```

Resultado esperado: todos os testes passam, incluindo os que cobrem ajuda, versão 2.3.0, precedência de subtítulo e capas dos perfis.

## 2. Converter com subtítulo informado pela CLI

Crie um documento com front matter contendo um subtítulo diferente e converta-o:

```bash
md2tex documento.md --config config.yaml --subtitle "Guia de referência" --force
```

Resultado esperado: o TEX gerado contém `Guia de referência` abaixo do título; o subtítulo do front matter não aparece.

## 3. Converter sem a opção de subtítulo

```bash
md2tex documento.md --config config.yaml --force
```

Resultado esperado: se houver `subtitle` no front matter, ele aparece; se não houver, nenhuma linha de subtítulo é produzida. O tipo de documento aparece com autoria, versão e data.

## 4. Limpar o subtítulo explicitamente

```bash
md2tex documento.md --config config.yaml --subtitle "" --force
```

Resultado esperado: nenhuma linha de subtítulo é produzida, inclusive quando o front matter possui um valor.

## 5. Confirmar a versão e a ajuda

```bash
md2tex --version
md2tex --help
```

Resultado esperado: a versão é 2.3.0 e a ajuda lista `--subtitle` com sua descrição.
