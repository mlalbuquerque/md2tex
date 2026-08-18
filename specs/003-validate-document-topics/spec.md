# Feature Specification: Validar tópicos por tipo documental

**Feature Branch**: `003-validate-document-topics`

**Created**: 2026-08-17

**Status**: Draft

**Input**: User description: "Hoje, o tipo do documento não importa tanto quando deveria. Queria que os tipos tivessem algum tipo de verificação para saber se falta algum tópico dentro do markdown (MD) antes de transformar pra TeX. Deve existir algum tipo regra ou configuração para cada tipo de documento para que essa verificação seja feita. Pode criar um comando pra criar esse arquivo com essa configuração ou regras - deixe exemplos de uso. Isso seria uma versão 2.4.0 (ajuste as RELEASES quanto a isso, e ajuste o README pra ter essa função a mais)."

## Clarifications

### Session 2026-08-17

- Q: O arquivo criado por `md2tex rules init` deve já trazer tópicos obrigatórios recomendados para cada tipo documental? → A: Incluir exemplos completos comentados, inativos até que a pessoa os habilite e ajuste os valores.
- Q: Quando a pessoa indicar explicitamente um arquivo de regras que não existe ou é inválido, a conversão deve parar mesmo fora do modo estrito? → A: Interromper a conversão sempre que o arquivo indicado explicitamente estiver ausente ou inválido.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validar tópicos antes da conversão (Priority: P1)

Como pessoa autora, quero que o tipo documental verifique os tópicos obrigatórios do meu Markdown antes da conversão para identificar lacunas no conteúdo a tempo de corrigi-las.

**Why this priority**: A verificação torna o tipo documental uma orientação prática de qualidade, sem exigir que a pessoa descubra tópicos ausentes somente depois de gerar o documento.

**Independent Test**: Converter um Markdown associado a um tipo com uma regra de tópicos obrigatórios e verificar que cada tópico ausente é informado antes de qualquer arquivo de saída ser criado.

**Acceptance Scenarios**:

1. **Given** um tipo documental com tópicos obrigatórios configurados e um Markdown que contém todos eles, **When** a pessoa inicia a conversão, **Then** a conversão prossegue sem aviso de tópicos ausentes.
2. **Given** um tipo documental com tópicos obrigatórios configurados e um Markdown que omite dois deles, **When** a pessoa inicia a conversão, **Then** a ferramenta identifica nominalmente os dois tópicos ausentes antes de gerar o TEX.
3. **Given** um Markdown com títulos equivalentes que diferem apenas em maiúsculas, minúsculas ou espaços nas extremidades, **When** a ferramenta verifica os tópicos, **Then** ela os reconhece como o mesmo tópico.

---

### User Story 2 - Criar e personalizar regras de tópicos (Priority: P2)

Como pessoa responsável por padronizar documentos, quero criar um arquivo-modelo de regras e definir tópicos obrigatórios para cada tipo para adequar a verificação ao meu processo.

**Why this priority**: Os tipos possuem necessidades diferentes; regras editáveis evitam impor uma estrutura única a todos os documentos.

**Independent Test**: Executar o comando de criação, preencher regras distintas para dois tipos e confirmar que cada conversão aplica somente os tópicos do tipo selecionado.

**Acceptance Scenarios**:

1. **Given** que ainda não existe um arquivo de regras, **When** a pessoa executa `md2tex rules init`, **Then** a ferramenta cria um modelo com exemplos completos, comentados e inativos para cada tipo documental suportado e orienta como habilitá-los e editá-los.
2. **Given** um arquivo de regras personalizado para Relatório e ADR, **When** a pessoa converte um ADR, **Then** apenas os tópicos definidos para ADR são verificados.
3. **Given** um destino já ocupado, **When** a pessoa tenta criar novamente o arquivo-modelo sem confirmar sobrescrita, **Then** a configuração existente permanece inalterada e a ferramenta explica como escolher outro destino ou sobrescrever conscientemente.

---

### User Story 3 - Escolher o impacto das pendências (Priority: P3)

Como pessoa autora, quero poder revisar avisos durante uma conversão normal e impedir a geração quando estiver usando validação estrita para equilibrar produtividade e conformidade.

**Why this priority**: Nem toda conversão exploratória deve ser bloqueada, mas documentos finais precisam de uma forma confiável de impedir a geração incompleta.

**Independent Test**: Converter o mesmo Markdown incompleto em modo normal e em modo estrito, verificando respectivamente um aviso com geração e uma interrupção sem saída.

**Acceptance Scenarios**:

1. **Given** tópicos obrigatórios ausentes, **When** a pessoa executa uma conversão normal, **Then** a ferramenta exibe avisos claros e pode gerar o TEX.
2. **Given** tópicos obrigatórios ausentes, **When** a pessoa executa a conversão em modo estrito, **Then** a ferramenta interrompe a conversão antes de criar ou substituir o arquivo TEX.
3. **Given** que não há arquivo de regras disponível para a conversão, **When** a pessoa converte um documento, **Then** o comportamento existente é preservado e a ferramenta não inventa tópicos obrigatórios.

