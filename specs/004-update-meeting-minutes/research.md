# Research: Atualizar memória de reunião

## Decision: usar YAML front matter como contrato de entrada

**Rationale**: o conversor já separa YAML front matter do corpo Markdown antes de normalizar títulos. Essa forma foi escolhida na clarificação e mantém identificação e participantes fora das seções narrativas.

**Alternatives considered**:

- Bloco livre `Campo: valor` no corpo: torna a validação e a separação do conteúdo ambíguas.
- Opções adicionais da CLI: adequadas a automações pontuais, mas não representam listas de participantes de forma legível.
- Aceitar os dois formatos: amplia a superfície de diagnóstico e documentação sem necessidade declarada.

## Decision: validar dados da memória depois da precedência de metadados

**Rationale**: o fluxo atual já compõe os metadados de front matter e opções CLI. A validação deve usar o valor efetivamente escolhido para não apontar uma ausência que foi preenchida pela CLI.

**Alternatives considered**:

- Validar o YAML bruto: ignoraria sobrescritas legítimas da CLI.
- Validar somente títulos com `rules.yaml`: não cobre valores estruturados, participantes ou linhas de pendência.

## Decision: representar participantes e período como dados estruturados

**Rationale**: `period` precisa ter início e fim, e cada participante tem nome e cargo/função. Mapas e listas YAML preservam essas relações e permitem renderização determinística.

**Alternatives considered**:

- Uma string única por grupo: dificulta validar nome e função separadamente.
- Tabelas Markdown como fonte dos participantes: mistura campos de cabeçalho com o corpo conversível e aumenta o acoplamento ao Pandoc.

## Decision: `Sem pendências` é a única declaração de ausência de pendências

**Rationale**: a convenção definida pelo usuário diferencia uma reunião sem ações de uma seção omitida ou uma tabela incompleta.

**Alternatives considered**:

- Tabela vazia: pode ser confundida com conteúdo faltante.
- Exigir uma pendência: cria informação artificial em reuniões internas ou conclusivas.

## Decision: preservar a configuração externa de estilo

**Rationale**: a constituição exige que classes, pacotes e tipografia venham de `config.yaml`. O template da memória só organiza conteúdo; o letterhead da Netra deve estar na configuração usada na conversão.

**Alternatives considered**:

- Incluir o pacote letterhead diretamente no template: viola a fonte única de estilo e torna o motor dependente de uma organização.
- Copiar o arquivo `.sty` para o projeto: aumenta acoplamento e não atende ao requisito de configuração explícita.
