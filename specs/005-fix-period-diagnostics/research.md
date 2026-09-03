# Research: Diagnósticos do período

## Decision: mapear apenas os dois caminhos de período para rótulos públicos

**Rationale**: `period.start` e `period.end` pertencem ao contrato YAML, mas não são linguagem adequada para o diagnóstico destinado ao autor. Um mapa localizado no formatador mantém os demais caminhos intactos.

**Alternatives considered**:

- Alterar as chaves YAML: rejeitado, pois quebraria o contrato e documentos existentes.
- Traduzir todos os diagnósticos: rejeitado, pois amplia o escopo do patch e muda mensagens já aceitas.
- Duplicar lógica no conversor: rejeitado, porque o validador já é a fonte de mensagens.
