# md2tex Roadmap & Future Releases

Este documento registra lançamentos e planejamento segundo [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## 🚀 Versões Futuras Planejadas

### 🌐 Versão v3.0.0 (Major Release - Multi-Formato e Interface Web)

- [ ] **Múltiplos Formatos de Saída (`--to docx | html | epub`)**.
- [ ] **Servidor Web & API Local (`md2tex serve`)**.
- [ ] **Cache Inteligente de Diagramas Mermaid**.

---

## 📌 Histórico de Versões Principais

- **v2.6.0** *(Minor Release, publicada)*:
  - Adiciona requisitos de campos e seções configuráveis por tipo documental em config.yaml, com orientações e exemplos copiáveis.
  - Mantém precedência da CLI, isolamento por perfil e bloqueio seguro em --strict.

- **v2.5.1** *(Patch Release, publicada)*:
  - Substitui os identificadores internos `period.start` e `period.end` pelos diagnósticos `Período — início` e `Período — fim` na validação de Memória de Reunião.

- **v2.5.0** *(Minor Release, publicada)*:
  - Adiciona o perfil `meeting-minutes` com front matter YAML para identificação, período e participantes.
  - Valida campos e seções obrigatórios; `--strict` bloqueia a saída antes de etapas externas.
  - Suporta grupos de participantes vazios e a declaração explícita `Sem pendências`.
  - Inclui exemplo público e documentação do contrato.


- **v2.4.0** *(Minor Release)*:
  - Adiciona regras YAML independentes de estilo para tópicos obrigatórios por perfil documental.
  - Inclui `md2tex rules init` para criar um modelo comentado e personalizável.
  - Adiciona `--rules PATH`, avisos de tópicos pendentes e o bloqueio antecipado com `--strict`.
  - Preserva a conversão quando não há regras configuradas e mantém `--no-validate` como opt-out das validações de tópicos.

- **v2.3.0** *(Minor Release)*:
  - Adiciona a opção `--subtitle` para sobrescrever o subtítulo do documento.
  - Agrupa o tipo de documento com autoria, versão e data nas capas.
  - Mantém o front matter quando a opção é omitida e permite limpar o subtítulo com valor vazio.


- **v2.2.0** *(Minor Release)*:
  - Adiciona a seção `tables` no YAML e sobrescritas de CLI para zebrado, bordas, largura, fonte e paisagem.
  - Suporta contornos `none`, `outer` e `grid`, além de adaptadores de tabelas no `netra-letterhead.sty`.

- **v2.1.2** *(Patch Release)*:
  - Valida pacotes LaTeX requeridos pelo fragmento Pandoc e orienta a inclusão em `style_packages` antes da compilação.

- **v2.1.1** *(Patch Release)*:
  - Detecta antecipadamente conflitos entre `page_geometry`/`style_packages` e pacotes carregados por arquivos `.sty`.
  - Acrescenta orientação de configuração para erros LaTeX de conflito de opções.

- **v2.1.0** *(Minor Release)*:
  - Adiciona `md2tex init` para criar uma configuração completa inicial.
  - Remove defaults de estilo e compilação do código; o YAML passa a ser obrigatório e validado estritamente.
  - Alinha documentação, contratos e referências legadas ao nome md2tex.


- **v2.0.2** *(Patch Release)*:
  - Corrige a conversão de sequências textuais de controle, como `\r\n`, que o Pandoc encaminhava como comandos LaTeX inválidos.

- **v2.0.0**: 
  - Renomeação completa do projeto para `md2tex`.
  - Sistema de configuração baseado exclusivamente em `~/.config/md2tex/config.yaml`.
  - Assistente interativo de dependências (`md2tex --setup` / `md2tex --check-deps`).
  - Pipeline CI/CD multi-OS no GitHub Actions com publicação de executáveis estáticos em Releases.
- **v1.2.x**: 
  - Suporte a comandos inline protegidos contra *moving arguments* no LaTeX.
- **v1.0.0**: 
  - Versão inicial do conversor Markdown para LaTeX.
