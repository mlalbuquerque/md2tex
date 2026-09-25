# Feature Specification: Perfil Documento de Arquitetura de Software

**Feature Branch**: `007-software-architecture-profile`  
**Created**: 2026-09-25  
**Status**: Draft  
**Input**: Criar um perfil próprio para gerar Documento de Arquitetura de Software a partir do modelo OPE-RQ-89, com nome do sistema opcional na capa e uma página obrigatória de Histórico de Revisões antes do sumário.

## User Scenarios & Testing

### User Story 1 - Gerar um Documento de Arquitetura de Software (Priority: P1)

Uma pessoa autora seleciona o perfil Documento de Arquitetura de Software e converte seu Markdown usando a estrutura de capa e documento prevista para esse tipo.

**Why this priority**: O perfil dedicado permite gerar esse documento sem alterar o comportamento do Documento Padrão ou dos demais tipos.

**Independent Test**: Converter um Markdown com o perfil de arquitetura e confirmar que o TEX gerado usa o layout correspondente, preservando o corpo do documento.

**Acceptance Scenarios**:

1. **Given** um Markdown válido, **When** a pessoa seleciona Documento de Arquitetura de Software, **Then** o `md2tex` gera o documento usando o perfil e o layout próprios.
2. **Given** um documento convertido com `default`, **When** comparado ao mesmo documento convertido com o perfil de arquitetura, **Then** o perfil `default` não ganha elementos exclusivos de arquitetura.
3. **Given** qualquer outro perfil existente, **When** ele é convertido, **Then** sua saída mantém o comportamento e o template próprios.

### User Story 2 - Identificar o sistema na capa (Priority: P1)

A pessoa autora pode informar o nome do sistema para que ele apareça no alto à direita da capa, abaixo da área do logotipo prevista pelo modelo.

**Why this priority**: A identificação torna a capa específica ao sistema sem exigir esse dado para documentos em que ele não se aplique.

**Independent Test**: Converter com e sem nome do sistema e verificar a posição/campo na capa e a ausência de texto quando omitido.

**Acceptance Scenarios**:

1. **Given** um nome informado nos metadados ou pela opção da CLI, **When** o documento é gerado, **Then** o nome aparece no alto à direita da capa, abaixo da área do logotipo.
2. **Given** que o nome do sistema não foi informado, **When** o documento é gerado, **Then** o espaço do campo permanece sem texto e a conversão continua normalmente.
3. **Given** valores diferentes no front matter e na CLI, **When** ambos são fornecidos, **Then** prevalece o valor passado pela CLI, inclusive quando vazio.
4. **Given** um nome composto apenas por espaços, **When** o documento é gerado, **Then** nenhum nome é impresso.

### User Story 3 - Consultar o histórico de revisões (Priority: P1)

A pessoa leitora encontra o Histórico de Revisões em página própria, antes do sumário, com as alterações do documento organizadas em tabela.

**Why this priority**: O histórico é parte obrigatória do modelo documental e precisa estar disponível em toda saída do perfil.

**Independent Test**: Converter com entradas de histórico e sem elas, com e sem sumário, confirmando a página e a tabela antes do sumário quando presente.

**Acceptance Scenarios**:

1. **Given** entradas de revisão no front matter, **When** o documento é gerado, **Then** uma página própria apresenta Data, Versão, Descrição e Autor para cada entrada.
2. **Given** nenhum histórico informado, **When** o documento é gerado, **Then** a página e a tabela ainda são incluídas, com uma linha inicial baseada na data, versão e autor do documento e descrição vazia.
3. **Given** que o sumário está habilitado, **When** o documento é gerado, **Then** a página do Histórico de Revisões precede o sumário.
4. **Given** que o sumário foi desabilitado, **When** o documento é gerado, **Then** a página do Histórico de Revisões continua presente.

### User Story 4 - Usar e compreender o perfil (Priority: P2)

A pessoa autora encontra o nome do novo tipo entre as opções da CLI e na documentação de uso, incluindo os metadados necessários para nome do sistema e revisões.

**Why this priority**: O perfil só é útil quando pode ser descoberto e usado sem consultar detalhes internos do programa.

**Independent Test**: Conferir ajuda da CLI e README contra os perfis realmente aceitos e seguir um exemplo documentado de conversão.

**Acceptance Scenarios**:

1. **Given** a ajuda da CLI, **When** a pessoa consulta `--type`, **Then** Documento de Arquitetura de Software aparece como uma opção selecionável.
2. **Given** o README, **When** a pessoa consulta a lista de perfis e as opções da CLI, **Then** ambas incluem todos os perfis aceitos, inclusive `default` e Documento de Arquitetura de Software.
3. **Given** o exemplo de metadados do perfil, **When** a pessoa o usa, **Then** os campos opcionais e a estrutura do histórico estão explicados e são copiáveis.

