# Feature Specification: Renaming to md2tex and Adding Generic Style Configuration

**Feature Branch**: `001-rename-md2tex-config`

**Created**: 2026-08-03

**Status**: Draft

**Input**: User description: "Quero q o sistema mude de nome pra "md2tex". E quero q ele seja mais genérico ainda, sem ser direcionado pra Netra. Então, vamos criar um arquivo de configuração onde podemos colocar informações de estilo (.sty) padrão. Tudo que tiver valor padrão, pode colocar nesse arquivo de configuração."

## Clarifications

### Session 2026-08-03

- Q: Formato e nome padrão do arquivo de configuração → A: YAML (`config.yaml`) no diretório de configuração do usuário (`~/.config/md2tex/config.yaml`).
- Q: Localização e hierarquia do arquivo de configuração → A: Apenas no diretório de configuração do usuário (`~/.config/md2tex/config.yaml`), sem valores padrão ou fallbacks embutidos nativamente no código-fonte.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - System Renaming and Netra Decoupling (Priority: P1)

As a user converting Markdown documents to LaTeX/PDF, I want the system to be named `md2tex` and be completely generic, so that I can use it for any project or context without hardcoded assumptions or branding tied to Netra.

**Why this priority**: Renaming the project and eliminating company/project-specific coupling establishes the core identity and scope of `md2tex` as a standalone, general-purpose CLI tool.

**Independent Test**: Execute the system under the `md2tex` command name and convert a generic Markdown file to LaTeX without any Netra-specific header, branding, or mandatory Netra dependencies appearing in the output.

**Acceptance Scenarios**:

1. **Given** a Markdown document with standard text and headings, **When** processed with `md2tex`, **Then** the system outputs a generic LaTeX document free of Netra-specific macros or references.
2. **Given** the command-line interface, **When** checking help or version information, **Then** the application identifies itself consistently as `md2tex`.

---

### User Story 2 - User Configuration File for Styling and Defaults (Priority: P1)

As a document author, I want all default LaTeX style packages (`.sty`), document class parameters, and formatting options to be defined exclusively in a user configuration file (`~/.config/md2tex/config.yaml`), so that the codebase remains completely decoupled from specific style defaults.

**Why this priority**: Centralizing all default parameters into a user configuration file without code-level hardcoded fallbacks ensures maximum flexibility and clean separation of concerns.

**Independent Test**: Create the user configuration file defining `.sty` packages and document settings, run `md2tex` on a Markdown file, and verify that the generated LaTeX document reads and applies those settings directly from the configuration file.

**Acceptance Scenarios**:

1. **Given** a user configuration file (`~/.config/md2tex/config.yaml`) with default style entries (such as default `.sty` package imports and page setup), **When** `md2tex` converts a Markdown file without explicit CLI styling flags, **Then** the generated LaTeX document includes all `.sty` packages and settings specified in the user configuration file.
2. **Given** no user configuration file is present at `~/.config/md2tex/config.yaml` and no explicit `--config` flag is passed, **When** `md2tex` executes, **Then** it prompts or alerts the user to provide/create a valid configuration file.

---

### User Story 3 - CLI Override and Precedence Hierarchy (Priority: P2)

As a power user, I want explicit command-line flags to override values defined in the user configuration file, so that I can easily customize individual conversion runs without altering my main configuration file.

**Why this priority**: Flexible parameter resolution allows per-run adjustments via CLI parameters while relying on the user config file as the single source of truth for defaults.

**Independent Test**: Pass a CLI flag that conflicts with a setting in `~/.config/md2tex/config.yaml` (e.g. specifying a different style package or document geometry), and confirm that the output reflects the CLI flag's value.

**Acceptance Scenarios**:

1. **Given** a user configuration file setting a default font size or style package and a CLI invocation specifying a different value, **When** conversion runs, **Then** the CLI value takes precedence over the user configuration file setting.

---

### Edge Cases

- **Missing Config File**: When no configuration file exists in `~/.config/md2tex/config.yaml` and no custom `--config` path is provided, `md2tex` must output a clear and helpful error/notice instructing the user to create the configuration file (since no internal defaults exist).
- **Malformed Config File**: When a configuration file contains syntax errors or invalid keys, `md2tex` must report a clear error message detailing the issue and line number.
- **Unreachable `.sty` Packages**: If a configured `.sty` package path is relative or not found in the TeX path, `md2tex` should emit a descriptive warning/error prior to or during compilation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST be renamed to `md2tex` across all CLI entry points, documentation, and user-facing outputs.
- **FR-002**: System MUST remove all hardcoded references, templates, and internal default values specific to Netra or default styling from the codebase.
- **FR-003**: System MUST load configuration exclusively from the user directory (`~/.config/md2tex/config.yaml`) unless a custom path is specified via `--config` CLI flag.
- **FR-004**: System MUST allow users to specify all default LaTeX style files (`.sty`), preamble includes, document classes, page geometry, and typography parameters inside the user configuration file.
- **FR-005**: The codebase MUST NOT contain hardcoded fallback default styling values; all defaults MUST originate from the user configuration file.
- **FR-006**: CLI arguments MUST take precedence over user configuration file values.
- **FR-007**: System MUST provide a mechanism to specify a custom configuration file path via `--config` CLI flag.
- **FR-008**: System MUST validate local `.sty` package file paths provided in configuration or via CLI flags, emitting a clear warning or error prior to compilation if a path is invalid or unreachable.
- **FR-009**: System MUST provide an interactive setup wizard and dependency reporting CLI flags (`md2tex setup` and `--check-deps`) to audit required/optional system binaries (Pandoc, TeX compiler, Mermaid CLI) and prompt for automated installation (TinyTeX, Mermaid CLI).
- **FR-010**: System MUST provide an automated CI/CD build matrix to generate standalone cross-platform executables for Linux, macOS, and Windows.

### Key Entities

- **User Configuration Profile**: A structured YAML entity stored in `~/.config/md2tex/config.yaml` containing document settings, `.sty` package references, preamble directives, compiler flags, and formatting rules.
- **Style Asset Reference**: A reference to an external or local `.sty` LaTeX style package to be included in the generated LaTeX preamble.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user-facing CLI commands, outputs, and documentation refer exclusively to `md2tex` instead of legacy project names.
- **SC-002**: Zero hardcoded default styling macros or Netra-specific strings exist in the conversion engine codebase.
- **SC-003**: A user can customize default `.sty` packages and document parameters by updating `~/.config/md2tex/config.yaml` without modifying source code.
- **SC-004**: Overriding any user config value via CLI flag succeeds in 100% of test scenarios.

## Assumptions

- The configuration file is stored in YAML format at `~/.config/md2tex/config.yaml` (or custom path via `--config`).
- Users have standard LaTeX toolchains (e.g. `pdflatex`, `xelatex`, or `lualatex`) installed if building PDF artifacts.
- Backward compatibility with Netra-specific workflows can be achieved by providing a Netra-tailored `.sty` file in the user's `config.yaml`.
