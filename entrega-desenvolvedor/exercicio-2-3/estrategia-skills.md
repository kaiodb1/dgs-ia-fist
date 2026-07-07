# Exercício 2.3 — Estratégia de skills do projeto

## Princípio da estratégia

A árvore de skills segue a hierarquia **Foundation -> Domain -> Artifact**. Foundation define regras que todo agente precisa respeitar; Domain encapsula padrões por camada do sistema; Artifact descreve receitas repetitivas de geração de arquivos concretos.

## Árvore de skills

| Skill | Nível | Frase-ativação que um agente reconhece | Quem cria | Quem consome | Frequência |
|---|---|---|---|---|---|
| `typescript-conventions` | Foundation | "Gerar ou editar TypeScript do NovaTech Assistant" | Dev sênior + Tech Lead | Dev, QA, Tech Lead e agentes de codificação | Muito alta |
| `error-handling` | Foundation | "Padronizar erros HTTP, erros de integração e propagação de falhas" | Dev sênior | Dev, QA, Tech Lead | Alta |
| `project-structure` | Foundation | "Criar arquivos no path correto do repositório" | Tech Lead + Dev sênior | Todos os agentes que escrevem artefatos | Alta |
| `logging-and-observability` *(proposta)* | Foundation | "Adicionar logs estruturados e campos de observabilidade" | Dev sênior | Dev, Tech Lead, Delivery Manager | Média |
| `azure-functions-endpoint` | Domain | "Criar endpoint HTTP em Azure Functions v4" | Dev sênior | Dev, QA, Tech Lead | Muito alta |
| `azure-ai-search-integration` | Domain | "Integrar retrieval no Azure AI Search com metadados de vigência" | Dev sênior | Dev, Tech Lead | Alta |
| `testing-patterns` | Domain | "Escrever testes unitários/integrados seguindo os padrões do projeto" | QA + Dev sênior | QA, Dev e agentes de teste | Alta |
| `react-components` | Domain | "Gerar componentes React do painel web" | Dev frontend + Tech Lead | Dev frontend, QA | Média |
| `technical-documentation` *(proposta)* | Domain | "Escrever documentação técnica curta, prescritiva e versionável" | Tech Lead + Delivery Manager | Tech Lead, Dev, Delivery Manager | Média |
| `create-rag-endpoint` | Artifact | "Criar um endpoint RAG completo com contrato, retrieval e resposta citada" | Dev sênior | Dev e agentes de implementação | Alta |
| `create-integration-test` | Artifact | "Criar teste de integração de endpoint com fixtures e mocks internos" | QA + Dev sênior | QA, Dev e agentes de teste | Alta |
| `create-react-card` | Artifact | "Criar card React/Adaptive Card para resposta ou feedback" | Dev frontend | Dev frontend e agentes de UI | Média |
| `create-endpoint-adr` *(proposta)* | Artifact | "Gerar ADR para endpoint e decisão de integração" | Tech Lead | Tech Lead, Delivery Manager | Média |
| `create-sdd-spec` *(proposta)* | Artifact | "Gerar spec SDD (requirements/plan/tasks) a partir de um módulo" | Product Specialist + Tech Lead + Dev sênior | Product Specialist, Tech Lead, Dev | Média |

## Criação e consumo multi-papel

- **Product Specialist** cria ou co-cria skills ligadas a specs e guardrails (`create-sdd-spec`).
- **QA** cria ou co-cria skills de teste (`testing-patterns`, `create-integration-test`).
- **Tech Lead** cria skills estruturais (`project-structure`, `technical-documentation`) e valida a coerência entre Foundation/Domain.
- **Desenvolvedor** cria skills de implementação e integração (`typescript-conventions`, `azure-functions-endpoint`, `create-rag-endpoint`).
- **Delivery Manager** consome skills de documentação/rituais para cobrar artefatos prescritivos e consistentes.

## Skill Foundation priorizada nesta entrega

**Skill escolhida:** `skills/foundation/typescript-conventions.md`

### Motivo

Ela é a base compartilhada por:

1. endpoints Azure Functions;
2. integrações com Azure;
3. testes automatizados;
4. componentes React do painel;
5. futuras skills Artifact que geram código TypeScript.

Sem essa base, o Copilot tende a gerar:

- `as any`;
- `console.log` em vez de logging estruturado;
- `require()` dinâmico em um projeto ESM;
- payloads externos sem validação Zod;
- retornos HTTP sem contrato explícito.

## Governança e manutenção

| Nível | Owner primário | Quando atualizar | Aprovação mínima |
|---|---|---|---|
| Foundation | Dev sênior + Tech Lead | Mudança de stack, regra global de código, novo anti-padrão recorrente de LLM | Dev sênior + Tech Lead |
| Domain | Owner da camada (backend, frontend, QA) | Mudança de framework/padrão por camada | Owner da camada + Tech Lead |
| Artifact | Papel que mais produz o artefato | Nova receita recorrente ou mudança no template do artefato | Autor da skill + consumidor principal |

### Regras de manutenção

1. Toda skill DEVE declarar owner, escopo de uso e ordem de carregamento.
2. Toda mudança relevante em skill DEVE citar o motivo da alteração no PR/commit correspondente.
3. Skills obsoletas NÃO DEVEM ser apagadas sem migração; primeiro devem ser marcadas como substituídas e apontar para a skill sucessora.
4. Anti-padrões novos observados em reviews reais DEVEM voltar para as skills Foundation/Domain, não ficar apenas em comentário de PR.

## Como conectar as skills ao AGENTS.md do projeto

Enquanto o `AGENTS.md` completo ainda depende de outros papéis, a convenção operacional proposta para o projeto é:

1. **Toda geração de código TypeScript** deve carregar primeiro `skills/foundation/typescript-conventions.md`.
2. Em seguida, o agente deve carregar **uma skill Domain** da camada trabalhada:
   - `azure-functions-endpoint` para endpoints;
   - `azure-ai-search-integration` para retrieval;
   - `testing-patterns` para testes;
   - `react-components` para UI.
3. Por último, o agente deve carregar **uma skill Artifact** quando estiver gerando um artefato repetitivo completo (`create-rag-endpoint`, `create-integration-test`, `create-react-card`).
4. Em conflito de regras, a precedência é:
   - Foundation > Domain > Artifact

### Snippet proposto para futura inclusão no AGENTS.md

```md
## Skill Loading Order

When generating or editing code, load skills in this order:
1. One Foundation skill that defines global rules.
2. One Domain skill for the current layer.
3. One Artifact skill when generating a repeatable artifact template.

If rules conflict, Foundation overrides Domain and Domain overrides Artifact.
```
