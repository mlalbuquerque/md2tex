# Feature Specification: Atualizar memória de reunião

**Feature Branch**: `004-update-meeting-minutes`  
**Created**: 2026-08-31  
**Status**: Draft  
**Input**: Atualizar o tipo Memória de Reunião para usar o padrão visual letterhead da Netra e exigir os campos identificados no documento de referência `COR-RQ-01 – Memória de Reunião, rev. 05`.

## Clarifications

### Session 2026-08-31

- Q: Quais campos devem bloquear a geração quando estiverem vazios? → A: Cliente/Projeto — incluindo o código NEP quando o projeto possuir um código NEP atribuído —, Produtor/a, Data, Período, Objetivos, Tópicos e Considerações/Definições; participantes são opcionais e pendências só exigem seus campos quando existirem.
- Q: Qual formato os metadados obrigatórios devem usar no início do Markdown? → A: Front matter YAML entre delimitadores `---` no início do arquivo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gerar uma memória no padrão Netra (Priority: P1)

Um autor seleciona o tipo Memória de Reunião e gera o documento com a apresentação corporativa letterhead da Netra, preenchendo a identificação e o conteúdo da reunião conforme o modelo de referência.

**Why this priority**: A entrega principal é disponibilizar um tipo documental que reproduza a estrutura de trabalho da Netra de forma consistente.

**Independent Test**: Uma memória completa, com todos os dados e seções requeridos, pode ser convertida e contém a identificação, participantes, seções e tabela de pendências previstos.

**Acceptance Scenarios**:

1. **Given** uma memória com todos os dados obrigatórios, **When** o autor a converte como Memória de Reunião, **Then** o resultado usa o padrão letterhead da Netra e apresenta todos os dados na estrutura do modelo.
2. **Given** uma memória com participantes do cliente e da Netra, **When** o autor a converte, **Then** cada participante é apresentado com nome e cargo/função no respectivo grupo.
3. **Given** uma memória com uma ou mais pendências, **When** o autor a converte, **Then** cada pendência apresenta descrição, responsável e prazo para solução.

---

### User Story 2 - Identificar informação obrigatória ausente (Priority: P2)

Um autor recebe indicação clara dos campos obrigatórios não preenchidos antes de produzir um documento final incompleto.

**Why this priority**: Evita memórias sem contexto, responsáveis ou encaminhamentos necessários para consulta posterior.

**Independent Test**: Ao validar uma memória que omite cada campo obrigatório, o autor recebe uma indicação nominal de cada ausência.

**Acceptance Scenarios**:

1. **Given** uma memória sem um campo obrigatório, **When** o autor solicita a conversão com validação, **Then** o sistema informa o campo ausente de forma acionável.
2. **Given** uma memória sem campos obrigatórios, **When** o autor usa o modo estrito, **Then** a geração do arquivo de saída é interrompida antes de alterá-lo.

---

### User Story 3 - Registrar reunião sem pendências (Priority: P3)

Um autor consegue registrar uma reunião encerrada sem itens de acompanhamento, sem precisar inventar uma pendência para satisfazer o modelo.

**Why this priority**: Nem toda reunião gera ações pendentes; o tipo não deve criar informação artificial.

**Independent Test**: Uma memória completa sem linhas de pendência é aceita quando a ausência de pendências é declarada conforme a convenção definida.

**Acceptance Scenarios**:

1. **Given** uma reunião que não gerou pendências, **When** o autor registra explicitamente essa condição, **Then** a memória é considerada completa e apresenta a situação de forma inequívoca.

### Edge Cases

