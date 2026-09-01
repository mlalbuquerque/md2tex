# Data Model: Memória de Reunião

## DocumentMetadata existente

A memória reutiliza `title`, `author`, `date` e `client` já suportados. Para o perfil `meeting-minutes`, a validação interpreta os dados adicionais do front matter e produz um contexto tipado para o template.

| Campo | Fonte YAML | Regra |
|---|---|---|
| Título | `title` | Opcional; mantém as regras gerais de título. |
| Cliente/Projeto | `client` | Obrigatório e texto não vazio. O valor inclui o código NEP quando o projeto possuir um código NEP atribuído. |
| Produtor/a | `author` | Obrigatório e texto não vazio. |
| Data | `date` | Obrigatória e texto não vazio. |
| Período | `period.start`, `period.end` | Ambos obrigatórios e textos não vazios. |
| Participantes do cliente | `participants.client` | Lista opcional; cada item informado exige `name` e `role`. |
| Participantes da Netra | `participants.netra` | Lista opcional; cada item informado exige `name` e `role`. |

## MeetingMinutesData

| Campo | Tipo lógico | Regra |
|---|---|---|
| `period_start` | texto | Valor de `period.start`; obrigatório. |
| `period_end` | texto | Valor de `period.end`; obrigatório. |
| `client_participants` | lista de Participant | Pode estar vazia. |
| `netra_participants` | lista de Participant | Pode estar vazia. |
| `has_no_pending_items` | booleano | Verdadeiro somente quando a seção Pendências contém exatamente a declaração `Sem pendências` após normalização. |

## Participant

| Campo | Tipo lógico | Regra |
|---|---|---|
| `name` | texto | Obrigatório para qualquer item de participante. |
| `role` | texto | Obrigatório para qualquer item de participante; corresponde a Cargo/Função. |
| `group` | enumeração | `client` ou `netra`; deriva do grupo YAML, não é preenchido em cada item. |

## Conteúdo do corpo

| Seção | Obrigatória | Regra |
|---|---|---|
| Objetivos da Reunião | Sim | Cabeçalho presente e conteúdo não vazio. |
| Tópicos Abordados | Sim | Cabeçalho presente e conteúdo não vazio. |
| Considerações Gerais e Definições | Sim | Cabeçalho presente e conteúdo não vazio. |
| Pendências | Sim | Contém `Sem pendências` ou uma tabela com Pendência, Responsável e Prazo para Solução e ao menos uma linha completa. |

## Relações e ciclos

Uma Memória de Reunião contém zero ou mais participantes em cada grupo e zero ou mais pendências. Não há persistência, identificador global ou transições de estado: cada conversão valida uma representação imutável do arquivo de entrada.
