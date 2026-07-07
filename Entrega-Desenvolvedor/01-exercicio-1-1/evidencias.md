# Evidencias de aderencia a rubrica - Exercicio 1.1 (Desenvolvedor)

## Arquivos entregues
- `analise-tecnica-final.md`
- `transcricao-iteracao.md`
- `evidencias.md`

## Cobertura dos criterios da rubrica

| Criterio avaliado | Evidencia no entregavel |
|---|---|
| **Desafios por tipo de fonte** | `analise-tecnica-final.md`, secao **1. Desafios por tipo de fonte**: cobre PDFs com tabelas complexas, PDFs escaneados, wiki com links/macros e planilhas com formulas; para cada um ha **desafio + impacto + mitigacao**. |
| **Estimativa de tokens razoavel** | `analise-tecnica-final.md`, secao **3. Estimativa do volume total em tokens**: mostra a matematica completa e chega a **~8,2M tokens**, dentro da ordem de grandeza esperada pela rubrica. |
| **Orcamento de contexto** | `analise-tecnica-final.md`, secao **4. Orcamento de contexto no GPT-4o 128K**: calcula `128K - 2K = 126K`, depois `126K / 500 = 252 chunks`, e explica por que o uso pratico deve ficar em **5-8 chunks**, com **ate 10** em casos mais complexos. |
| **Chunking justificado** | `analise-tecnica-final.md`, secao **5. Estrategia de chunking recomendada**: justifica o chunking por **tipo de pergunta** e pelo efeito **lost in the middle**, com exemplos especificos da NovaTech. |
| **Iteracao com ferramenta** | `transcricao-iteracao.md`: registra o **prompt inicial**, o **v1**, as **fraquezas**, o **prompt de auto-revisao**, os **achados da revisao** e as **melhorias incorporadas**. |
| **Especificidade ao dominio NovaTech** | Ao longo do texto final ha referencias diretas a **POL-001**, **PROC-042 / PROC-042-v2**, **SLA-2024**, **FAQ informal**, `frete-base-AAAAMM.xlsx`, SharePoint, Confluence e Azure. |

## Checagens internas de consistencia
- A estimativa total foi mantida igual em todo o material: **~8,2 milhoes de tokens**.
- O calculo de contexto foi mantido igual em todo o material: **126K uteis** e **~252 chunks matematicos**.
- A recomendacao pratica foi mantida igual em todo o material: **5-8 chunks normalmente; ate 10 em queries multi-documento**.
- O tratamento de conflito de versoes foi mantido igual em todo o material: **nao mesclar PROC-042 com PROC-042-v2 sem vigencia explicita**.

## Decisoes tecnicas centrais do entregavel
1. **Nao usar a janela de 128K como desculpa para mandar muitos chunks.**
2. **Tratar autoridade e vigencia como parte do dado**, nao como detalhe de prompt.
3. **Preservar estrutura em tabelas e formulas**, porque NovaTech depende disso para SLA e frete.
4. **Usar FAQ informal apenas como apoio**, nunca como fonte principal para regra critica.
5. **Tratar planilhas de frete como dado semiestruturado com calculo**, nao so como texto embedado.

## Sintese final
O entregavel atende o exercicio porque nao responde "RAG" de forma generica. Ele traduz os problemas da base da **NovaTech** em decisoes tecnicas concretas de ingestao, retrieval, chunking e governanca de contexto.

