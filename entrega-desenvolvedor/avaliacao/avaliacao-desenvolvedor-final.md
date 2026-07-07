## Avaliação do Exercício 2.1

### Resumo
A entrega está forte e demonstra execução real dos MCP servers no estado atual do repositório. O mapeamento em `deliverables/desenvolvedor/exercicio-2-1/mapeamento-e-riscos-mcp.md`, a configuração em `.mcp/mcp.json` e a evidência reproduzível em `deliverables/desenvolvedor/evidencias/mcp/` atendem bem ao núcleo do exercício.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | O mapeamento distingue corretamente necessidades, servers, escopo e natureza de tools/resources/prompts para `filesystem`, `git`, `memory` e `everything` em `deliverables/desenvolvedor/exercicio-2-1/mapeamento-e-riscos-mcp.md`. |
| D2 — Uso de Ferramentas | 3 | Há evidência real e reproduzível: `deliverables/desenvolvedor/evidencias/mcp/run-mcp-evidence.mjs` conecta via SDK oficial aos servers; `mcp-evidence.json`/`mcp-evidence.md` mostram leitura de `docs/novatech`, recuperação de chunk do corpus e leitura de histórico Git; `registro-de-execucao.md` documenta a iteração da tentativa manual para o SDK. |
| D3 — Qualidade do Entregável | 2 | `.mcp/mcp.json` é válido e coerente, mas os servers `filesystem-docs` e `filesystem-corpus` ainda expõem tools de escrita segundo `deliverables/desenvolvedor/evidencias/mcp/mcp-evidence.md`; o “read-only” depende de ACL local via `set-readonly-sources.ps1` e logs, não de uma restrição autoexplicativa na configuração MCP. |
| D4 — Pensamento Crítico | 3 | A análise de riscos é específica ao contexto local: exposição de segredos por escopo amplo, alteração indevida de corpus/documentação, vazamento via histórico Git e obsolescência da memória, com mitigação acionável no próprio mapeamento. |
| D5 — Aplicabilidade ao Projeto | 3 | A entrega está profundamente ancorada no starter repo e no domínio NovaTech: usa `docs/novatech`, `data/retrieval-corpus`, `.git` local e a estrutura real do repositório descrita em `README.md`. |

**Score do exercício: 2.8**

### Verificação de Artefatos Machine-Readable
`.mcp/mcp.json` é consumível por ferramenta e a evidência em `mcp-evidence.json` é especialmente boa por ser estruturada. O ponto fraco é que o caráter read-only de `docs/novatech` e `data/retrieval-corpus` não está codificado no artefato MCP em si; ele depende de endurecimento externo (`set-readonly-sources.ps1`, `readonly-setup.log`, `readonly-write-check.log`).

### Pontos Fortes
- Evidência real, reproduzível e em formato humano + JSON (`mcp-evidence.md` e `mcp-evidence.json`).
- Least privilege bem melhor que o scaffold padrão: workspace separado de docs, corpus e Git.
- Riscos locais bem contextualizados, sem generalidades vagas.

### Pontos de Melhoria
- Tornar a restrição de leitura mais autoevidente para agentes, reduzindo dependência de ACL externa.
- Explicitar no artefato/evidência como o cliente deve evitar tools de escrita nos servers de docs/corpus.
- Se possível, registrar também uma evidência de falha de escrita disparada via MCP, não só via sistema de arquivos.

### Classificação
Aprovado com distinção

### Tópicos da Trilha para Reforço
- MCP: estratégias de hardening e prescritividade machine-readable para permissões.

---

## Avaliação do Exercício 2.2

### Resumo
A entrega atual está consistente e funcional. `specs/query-endpoint/tasks.md`, o código em `src/functions/query/` e a revisão crítica em `deliverables/desenvolvedor/exercicio-2-2/revisao-critica-copilot.md` mostram boa decomposição SDD e implementação aderente à stack proposta.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | `specs/query-endpoint/tasks.md` traz tasks atômicas com ID, dependências, critérios de aceite e estimativa; `validator.ts`, `handler.ts` e `response-builder.ts` seguem TypeScript + Zod + Azure Functions v4 + pino, em linha com `specs/query-endpoint/plan.md`. |
| D2 — Uso de Ferramentas | 2 | Há evidência plausível de uso real do Copilot CLI em `deliverables/desenvolvedor/evidencias/copilot/registro-de-execucao.md` e revisão posterior em `revisao-critica-copilot.md`, mas a trilha de geração/reescrita não está tão granular nem tão reproduzível quanto no exercício 2.1. |
| D3 — Qualidade do Entregável | 3 | O entregável está completo e verificável: os arquivos estão nos paths corretos (`src/functions/query/`, `tests/unit/functions/query/`), e no estado atual `test`, `build` e `lint` definidos em `package.json` passam. |
| D4 — Pensamento Crítico | 3 | A revisão crítica aponta dois defeitos reais já corrigidos (formato do `HttpRequest` no teste e `HttpMethod[]` no registro) e dois riscos críveis para produção (payload/correlation id e crescimento indevido do handler). |
| D5 — Aplicabilidade ao Projeto | 2 | A entrega referencia bem ADR-0002, ADR-0003 e `prompts/system-prompt.md` em `requirements.md`, `plan.md` e `tasks.md`, mas não explicita tão claramente a continuidade do protótipo open-source do cenário 1 mencionada no critério específico do papel. |

