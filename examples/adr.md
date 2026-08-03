---
title: Adoção do Keycloak como provedor de identidade
status: Aceito
date: 2026-07-30
version: "1.0"
document-type: Registro de Decisão Arquitetural (ADR)
---

## 1. Contexto

Os sistemas internos precisam compartilhar autenticação e autorização.

## 2. Decisão

::: decision
Adotar o Keycloak integrado ao AD/LDAP como provedor central de identidade.
:::

## 3. Consequências

- Centralização de autenticação.
- Necessidade de governança de realms, clients, roles e grupos.
