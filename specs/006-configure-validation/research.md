# Research: Requisitos declarativos

## Decision: incluir `document_requirements` no `config.yaml`

**Rationale**: o arquivo já é a configuração explícita do usuário e sua carga é validada antes da conversão. Uma seção opcional permite configurar requisitos sem segundo arquivo, caminho ou precedência.

**Alternatives considered**:

- Reutilizar `rules.yaml`: rejeitado, pois ele descreve somente títulos e não comporta rótulo, exemplo ou instrução sem quebrar seu contrato.
- Criar um novo arquivo de requisitos: rejeitado, pois aumenta a configuração obrigatória e conflita com a solicitação de usar `config.yaml`.
- Mensagens hardcoded por perfil: rejeitado, pois exige alterar código para cada processo documental.

## Decision: regras declarativas complementam validadores estruturais

**Rationale**: regras configuradas definem exigência e orientação pública; a validação existente continua responsável por formatos complexos, como participantes e tabelas. Para caminho ou seção equivalente, a orientação configurada substitui a mensagem genérica, evitando duplicação.

**Alternatives considered**:

- Substituir todo validador específico: rejeitado, pois perde validações estruturais essenciais.
- Exibir ambas as mensagens: rejeitado, pois repete a mesma pendência e dificulta a correção.

## Decision: campos usam metadados após precedência e seções usam o corpo Markdown

**Rationale**: campos equivalentes à CLI devem respeitar o valor final já resolvido; seções não possuem sobreposição de CLI e são verificadas nos títulos e conteúdos do documento.
