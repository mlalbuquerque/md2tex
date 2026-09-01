# Contract: Front Matter da Memória de Reunião

## Aplicação

Este contrato é aplicado somente quando o documento é convertido com `--type meeting-minutes`. O arquivo deve começar com YAML front matter delimitado por `---`.

## Formato aceito

```yaml
---
title: Memória de Reunião
client: Cliente / Projeto (NEP-001)
author: Nome do produtor ou produtora
date: 2026-08-31
period:
  start: "09:00"
  end: "10:30"
participants:
  client:
    - name: Nome do cliente
      role: Cargo/Função
  netra:
    - name: Nome da Netra
      role: Cargo/Função
---

# Objetivos da Reunião

Definir os objetivos.

# Tópicos Abordados

Registrar os tópicos.

# Considerações Gerais e Definições

Registrar decisões e definições.

# Pendências

| Pendência | Responsável | Prazo para Solução |
|---|---|---|
| Enviar proposta | Nome | 2026-09-05 |
```

## Regras normativas

- `client`, `author`, `date`, `period.start` e `period.end` devem ser textos não vazios. Quando o projeto possuir um código NEP atribuído, `client` deve incluí-lo.
- `participants` é opcional; `client` e `netra` podem ser listas vazias ou omitidas.
- Cada participante informado deve ser um mapa com `name` e `role` não vazios. Chaves adicionais ou tipos incompatíveis devem gerar diagnóstico acionável.
- As seções Objetivos da Reunião, Tópicos Abordados, Considerações Gerais e Definições e Pendências devem existir e ter conteúdo válido.
- A seção Pendências deve conter uma tabela com as três colunas obrigatórias e linhas completas, ou conter exclusivamente `Sem pendências` como declaração de ausência de ações.
- Espaços em branco não satisfazem campos ou células obrigatórias.
- Opções equivalentes da CLI mantêm a precedência existente sobre `title`, `author`, `date` e `client`; os demais dados são fornecidos pelo front matter.
- No modo normal, pendências de validação são reportadas; em `--strict`, elas interrompem antes de qualquer geração ou alteração do destino.

## Diagnósticos mínimos

Cada ausência ou estrutura inválida deve citar o caminho do campo ou seção, por exemplo: `period.end`, `participants.netra[0].role`, `Objetivos da Reunião` ou `Pendências[1].Prazo para Solução`.
