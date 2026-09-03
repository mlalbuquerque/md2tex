# Data Model: Requisitos documentais declarativos

## UserConfig

| Campo | Tipo | Regra |
|---|---|---|
| `document_requirements` | mapa opcional | Perfis conhecidos para regras de requisitos; ausência equivale a mapa vazio. |

## ProfileRequirements

| Campo | Tipo | Regra |
|---|---|---|
| `fields` | lista | Requisitos para chaves do front matter ou metadados finais. |
| `sections` | lista | Requisitos para títulos e conteúdo Markdown. |

## Requirement

| Campo | Tipo | Regra |
|---|---|---|
| `path` / `section` | texto | Identificador não vazio e único na respectiva lista. |
| `label` | texto | Rótulo público não vazio. |
| `required` | booleano | `true` gera pendência para ausência; `false` não gera. |
| `instruction` | texto | Orientação não vazia para o autor. |
| `example` | texto | Trecho YAML ou Markdown não vazio, inclusive multilinha. |

## Relações e precedência

Um perfil possui zero ou mais requisitos de campo e seção. Para campos, o valor final considera a precedência CLI → front matter. Uma regra configurada para caminho ou seção equivalente fornece a mensagem pública; validadores estruturais permanecem responsáveis por formas complexas não representadas como requisito simples.
