# Exercício 3.2 — Revisão crítica de código gerado por IA

## Objetivo

Revisar criticamente o handler gerado por IA antes do merge, comparar a analise humana com uma segunda revisão no estilo pedido pelo exercício e reescrever o modulo para aderir ao AGENTS.md.

## Arquivo final

- `src/functions/feedback/handler.ts`

## Evidência de uso de ferramenta

### GitHub Copilot

Prompt de reescrita usado como guia:

`Reescreva o feedback handler em TypeScript strict com Zod, pino, import estático, sem console.log e sem logar attendantEmail.`

Registro salvo em `docs/copilot-prompts.md`.

### Claude

Prompt de segunda revisão usado como guia:

`Revise o snippet original e classifique cada problema como violação do AGENTS.md, problema de segurança ou bug potencial.`

Saída consolidada salva em `docs/claude-review-3.2.md`.

## Minha revisão ANTES do Claude

| Problema identificado | Classificação | Por que é um problema |
|---|---|---|
| `await request.json() as any` | Violação do AGENTS.md + bug potencial | Ignora validação de fronteira; tipos e formatos inválidos entram no fluxo sem Zod |
| `console.log` no lugar de `pino` | Violação do AGENTS.md | Fere a convenção do projeto e piora observabilidade estruturada |
| `require('@azure/cosmos')` dentro do handler | Violação do AGENTS.md | Contraria a regra de imports estáticos e piora previsibilidade/testabilidade |
| `attendantEmail` sendo logado | Problema de segurança + violação do AGENTS.md | Vaza dado pessoal em logs com retenção ampla |
| Persistência cega dos campos do body | Bug potencial | `queryId`, `rating` e `comment` podem chegar vazios, fora de faixa ou em tipo incorreto |

## Segunda revisão com Claude

O Claude confirmou as quatro armadilhas obrigatórias e acrescentou tres observacoes operacionais:

1. ausencia de tratamento explicito para falhas de input e persistencia;
2. recriacao do `CosmosClient` a cada requisicao;
3. ausencia de validacao para `null`/`undefined` vindos do `request.json()`.

## Comparação honesta: humano vs Claude

| Ponto | Minha revisão | Revisão do Claude |
|---|---|---|
| `as any` sem Zod | Identifiquei | Confirmou |
| `console.log` | Identifiquei | Confirmou |
| `require` dinâmico | Identifiquei | Confirmou |
| Log de `attendantEmail` | Identifiquei | Confirmou |
| Falta de robustez operacional | Citei de forma genérica como persistência cega | Tornou explícitos os riscos de erro, conexão e parsing |

Conclusao: minha revisão capturou os quatro problemas críticos exigidos pelo exercício. O Claude agregou principalmente refinamento operacional e de performance.

## Reescrita final aplicada

O handler final corrige o modulo com as seguintes decisões:

1. **Validação Zod na fronteira** com `feedbackRequestSchema.strict()`.
2. **Logging com pino** e sem qualquer PII.
3. **Imports estáticos** no topo do arquivo.
4. **Sem persistir ou logar `attendantEmail`**; o dado e validado, mas o documento salvo contem apenas `queryId`, `rating`, `comment` e `receivedAt`.
5. **Handler testável** via `createFeedbackHandler(...)`, com container e logger injetáveis.
6. **Reuso de container** com cache lazily initialized, evitando reinstanciar cliente a cada chamada.

## Resultado

O codigo reescrito atende ao AGENTS.md resumido no cenário e elimina as quatro armadilhas obrigatórias sem recorrer a `any`, `console.log`, `require` dinâmico ou logs de e-mail.
