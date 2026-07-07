# Entrega — Cenário 3 / Desenvolvedor

Esta pasta contém uma entrega standalone para os exercícios **3.1** e **3.2** do papel **Desenvolvedor** no cenário 3 da trilha AI First.

## Estrutura

- `AGENTS.md`: convenções do projeto usadas na reescrita do código.
- `src/services/response-validator.ts`: structured output + guardrails determinísticos do exercício 3.1.
- `src/functions/feedback/handler.ts`: handler reescrito do exercício 3.2.
- `tests/`: testes direcionados para os dois módulos.
- `docs/`: documentação dos entregáveis, prompts usados, saídas do Claude e avaliação final.

## Comandos

```bash
npm install
npm run typecheck
npm test
```

## Observações

- O workspace original continha apenas os arquivos do cenário e da correção, sem um repositório NovaTech para editar.
- Por isso, a solução foi organizada como um projeto TypeScript mínimo, com validação Zod, logging com pino e testes em Vitest, em linha com o AGENTS.md resumido no cenário.
