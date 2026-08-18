# Data Model: validação de tópicos

```yaml
rules:
  report:
    - Objetivo
    - Conclusão
  adr:
    - Contexto
    - Decisão
```

| Campo | Tipo | Regras |
|---|---|---|
| `rules` | mapa | Única chave de topo; pode ser vazia. |
| `rules.<profile>` | lista de strings | Perfil deve ser um dos cinco IDs de `profiles.py`; lista vazia não exige tópico. |
| item | string | Não vazia após `strip()` e não repetida após `strip().casefold()`. |

Chaves extras/desconhecidas, tipos incompatíveis e YAML inválido tornam o arquivo inteiro inválido: regras parciais nunca são usadas.

| Entidade | Campos | Relação |
|---|---|---|
| Regra de tópicos | `profile`, `required_topics` | Associação editável de perfil a tópicos. |
| Tópico obrigatório | `display_name`, `normalized_name` | Nome normalizado serve à comparação; original é exibido. |
| Título encontrado | `text`, `normalized_name`, `level` | Qualquer nível pode satisfazer uma regra. |
| Pendência | `profile`, `required_topic` | Uma por tópico obrigatório não encontrado. |
| Opções | `rules_path`, `validate`, `strict` | Caminho explícito vence padrão; modo estrito bloqueia pré-saída. |
