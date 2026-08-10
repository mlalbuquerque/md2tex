# Data Model: Subtítulo pela CLI

## Opções de conversão

| Campo | Regra |
| --- | --- |
| `subtitle` | Texto recebido por `--subtitle`; espaços são normalizados como vazio. |
| presença de `subtitle` | Distingue a opção omitida de uma opção explicitamente vazia. |

## Metadados do documento

| Campo | Fonte e precedência | Apresentação |
| --- | --- | --- |
| `subtitle` | CLI fornecida; se omitida, front matter; se ausente, vazio | Somente quando não vazio. |
| `document_type` | Front matter ou rótulo do perfil | Sempre no bloco de identificação. |
| `author`, `version`, `date` | Fluxo existente | Junto de `document_type`. |

## Transições

1. A CLI registra o valor e a presença da opção.
2. A resolução usa a CLI somente se ela foi informada; caso contrário, usa front matter.
3. Conteúdo vazio resulta em subtítulo efetivo vazio.
4. A capa condiciona a linha de subtítulo e sempre agrupa o tipo aos demais metadados.
