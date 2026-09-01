<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: IV. Testability & Quality Assurance (requires tests to run
  through the repository-local virtual environment)
- Added sections: Governance amendment, versioning, and compliance expectations
- Removed sections: none
- Follow-up TODOs: none
-->

# md2tex Constitution

## Core Principles

### I. Generic & Decoupled Architecture
The system MUST function as a standalone, domain-agnostic CLI tool. No company branding, specific organization macros, or hardcoded project templates are permitted in the core engine.

### II. Single Source of Truth for Defaults
All LaTeX style definitions (`.sty`), document classes, geometry, and typography defaults MUST originate from the user configuration file (`~/.config/md2tex/config.yaml`). The codebase MUST NOT include hardcoded fallback values for document styling.

### III. Strict CLI Precedence Hierarchy
Command-line arguments passed during invocation MUST always override corresponding values specified in the user configuration file.

### IV. Testability & Quality Assurance
All features, configuration loader behaviors, and CLI entry points MUST be covered by automated
tests (`pytest`) ensuring clean output and proper error handling. Test commands MUST run through
the repository-local virtual environment, using `./.venv/bin/pytest`; agents MUST verify that
executable exists and MUST NOT substitute a global interpreter or an alternative environment runner.

## Governance
Amendments require an explicit update to this document, a Sync Impact Report, and a compliance
review of active plans and tasks. Constitutional changes use semantic versioning: MAJOR for
incompatible removals or redefinitions, MINOR for new or materially expanded guidance, and PATCH
for clarifications without behavioral change.

Version: 1.1.0 | Ratified: 2026-08-03 | Last Amended: 2026-09-01