**Score do exercício: 2.6**

### Verificação de Artefatos Machine-Readable
`tasks.md` é prescritivo o suficiente para um agente executar: cada item tem dependências e critérios verificáveis. O código também é consumível por tooling real; `tests/unit/functions/query/handler.test.ts` e os scripts de `package.json` tornam a entrega objetiva e executável.

### Pontos Fortes
- Boa decomposição SDD, sem tasks infladas ou vagas.
- Código enxuto e alinhado à stack do plano.
- Revisão crítica honesta, ancorada em falhas reais observadas durante build/teste.

### Pontos de Melhoria
- Preservar evidência mais direta da iteração com Copilot (prompt, output inicial e ajuste aplicado).
- Explicitar melhor a ponte com o protótipo do cenário 1, além das ADRs.
- Antecipar no plano de próximas tasks itens de robustez operacional (payload limit, correlation id, serviço de aplicação).

### Classificação
Aprovado com distinção

### Tópicos da Trilha para Reforço
- SDD: rastreabilidade entre geração do agente e revisão humana.
- Conexão entre cenário 1 e endurecimento de produção.

---

## Avaliação do Exercício 2.3

### Resumo
A estratégia está bem pensada e útil para o projeto real. `deliverables/desenvolvedor/exercicio-2-3/estrategia-skills.md` tem boa visão multi-papel, e `skills/foundation/typescript-conventions.md` é prescritiva, concreta e relevante para Copilot.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | A hierarquia Foundation → Domain → Artifact está correta e aplicada a necessidades reais do projeto (RAG endpoint, testes, React, documentação, specs). |
| D2 — Uso de Ferramentas | 2 | `deliverables/desenvolvedor/evidencias/copilot/registro-de-execucao.md` registra o uso do Copilot CLI para produzir a skill, mas sem trilha mais detalhada de prompt/saída/iteração. |
| D3 — Qualidade do Entregável | 2 | O conteúdo de `skills/foundation/typescript-conventions.md` é forte, porém a entrega não segue literalmente a convenção pedida de um `SKILL.md`; para um agente, o conteúdo é bom, mas a embalagem/descoberta do artefato ficou menos padronizada do que o enunciado sugere. |
| D4 — Pensamento Crítico | 3 | A skill Foundation traz anti-padrões úteis e realistas de LLM (`as any`, `console.log`, `require()` dinâmico, fallback silencioso), além de precedência entre camadas e gatilhos de atualização. |
| D5 — Aplicabilidade ao Projeto | 3 | A árvore proposta conversa diretamente com a estrutura real (`skills/foundation`, `skills/domain`, `skills/artifact`) e com artefatos recorrentes do NovaTech Assistant. |

**Score do exercício: 2.6**

### Verificação de Artefatos Machine-Readable
O arquivo `skills/foundation/typescript-conventions.md` é majoritariamente prescritivo: usa “DEVE/NÃO DEVE”, exemplos DO/DON'T, anti-padrões e ordem de carregamento. O principal gap machine-readable é de convenção de empacotamento: o conteúdo parece um bom SKILL, mas não está apresentado como `SKILL.md`.

### Pontos Fortes
- Estratégia coerente com o fluxo real do projeto e com múltiplos papéis.
- Skill Foundation concreta, com exemplos de código úteis.
- Boa definição de governança e precedência entre Foundation/Domain/Artifact.

### Pontos de Melhoria
- Materializar a skill no formato/convenção literal de `SKILL.md`.
- Acrescentar evidência mais direta da iteração com Copilot para a criação da skill.
- Evoluir da estratégia para um pequeno conjunto inicial materializado de skills Domain/Artifact prioritárias.

### Classificação
Aprovado com distinção

### Tópicos da Trilha para Reforço
- Skills: empacotamento e convenções de descoberta por agentes.
- Evidência de teste/iteração de artefatos gerados por IA.

---

## Veredito Consolidado

No estado atual em disco, o entregável do papel Desenvolvedor para o Cenário 2 está **aprovado com distinção**. Considerei válidas as evidências em Copilot CLI (`deliverables/desenvolvedor/evidencias/copilot/registro-de-execucao.md` e `deliverables/desenvolvedor/evidencias/mcp/`) sem exigir material separado do Claude; os principais gaps restantes são **prescritividade machine-readable mais forte no empacotamento da skill** e **trilha mais granular da iteração com Copilot**.
