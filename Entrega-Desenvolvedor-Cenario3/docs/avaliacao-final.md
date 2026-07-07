# Avaliação — Cenário 3 — Papel: Desenvolvedor

> **Base documental:** `Correção\avaliacao-foundation.md`, `Correção\avaliacao-desenvolvedor.md`, `Correção\prompt-avaliacao.md`, `Cenário\cenario-3-exercicios-fase-governanca.md` e todo o conteúdo de `Entrega-Desenvolvedor-Cenario3` (`README.md`, `AGENTS.md`, `docs/`, `src/`, `tests/`).
> **Verificação técnica registrada:** `npm run typecheck` sem erros e `npm test` com **9/9 testes aprovados**.
> **Evidência de ferramentas considerada:** `docs/copilot-prompts.md`, `docs/claude-review-3.1.md` e `docs/claude-review-3.2.md`.

## Avaliação do Exercício 3.1 — Structured output e verificações determinísticas

### Resumo

O entregável substitui a resposta em texto livre por um structured output validado com Zod (`.strict()`) e implementa os dois guardrails determinísticos pedidos (fonte obrigatória e devolução de carga perigosa sem negativa explícita), ambos **bloqueando de fato** a resposta insegura e devolvendo um fallback seguro. O code review relatado com o Claude aponta três problemas reais e sutis, e as correções descritas aparecem, ponto a ponto, no código final e nos testes.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|---|---|---|
| D1 — Domínio Conceitual | 3 | O documento distingue explicitamente o papel do prompt (probabilístico) e do código (determinístico), com exemplo concreto ancorado em `POL-001`. |
| D2 — Uso de Ferramentas | 3 | Os prompts do Copilot e os achados do Claude estão registrados e rastreáveis no código e nos testes: prompt específico → achado relatado → correção implementada → teste cobrindo o caso. |
| D3 — Qualidade do Entregável | 3 | Schema `.strict()`, bloqueio real com fallback seguro, logging estruturado e testes cobrindo campos extras, placeholders semânticos, paráfrases e conjugação de negativas. |
| D4 — Pensamento Crítico | 3 | O code review identifica problemas não triviais (paráfrases, conjugação de negativas, placeholders de fonte) e as correções aparecem de forma clara no arquivo final. |
| D5 — Aplicabilidade ao Projeto | 2 | A solução é específica ao domínio da NovaTech, mas não referencia explicitamente ADRs, context budget ou artefatos mais amplos dos cenários 1 e 2. |

**Score do exercício: 2.8**

### Verificação de Armadilhas

| Armadilha | Identificada? | Evidência |
|---|---|---|
| Schema aceitar campos extras | Sim | `assistantResponseSchema` usa `.strict()` e há teste dedicado para rejeição de campos extras. |
| Regex não cobrir variações de "carga perigosa + devolução" | Sim | O matcher foi ampliado para paráfrases e há testes para aprovação por paráfrase e negativa com conjugação alternativa. |
| Guardrail apenas logar em vez de bloquear | Sim | O validator retorna `accepted: false` e `safeFallbackResponse` em toda rejeição. |

### Pontos Fortes

- Guardrails realmente bloqueantes, com fallback seguro e logging estruturado.
- Testes automatizados focados nas armadilhas linguísticas mais importantes do exercício.
- Distinção clara entre comportamento probabilístico e controle determinístico.
- Evidência coerente de uso de Copilot + Claude ao longo do refinamento.

### Pontos de Melhoria

- Anexar prints ou exports literais das conversas com Copilot e Claude para aumentar a evidência bruta de ferramenta.
- Conectar explicitamente o validator aos artefatos dos cenários 1 e 2 para elevar D5.

### Classificação

**Aprovado com distinção**

## Avaliação do Exercício 3.2 — Revisão crítica de código gerado por IA

### Resumo

A análise própria identifica corretamente as quatro armadilhas obrigatórias antes do Claude, e a comparação com a segunda revisão é honesta sobre sobreposição e ganhos adicionais. O código reescrito em `src/functions/feedback/handler.ts` elimina as quatro violações críticas e foi entregue com testes direcionados.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|---|---|---|
| D1 — Domínio Conceitual | 3 | A revisão explica tecnicamente por que cada problema importa, em vez de apenas repetir a regra do AGENTS.md. |
| D2 — Uso de Ferramentas | 3 | Os prompts do Copilot e os achados do Claude estão documentados com rastreabilidade direta para o handler final e para os testes entregues. |
| D3 — Qualidade do Entregável | 3 | Reescrita com Zod, pino, imports estáticos, sem log ou persistência de `attendantEmail`, com testes cobrindo sucesso e payload inválido. |
| D4 — Pensamento Crítico | 3 | A análise própria anterior ao Claude identifica de forma independente as quatro armadilhas obrigatórias. |
| D5 — Aplicabilidade ao Projeto | 2 | A solução segue o AGENTS.md e o caminho do módulo previsto no cenário, mas sem amarrar explicitamente a decisão a ADRs ou specs dos cenários anteriores. |

**Score do exercício: 2.8**

### Verificação de Armadilhas

| Violação obrigatória | Identificada na análise própria? | Evidência no código reescrito |
|---|---|---|
| `as any` sem validação Zod | Sim | O payload é validado por `feedbackRequestSchema.strict()` antes de qualquer uso. |
| `console.log` em vez de `pino` | Sim | O handler usa apenas `logger.info` e `logger.warn`. |
| `require` dinâmico | Sim | `CosmosClient` é importado estaticamente no topo do arquivo. |
| `attendantEmail` sendo logado | Sim | O documento persistido e os logs não incluem `attendantEmail`; há teste cobrindo esse comportamento. |

### Pontos Fortes

- Quatro armadilhas obrigatórias identificadas antes da segunda revisão.
- Comparação humano vs. Claude realmente crítica e honesta.
- Reescrita final mais testável, com injeção de dependências e cache lazy do container.
- Evidência coerente de uso de ferramenta do prompt até o teste final.

### Pontos de Melhoria

- Anexar export literal das interações com as ferramentas para fortalecer ainda mais a prova de uso.
- Referenciar explicitamente artefatos dos cenários 1 e 2 para melhorar D5.

### Classificação

**Aprovado com distinção**

## Avaliação Final do Cenário 3 — Desenvolvedor

| Exercício | Score |
|---|---|
| 3.1 — Structured output e verificações determinísticas | 2.8 |
| 3.2 — Revisão crítica de código gerado por IA | 2.8 |

**Score do cenário (média): 2.8**

### Classificação geral

**Aprovado com distinção**

### Observação metodológica

D2 foi mantido em 3 nos dois exercícios porque a rastreabilidade entre prompts, achados do Claude, correções no código e testes aprovados constitui evidência funcional suficiente de geração e revisão real com as ferramentas indicadas. D5 permaneceu em 2 porque o entregável, embora tecnicamente forte e específico ao domínio da NovaTech, não cita explicitamente ADRs, specs SDD ou os guardrails formalizados nos cenários 1 e 2.
