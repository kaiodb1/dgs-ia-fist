# Resumo da avaliacao final — Papel Desenvolvedor

## Resultado consolidado

| Exercicio | Score | Classificacao | Arquivo |
|---|---:|---|---|
| 1.1 — Analise de viabilidade tecnica | 2.8 | Aprovado com distincao | `avaliacao-exercicio-1-1.md` |
| 1.2 — Prototipacao de prompt | 2.8 | Aprovado com distincao | `avaliacao-exercicio-1-2.md` |
| 1.3 — Pipeline de RAG | 2.8 | Aprovado com distincao | `avaliacao-exercicio-1-3.md` |

**Media geral dos 3 exercicios: 2.8**  
**Classificacao geral: Aprovado com distincao**

## Leitura consolidada
O conjunto da entrega ficou forte e coerente com o cenario da NovaTech. Os tres exercicios demonstram:
- dominio conceitual consistente sobre **engenharia de contexto** e **RAG**;
- boa capacidade de **iterar criticamente** em vez de aceitar o primeiro output;
- forte ancoragem no dominio, com referencias concretas a `POL-001`, `PROC-042`, `PROC-042-v2`, `SLA-2024` e `FAQ-Atendimento`.

O ponto mais forte do pacote e o exercicio 1.3, porque ele vai alem da analise textual e entrega um **pipeline real e executavel**, com testes comparados ao Anexo B e problemas concretos derivados da execucao.

## Pontos fortes recorrentes
1. **Especificidade ao contexto NovaTech** em vez de respostas genericas.
2. **Pensamento critico** visivel, especialmente na identificacao de conflito entre versoes, FAQ informal e falta de cobertura documental.
3. **Completude dos artefatos**, com entregaveis bem organizados por exercicio.

## Pontos de melhoria recorrentes
1. **Evidencia de ferramenta**: as avaliacoes reconheceram que a documentacao do uso do Copilot CLI ficou boa, mas sem transcript bruto ou prova primaria equivalente ao uso do Claude pedido no enunciado.
2. **Cobertura adicional de armadilhas**: no exercicio 1.3, ainda valeria testar explicitamente cenarios como `cliente Platinum` e perguntas multi-dominio.
3. **Guardrails determinísticos**: a estrategia de prompt esta boa, mas a implementacao ainda se beneficiaria de filtros mais fortes para versao vigente, no-answer e prioridade de fonte.

## Arquivos de referencia
- `avaliacao-exercicio-1-1.md`
- `avaliacao-exercicio-1-2.md`
- `avaliacao-exercicio-1-3.md`
- `enunciado-desenvolvedor-cenario-1.md`
- `insumos\cenario-1-avaliacao-foundation.md`
- `insumos\cenario-1-avaliacao-desenvolvedor.md`
- `insumos\cenario-1-prompt-avaliacao.md`
