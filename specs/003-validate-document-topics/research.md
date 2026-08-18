# Research: validação de tópicos por tipo documental

## Localização e schema

**Decision**: Usar `~/.config/md2tex/rules.yaml` como padrão e `--rules PATH` por conversão. Aceitar somente a raiz YAML `rules`, mapeando IDs de perfil para listas de strings não vazias.

**Rationale**: `config.yaml` é um schema estrito dedicado a estilo. Regras de conteúdo são independentes e podem ser específicas de projeto; IDs válidos já vivem em `profiles.py`.

**Alternatives considered**: Inserir regras em `config.yaml` mistura responsabilidades; procurar automaticamente no diretório atual cria comportamento implícito.

## Inicialização

**Decision**: Fornecer `md2tex rules init [--rules PATH] [--force]`, com modelo distribuído de exemplos completos, comentados e inativos para os cinco perfis.

**Rationale**: Espelha o `md2tex init` existente: cria diretórios pai e só sobrescreve com confirmação explícita.

**Alternatives considered**: `rules-init` ou sobrecarregar `init` não atendem ao comando especificado; exemplos ativos introduziriam regras implícitas.

## Comparação de títulos

**Decision**: Extrair títulos ATX e Setext de qualquer nível depois de remover numeração manual e normalizar níveis, ignorando fenced code. Comparar `strip().casefold()` e preservar a escrita configurada nos avisos.

**Rationale**: Atende equivalência de caixa/espaços, evita títulos falsos em código e se alinha ao Markdown convertido. Conjuntos eliminam duplicidade.

**Alternatives considered**: AST JSON do Pandoc exigiria execução externa adicional; a regex atual não cobre Setext nem fences.

## Gate estrito e falhas

**Decision**: Carregar regras e validar tópicos no começo de `convert()`, antes de Mermaid, Pandoc, renderização e escrita. Pendências são avisos no modo normal e `ValidationError` imediato com `--strict`. `--rules` explícito inválido falha mesmo sem `--strict` ou com `--no-validate`; ausência do padrão é silenciosa e padrão inválido é aviso sem aplicação parcial.

**Rationale**: O gate atual é tardio para assegurar que TEX não seja criado ou substituído. A indicação explícita não pode ser interpretada parcialmente (FR-009), enquanto a ausência padrão preserva a conversão atual.

**Alternatives considered**: Reutilizar o gate tardio ainda faria processamento e violaria o requisito de pré-saída; ignorar caminho explícito inválido com `--no-validate` conflita com FR-009.
