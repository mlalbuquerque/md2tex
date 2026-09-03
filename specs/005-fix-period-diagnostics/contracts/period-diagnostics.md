# Contract: Diagnósticos de período

Para o perfil `meeting-minutes`, a mensagem mantém o prefixo `Memória de reunião: campo ou seção inválida:` e troca somente o identificador final:

- `period.start` → `Período — início`
- `period.end` → `Período — fim`

As chaves do front matter YAML não mudam. Os demais diagnósticos permanecem literais.
