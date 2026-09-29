# Feature Validation Quickstart

This guide explains how to validate the generic `--cover` support and the exclusivity rules between `--template` and `--type`.

## Prerequisites
- A working `md2tex` local development environment.
- The `md2tex` CLI updated with the `custom-cover-support` feature.
- A dummy markdown file `test.md`.
- A dummy cover file `my-cover.j2.tex`.

```bash
echo "# Test Document" > test.md
echo "\\begin{titlepage} \\centering {\\Huge {{ title }}} \\end{titlepage}" > my-cover.j2.tex
```

## Scenario 1: Mutual Exclusivity Validation
Verify that providing both `--type` and `--template` is rejected.

```bash
# Run command
python -m md2tex.cli test.md --type software-architecture --template custom.tex

# Expected Outcome
# The command should immediately fail with a click UsageError:
# "Usage: cli.py [OPTIONS] [INPUT_FILE]
# Try 'cli.py -h' for help.
# Error: --template and --type are mutually exclusive."
```

## Scenario 2: Standard Cover Injection
Verify that `--cover` correctly renders Jinja2 variables and replaces the cover.

```bash
# Run command
python -m md2tex.cli test.md --title "Architecture 2026" --cover my-cover.j2.tex --keep-build

# Expected Outcome
# The command should succeed.
# Inspect the generated `test.tex` file. The start of the document should contain:
# \begin{titlepage} \centering {\Huge Architecture 2026} \end{titlepage}
# overriding the default cover.
```

## Scenario 3: Cover Overriding Type
Verify that `--cover` works seamlessly even when a `--type` profile is selected.

```bash
# Run command
python -m md2tex.cli test.md --title "Architecture 2026" --type software-architecture --cover my-cover.j2.tex --keep-build

# Expected Outcome
# The command should succeed.
# Inspect the generated `test.tex` file. The cover should be the output of `my-cover.j2.tex` 
# rather than the hardcoded `software-architecture` cover. The rest of the document 
# (e.g., TOC, Revision History check) respects the `software-architecture` profile.
```
