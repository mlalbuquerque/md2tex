# Feature Specification: md2tex 2.2.0 — Configuração Explícita e Inicialização

**Feature Branch**: `001-rename-md2tex-config`
**Created**: 2026-08-03
**Status**: Implemented (2.2.0)

## Context

O md2tex não possui valores de estilo ou de compilação embutidos. A configuração YAML do usuário é a única fonte de classe, pacotes, geometria, tipografia, preâmbulo e motor LaTeX. O comando `md2tex init` cria um modelo completo inicial sem sobrescrever um arquivo existente por padrão.

## User Scenarios & Testing

### User Story 1 — Criar a configuração inicial (P1)

Como novo usuário, quero executar `md2tex init` para obter uma configuração funcional com todos os campos obrigatórios.

**Acceptance scenarios**:
1. `md2tex init` cria `~/.config/md2tex/config.yaml` com um modelo válido.
2. Um arquivo existente não é sobrescrito sem `--force`.
3. `md2tex init --config caminho.yaml` cria o arquivo no caminho informado.

### User Story 2 — Converter com configuração explícita (P1)

Como autor, quero que toda conversão use exclusivamente os valores do meu YAML, sem estilo implícito no md2tex.

**Acceptance scenarios**:
1. Uma configuração válida define classe, opções, pacotes, geometria, tipografia, preâmbulo e motor.
2. Sem configuração válida, a conversão falha e orienta o uso de `md2tex init` ou `--config`.
3. O LaTeX gerado não adiciona pacotes, idioma, macros ou defaults de estilo que não estejam na configuração.

### User Story 3 — Validar e sobrescrever configuração (P2)

Como usuário avançado, quero receber erros claros para YAML incompleto/inválido e sobrescrever opções por CLI quando suportado.

**Acceptance scenarios**:
1. Chaves ausentes, desconhecidas ou com tipo inválido são rejeitadas antes da conversão.
2. `--engine` e `--style` têm precedência sobre o YAML.
3. Pacotes `.sty` locais inacessíveis em YAML ou `--style` geram aviso descritivo.

## Functional Requirements

- **FR-001**: O nome público e os artefatos ativos usam exclusivamente `md2tex`.
- **FR-002**: Nenhum default de classe, pacote, idioma, geometria, tipografia, macro de estilo ou motor LaTeX existe no código de conversão.
- **FR-003**: O YAML deve conter explicitamente `document_class`, `class_options`, `style_packages`, `page_geometry`, `typography`, `preamble_includes` e `compiler_options`.
- **FR-004**: `md2tex init` cria um YAML completo e não sobrescreve arquivo existente sem `--force`.
- **FR-005**: A CLI valida schema e tipos do YAML, incluindo engine permitido e chaves desconhecidas.
- **FR-006**: `--engine` e `--style` prevalecem sobre a configuração carregada.
- **FR-007**: `typography` aplica idioma, tamanho, fonte principal e espaçamento quando informados.
- **FR-008**: `--setup` e `--check-deps` permanecem as interfaces de dependências.

## Success Criteria

- **SC-001**: 100% das conversões utilizam uma configuração YAML válida antes de gerar TEX.
- **SC-002**: `md2tex init` gera uma configuração que passa pela validação sem edição manual.
- **SC-003**: Testes automatizados cobrem criação, proteção contra sobrescrita, schema inválido e conversão configurada.

### User Story 4 — Configurar aparência de tabelas (P1)

Como autor, quero definir zebrado, bordas, largura, fonte e paisagem por configuração ou flags, inclusive com estilos `.sty` próprios.

**Acceptance scenarios**:
1. `tables.borders: grid` gera uma grade completa.
2. `tables.zebra: true` aciona as macros de zebrado configuradas pelo estilo.
3. `--table-borders` e `--table-zebra` sobrescrevem o YAML.

- **FR-009**: O YAML deve conter `tables.landscape`, `tables.font`, `tables.width`, `tables.borders` e `tables.zebra`.
- **FR-010**: O md2tex deve aplicar os valores de tabelas e permitir sobrescrita por CLI.

## Assumptions

- O perfil criado por `init` usa XeLaTeX e pacotes comuns; o usuário pode ajustá-lo para sua distribuição TeX.
- Bibliografia e filtros Lua externos não fazem parte da 2.2.0.
