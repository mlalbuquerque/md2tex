# Phase 0: Outline & Research

## Research Findings

### 1. Template Rendering Engine
- **Decision**: Use existing `jinja2.Environment` available in `src/md2tex/templates.py`.
- **Rationale**: Jinja2 is already a dependency and is used to render the main `.tex` templates. The `--cover` argument will simply load an external file, render it via a `jinja2.FileSystemLoader` (or directly from string if preferred) providing the same variables/context that the main document receives, and inject the result into the main template.
- **Alternatives considered**: None, using the existing engine is optimal and adheres to project standards.

### 2. Validation & Exclusivity Logic
- **Decision**: Add validation in `src/md2tex/cli.py` (via `click` callback or post-parsing logic) to enforce mutual exclusivity between `--type` and `--template`.
- **Rationale**: Checking at the CLI entry point ensures fail-fast behavior before any processing or LaTeX compilation attempts occur.
- **Alternatives considered**: Checking inside the converter logic. However, CLI-level validation is more standard for `click`-based apps.

### 3. Constitution Alignment
- **Decision**: The feature completely externalizes company-specific covers (like the architecture document cover), perfectly aligning with Principle I (Generic & Decoupled Architecture). No hardcoded specific layouts will be added to the Python codebase.
- **Rationale**: Satisfies the governance requirement while delivering the feature to the end user.
