# Feature Specification: 000-primeira-versao (Funcionalidades Atuais do netra-md2tex)

**Feature Directory**: `specs/000-primeira-versao`

**Created**: 2026-08-02

**Status**: Baseline Specification (Current Application State)

**Input**: User description: "Quero que crie a especificação do que existe hoje como 000-primeira-versao, colocando tudo o que o app faz hoje já. Pode colocar as saídas do "--help" no arquivo também como referência. Pode usar o README.md como referência também."

---

## Executive Overview

`netra-md2tex` é uma ferramenta CLI em Python projetada para converter documentos em Markdown (`.md`) para LaTeX (`.tex`) e compilá-los opcionalmente para PDF (`.pdf`), garantindo total aderência ao padrão visual da Netra Tecnologia e ao pacote LaTeX `netra-letterhead`.

A solução utiliza o Pandoc para parsing semântico (gerando uma AST intermediária em vez de regex), filtros Lua customizados (`netra.lua`), pré-processamento de metadados YAML Front Matter, renderização de diagramas Mermaid (`mmdc`), preenchimento de templates LaTeX com Jinja2 e compilação automatizada com `latexmk` (XeLaTeX/LuaLaTeX/PDFLaTeX).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversão Básica de Markdown para TEX e PDF (Priority: P1)

Como um autor de documentação técnica da Netra, quero converter um arquivo Markdown contendo títulos, listas, textos formatados e metadados YAML em um arquivo `.tex` bem-formatado e gerar seu `.pdf` correspondente via CLI.

**Why this priority**: É a funcionalidade central e o MVP primário da aplicação. Sem ela, nenhuma conversão documental é possível.

**Independent Test**: Pode ser testado de forma isolada executando `netra-md2tex documento.md --pdf` e verificando a geração válida de `documento.tex` e `documento.pdf`.

**Acceptance Scenarios**:

1. **Given** um arquivo `relatorio.md` válido com Front Matter YAML (título, autor, data), **When** o usuário executa `netra-md2tex relatorio.md`, **Then** o sistema gera `relatorio.tex` utilizando o template de relatório padrão (`report`) e incluindo os metadados.
2. **Given** um arquivo `relatorio.md`, **When** o usuário executa `netra-md2tex relatorio.md --pdf`, **Then** o sistema invoca o `latexmk` (XeLaTeX por padrão) e produz o arquivo `relatorio.pdf` sem erros de compilação.
3. **Given** a existência prévia de `documento.tex`, **When** o usuário executa `netra-md2tex documento.md` sem a flag `--force`, **Then** o sistema encerra informando erro de sobrescrita. Se a flag `--force` for usada, o arquivo é sobrescrito com sucesso.

---

### User Story 2 - Seleção de Perfis Documentais e Sobrescrita de Metadados (Priority: P2)

Como um gerente de projetos ou engenheiro, quero escolher o tipo de documento (`report`, `meeting-minutes`, `adr`, `technical-plan`) e ajustar título, cliente ou versão pela CLI para reutilizar o mesmo Markdown para diferentes fins.

**Why this priority**: Permite flexibilidade corporativa e adequação visual às diversas necessidades da empresa (atas de reunião, ADRs, relatórios e planos).

**Independent Test**: Pode ser testado executando `netra-md2tex documento.md --type adr --title "ADR 001" --document-version "1.0"` e verificando a aplicação do template `adr.tex.j2` e os valores fornecidos via CLI no TEX final.

**Acceptance Scenarios**:

1. **Given** um documento Markdown sem Front Matter, **When** o usuário executa `netra-md2tex doc.md --type meeting-minutes --client "Cliente X"`, **Then** o sistema aplica o template de memória de reunião e injeta "Cliente X" no contexto do template.
2. **Given** um documento Markdown com `title: "Título YAML"`, **When** o usuário executa `netra-md2tex doc.md --title "Título CLI"`, **Then** a precedência garante que "Título CLI" seja utilizado no documento final.

