# Quickstart: Requisitos configuráveis

## Pré-requisito

Use uma cópia válida de `config.yaml` e acrescente o exemplo de `document_requirements` do [contrato](contracts/config-document-requirements.md).

## Cenário 1 — orientação de campo

1. Remova `client` de uma Memória de Reunião.
2. Execute `md2tex --type meeting-minutes --config config.yaml arquivo.md`.
3. Confirme o rótulo `Cliente/Projeto`, a instrução configurada e o exemplo YAML; `client` não deve ser o rótulo público.

## Cenário 2 — orientação de seção e bloqueio estrito

1. Remova a seção Objetivos da Reunião.
2. Execute com `--strict` e um destino existente.
3. Confirme o exemplo Markdown na mensagem e que o destino não foi alterado.

## Cenário 3 — isolamento e compatibilidade

1. Converta um tipo sem `document_requirements`.
2. Confirme que sua validação existente não mudou.
3. Execute uma Memória de Reunião com `--client` e confirme que o valor da CLI satisfaz o requisito.

## Cenário 4 — configuração inválida

1. Remova `example` de uma regra.
2. Execute a conversão.
3. Confirme que a configuração é recusada antes de gerar saída e identifica a regra incompleta.
