# Transcricao de iteracao - Copilot CLI como substituto pratico do Claude

## Contexto
O exercicio pedia evidencia de iteracao com Claude. Como houve autorizacao explicita para usar o **GitHub Copilot CLI** como substituto pratico, a iteracao abaixo foi feita no proprio Copilot CLI em duas passadas: **rascunho inicial** e **revisao critica orientada pela rubrica**.

---

## 1) Prompt inicial / pedido de rascunho

> **Prompt usado (resumido fielmente):**
>
> "Com base no cenario da NovaTech, escreva uma analise tecnica inicial de viabilidade para o assistente RAG. Cubra PDFs com tabelas, PDFs escaneados, wiki com links/macros e planilhas com formulas. Para cada tipo, explique desafio de ingestao/RAG, impacto na qualidade da resposta e mitigacao. Estime tokens para ~800 PDFs de 10 paginas, ~400 paginas wiki de 1.500 palavras e ~50 planilhas usando ~0,75 palavras por token. Analise o orcamento de contexto do GPT-4o 128K com ~2K reservados para sistema e chunks de ~500 tokens. Recomende uma estrategia de chunking."

---

## 2) Resultado do rascunho v1 (resumo)

O rascunho v1:
- cobriu os 4 tipos de fonte pedidos;
- reconheceu os riscos basicos de OCR, perda de estrutura em tabelas, macros da wiki e formulas em planilhas;
- calculou corretamente `128K - 2K = 126K` e `126K / 500 = 252 chunks`;
- estimou a base em **~6,63 milhoes de tokens**;
- recomendou **10 a 12 chunks** por pergunta;
- sugeriu chunking "por secao logica / por linhas / por aba", ainda de forma generica.

---

## 3) Fraquezas percebidas no v1

| Fraqueza do v1 | Por que isso era um problema para a rubrica |
|---|---|
| Estimativa de volume em **~6,63M tokens** | Ficou defensavel matematicamente, mas **otimista demais** para o esperado do exercicio. Nao considerava direito a inflacao causada por tabelas serializadas, OCR e planilhas com formula. |
| Recomendacao de **10-12 chunks** | A rubrica pede entendimento de que o uso pratico costuma ficar em algo como **5-10 chunks**, nao perto do teto. |
| Chunking muito generico | "Por secao logica" e "por linhas" ainda funcionaria para qualquer projeto; faltava amarracao com perguntas reais da NovaTech. |
| Pouca especificidade de dominio | O v1 quase nao usava os casos criticos da base: **PROC-042 vs PROC-042-v2**, **FAQ informal**, "**carga perigosa**", tiers e planilha de frete mensal. |
| Planilhas tratadas so como "texto estruturado" | Para a NovaTech isso e fraco: a pergunta de frete pode depender de formula e snapshot mensal; retrieval puro pode nao bastar. |
| Autoridade/vigencia pouco tratadas | Sem metadados de versao e autoridade, o assistente pode misturar procedimento antigo, revisao nova e FAQ informal na mesma resposta. |

---

## 4) Prompt de auto-revisao enviado ao Copilot CLI

> **Prompt usado na revisao (resumido fielmente):**
>
> "Revise criticamente o rascunho abaixo contra os requisitos do exercicio 1.1 do papel Desenvolvedor e contra a rubrica. Aponte fraquezas concretas, onde ele ainda esta generico ou pouco especifico a NovaTech, se alguma estimativa parece otimista/pouco sustentada e quais melhorias fariam o entregavel atingir score 3. Considere explicitamente: PROC-042 vs PROC-042-v2, FAQ informal nao validado, devolucao de carga perigosa, atualizacao mensal por areas diferentes, stack com SharePoint/Teams e Azure AI Services, alem da expectativa de 5-10 chunks praticos."

---

## 5) Achados da revisao

A revisao do Copilot CLI apontou, em essencia:

- **"Ainda nao atinge score 3."**
- A analise estava **pouco especifica a NovaTech**.
- A estimativa de **6,63M tokens** parecia **otimista e pouco sustentada**.
- O texto nao tratava com forca suficiente o problema de **contradicao/versionamento**.
- A recomendacao de **10-12 chunks** precisava cair para um intervalo mais aderente a pratica.
- O chunking ainda estava generico e nao cobria bem perguntas de **regra + excecao**.
- Faltava citar o stack ja disponivel na empresa (principalmente **Azure** e **SharePoint**) como parte da mitigacao.

Trechos-chave da revisao:

> "Estimativa de tokens parece otimista/pouco sustentada."

> "Para score 3, a analise deveria defender algo na ordem de 8-15M tokens."

> "Chunking ainda esta generico."

> "Faltou justificar por tipo de pergunta e pelo risco de lost in the middle."

> "Adicionar mitigacao de conflito/autoridade: priorizar documento aprovado/mais recente, rebaixar FAQ informal, e sinalizar conflito quando coexistirem versoes."

---

## 6) Melhorias incorporadas na versao final

| Melhoria incorporada | Como entrou no documento final |
|---|---|
| Reestimar o volume total da base | A conta foi refeita para **~8,2 milhoes de tokens**, com premissas explicitas para PDFs, wiki e planilhas. |
| Tornar a analise especifica da NovaTech | O texto final usa exemplos concretos: **POL-001**, **PROC-042 / PROC-042-v2**, **SLA-2024**, **FAQ-Atendimento** e `frete-base-AAAAMM.xlsx`. |
| Tratar conflito de versoes como decisao transversal | Foi criada uma secao especifica de **autoridade, vigencia e conflito de versoes**, com regra pratica de priorizacao e exposicao de divergencia. |
| Ajustar o orcamento de contexto para pratica real | A recomendacao final passou a ser **5-8 chunks** na maioria das perguntas e **ate 10** em casos multi-documento. |
| Justificar chunking por tipo de pergunta | O documento final mostra por que perguntas como "prazo de devolucao", "carga perigosa" e "frete para 600kg em Manaus" exigem chunking diferente. |
| Endurecer o tratamento de planilhas | A conclusao passou a dizer explicitamente que, para valores de frete, o ideal e **RAG + camada deterministica de calculo**, nao so embeddings. |
| Conectar mitigacao ao stack disponivel | A extracao de PDFs passou a recomendar **Azure Document Intelligence**, coerente com o contexto de Azure ja aceito pela NovaTech. |

---

## 7) Resultado da iteracao

A principal diferenca entre v1 e a versao final e que o texto deixou de ser uma analise "correta, mas generica" e passou a ser uma analise **acionavel para a NovaTech**. A revisao ajudou a fortalecer exatamente os pontos que a rubrica valoriza mais:
- especificidade de dominio;
- calculo de volume defensavel;
- gestao pratica do orcamento de contexto;
- chunking orientado por pergunta e por risco de interpretacao;
- e governanca de autoridade/versionamento.