---

### User Story 3 - Renderização de Diagramas Mermaid e Tratamento de Tabelas (Priority: P2)

Como um arquiteto de software, quero que blocos de código `mermaid` sejam convertidos automaticamente em imagens (PNG/PDF/SVG) e que tabelas extensas sejam dispostas automaticamente em orientação paisagem quando necessário.

**Why this priority**: Garante que diagramas de arquitetura e tabelas com muitas colunas fiquem legíveis no PDF final sem quebras de layout ou extrapolação de margem.

**Independent Test**: Pode ser testado fornecendo um Markdown contendo um bloco ````mermaid ... ```` e uma tabela de 7 colunas, executando com `--mermaid-format png --landscape-tables auto` e verificando a criação da imagem em `figures/` e a marcação de paisagem na tabela.

**Acceptance Scenarios**:

1. **Given** um documento com um bloco ````mermaid ... ```` e o `mmdc` instalado, **When** o comando é executado, **Then** o diagrama é exportado para a pasta `figures/` no formato especificado e referenciado no LaTeX via `\includegraphics`.
2. **Given** uma tabela com 6 ou mais colunas e `--landscape-tables auto`, **When** o documento é convertido, **Then** a tabela é configurada em modo paisagem (`pdflscape`/`landscape`).
3. **Given** a flag `--table-font scriptsize`, **When** as tabelas são geradas no LaTeX, **Then** a fonte interna é definida como `\scriptsize`.

---

### User Story 4 - Validação Automática, Leitura de Logs e Modo Estrito (Priority: P3)

Como um engenheiro de DevOps configurando um pipeline de CI/CD, quero que a ferramenta valide a ausência de imagens faltantes, placeholders não convertidos (`@@PHn@@`), pulos na hierarquia de cabeçalhos e erros de compilação, interrompendo o pipeline (`exit 2`) quando a flag `--strict` estiver ativa.

**Why this priority**: Previne que documentos com erros sutis de compilação, imagens quebradas ou referências pendentes sejam publicados em produção.

**Independent Test**: Executar `netra-md2tex documento_com_erro.md --strict` e validar se o código de saída é `2` e as mensagens de validação aparecem no terminal.

**Acceptance Scenarios**:

1. **Given** um Markdown referenciando uma imagem inexistente `imagem_quebrada.png`, **When** executado com `--validate`, **Then** o sistema gera um aviso de validação.
2. **Given** erros de compilação ou placeholders remanescentes e a opção `--strict` habilitada, **When** a conversão ocorre, **Then** o processo encerra com código de retorno 2.
3. **Given** a compilação com `--clean`, **When** concluída com sucesso, **Then** os arquivos auxiliares do LaTeX (`.aux`, `.log`, etc.) são removidos, preservando o `.toc`.

---

### Edge Cases

