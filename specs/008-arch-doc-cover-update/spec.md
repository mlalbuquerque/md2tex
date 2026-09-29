# Feature Specification: custom-cover-support

**Feature Branch**: `[008-custom-cover-support]`

**Created**: 2026-09-28

**Status**: Draft

**Input**: User description: "Vamos mudar a especificação: quero criar um comando --cover pra estebelecer uma capa. Ela passa por cima de --type e --template (--cover tem prioridade)..."

## Clarifications
### Session 2026-09-28
- Q: Como o arquivo fornecido no argumento --cover deve ser processado internamente pelo md2tex? → A: Processar como template Jinja2 (acesso às variáveis dinâmicas do Markdown)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Apply custom cover overlay (Priority: P1)

As a CLI user, I want to use the `--cover` argument to supply a custom cover layout, so that I can override the default cover provided by `--type`, `--template`, or `--style` and apply company-specific designs without hardcoding them into md2tex.

**Why this priority**: Core enabler for decoupling company-specific templates from the generic md2tex engine.

**Independent Test**: Can be tested by invoking md2tex with `--cover mycover.tex` and verifying the resulting PDF displays `mycover.tex` as the first page instead of the default cover.

### User Story 2 - Prevent conflicting configurations (Priority: P2)

As a CLI user, I want the system to reject the usage of `--template` and `--type` in the same command, so that the document generation logic remains predictable and I am guided to use only one structural definition method.

**Why this priority**: Avoids complex resolution logic and undefined behavior when two different structural profiles collide.

**Independent Test**: Can be tested by invoking `md2tex --type software-architecture --template custom.tex` and observing a validation error preventing execution.

### Edge Cases

- **Arquivo `--cover` inexistente**: O sistema interceptará isso imediatamente via validação de argumentos da CLI, abortando a execução antes do processamento.
- **Erros de sintaxe ou variáveis inexistentes no Jinja2**: O sistema abortará a compilação de forma segura, informando ao usuário que a capa personalizada contém erros de renderização.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The CLI MUST accept a `--cover FILE` argument.
- **FR-002**: If `--cover` is provided, it MUST override and completely replace any cover page generation logic defined by the active `--type`, `--template`, or default styles.
- **FR-003**: The CLI MUST enforce mutual exclusivity between the `--type` and `--template` arguments, raising a validation error if both are provided.
- **FR-004**: The system MUST remain backward compatible with existing usages of `--type` or `--template` when `--cover` is not provided (this targets patch version 2.7.2).
- **FR-005**: The `--cover` mechanism MUST support external files so that specific covers can be maintained outside the md2tex source code.
- **FR-006**: The `--cover` file MUST be processed internally as a Jinja2 template, allowing it to dynamically resolve markdown variables (like title, client, etc.) before LaTeX compilation.
- **FR-007**: The CLI MUST validate the existence of the file passed to `--cover` natively (e.g., via parameter type checks) before attempting any document processing.
- **FR-008**: The system MUST gracefully handle Jinja2 rendering errors (e.g., `TemplateSyntaxError`) originating from the `--cover` file, halting execution and informing the user.

### Key Entities

- **Cover Overlay**: The file (e.g., a `.j2.tex` template snippet or `.sty` configuration) injected specifically to replace the document's cover page.
- **CLI Configuration Flags**: `--cover`, `--type`, `--template`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully generate a PDF using `--cover` where the cover page exactly matches the provided external file, ignoring internal cover generation rules.
- **SC-002**: Passing both `--type` and `--template` results in immediate execution abortion with a clear validation error message.
- **SC-003**: All existing unit tests pass, ensuring backward compatibility for document generation without `--cover`.

## Assumptions

- The `--cover` file is responsible for its own self-contained formatting (e.g., managing `\begin{titlepage}` constraints).
- The creation of the specific external Software Architecture cover file (based on the OneDrive docx) is out of scope for the md2tex feature tasks themselves, as it will be managed as an external asset.
