# Quickstart: Memória de Reunião

## Pré-requisitos

1. Instale o projeto e dependências de desenvolvimento.
2. Configure o pacote letterhead da Netra em `config.yaml`, conforme a instalação local. O perfil não adiciona estilo automaticamente.
3. Use o contrato de entrada em [contracts/meeting-minutes-frontmatter.md](contracts/meeting-minutes-frontmatter.md).

## Cenário 1 — memória completa

1. Crie `memoria.md` com o front matter e as quatro seções do contrato.
2. Execute:

   ```bash
   md2tex memoria.md --type meeting-minutes --config ./config.yaml --output memoria.tex
   ```

3. Confirme que o TEX inclui Cliente/Projeto, Produtor/a, data, período, os grupos de participantes e a tabela de pendências; não deve haver aviso de dados obrigatórios ausentes.

## Cenário 2 — reunião interna sem participantes nem pendências

1. Omita os dois grupos de participantes.
2. Em `# Pendências`, escreva somente `Sem pendências`.
3. Converta como no cenário 1.
4. Confirme que a conversão é aceita e que a declaração é apresentada no resultado.

## Cenário 3 — campo obrigatório ausente

1. Remova `period.end` da memória completa.
2. Execute a conversão normal.
3. Confirme o diagnóstico que cita `period.end`; a saída normal pode ser gerada conforme o comportamento de validação não estrita.

## Cenário 4 — bloqueio estrito e preservação do destino

1. Crie um `memoria.tex` com conteúdo conhecido.
2. Use a memória inválida do cenário 3 e execute:

   ```bash
   md2tex memoria.md --type meeting-minutes --config ./config.yaml --strict --output memoria.tex --force
   ```

3. Confirme saída não zero, diagnóstico nominal e que `memoria.tex` permanece byte a byte inalterado.

## Verificação automatizada

```bash
ruff check src tests
pytest -q
```

Confirme os testes específicos de metadados, validador, CLI e integração da memória de reunião.
