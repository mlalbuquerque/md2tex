# md2tex Roadmap & Future Releases

Este documento registra lançamentos e planejamento segundo [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## 🚀 Versões Futuras Planejadas

### 🎨 Versão v2.4.0 (Minor Release - Produtividade e Estilização Avançada)

- [ ] **Modo Watch (`md2tex watch document.md`)**.
- [ ] **Temas de Destaque de Sintaxe (`minted` / `listings`)**.
- [ ] **Layouts de Capa Selecionáveis**.

### 🌐 Versão v3.0.0 (Major Release - Multi-Formato e Interface Web)

- [ ] **Múltiplos Formatos de Saída (`--to docx | html | epub`)**.
- [ ] **Servidor Web & API Local (`md2tex serve`)**.
- [ ] **Cache Inteligente de Diagramas Mermaid**.

---

## 📌 Histórico de Versões Principais

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
