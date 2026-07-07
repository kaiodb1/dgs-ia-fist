## Avaliação do Exercício 1.2

### Resumo
O entregável é forte e cobre os artefatos pedidos: `system prompt` v1, mapa de contexto estático/dinâmico com estimativa de tokens, duas rodadas de teste com as 3 perguntas obrigatórias e análise crítica consolidada. O melhor ponto é a identificação explícita da armadilha de carga perigosa e a iteração material da v1 para a v2. A principal ressalva é metodológica: o exercício pedia Claude, mas os arquivos evidenciam uso de Copilot CLI como substituto, sem prova externa da aprovação dessa troca.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | `mapa-contexto-e-analise.md` mostra boa compreensão de contexto estático vs. dinâmico, orçamento de tokens, ordem de composição, poda e risco de resposta com fórmula incompleta. `system-prompt-v2.md` incorpora hierarquia de fontes, exceção antes da regra e resposta conservadora quando faltam dados. |
| D2 — Uso de Ferramentas | 2 | Há ciclo claro de gerar → testar → analisar → iterar em `transcricao-testes.md`, `system-prompt-v1.md` e `system-prompt-v2.md`, e a melhora da v2 é concreta. Porém `evidencias.md` registra uso de Copilot CLI em vez de Claude; como a ferramenta exigida não está evidenciada no entregável, a regra da Foundation limita D2 a no máximo 2. |
| D3 — Qualidade do Entregável | 3 | O pacote está completo e utilizável: inclui prompts versionados, resultados das 3 perguntas, análise das falhas e justificativa das mudanças. Outro membro do time conseguiria reaproveitar a v2 e a anatomia de contexto sem pedir esclarecimentos adicionais. |
| D4 — Pensamento Crítico | 3 | O participante não aceita a v1 de forma acrítica: em `mapa-contexto-e-analise.md` identifica a falha sutil da carga perigosa, a insuficiência de contexto para cálculo de frete e as causas-raiz do erro. Também propõe validações determinísticas fora do prompt, o que reforça julgamento próprio. |
| D5 — Aplicabilidade ao Projeto | 3 | O entregável é profundamente conectado ao caso NovaTech: cita POL/PROC/SLA, Gold 24h, Manaus/região Norte 1,8, classes 1 a 6 da ANTT e o risco operacional de misturar regra geral com exceção. Não é um prompt genérico. |

**Score do exercício: 2.8**

### Verificação de Armadilhas
- **Armadilha obrigatória — “Qual o prazo de devolução para carga perigosa?”**: **Encontrada.** Em `transcricao-testes.md` (Rodada 1, Teste 1), a v1 abre com o prazo geral de 7 dias; em `mapa-contexto-e-analise.md` (seções 3.2 e 3.3), isso é corretamente tratado como falha. A v2 corrige para **“não é elegível para devolução pelo processo padrão”** e encaminha para Gestão de Riscos.
- **Verificação obrigatória — a melhoria v1 → v2 é material?**: **Sim.** `system-prompt-v2.md` adiciona hierarquia de autoridade, precedência explícita de exceção/proibição, regra de completude para cálculos e um formato de resposta com `Limites/condições` e `Encaminhamento`. Não é uma mudança cosmética.
- **Regra de corte “v1 ≈ v2”**: **Não se aplica.** A iteração é substancial e verificável nos artefatos.

### Pontos Fortes
- Capturou a armadilha mais importante do exercício e mostrou a falha da v1 de forma explícita.
- Fez bom mapeamento de contexto estático/dinâmico com estimativa de tokens, ordem e poda.
- Melhorou o prompt para cenários de exceção e perguntas numéricas com contexto incompleto.

### Pontos de Melhoria
- Entregar evidência direta da ferramenta pedida (Claude) ou anexar a autorização explícita da substituição; no estado atual, isso fica apenas declarado em `evidencias.md`.
- Evitar mover regra de negócio potencialmente volátil para o `system prompt` estático (ex.: detalhe operacional de carga perigosa/ramal); o ideal é deixar o comportamento estático e o conteúdo documental no contexto dinâmico.
- Fortalecer a rastreabilidade com export bruto/screenshot da conversa e citação sempre granular do chunk/seção usado.

### Classificação
Aprovado com distinção

### Tópicos da Trilha para Reforço
Não aplicável pelo score. Como refinamento opcional, vale revisar separação entre guardrails estáticos e regras de negócio dinâmicas, além de práticas de evidência de uso da ferramenta exigida.
