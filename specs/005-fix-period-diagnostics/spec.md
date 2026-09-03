# Feature Specification: Corrigir diagnósticos do período

**Feature Branch**: `005-fix-period-diagnostics`  
**Created**: 2026-09-02  
**Status**: Draft  
**Input**: Corrigir, como patch v2.5.1, as mensagens da Memória de Reunião para que `period.start` e `period.end` usem rótulos claros ao autor.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Entender pendências do período (Priority: P1)

Um autor que converte uma Memória de Reunião com período incompleto identifica se falta o horário de início ou de fim, sem conhecer identificadores internos do front matter.

**Why this priority**: Diagnósticos claros permitem corrigir o documento sem tentativa e erro.

**Independent Test**: Uma memória sem início, sem fim e sem toda a estrutura de período produz os rótulos documentais correspondentes.

**Acceptance Scenarios**:

1. **Given** uma memória sem o início do período, **When** validada, **Then** o diagnóstico informa `Período — início`.
2. **Given** uma memória sem o fim do período, **When** validada, **Then** o diagnóstico informa `Período — fim`.
3. **Given** uma memória sem a estrutura de período, **When** validada, **Then** ambos os diagnósticos documentais são informados.

---

### User Story 2 - Preservar os demais diagnósticos (Priority: P2)

Um autor continua recebendo os rótulos atuais para outros campos, seções, participantes e pendências inválidos.

**Why this priority**: O patch corrige somente a terminologia inconsistente, sem regressões.

**Independent Test**: Uma validação com pendências de período e de outros tipos mantém os textos existentes para os outros itens.

**Acceptance Scenarios**:

1. **Given** uma memória com vários valores obrigatórios ausentes, **When** validada, **Then** somente os dois rótulos de período deixam de usar identificadores internos.

### Edge Cases

- Estrutura `period` ausente ou inválida mantém dois diagnósticos, um por limite.
- Valores em branco usam o mesmo rótulo documental da ausência do respectivo campo.
- Caminhos de participantes, linhas de pendência e seções permanecem inalterados.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST apresentar `Período — início` quando o início estiver ausente, em branco ou inválido.
- **FR-002**: O sistema MUST apresentar `Período — fim` quando o fim estiver ausente, em branco ou inválido.
- **FR-003**: Quando a estrutura de período estiver ausente ou inválida, o sistema MUST apresentar os dois rótulos.
- **FR-004**: O sistema MUST preservar literalmente os diagnósticos existentes para itens que não sejam os dois limites do período.
- **FR-005**: O lançamento MUST identificar a versão pública como v2.5.1.

### Key Entities

- **Limite do período**: Horário de início ou fim da reunião.
- **Diagnóstico de validação**: Mensagem que indica uma pendência ao autor.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% das validações com início ausente usam `Período — início`.
- **SC-002**: 100% das validações com fim ausente usam `Período — fim`.
- **SC-003**: A suíte automatizada mantém aprovação integral, incluindo diagnósticos não relacionados ao período.
- **SC-004**: O modo estrito continua listando pendências e interrompendo a geração quando há campos inválidos.

## Assumptions

- O YAML continua usando `period.start` e `period.end`; somente o texto do diagnóstico muda.
- Os rótulos adotados são `Período — início` e `Período — fim`.
- Esta correção é um patch compatível v2.5.1.
