# md2tex Constitution

## Core Principles

### I. Generic & Decoupled Architecture
The system MUST function as a standalone, domain-agnostic CLI tool. No company branding, specific organization macros, or hardcoded project templates are permitted in the core engine.

### II. Single Source of Truth for Defaults
All LaTeX style definitions (`.sty`), document classes, geometry, and typography defaults MUST originate from the user configuration file (`~/.config/md2tex/config.yaml`). The codebase MUST NOT include hardcoded fallback values for document styling.

### III. Strict CLI Precedence Hierarchy
Command-line arguments passed during invocation MUST always override corresponding values specified in the user configuration file.

### IV. Testability & Quality Assurance
All features, configuration loader behaviors, and CLI entry points MUST be covered by automated tests (`pytest`) ensuring clean output and proper error handling.

## Governance
Version: 1.0.0 | Ratified: 2026-08-03 | Last Amended: 2026-08-03