### Edge Cases

- O nome do sistema contém caracteres acentuados ou caracteres especiais que precisam ser escapados na saída.
- O valor do nome do sistema contém espaços no início/fim ou somente espaços.
- Uma entrada de revisão possui um dos valores de célula vazio.
- O histórico contém várias entradas e precisa permanecer legível sem perder linhas ou colunas.
- O documento não usa sumário, mas ainda precisa conter a página de revisões.
- O perfil é selecionado, mas não há dados explícitos de revisão; ainda assim, a tabela deve existir.
- Regras de tópicos obrigatórios podem ser aplicadas ao perfil novo sem serem associadas automaticamente a outro perfil.

## Requirements

### Functional Requirements

- **FR-001**: O sistema MUST oferecer um perfil próprio chamado Documento de Arquitetura de Software, selecionável pela CLI.
- **FR-002**: O perfil MUST ter template próprio e MUST preservar o comportamento dos perfis existentes, incluindo `default`.
- **FR-003**: O sistema MUST permitir informar opcionalmente o nome do sistema por front matter e pela CLI; espaços no início e fim são removidos e valor composto somente por espaços é tratado como vazio.
- **FR-004**: Quando informado, o nome do sistema MUST aparecer no alto à direita da capa, abaixo da área destinada ao logotipo; quando omitido, nenhum texto de nome deve aparecer.
- **FR-005**: Quando a opção `--system-name` for fornecida, seu valor MUST prevalecer sobre o front matter, inclusive quando for vazio.
- **FR-006**: O perfil MUST gerar uma página própria de Histórico de Revisões com tabela de Data, Versão, Descrição e Autor.
- **FR-007**: A página de Histórico de Revisões MUST aparecer antes do sumário e MUST continuar presente quando o sumário estiver desabilitado.
- **FR-008**: O sistema MUST permitir fornecer zero ou mais entradas de revisão com data, versão, descrição e autor.
- **FR-009**: Quando não forem fornecidas entradas, o sistema MUST manter a página/tabela e incluir uma linha inicial baseada na data, versão e autor do documento, com descrição vazia.
- **FR-010**: Os valores de revisão MUST ser escapados corretamente para a saída LaTeX e células vazias não devem invalidar a tabela.
- **FR-011**: As regras de tópicos obrigatórios MUST aceitar o novo perfil pelo seu identificador sem aplicar as regras automaticamente a outros perfis.
- **FR-012**: O README MUST documentar o perfil, seu identificador, opções/metadados e a ordem da página de revisões; a referência de `--type` MUST corresponder a todos os perfis realmente aceitos, incluindo `default`.
- **FR-013**: A ajuda da CLI MUST listar o novo perfil e descrever a opção de nome do sistema sem atribuí-la a `default`.

### Key Entities

- **Perfil documental**: Tipo selecionável que associa rótulo público, template e regras de tópicos próprias.
- **Nome do sistema**: Texto opcional exibido na capa do Documento de Arquitetura de Software.
- **Entrada de revisão**: Registro ordenado com data, versão, descrição e autor, apresentado na tabela do histórico.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Em todos os cenários de uso testados, selecionar Documento de Arquitetura de Software gera um documento com a estrutura específica desse tipo, sem alterar os documentos dos outros perfis.
- **SC-002**: Em todos os cenários de nome testados, valor preenchido aparece na capa e valor ausente, vazio ou só com espaços não produz texto; valor vazio passado pela CLI suprime o valor do front matter.
- **SC-003**: Em 100% das conversões do perfil, a página de Histórico de Revisões e sua tabela estão presentes antes do sumário, quando habilitado.
- **SC-004**: Entradas explícitas preservam os quatro campos e a ordem fornecida; ausência de entradas produz a linha inicial definida.
- **SC-005**: A lista de perfis do README e a referência da CLI correspondem às opções efetivamente aceitas.
- **SC-006**: A ajuda da CLI e a documentação permitem encontrar o nome e a opção de seleção do perfil sem consultar outra fonte.

## Assumptions

- O identificador CLI do perfil será `software-architecture`, seguindo o padrão kebab-case dos perfis existentes.
- O perfil não inclui arquivo de logotipo. A capa reserva uma área superior para o estilo/layout do usuário renderizá-lo, quando configurado. O nome do sistema fica alinhado à direita logo abaixo dessa área; sem logotipo, conserva-se o mesmo posicionamento.
- As entradas de revisão são fornecidas no front matter como uma lista de objetos com `date`, `version`, `description` e `author`.
- A linha inicial automática quando não há histórico explícito preserva o comportamento já implementado para esse recurso.
- O perfil mantém os metadados gerais existentes de título, autor, data, versão e cliente/projeto, salvo quando o layout de referência definir sua apresentação própria.
