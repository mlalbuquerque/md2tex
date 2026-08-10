# Research: md2tex 2.2.0

## Decisions

1. **Configuração estrita** — YAML com campos obrigatórios e chaves conhecidas; evita defaults ocultos e erros tardios.
2. **Init como argumento especial** — `md2tex init` preserva o formato existente `md2tex arquivo.md` sem criar uma CLI de subcomandos incompatível.
3. **Modelo empacotado** — o arquivo copiado pelo init é dado de configuração explícita e não participa como fallback em conversões.
4. **Sem compatibilidade Netra** — aliases e metadados legados foram removidos para cumprir o desacoplamento.
