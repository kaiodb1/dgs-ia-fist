# AGENTS.md — Resumo operacional do projeto NovaTech

## Regras obrigatórias

1. **TypeScript strict mode** em todo o projeto.
2. **Zod** para validar inputs e structured outputs nas fronteiras do sistema.
3. **pino** para logging; `console.log` nao e permitido.
4. **Nunca logar dados pessoais**, como e-mail ou nome de atendentes/clientes.
5. **Imports estaticos no topo do arquivo**; `require` dinamico nao e permitido.
6. **Vitest** e o framework de testes do projeto.

## Guardrails relevantes ao cenário 3

1. Toda resposta do assistente precisa chegar em formato validavel, com `answer`, `source_document` e `confidence_score`.
2. Respostas sem fonte util nao podem seguir para o usuario final.
3. Respostas sobre **devolucao de carga perigosa** precisam trazer negativa explicita; caso contrario, devem ser bloqueadas.

## Criterio de qualidade

- Guardrails determinísticos precisam **bloquear** respostas invalidas, nao apenas registrar em log.
- Revisoes de codigo precisam demonstrar analise propria e confronto critico com uma segunda revisao.
