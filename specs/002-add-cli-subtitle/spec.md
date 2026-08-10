# Feature Specification: Adicionar subtítulo pela CLI

**Feature Branch**: `002-add-cli-subtitle`

**Created**: 2026-08-10

**Status**: Draft

**Input**: User description: "Quero trazer o subtítulo ao md2tex (opção: --subtitle \"TEXTO\"). Hoje, como subtítulo aparece o tipo de documento. Podemos deixar o tipo de documento junto da versão, autor e data na capa. E deixar em branco o subtítutlo, no caso de não colocar nada nas opções. Essa será a versão 2.3.0 (ajustar o que precisar nos docs pra deixar com essa versão)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Definir subtítulo na conversão (Priority: P1)

Como pessoa autora de um documento, quero informar um subtítulo ao executar a conversão para que a capa apresente o contexto complementar que escolhi.

**Why this priority**: O subtítulo explícito evita que a capa use uma informação de classificação no lugar de uma informação descritiva do documento.

**Independent Test**: Converter um documento com título e uma opção de subtítulo e verificar que a capa exibida contém exatamente o subtítulo informado abaixo do título.

**Acceptance Scenarios**:

1. **Given** um documento válido, **When** a pessoa executa a conversão com `--subtitle "Guia de referência"`, **Then** a capa apresenta "Guia de referência" como subtítulo.
2. **Given** um documento cujo front matter também contém subtítulo, **When** a pessoa informa `--subtitle "Texto da opção"`, **Then** a capa apresenta "Texto da opção" como subtítulo.

---

### User Story 2 - Gerar capa sem subtítulo (Priority: P2)

Como pessoa autora que não precisa de subtítulo, quero gerar a capa sem uma linha substituta para que o espaço do subtítulo permaneça vazio.

**Why this priority**: A ausência da opção não deve exibir o tipo de documento no local reservado ao subtítulo.

**Independent Test**: Converter um documento sem subtítulo no front matter e sem a opção de subtítulo; a capa não deve conter uma linha de subtítulo.

**Acceptance Scenarios**:

1. **Given** um documento sem subtítulo, **When** a pessoa executa a conversão sem informar a opção de subtítulo, **Then** a capa não exibe subtítulo.
2. **Given** um documento sem subtítulo, **When** a pessoa informa um valor vazio para a opção de subtítulo, **Then** a capa não exibe subtítulo.

---

### User Story 3 - Consultar identificação completa na capa (Priority: P3)

Como leitora ou leitor do documento, quero encontrar o tipo de documento junto da versão, autoria e data para que as informações de identificação estejam agrupadas na capa.

**Why this priority**: O agrupamento torna clara a diferença entre o subtítulo livre e os metadados de identificação.

**Independent Test**: Converter um documento de cada tipo suportado e verificar que sua capa mostra o tipo de documento na mesma área visual de versão, autoria e data, sem repeti-lo como subtítulo.

**Acceptance Scenarios**:

1. **Given** um documento com tipo, versão, autoria e data, **When** a conversão é concluída, **Then** a capa apresenta o tipo de documento junto dessas três informações de identificação.
2. **Given** um documento com subtítulo e tipo de documento, **When** a conversão é concluída, **Then** o subtítulo e o tipo de documento aparecem em áreas distintas da capa.

### Edge Cases

- Um valor de subtítulo contendo acentos, aspas ou caracteres de marcação não deve alterar os demais dados exibidos na capa.
- Um subtítulo composto apenas por espaços é tratado como ausência de subtítulo.
- Quando não houver subtítulo em nenhuma fonte, o tipo de documento continua disponível entre os metadados de identificação da capa.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O md2tex DEVE disponibilizar a opção `--subtitle` para a pessoa usuária informar o subtítulo da conversão.
- **FR-002**: Quando fornecido, o valor de `--subtitle` DEVE prevalecer sobre qualquer subtítulo declarado no documento de entrada.
- **FR-003**: O md2tex DEVE exibir o subtítulo na área de subtítulo da capa somente quando existir um valor não vazio.
- **FR-004**: Quando nenhum subtítulo for informado por opção ou no documento de entrada, o md2tex DEVE deixar a área de subtítulo da capa vazia.
- **FR-005**: O md2tex NÃO DEVE usar o tipo de documento como substituto do subtítulo.
- **FR-006**: O md2tex DEVE exibir o tipo de documento na área de identificação da capa, junto de versão, autoria e data, para todos os tipos de documento que possuem capa.
- **FR-007**: A identificação pública da distribuição e os materiais de documentação que declaram a versão atual DEVEM indicar a versão 2.3.0.
- **FR-008**: A documentação da linha de comando DEVE explicar a opção `--subtitle` e seu efeito quando omitida.

### Key Entities

- **Subtítulo**: Texto opcional que complementa o título e é exibido na área própria da capa.
- **Tipo de documento**: Classificação do documento que integra os metadados de identificação da capa e não substitui o subtítulo.
- **Metadados de identificação**: Conjunto composto por tipo de documento, versão, autoria e data exibido na capa.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em 100% das conversões de documentos com a opção de subtítulo, a capa apresenta exatamente o texto informado como subtítulo.
- **SC-002**: Em 100% das conversões sem subtítulo fornecido, a capa não apresenta tipo de documento nem texto de preenchimento na área de subtítulo.
- **SC-003**: Em 100% das capas geradas para os tipos de documento suportados, o tipo de documento aparece junto dos demais metadados de identificação.
- **SC-004**: A ajuda da linha de comando e a documentação publicada da ferramenta identificam a versão 2.3.0 e descrevem a opção de subtítulo.

## Assumptions

- O subtítulo existente no front matter continua sendo uma fonte válida quando a opção `--subtitle` não é usada.
- A opção de linha de comando segue a precedência já aplicada aos demais metadados que podem ser sobrescritos durante a conversão.
- Esta versão não altera os formatos de entrada aceitos nem acrescenta novos tipos de documento ou variações de capa.
