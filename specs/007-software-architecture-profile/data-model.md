# Data Model: Perfil Documento de Arquitetura de Software

## Entities

### Software Architecture Profile

Identifica uma variante documental disponível ao conversor.

| Field | Type | Required | Rules |
|---|---|---:|---|
| identifier | string | yes | `software-architecture`; único no registro de perfis |
| label | string | yes | `Documento de Arquitetura de Software` |
| template | string | yes | Template dedicado ao perfil |

O identificador é a chave de `--type` e `rules.yaml`. Não altera automaticamente as regras dos outros perfis.

### System Name

Valor de apresentação opcional para a capa.

| Field | Type | Required | Rules |
|---|---|---:|---|
| value | string | no | Espaços externos são removidos; saída omitida se ausente ou vazia após normalização |
| source | front matter or CLI | no | Se `--system-name` for fornecido, prevalece sobre front matter, inclusive se vazio |

O texto aparece alinhado à direita logo abaixo da área superior reservada para logotipo. O perfil não fornece imagem nem estilo institucional; sem logotipo, mantém a mesma posição.

### Revision Entry

Registro ordenado exibido em uma linha da tabela do Histórico de Revisões.

| Field | Type | Required | Rules |
|---|---|---:|---|
| date | string | no | Texto da célula; valores ausentes resultam em célula vazia |
| version | string | no | Texto da célula; valores ausentes resultam em célula vazia |
| description | string | no | Texto da célula; valores ausentes resultam em célula vazia |
| author | string | no | Texto da célula; valores ausentes resultam em célula vazia |

`revision-history` é uma lista de entradas. A sequência fornecida é preservada. Se não houver entradas, o perfil gera uma única entrada baseada nos metadados `date`, `version` e `author`, com `description` vazia. A página e os cabeçalhos da tabela continuam obrigatórios.

## Relationships

- Um perfil selecionado tem exatamente um template.
- Um documento convertido para `software-architecture` tem zero ou mais entradas de revisão explícitas; a saída sempre contém uma tabela e, no caso de lista vazia/ausente, uma linha inicial derivada dos metadados gerais.
- Um documento tem no máximo um nome de sistema efetivo, resolvido pela precedência CLI sobre front matter.

## Validation and Rendering Rules

1. `system-name` aceita texto opcional; não deve ser tratado como requisito de validação.
2. `revision-history` aceita uma lista ordenada de mapas com `date`, `version`, `description` e `author`.
3. Os quatro valores de célula são escapados como texto LaTeX; strings vazias permanecem células válidas.
4. A tabela contém cabeçalhos `Data`, `Versão`, `Descrição` e `Autor`.
5. A página do histórico é emitida após a capa e antes do TOC, independentemente da opção de TOC.
6. `default`, `report`, `meeting-minutes`, `adr` e `technical-plan` não devem receber capa ou histórico próprios da arquitetura.
