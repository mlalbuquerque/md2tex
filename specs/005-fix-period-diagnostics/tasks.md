# Tasks: Corrigir diagnósticos do período

**Input**: Design documents from `/specs/005-fix-period-diagnostics/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contract](contracts/period-diagnostics.md), [quickstart.md](quickstart.md)

**Tests**: Incluídos porque a constituição exige cobertura automatizada.

## Phase 1: Setup

**Purpose**: Preparar expectativas públicas do patch.

- [X] T001 Add v2.5.1 release entry in RELEASES.md

---

## Phase 3: User Story 1 - Entender pendências do período (Priority: P1) 🎯 MVP

**Goal**: Exibir rótulos claros para o início e o fim ausentes do período.

**Independent Test**: Validar períodos ausentes, incompletos e em branco, observando ambos os rótulos públicos.

- [X] T002 [US1] Add focused absent, blank, and invalid-period label cases in tests/test_validator.py
- [X] T003 [US1] Render public period labels from validation diagnostics in src/md2tex/validator.py
- [X] T004 [US1] Run the focused period-diagnostic tests with ./.venv/bin/pytest in tests/test_validator.py

---

## Phase 4: User Story 2 - Preservar os demais diagnósticos (Priority: P2)

**Goal**: Garantir que somente os dois rótulos de período sejam alterados.

**Independent Test**: Uma validação combinada mantém os rótulos existentes de cliente e seções, além dos novos rótulos de período.

- [X] T005 [US2] Add mixed-diagnostic regression coverage in tests/test_validator.py
- [X] T006 [US2] Add strict CLI diagnostic coverage for public period labels in tests/test_cli.py
- [X] T007 [US2] Run validator and CLI regression tests with ./.venv/bin/pytest in tests/test_validator.py and tests/test_cli.py

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Publicar o patch e verificar a distribuição.

- [X] T008 Update public version to 2.5.1 in pyproject.toml and src/md2tex/__init__.py
- [X] T009 Run ruff and the complete pytest suite with ./.venv/bin/ruff and ./.venv/bin/pytest
- [X] T010 Verify the strict CLI output in specs/005-fix-period-diagnostics/quickstart.md

## Dependencies & Execution Order

- T001 e T002 precedem T003; T003 precede T004.
- US2 depende de US1 para verificar a regressão sobre a mensagem final.
- T008–T010 dependem de US1 e US2.

## Parallel Opportunities

- T001 pode ocorrer em paralelo com T002.
- Após T003, T005 e T006 podem ser preparados em paralelo por afetarem arquivos distintos.

## Implementation Strategy

1. Estabelecer a mensagem pública e os testes de unidade (MVP).
2. Confirmar que a CLI estrita expõe a mesma mensagem e que os demais diagnósticos não mudaram.
3. Atualizar a versão, executar a suíte completa e reproduzir o quickstart.
