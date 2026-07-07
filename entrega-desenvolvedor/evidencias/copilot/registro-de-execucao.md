# Registro de execução — Copilot CLI

> Esta entrega foi executada integralmente com o Copilot CLI, conforme alinhado para a prática.

## Exercício 2.1 — MCP

1. Leitura do enunciado, rubricas e anexos para identificar os servers esperados (`filesystem`, `git`, `memory`, `everything`).
2. Inspeção do starter repo dentro do ZIP para confirmar estado inicial de `.mcp/mcp.json`, presença do `.git` local e dos diretórios `docs/novatech` e `data/retrieval-corpus`.
3. Verificação de ferramentas locais (`node`, `npm`, `uvx`, `git`, `docker`) e leitura do README oficial dos servers para confirmar a sintaxe no Windows.
4. Primeira tentativa de evidência com um cliente stdio escrito manualmente.
5. Revisão crítica da tentativa: o handshake manual ficou preso; a estratégia foi trocada pelo **SDK oficial do MCP**.
6. Segunda execução com o SDK oficial, gerando `mcp-evidence.json` e `mcp-evidence.md`.

## Exercício 2.2 — SDD e implementação

1. Materialização de `requirements.md` e `plan.md` do `query-endpoint` a partir do contexto fornecido no enunciado.
2. Geração do `tasks.md` com decomposição atômica e critérios verificáveis.
3. Implementação do contrato inicial do endpoint (`validator.ts`, `response-builder.ts`, `handler.ts`, `logger.ts`).
4. Primeira rodada de testes falhou porque o harness usava `HttpRequest` com body no formato errado.
5. Ajuste aplicado: `body.string` no construtor de teste do `@azure/functions`.
6. Primeira rodada de build falhou porque `app.http()` esperava `HttpMethod[]`.
7. Ajuste aplicado: tipagem explícita do array de métodos.

## Exercício 2.3 — Skills

1. Mapeamento da árvore Foundation -> Domain -> Artifact com autores, consumidores e frequência.
2. Escolha da skill Foundation prioritária: `typescript-conventions`.
3. Escrita da skill com regras prescritivas, exemplos DO/DON'T e anti-padrões reais de LLM.

## Evidências correlatas

- MCP: `deliverables/desenvolvedor/evidencias/mcp/`
- Revisão crítica: `deliverables/desenvolvedor/exercicio-2-2/revisao-critica-copilot.md`
- Skill Foundation: `skills/foundation/typescript-conventions.md`
