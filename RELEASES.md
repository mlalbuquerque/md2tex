# md2tex Roadmap & Future Releases

Este documento descreve as sugestões de evolução e ideias para as próximas versões do **md2tex**, organizadas conforme o versionamento semântico ([Semantic Versioning - SemVer](https://semver.org/lang/pt-BR/)).

---

## 🚀 Versões Futuras Planejadas

### 📦 Versão v2.1.0 (Minor Release - Usabilidade & Bibliografia)
> **Foco**: Melhorias na experiência inicial do desenvolvedor e suporte a referências acadêmicas.

- [ ] **Comando `md2tex init`**:
  - Comando interativo para criar o arquivo de configuração `~/.config/md2tex/config.yaml` pré-preenchido com comentários e exemplos explicativos.
- [ ] **Suporte a Bibliografia e Citações (`.bib` / BibLaTeX)**:
  - Reconhecimento automático de citações no formato Markdown `[@chave2026]` e injeção dos pacotes `biblatex`/`biber` no preâmbulo do LaTeX.
- [ ] **Filtros Lua Customizados no `config.yaml`**:
  - Permitir que os usuários adicionem caminhos de filtros Lua personalizados na chave `lua_filters` do `config.yaml`.

---

### 🎨 Versão v2.2.0 (Minor Release - Produtividade & Estilização Avançada)
> **Foco**: Recompilação em tempo real e opções visuais avançadas.

- [ ] **Modo Watch (`md2tex watch document.md`)**:
  - Monitoramento contínuo do arquivo Markdown com recompilação automática do PDF a cada alteração salva (*live reload*).
- [ ] **Temas de Destaque de Sintaxe (`minted` / `listings`)**:
  - Configuração de temas de cores para blocos de código no `config.yaml` (`theme: nord`, `theme: dracula`, `theme: github`).
- [ ] **Layouts de Capa Selecionáveis**:
  - Opção no `config.yaml` ou CLI (`--cover-style`) para alternar entre capas *modern*, *classic*, *minimalist* ou *academic*.

---

### 🌐 Versão v3.0.0 (Major Release - Multi-Formato & Interface Web)
> **Foco**: Expansão para múltiplos formatos de saída e servidor web local.

- [ ] **Múltiplos Formatos de Saída (`--to docx | html | epub`)**:
  - Capacidade de exportar o documento para Word (`.docx`), HTML responsivo ou e-Books (`.epub`) além de LaTeX/PDF.
- [ ] **Servidor Web & API Local (`md2tex serve`)**:
  - Interface gráfica web executada localmente no navegador com pré-visualização lado a lado do PDF.
- [ ] **Cache Inteligente de Diagramas Mermaid**:
  - Armazenamento em cache de imagens geradas pelo `mmdc` para evitar renderização duplicada em documentos grandes, acelerando as compilações subsequentes.

---

## 📌 Histórico de Versões Principais

- **v2.0.0**: 
  - Renomeação completa do projeto para `md2tex`.
  - Sistema de configuração baseado exclusivamente em `~/.config/md2tex/config.yaml`.
  - Assistente interativo de dependências (`md2tex --setup` / `md2tex --check-deps`).
  - Pipeline CI/CD multi-OS no GitHub Actions com publicação de executáveis estáticos em Releases.
- **v1.2.x**: 
  - Suporte a comandos inline protegidos contra *moving arguments* no LaTeX.
- **v1.0.0**: 
  - Versão inicial do conversor Markdown para LaTeX no padrão Netra.
