## Avaliação do Exercício 1.3

### Resumo
O entregável é forte e majoritariamente completo. O código implementa ingestão, chunking, embeddings, retrieval, montagem de prompt e validação por cenários; na validação do avaliador, `python .\run.py run-tests --reuse-index` retornou 7 cenários (6 corretos, 1 parcial) e uma ingestão isolada reindexou 5 documentos em 34 chunks. O ponto que mais segura a nota máxima está na evidência de ferramenta: há boa narrativa de uso/iteração do Copilot, mas sem transcript bruto de completions nem conversa do Claude.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | O participante demonstra domínio real de RAG como pipeline de engenharia: chunking sensível a seções/tabelas/listas (`README.md`, `src\rag_prototype\chunking.py`), reranqueamento híbrido e tratamento explícito de autoridade de fonte e conflito entre versões (`src\rag_prototype\pipeline.py`). Não ficou dependente de abstração opaca de framework e conectou o desenho aos riscos do corpus NovaTech. |
| D2 — Uso de Ferramentas | 2 | Há evidência de uso do GitHub Copilot com iteração real em `evidencias-copilot.md` (resultado antes/depois e prompt principal) e de uso do pipeline nos artefatos gerados. Porém a evidência é indireta: faltam transcripts/completions brutos do Copilot e a etapa de avaliação do LLM foi documentada com Copilot CLI como substituto prático do Claude, o que reduz a força da comprovação. |
| D3 — Qualidade do Entregável | 3 | O entregável é utilizável: contém código executável (`run.py`, `src\rag_prototype\cli.py`, `pipeline.py`), README operacional, relatório de testes, avaliação das respostas do LLM e análise de problemas. A validação do avaliador confirmou pipeline funcional tanto em retrieval (`run-tests --reuse-index`: 6 corretos, 1 parcial) quanto em ingestão isolada (5 documentos, 34 chunks). |
| D4 — Pensamento Crítico | 3 | O participante não aceitou o output de forma acrítica. `analise-problemas-e-correcoes.md` documenta 3 problemas reais extraídos dos testes (mistura v1/v2, ausência de abstenção forte e FAQ superando fonte normativa), e `avaliacao-respostas-llm.md` discute conflito entre fontes, limites de cobertura e prudência nas respostas. |
| D5 — Aplicabilidade ao Projeto | 3 | O protótipo está profundamente ancorado no contexto NovaTech: IDs reais do Anexo B, distinção entre POL/PROC/SLA/FAQ, conflito PROC-042 vs PROC-042-v2, caso de Manaus/Norte, tiers Gold/Silver/Standard e perguntas sem cobertura formal. Não é um artefato genérico. |

**Score do exercício: 2.8**

### Verificações obrigatórias do exercício
- Pipeline funcional: **Sim.** O código executa ingestão, retrieval e montagem de prompt. Validação do avaliador: `python .\run.py run-tests --reuse-index` => 7 cenários, 6 corretos, 1 parcial; ingestão isolada em `04-avaliacao` => 5 documentos, 34 chunks, com `SLA-2024-B` em rank 1 para “Qual o SLA do cliente Gold?”.
- Chunking justificado: **Sim.** O `README.md` e `src\rag_prototype\chunking.py` explicam chunking por seção, preservação de tabelas/listas e split temático da tabela de SLA.
- Testes comparados ao Anexo B: **Sim.** `src\rag_prototype\scenarios.py` e `resultados-testes.md` confrontam os chunks recuperados com o mapa/gabarito do Anexo B.
- 2+ problemas reais identificados: **Sim.** `analise-problemas-e-correcoes.md` documenta 3 problemas observados nos testes (conflito v1/v2, ausência de abstenção forte e FAQ superando fonte normativa).
- Uso de Copilot evidenciado: **Sim, mas de forma indireta.** `evidencias-copilot.md` descreve prompt, arquivos gerados e duas iterações com métricas antes/depois; faltam transcripts brutos ou prints de completions.

### Verificação de Armadilhas
- **Contradição PROC-042 vs PROC-042-v2:** identificada. O entregável mostra a recuperação simultânea das duas versões e trata isso como risco real.
- **FAQ como fonte para informação crítica:** identificada. O participante registra o risco de FAQ superar fonte normativa em perguntas sensíveis.
- **Tier inexistente (Platinum):** não verificado explicitamente. O caso existe no Anexo B, mas não entrou na bateria executada.
- **Inversão de regra em carga perigosa:** identificada e evitada. O cenário “Posso devolver carga perigosa?” foi testado e a resposta final respeita o POL-001-B.
- **Pergunta sem cobertura (< 500kg):** identificada. O cenário de 300kg para Salvador foi tratado como caso de cobertura insuficiente e virou problema real documentado.

### Pontos Fortes
- Pipeline real, legível e manual, sem depender de abstrações excessivas: ingestão, chunking, rerank híbrido, prompt builder e CLI.
- Chunking bem pensado para o corpus: preserva tabelas, listas e faz split semântico da tabela de SLA, o que melhora a recuperação tabular.
- Boa postura crítica: os problemas levantados saem dos testes reais e geram correções concretas, não inventadas.

### Pontos de Melhoria
- Anexar evidência bruta do uso do Copilot/Claude (prints, transcript ou export de conversa), não apenas narrativa resumida.
- Incluir explicitamente mais armadilhas do Anexo B na bateria, sobretudo “cliente Platinum” e o cenário multi-domínio.
- Endurecer o pré-prompt com deduplicação por família/versionamento e regra de abstenção para perguntas fora da cobertura documental.

### Classificação
Aprovado com distinção

### Tópicos da Trilha para Reforço
Sem reforço prioritário. Como evolução, vale aprofundar evidência auditável de uso de ferramenta e técnicas de abstenção/versionamento em RAG.
