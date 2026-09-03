# Feature Specification: Configurar requisitos de validação

**Feature Branch**: `006-configure-validation`  
**Created**: 2026-09-02  
**Status**: Draft  
**Input**: Permitir configurar, no `config.yaml`, requisitos e orientações de preenchimento por tipo documental, incluindo a apresentação pública de Cliente.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar requisitos de um tipo documental (Priority: P1)

Um administrador define no arquivo de configuração quais campos e seções cada tipo documental exige e como esses itens devem ser apresentados a quem escreve o Markdown.

**Why this priority**: Cada organização pode adaptar o documento aos seus processos sem alterar o programa.

**Independent Test**: Uma regra configurada para um tipo documental é aplicada à conversão desse tipo e não afeta outro tipo sem regra.

**Acceptance Scenarios**:

1. **Given** um tipo documental com requisitos configurados, **When** o autor converte esse tipo, **Then** o sistema valida os campos e seções definidos para ele.
2. **Given** tipos com requisitos diferentes, **When** cada um é convertido, **Then** cada conversão aplica somente as suas próprias regras.
3. **Given** um tipo sem requisitos configurados, **When** convertido, **Then** seu comportamento de validação existente é preservado.

---

### User Story 2 - Corrigir o campo ausente com orientação (Priority: P1)

Um autor recebe um diagnóstico claro para cada campo obrigatório ausente, com rótulo compreensível, instrução e exemplo pronto para copiar no arquivo Markdown.

**Why this priority**: O diagnóstico deve reduzir a necessidade de consultar documentação ou conhecer chaves internas.

**Independent Test**: Um campo obrigatório ausente produz uma mensagem com rótulo, motivo, instrução e exemplo configurados.

**Acceptance Scenarios**:

1. **Given** o início do período ausente em uma Memória de Reunião, **When** a validação falha, **Then** a mensagem identifica `Período — início` e mostra um exemplo para adicioná-lo ao front matter.
2. **Given** o campo técnico `client` ausente, **When** a validação falha, **Then** a mensagem exibe o rótulo público `Cliente/Projeto`, e não `client`.
3. **Given** uma seção obrigatória ausente, **When** a validação falha, **Then** a mensagem mostra um exemplo Markdown apropriado para essa seção.
4. **Given** várias pendências, **When** o modo estrito é usado, **Then** todas as orientações são exibidas e a saída continua bloqueada.

---

### User Story 3 - Manter uma configuração segura (Priority: P2)

Um administrador recebe diagnóstico acionável quando uma regra de requisitos no arquivo de configuração é inválida, em vez de uma conversão parcialmente configurada.

**Why this priority**: Regras malformadas não devem resultar em documentos validados de maneira ambígua.

**Independent Test**: Uma configuração inválida informa o item e o problema; uma configuração válida preserva a precedência da CLI e as regras existentes.

**Acceptance Scenarios**:

1. **Given** uma regra sem informação obrigatória para orientar o autor, **When** a configuração é carregada, **Then** o sistema informa a regra inválida de forma acionável.
2. **Given** valores equivalentes na CLI e no front matter, **When** uma regra configurada é validada, **Then** a precedência atual da CLI é preservada.

### Edge Cases

- Um campo opcional com valor ausente não produz erro nem orientação obrigatória.
- Um exemplo multilinha preserva a formatação necessária para o autor copiá-lo.
- Uma regra para caminho aninhado, como o início de um período, aponta para o local correto no front matter.
- Configurações existentes que não definem requisitos declarativos continuam válidas.
- As regras estruturais específicas já existentes continuam protegendo o documento quando não forem substituídas por configuração compatível.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST permitir declarar requisitos de campos e seções por tipo documental no `config.yaml`.
- **FR-002**: Cada requisito declarativo MUST permitir definir caminho ou seção, rótulo público, obrigatoriedade, instrução e exemplo de preenchimento.
- **FR-003**: Para uma pendência de requisito obrigatório, o sistema MUST mostrar rótulo público, descrição do problema, instrução e exemplo copiável na mensagem de validação.
- **FR-004**: O sistema MUST usar `Cliente/Projeto` como rótulo público para a pendência do campo técnico `client` da Memória de Reunião.
- **FR-005**: O sistema MUST permitir exemplos YAML para campos de front matter e exemplos Markdown para seções do corpo.
- **FR-006**: O sistema MUST ignorar a ausência de requisito opcional sem gerar pendência.
- **FR-007**: O sistema MUST manter as regras configuradas isoladas por tipo documental e preservar o comportamento dos tipos sem configuração declarativa.
- **FR-008**: O sistema MUST rejeitar configuração declarativa inválida com diagnóstico que identifique a regra e a correção necessária.
- **FR-009**: O sistema MUST preservar a precedência atual de argumentos da CLI sobre valores equivalentes do front matter e continuar bloqueando saída inválida com `--strict`.
- **FR-010**: O sistema MUST documentar o formato de configuração e fornecer um exemplo funcional para Memória de Reunião.

### Key Entities

- **Requisito documental**: Regra configurada para um tipo, que declara o que é exigido e como orientar o autor.
- **Orientação de preenchimento**: Rótulo, instrução e exemplo público exibidos quando um requisito falha.
- **Tipo documental**: Categoria selecionada na conversão, com conjunto próprio de requisitos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em todos os campos e seções obrigatórios configurados testados, 100% dos diagnósticos incluem rótulo, instrução e exemplo.
- **SC-002**: Em todos os cenários de Memória de Reunião com Cliente/Projeto ausente, nenhum diagnóstico expõe o identificador `client` como rótulo ao autor.
- **SC-003**: Tipos sem requisitos declarativos mantêm 100% dos cenários de validação existentes aprovados.
- **SC-004**: Em modo estrito, 100% das conversões com requisito obrigatório inválido deixam a saída inexistente ou inalterada.
- **SC-005**: Uma configuração inválida é recusada antes da conversão e identifica a regra que precisa ser corrigida.

## Assumptions

- O `config.yaml` já usado pelo usuário é a fonte de configuração para as novas regras; não será necessário um arquivo adicional.
- A configuração complementa as validações estruturais existentes; não permite desligar proteções essenciais por acidente.
- Os tipos existentes podem adotar regras declarativas gradualmente, enquanto tipos não configurados preservam o comportamento atual.
- A expressão pública para o campo `client` da Memória de Reunião é `Cliente/Projeto`.
