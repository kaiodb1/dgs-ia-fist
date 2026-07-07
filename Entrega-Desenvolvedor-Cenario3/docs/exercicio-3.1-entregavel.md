# Exercício 3.1 — Structured output e verificações determinísticas

## Objetivo

Substituir a resposta em texto livre por um **structured output validável** e bloquear, de forma determinística, duas classes de resposta insegura:

1. respostas sem `source_document` útil;
2. respostas sobre **devolução de carga perigosa** sem negativa explícita.

## Arquivo principal

- `src/services/response-validator.ts`

## Evidência de uso de ferramenta

### GitHub Copilot

Prompts de implementação usados como guia:

1. `Defina um schema Zod strict para { answer, source_document, confidence_score } e rejeite campos extras.`
2. `Implemente um response-validator que valide o structured output, faça log estruturado e bloqueie respostas sem fonte ou com devolução indevida de carga perigosa.`

Registro salvo em `docs/copilot-prompts.md`.

### Claude

Prompt de revisão usado como guia:

`Revise o response-validator atual, encontre pelo menos 2 problemas reais em schema/source_document/guardrails e proponha correções precisas.`

Saída consolidada salva em `docs/claude-review-3.1.md`.

## Estrutura final do validator

### Schema Zod

O schema final exportado em `assistantResponseSchema` usa `z.object(...).strict()` com os campos obrigatórios:

- `answer: string`
- `source_document: string`
- `confidence_score: number` entre `0` e `1`

Isso garante que o primeiro bloqueio seja estrutural: se o JSON vier incompleto, mal tipado ou com chaves extras inesperadas, a resposta já e rejeitada antes de qualquer regra de negocio.

### Guardrails determinísticos implementados

1. **Fonte obrigatória**  
   `source_document` precisa existir e nao pode ser placeholder semantico como `—`, `sem fonte`, `null`, `undefined`, `nao encontrado`, etc.

2. **Devolução de carga perigosa**  
   Se a resposta tratar simultaneamente de carga perigosa e devolucao, ela so passa se trouxer **negativa explicita**. Respostas permissivas ou ambiguas sao bloqueadas.

### Resposta segura padrao

Em qualquer falha, o validator:

- registra o motivo com `pino`;
- retorna `safeFallbackResponse`, com mensagem segura e `source_document: SYSTEM-GUARDRAIL`.

## Code review com Claude e correções aplicadas

| Achado confirmado pelo Claude | Impacto | Correção aplicada |
|---|---|---|
| O guardrail so reconhecia `carga perigosa` quando a expressao aparecia quase literal; parafrases como `carga classificada como perigosa` podiam passar | **Fail-open**: resposta insegura podia chegar ao usuario | O matcher foi expandido para sinonimos/parafrases e passou a avaliar janelas de texto por sentenca |
| O regex de negativa nao cobria conjugacoes comuns como `nao podemos devolver` | **Fail-closed indevido**: respostas corretas podiam ser bloqueadas | A deteccao de negativa foi generalizada com stems (`devolv*`, `pode*`) e contexto textual |
| A verificacao de `source_document` rejeitava poucos placeholders | Fonte sem utilidade pratica ainda podia passar | A lista fixa virou uma validacao baseada em padroes semanticos (`sem fonte`, `null`, `nao encontrado`, etc.) |

## Probabilístico vs determinístico

- **Probabilístico (prompt/modelo):** orientar o LLM a responder em JSON e a respeitar a politica da NovaTech.
- **Determinístico (codigo):** validar schema, rejeitar placeholders de fonte e bloquear respostas sobre devolucao de carga perigosa sem negativa explicita.

Os dois se complementam: o prompt aumenta a chance de vir correto; o codigo impede que uma resposta errada ou incompleta siga adiante.