- Participante listado sem nome ou sem cargo/função deve ser apontado como incompleto.
- Uma reunião pode ter múltiplos participantes em cada grupo, inclusive nenhum participante em um dos grupos somente se isso for permitido pela regra definida.
- Cada pendência deve manter seu responsável e prazo associado, mesmo com várias pendências.
- Campos preenchidos apenas com espaços em branco não devem satisfazer uma exigência. Valores de exemplo são aceitos quando forem textos não vazios.
- A ausência de pendências deve ser distinguida de uma tabela de pendências parcialmente preenchida.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST disponibilizar a Memória de Reunião como tipo documental com apresentação compatível com o padrão letterhead da Netra já configurado pelo usuário.
- **FR-002**: O sistema MUST exigir na identificação da memória os campos Cliente/Projeto, Produtor/a, Data e Período de início e fim; Cliente/Projeto deve incluir o código NEP quando o projeto possuir um código NEP atribuído.
- **FR-003**: O sistema MUST estruturar participantes em dois grupos: Cliente e Netra; cada participante deve conter Nome e Cargo/Função.
- **FR-004**: O sistema MUST exigir as seções Objetivos da Reunião, Tópicos Abordados e Considerações Gerais e Definições.
- **FR-005**: O sistema MUST estruturar cada Pendência informada com os campos Pendência, Responsável e Prazo para Solução, sem exigir a existência de uma pendência.
- **FR-006**: O sistema MUST indicar nominalmente cada campo ou seção obrigatória não preenchida durante a validação.
- **FR-007**: O sistema MUST impedir a criação ou alteração da saída no modo estrito quando houver campos ou seções obrigatórias pendentes.
- **FR-008**: O sistema MUST aceitar o texto `Sem pendências` como a declaração explícita de que a reunião não gerou itens de acompanhamento.
- **FR-009**: O sistema MUST permitir que os grupos Cliente e Netra não tenham participantes, para atender inclusive a reuniões exclusivamente internas da Netra; cada participante informado deve conter Nome e Cargo/Função.
- **FR-010**: O sistema MUST receber os dados de identificação e participantes em front matter YAML, delimitado por `---`, no início do Markdown.

### Key Entities

- **Memória de Reunião**: Registro de uma reunião, identificado por cliente/projeto, código NEP quando atribuído, produtor/a, data e período.
- **Participante**: Pessoa vinculada ao grupo Cliente ou Netra, com nome e cargo/função.
- **Pendência**: Ação de acompanhamento com descrição, responsável e prazo para solução.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Uma memória preenchida com todos os dados obrigatórios é convertida sem avisos de campos obrigatórios ausentes.
- **SC-002**: Em uma memória que omite qualquer combinação de campos obrigatórios, 100% das ausências são identificadas nominalmente na validação.
- **SC-003**: No modo estrito, 100% das memórias com campos obrigatórios ausentes deixam o arquivo de saída inexistente ou inalterado.
- **SC-004**: Um autor consegue registrar uma reunião completa, incluindo pelo menos dois participantes e duas pendências, usando somente a estrutura documentada do tipo.

## Assumptions

- O padrão visual letterhead da Netra já está disponível na configuração de estilo do usuário; esta feature não altera nem incorpora regras de estilo no mecanismo central.
- Os campos extraídos do documento de referência são candidatos a obrigatórios: Cliente/Projeto, código NEP quando atribuído, Produtor/a, Data, Período, Nome e Cargo/Função dos participantes, Objetivos da Reunião, Tópicos Abordados, Considerações Gerais e Definições, e os três campos de cada pendência.
- A data é uma única data de reunião e o período contém horário inicial e final.
- A feature se limita ao tipo Memória de Reunião e não altera os requisitos dos demais tipos documentais.
- Uma reunião sem pendências declara essa condição com o texto `Sem pendências`.
- Os grupos Cliente e Netra podem ficar vazios; reuniões internas da Netra são um caso válido.
- Os campos que bloqueiam a geração quando vazios são Cliente/Projeto, Produtor/a, Data, Período, Objetivos da Reunião, Tópicos Abordados e Considerações Gerais e Definições; o código NEP é exigido quando tiver sido atribuído ao projeto.
- Os metadados obrigatórios usam front matter YAML delimitado por `---` no início do arquivo.
