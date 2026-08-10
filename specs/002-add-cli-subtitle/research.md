# Research: Subtítulo pela CLI

## Decisão: preservar a presença explícita da opção de subtítulo

- **Decision**: Representar separadamente a ausência de `--subtitle` e um `--subtitle` fornecido sem texto; normalizar texto composto apenas por espaços como vazio antes de produzir os metadados.
- **Rationale**: A omissão deve manter o subtítulo do front matter, enquanto uma opção explicitamente vazia deve vencê-lo e deixar a capa sem subtítulo. Um teste de verdade simples não distingue os dois casos.
- **Alternatives considered**:
  - Usar o primeiro valor não vazio entre CLI e front matter: menor alteração, mas viola a precedência quando a CLI é vazia.
  - Remover o subtítulo do front matter: contraria a especificação e rompe compatibilidade com documentos existentes.

## Decisão: tratar o tipo de documento como metadado de identificação

- **Decision**: Exibir o tipo documental no bloco de identificação, antes de autoria, versão e data, em cada template de capa.
- **Rationale**: Mantém a área de subtítulo reservada apenas ao subtítulo e torna uniforme a identificação nos perfis existentes.
- **Alternatives considered**:
  - Manter o tipo como uma linha isolada entre título e identificação: não atende ao agrupamento solicitado.
  - Omitir o tipo de documento: reduziria informação útil já disponível na capa.

## Decisão: atualizar os pontos públicos da versão em conjunto

- **Decision**: Atualizar metadado de distribuição, versão exposta pela CLI, teste de identidade e documentação que reproduz ajuda/exemplos para 2.3.0.
- **Rationale**: Evita divergência entre instalação, comando de versão, testes e materiais de uso.
- **Alternatives considered**:
  - Atualizar somente o metadado de distribuição: deixaria a CLI e a documentação inconsistentes.
