# Research: Perfil Documento de Arquitetura de Software

**Date**: 2026-09-25  
**Scope**: Decisões de produto e integração necessárias para planejar o perfil solicitado.

## Decision: Identificador `software-architecture`

**Rationale**: Os perfis existentes usam identificadores em inglês e kebab-case (`meeting-minutes`, `technical-plan`). O identificador será passado a `--type` e usado como chave em `rules.yaml`.

**Alternatives considered**: `architecture` seria mais curto, mas é menos específico e pode se confundir com um ADR; `documento-arquitetura` romperia o padrão dos identificadores existentes.

## Decision: Template dedicado, metadados específicos ao perfil

**Rationale**: O pedido atualizado define um tipo documental próprio. O conteúdo atual adicionado a `base.tex.j2` deve ser transferido para o novo template; `default` deve voltar ao comportamento genérico anterior. O mecanismo existente já resolve template por entrada em `PROFILES`.

**Alternatives considered**: Manter os campos no template base afetaria todos os documentos genéricos. Usar apenas `--template` não oferece seleção estável do perfil nem validação de regras sob identificador próprio.

## Decision: Nome do sistema opcional com precedência da CLI

**Rationale**: Usar `system-name` no front matter e `--system-name` na linha de comando mantém o estilo de metadados existente. A CLI vence o front matter conforme a regra constitucional, inclusive se explicitamente vazia. Espaços externos são removidos e valor vazio não imprime rótulo ou placeholder.

**Alternatives considered**: Criar um novo arquivo de configuração misturaria dados do documento com estilo e duplicaria os mecanismos existentes.

## Decision: Histórico como lista ordenada no front matter

**Rationale**: Representar revisões como lista de objetos `revision-history` mantém a ordem de leitura, permite as quatro colunas do modelo OPE-RQ-89 e evita converter valores livres do corpo em metadados. Sem entradas, gerar uma linha inicial usando data, versão e autor documentais, com descrição vazia, preserva o comportamento que já foi implementado.

**Alternatives considered**: Uma tabela Markdown no corpo não garante página dedicada antes do TOC. Campos separados por revisão tornam o formato difícil de ampliar.

## Decision: Página de revisões independente do TOC

**Rationale**: Renderizar capa, página de revisões, TOC opcional e corpo nesta ordem satisfaz a posição obrigatória. O histórico continua presente com `--no-toc`.

**Alternatives considered**: Colocar a tabela no corpo a faria aparecer após o TOC ou dependeria do autor incluir uma seção.

## Decision: Layout sem identidade corporativa embutida

**Rationale**: A posição do nome do sistema deve ficar no alto à direita, sob uma área superior reservada ao logotipo, enquanto logotipo, classe, geometria e tipografia permanecem responsabilidade da configuração/estilo do usuário. Sem logotipo, o nome conserva a mesma posição. O perfil não deve incluir um logo Netra/UEFS nem estilos próprios.

**Alternatives considered**: Embutir o logo do DOCX de referência violaria os princípios de arquitetura genérica e estilo configurável.

## Existing Integration Points

- `src/md2tex/profiles.py` é o registro compartilhado usado pela CLI e pelo carregador de regras de tópicos.
- `src/md2tex/metadata.py` constrói os metadados efetivos depois de ler o front matter; `ConversionOptions` representa opções da CLI.
- `src/md2tex/converter.py` seleciona template pelo perfil e expõe o objeto `metadata` ao Jinja.
- `src/md2tex/templates/base.tex.j2` atualmente contém as alterações de nome do sistema e histórico que devem ser isoladas no novo perfil.
- `src/md2tex/templates/rules.yaml` e `README.md` enumeram os perfis; a referência CLI do README omite hoje `default`.
- Os testes existentes estão em `tests/test_metadata.py`, `tests/test_cli.py`, `tests/test_rules.py` e `tests/test_integration.py`.
