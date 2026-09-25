# md2tex Roadmap

Planejamento futuro do projeto. As versões já publicadas estão em [RELEASES.md](RELEASES.md).

## 🚀 Versões Futuras Planejadas

### v2.8.0 — Múltiplos Formatos de Saída
- [ ] Suporte a múltiplos formatos de saída via opção `--to pdf|html|epub|docx|odt`.
- [ ] Descontinuação e remoção da opção `--pdf` (o comportamento passa a ser coberto por `--to pdf`).

### v2.9.0 — Imagens e Cache Inteligente
- [ ] Implementação de cache inteligente para os diagramas gerados pelo Mermaid.
- [ ] Suporte aprimorado para marcação de imagens no Markdown: ao passar o caminho da imagem, ela será automaticamente ajustada à página.
- [ ] Inclusão de suporte e renderização automática de legendas nas imagens.

### v3.0.0 — Servidor Web e API Local
- [ ] Lançamento do comando `md2tex serve` para iniciar uma API local e servidor Web.
- [ ] Interface gráfica na Web contendo:
  - Espaço para upload e visualização do arquivo Markdown.
  - Painel de opções interativo (para marcar/desmarcar flags e configurar valores das opções da CLI).
  - Espaço para exibir logs e os resultados gerados.
  - Visualizador de documentos integrado (exibição direta do conteúdo gerado como PDF, ODT, HTML, etc).

### v3.1.0 — Assistente de Criação de Templates (CLI)
- [ ] Nova ferramenta de apoio ("scaffolding"): criação de templates e novos perfis de documento gerados baseados em um documento de referência pronto.
- [ ] Leitura e extração da estrutura a partir de arquivos modelo em formato `.pdf`, `.docx`, `.html` ou `.odt`.

### v3.2.0 — Assistente de Criação de Templates (Web)
- [ ] Integração da funcionalidade de criação de templates baseados em arquivos de referência (criada na v3.1.0) diretamente na interface do servidor Web (página Web).

---
*As prioridades e o escopo podem evoluir conforme as necessidades do projeto.*