### Edge Cases

- Uma regra sem tópicos obrigatórios para um tipo não produz aviso nem impede a conversão.
- Títulos repetidos no Markdown atendem uma regra somente uma vez e não produzem avisos extras.
- Um tópico configurado para um tipo não é exigido para outro tipo, inclusive para o tipo documental padrão.
- Se um arquivo de regras estiver ilegível ou estruturalmente inválido, a ferramenta explica o problema e não usa regras parciais ou ambíguas.
- Quando um arquivo de regras for indicado explicitamente e não puder ser usado, a conversão é interrompida mesmo fora do modo estrito.
- A opção de não executar validações mantém o comportamento já esperado de não verificar tópicos obrigatórios.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O md2tex DEVE permitir associar, para cada tipo documental suportado, uma lista editável de tópicos obrigatórios.
- **FR-002**: O md2tex DEVE fornecer o comando `md2tex rules init` para criar um arquivo-modelo de regras com exemplos completos, comentados e inativos para todos os tipos documentais suportados.
- **FR-003**: O comando de criação DEVE recusar sobrescrever um arquivo de regras existente sem uma confirmação explícita da pessoa usuária.
- **FR-004**: Antes de iniciar a transformação do Markdown em TEX, o md2tex DEVE comparar os títulos do documento com as regras do tipo selecionado e identificar cada tópico obrigatório ausente.
- **FR-005**: A comparação de títulos DEVE ignorar diferenças de maiúsculas/minúsculas e espaços nas extremidades, preservando o texto original nos avisos.
- **FR-006**: Na execução normal, o md2tex DEVE apresentar pendências de tópicos como avisos e manter a conversão disponível.
- **FR-007**: Na execução em modo estrito, o md2tex DEVE tratar pendências de tópicos como erro e interromper a conversão antes de criar ou substituir o arquivo TEX.
- **FR-008**: Quando não houver regras disponíveis para o tipo selecionado, o md2tex DEVE manter o comportamento de conversão existente sem exigir tópicos implícitos.
- **FR-009**: Quando um arquivo de regras for indicado explicitamente, o md2tex DEVE informar de forma acionável se ele estiver inválido ou inacessível, não aplicar regras parcialmente interpretadas e interromper a conversão.
- **FR-010**: A pessoa usuária DEVE poder indicar um arquivo de regras específico para uma conversão; essa indicação DEVE prevalecer sobre a localização padrão de regras.
- **FR-011**: O README DEVE documentar a criação, a estrutura conceitual, a personalização e o uso das regras, incluindo exemplos para conversão normal e estrita.
- **FR-012**: RELEASES, a identificação pública da distribuição e os materiais de documentação que declaram a versão atual DEVEM indicar a versão 2.4.0 e descrever a validação de tópicos por tipo documental.

### Key Entities

- **Regra de tópicos**: Conjunto editável que associa um tipo documental a seus tópicos obrigatórios.
- **Tópico obrigatório**: Nome de uma seção que deve estar presente no Markdown para o tipo documental correspondente ser considerado completo.
- **Pendência de tópico**: Registro apresentado à pessoa usuária quando um tópico obrigatório não é encontrado no documento.
- **Arquivo de regras**: Configuração criada ou escolhida pela pessoa usuária que contém as regras de tópicos por tipo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em 100% das conversões com regras válidas, cada tópico obrigatório ausente é listado uma única vez antes da geração do TEX.
- **SC-002**: Em 100% das conversões estritas com ao menos uma pendência, nenhum arquivo TEX novo é criado nem um arquivo TEX existente é substituído.
- **SC-003**: Uma pessoa consegue criar o arquivo-modelo de regras e realizar uma primeira validação para um tipo documental em até cinco minutos, seguindo somente os exemplos do README.
- **SC-004**: O arquivo-modelo contém exemplos completos, comentados e habilitáveis para todos os cinco tipos documentais suportados.
- **SC-005**: A ajuda da linha de comando, o README e RELEASES identificam a versão 2.4.0 e explicam a nova funcionalidade.

## Assumptions

- Os cinco tipos documentais atualmente suportados permanecem os únicos abrangidos nesta versão.
- O arquivo-modelo é criado em uma localização padrão de configuração, mas pode ser criado em um destino explicitamente indicado pela pessoa usuária.
- Exemplos comentados não são regras ativas; a pessoa usuária os habilita removendo o comentário e ajustando os tópicos para seu processo.
- A configuração de regras é independente das preferências de estilo e não introduz estilos, classes, geometria ou tipografia.
- Tópicos obrigatórios são satisfeitos por títulos Markdown em qualquer nível de seção; a ordem dos tópicos não é exigida nesta versão.
- A conversão normal mantém a filosofia de avisos existente, enquanto o modo estrito transforma as pendências em bloqueio.
- A versão 2.4.0 substitui a entrada de versão futura de mesmo número em RELEASES; funcionalidades futuras não relacionadas permanecem planejadas separadamente.