- **Ausência de Pandoc ou latexmk**: O sistema detecta a ausência de ferramentas externas no ambiente e retorna mensagens de erro amigáveis sem causar tracebacks não tratados.
- **Ausência do mmdc (Mermaid CLI)**: Quando o `mmdc` não está instalado e `--mermaid` está ativo, o bloco Mermaid é mantido como bloco de código fonte no LaTeX e um aviso de validação é emitido. Se `--strict` estiver ativo, o processo falha.
- **Tabelas sem cabeçalho ou vazias**: O filtro Lua aceita e trata graciosamente tabelas atípicas.
- **Conflito de Flags de Limpeza**: Especificar `--clean` e `--clean-all` simultaneamente resulta em um erro de uso da CLI (`UsageError`).
- **Nomes de Arquivo com Espaços e Caracteres Especiais**: O pré-processador e o compilador lidam com caminhos absolutos e relativos contendo espaços.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST aceitar um arquivo de entrada Markdown (`.md`) e gerar o arquivo de saída LaTeX (`.tex`).
- **FR-002**: O sistema MUST suportar a compilação opcional para PDF (`.pdf`) utilizando `latexmk` com suporte aos motores `xelatex`, `lualatex` e `pdflatex`.
- **FR-003**: O sistema MUST suportar os 4 perfis documentais padrão: `report` (Relatório), `meeting-minutes` (Memória de Reunião), `adr` (Decisão Arquitetural) e `technical-plan` (Plano Técnico).
- **FR-004**: O sistema MUST ler e interpretar metadados YAML Front Matter (título, autor, data, versão, cliente, subtítulo, status).
- **FR-005**: O sistema MUST obedecer à hierarquia de precedência de metadados: CLI Options > YAML Front Matter > Primeiro H1 do Markdown > Nome do arquivo.
- **FR-006**: O sistema MUST normalizar títulos Markdown, removendo numeração manual (ex: `## 1. Introdução` -> `\section{Introdução}`) para deixar a numeração a cargo do LaTeX.
- **FR-007**: O sistema MUST utilizar o Pandoc e um filtro Lua customizado (`netra.lua`) para interpretar o AST do Markdown.
- **FR-008**: O sistema MUST aplicar a formatação inline de código:
  - Caminhos de arquivo (Linux/Windows) via `\path{...}`.
  - URLs via `\url{...}` (com suporte `xurl`).
  - Comandos de terminal com argumentos via `\lstinline{...}`.
  - Termos e código simples via `\texttt{...}`.
- **FR-009**: O sistema MUST gerenciar o layout de tabelas:
  - Envolvimento por `\netraStartTable` e `\netraEndTable`.
  - Orientação automática em paisagem (`auto`, `always`, `never`).
  - Ajuste de tamanho de fonte (`normalsize`, `small`, `footnotesize`, `scriptsize`).
  - Estratégias de largura de coluna (`auto`, `equal`, `natural`).
- **FR-010**: O sistema MUST renderizar blocos anotados (`::: note`, `::: warning`, `::: decision`) como caixas destacadas `tcolorbox`.
- **FR-011**: O sistema MUST suportar checklists de tarefas (`- [x]` / `- [ ]`).
- **FR-012**: O sistema MUST limitar o tamanho de imagens à largura e altura úteis da página (respeitando limites máximos de 95% de `\linewidth` e 78% de `\textheight`), garantindo a preservação da proporção original (sem distorção).
- **FR-013**: O sistema MUST converter blocos de código `mermaid` para imagens (PNG, PDF ou SVG) via `mmdc` (Mermaid CLI).
- **FR-014**: O sistema MUST realizar validações automáticas no documento (imagens ausentes, pulo de hierarquia de títulos, placeholders `@@PHn@@`, citações/referências pendentes, avisos de `Overfull \hbox`).
- **FR-015**: O sistema MUST oferecer o modo estrito (`--strict`), que encerra a execução com código de saída 2 caso ocorram erros de validação.
- **FR-016**: O sistema MUST oferecer suporte à limpeza de arquivos auxiliares de compilação via `--clean` (mantendo `.toc`) e `--clean-all` (removendo `.toc`).
- **FR-017**: O sistema MUST permitir a especificação de um caminho customizado para o pacote de estilo `--style-path` (padrão: `netra-letterhead`).
- **FR-018**: O sistema MUST permitir o uso de templates Jinja2 customizados (`--template`).
- **FR-019**: O sistema MUST permitir salvar os arquivos intermediários de build (`.documento-build/`) através da flag `--keep-build`.

### Key Entities

