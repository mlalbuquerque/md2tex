# Quickstart: Diagnósticos de período

1. Crie uma Memória de Reunião válida, omitindo `period.start`.
2. Execute `md2tex --type meeting-minutes --strict arquivo.md`.
3. Confirme o diagnóstico `Período — início`.
4. Repita omitindo `period.end` e confirme `Período — fim`.
5. Omita todo `period` e confirme ambos os rótulos; confirme também que `client` e as seções preservam seus nomes atuais.
