# Contract: Perfil Documento de Arquitetura de Software

## CLI

```text
md2tex INPUT.md --type software-architecture [--system-name TEXT] [--toc|--no-toc]
```

- `software-architecture` seleciona o perfil Documento de Arquitetura de Software.
- `--system-name TEXT` define o nome opcional na capa e prevalece sobre o front matter quando a opção é fornecida.
- O valor é aparado nas extremidades. Sem opção de CLI, usa-se `system-name` do front matter; opção vazia ou composta somente por espaços suprime o nome, mesmo que o front matter tenha valor.
- `--toc`/`--no-toc` controla apenas o sumário. Não controla a página de revisões.

## Markdown Front Matter

```yaml
---
title: Documento de Arquitetura do Sistema Aurora
author: Ana Silva
date: 2026-09-25
version: "1.0"
client: Projeto Aurora
system-name: Sistema Aurora
revision-history:
  - date: 2026-09-25
    version: "1.0"
    description: Criação do documento
    author: Ana Silva
  - date: 2026-10-01
    version: "1.1"
    description: Atualização da arquitetura
    author: Bruno Souza
---
```

`system-name` é opcional; espaços externos são removidos e valor vazio não é impresso. `revision-history` pode ser omitido ou ser uma lista vazia; nesses casos o perfil apresenta uma linha inicial derivada de `date`, `version` e `author`, deixando `description` vazia. Cada mapa da lista pode omitir valores de célula, que são renderizados em branco.

## Output Order

1. Capa do Documento de Arquitetura de Software; reserva-se uma área superior para o logotipo do estilo/layout, quando configurado, e o nome opcional fica alinhado à direita logo abaixo dela. Sem logotipo, o nome conserva essa posição.
2. Página própria intitulada **Histórico de Revisões**, com tabela de Data, Versão, Descrição e Autor.
3. Sumário, se habilitado.
4. Corpo convertido do Markdown.

## Topic Rules and Configured Requirements

O identificador `software-architecture` é aceito como chave em `rules.yaml`. Regras para esse identificador são aplicadas somente quando esse perfil é selecionado; nenhuma lista de tópicos é automaticamente definida por este contrato.

## Compatibility

A seleção dos perfis já existentes conserva o seu template e saída atuais. Os campos de capa e a página de revisões deste contrato são específicos ao novo perfil.