- **DocumentOptions / ConversionOptions**: Modelo de dados que consolida todas as opções de conversão (caminho de entrada, saída, perfil, metadados, motores de compilação, flags de tabela e imagens).
- **DocumentMetadata**: Estrutura contendo o título, autor, data, versão, cliente, subtítulo, status e campos adicionais.
- **ValidationMessage**: Objeto que representa um aviso ou erro retornado pelo validador (nível, origem e mensagem).
- **ConversionResult**: Objeto de resultado da conversão contendo os caminhos gerados (`.tex`, `.pdf`, diretório de build) e a lista de mensagens de validação.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos documentos Markdown válidos são convertidos para TEX sem a presença de resíduos de parsing como `@@PHn@@`.
- **SC-002**: A compilação PDF produz documentos que respeitam integralmente as margens e a área útil da página (imagens não distorcidas e sem invasão de margens).
- **SC-003**: 100% das suítes de testes automatizados (`pytest`) executam com sucesso.
- **SC-004**: No modo estrito (`--strict`), 100% dos documentos com imagens quebradas ou erros fatais de compilação resultam em código de saída `2`.

---

## Saída do Comando `--help` (Referência)

Abaixo está registrada a saída oficial do comando `netra-md2tex --help` para referência técnica completa dos parâmetros suportados pela aplicação:

```text
Usage: netra-md2tex [OPTIONS] INPUT_FILE

  Converte INPUT_FILE Markdown para um documento TEX/PDF no padrão Netra.

Options:
  -o, --output FILE               Arquivo TEX de saída.
  --type [report|meeting-minutes|adr|technical-plan]
                                  Perfil documental aplicado ao documento.
                                  [default: report]
  --title TEXT                    Sobrescreve o título do YAML/H1.
  --author TEXT                   Sobrescreve o autor.
  --date TEXT                     Sobrescreve a data do documento.
  --document-version TEXT         Sobrescreve a versão documental.
  --client TEXT                   Sobrescreve o cliente/projeto.
  --style-path TEXT               Caminho do pacote netra-letterhead, sem a
                                  extensão .sty.  [default: /home/mlalbuquerque
                                  /Dropbox/Netra/projetos/netra-letterhead]
  --figures DIRECTORY             Diretório das imagens e diagramas Mermaid.
                                  [default: figures]
  --template FILE                 Template Jinja2 TEX personalizado.
  --pdf / --no-pdf                Compila o TEX para PDF.
  --validate / --no-validate      Executa validações antes/depois da conversão.
  --strict                        Interrompe a execução quando houver erros de
                                  validação.
  --toc / --no-toc                Inclui ou remove o sumário.
  --engine [xelatex|lualatex|pdflatex]
                                  Motor LaTeX usado com --pdf.  [default:
                                  xelatex]
  --mermaid / --no-mermaid        Renderiza blocos fenced mermaid.
  --mermaid-format [png|pdf|svg]  Formato de saída dos diagramas Mermaid.
                                  [default: png]
  --landscape-tables [auto|always|never]
                                  Coloca tabelas largas em páginas paisagem.
                                  [default: auto]
  --table-font [normalsize|small|footnotesize|scriptsize]
                                  Tamanho da fonte usado dentro das tabelas.
                                  [default: small]
  --table-width [auto|equal|natural]
                                  Estratégia de largura das colunas:
                                  proporcional, igual ou natural.  [default:
                                  auto]
  --shell-escape                  Habilita shell-escape na compilação LaTeX.
  --keep-build                    Mantém Markdown pré-processado e fragmento
                                  TEX.
  --clean                         Remove auxiliares LaTeX após a execução,
                                  preservando o .toc.
  --clean-all                     Remove todos os auxiliares LaTeX, inclusive o
                                  .toc.
  --force                         Sobrescreve o arquivo de saída existente.
  -v, --verbose                   Mostra os comandos externos executados.
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.
```

---

## Assumptions

- **Ambiente Linux**: A ferramenta assume um ambiente Linux/Debian/Ubuntu com Python 3.10+, Pandoc e TeX Live instalados.
- **Pacote netra-letterhead**: Assume a existência e compatibilidade com o pacote corporativo `netra-letterhead`.
- **Precedência de Metadados**: Assume que os parâmetros fornecidos via CLI têm prioridade máxima sobre o Front Matter YAML e a estrutura H1.
