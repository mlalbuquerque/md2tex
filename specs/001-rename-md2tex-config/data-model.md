# Data Model: md2tex 2.2.0

## UserConfig

| Campo | Tipo | Obrigatório | Uso |
|---|---|---:|---|
| `document_class` | string | Sim | Classe LaTeX |
| `class_options` | lista de strings | Sim | Opções da classe |
| `style_packages` | lista de strings | Sim | Pacotes carregados |
| `page_geometry` | mapa string/string | Sim | Opções de geometry |
| `typography` | mapa string/string | Sim | `language`, `fontsize`, `mainfont`, `line_spacing` |
| `preamble_includes` | lista de strings | Sim | Macros e ajustes explícitos |
| `compiler_options` | mapa | Sim | Contém apenas `engine` |
| `tables` | mapa | Sim | `landscape`, `font`, `width`, `borders` e `zebra` |

Não há defaults no schema. O modelo gerado por `md2tex init` fornece valores iniciais editáveis.
