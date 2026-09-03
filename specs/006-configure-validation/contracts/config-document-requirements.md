# Contract: `document_requirements` no config.yaml

## Formato

```yaml
document_requirements:
  meeting-minutes:
    fields:
      - path: client
        label: Cliente/Projeto
        required: true
        instruction: Adicione o cliente ou projeto no front matter.
        example: 'client: "Cliente / Projeto (NEP-001)"'
      - path: period.start
        label: Período — início
        required: true
        instruction: Informe o horário de início dentro de `period`.
        example: |
          period:
            start: "09:00"
    sections:
      - section: Objetivos da Reunião
        label: Objetivos da Reunião
        required: true
        instruction: Adicione a seção e descreva os objetivos.
        example: |
          # Objetivos da Reunião

          Descreva os objetivos da reunião.
```

## Regras

- `document_requirements` é opcional e aceita somente IDs de perfil conhecidos.
- Cada perfil aceita somente `fields` e `sections`; ambas são listas e podem ser vazias.
- Cada campo de `fields` exige `path`, `label`, `required`, `instruction` e `example`.
- Cada item de `sections` exige `section`, `label`, `required`, `instruction` e `example`.
- Caminhos e seções duplicados, valores vazios, tipos incompatíveis ou chaves extras invalidam toda a configuração antes da conversão.
- Itens com `required: false` documentam orientação, mas não geram pendência quando ausentes.
- Para requisito obrigatório ausente, a mensagem inclui rótulo, motivo, instrução e o exemplo, em bloco copiável.
- Campos são avaliados após a precedência CLI → front matter. Seções são avaliadas no corpo Markdown.
- Configurações sem `document_requirements` mantêm o comportamento atual.
