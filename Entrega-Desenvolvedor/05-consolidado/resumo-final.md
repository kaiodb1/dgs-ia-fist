# Resumo final da entrega — Desenvolvedor / Cenario 1

## O que foi entregue
Esta entrega cobre integralmente os exercicios **1.1, 1.2 e 1.3** do papel **Desenvolvedor**, mantendo todos os artefatos dentro da pasta separada `Entrega-Desenvolvedor\`.

## Sintese por exercicio

### Exercicio 1.1
- Analise tecnica de viabilidade com desafios por tipo de fonte, estimativa de `~8,2M` tokens, orcamento pratico de contexto e estrategia de chunking orientada por risco e tipo de pergunta.
- Evidencia de iteracao registrada em `01-exercicio-1-1\transcricao-iteracao.md`.

### Exercicio 1.2
- System prompt v1 e v2 com iteracao material.
- Mapa de contexto estatico/dinamico com estimativa de tokens.
- Testes com as 3 perguntas obrigatorias e analise da armadilha de **carga perigosa**.

### Exercicio 1.3
- Prototipo local de RAG em Python com ingestao, chunking, embeddings, ChromaDB, retrieval, montagem de prompt e CLI.
- Relatorio de testes comparado ao Anexo B: **7 cenarios executados, 6 corretos e 1 parcial**.
- Avaliacao das respostas do LLM com prompts montados pelo pipeline em `03-exercicio-1-3\avaliacao-respostas-llm.md`.
- Analise de problemas reais e correcoes propostas em `03-exercicio-1-3\analise-problemas-e-correcoes.md`.

## Resultado da avaliacao final

| Exercicio | Score | Classificacao |
|---|---:|---|
| 1.1 | 2.8 | Aprovado com distincao |
| 1.2 | 2.8 | Aprovado com distincao |
| 1.3 | 2.8 | Aprovado com distincao |

**Media geral: 2.8**  
**Classificacao geral: Aprovado com distincao**

Os detalhes das avaliacoes estao em:
- `04-avaliacao\avaliacao-exercicio-1-1.md`
- `04-avaliacao\avaliacao-exercicio-1-2.md`
- `04-avaliacao\avaliacao-exercicio-1-3.md`
- `04-avaliacao\resumo-avaliacao-final.md`

## Observacao metodologica
Nas etapas do enunciado que pediam **Claude**, foi usado o **GitHub Copilot CLI como substituto pratico**, conforme autorizacao explicita do usuario, e essa decisao foi registrada nas evidencias e nas avaliacoes.
