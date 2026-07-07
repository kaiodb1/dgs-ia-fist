## Avaliacao do Exercicio 1.1

### Resumo
O entregavel e forte no conteudo tecnico: `analise-tecnica-final.md` cobre bem os desafios por tipo de fonte, faz a conta de volume da base ate chegar a `~8,2 milhoes de tokens` e traduz a janela de `128K` em uma estrategia pratica de retrieval curto. A analise e especifica para a NovaTech e mostra bom julgamento sobre autoridade, vigencia, conflito de versoes e tratamento especial para planilhas. O principal gap esta na evidencia de uso da ferramenta pedida: a iteracao foi documentada em `transcricao-iteracao.md` como resumo e com **Copilot CLI como substituto do Claude**, sem export/print/transcricao primaria do chat.

### Scores por Dimensao

| Dimensao | Score | Justificativa |
|----------|-------|---------------|
| D1 — Dominio Conceitual | 3 | `analise-tecnica-final.md` demonstra entendimento solido de RAG e engenharia de contexto. A secao de desafios por fonte diferencia bem perda de estrutura em PDFs tabulares, risco semantico de OCR, macros/hierarquia do Confluence e dependencia de formulas em planilhas; alem disso, a analise de `lost in the middle`, autoridade e vigencia vai alem do basico. |
| D2 — Uso de Ferramentas | 2 | Ha iteracao visivel em `transcricao-iteracao.md`: o material registra um rascunho v1, a auto-critica, os achados da revisao e as melhorias incorporadas. Porem, o exercicio pedia **Claude (chat)** e a evidencia apresentada usa **Copilot CLI como substituto**, alem de trazer apenas um resumo do historico, sem transcript/export primario do chat; por isso, a evidencia de ferramenta fica parcial. |
| D3 — Qualidade do Entregavel | 3 | O artefato final e completo e utilizavel. `analise-tecnica-final.md` cobre todos os itens pedidos: desafios por tipo de fonte, estimativa de tokens com calculo, orcamento de contexto, estrategia de chunking e recomendacao arquitetural final; outro membro tecnico do time conseguiria usar esse documento para orientar discovery e desenho de pipeline. |
| D4 — Pensamento Critico | 3 | O participante nao aceita o numero teorico de `252 chunks` como recomendacao operacional e explica por que trabalhar com `5-8` chunks e mais seguro. Tambem identifica riscos nao obvios e muito relevantes para o cenario — como misturar `PROC-042` com `PROC-042-v2`, dar peso indevido ao `FAQ-Atendimento` e inverter excecoes criticas por falha de OCR — mostrando julgamento proprio, nao mera aceitacao do output inicial. |
| D5 — Aplicabilidade ao Projeto | 3 | O texto esta profundamente conectado a NovaTech: cita `POL-001`, `PROC-042`, `PROC-042-v2`, `SLA-2024`, `FAQ-Atendimento`, `frete-base-AAAAMM.xlsx`, SharePoint, Confluence e Azure Document Intelligence. As recomendacoes fazem sentido para o contexto operacional descrito no enunciado e para a expectativa de reduzir o tempo medio de busca. |

**Score do exercicio: 2.8**

### Verificacao de Armadilhas
Nenhuma armadilha explicita esta listada na rubrica do exercicio 1.1.

### Consideracoes Intencionais Relevantes
- **Desafios por tipo de fonte:** atendido com boa especificidade; cada fonte recebeu desafio, impacto e estrategia concretos em `analise-tecnica-final.md`.
- **Estimativa de tokens:** atendida e razoavel; o total de `~8,2M tokens` fica na ordem de grandeza esperada pela rubrica e a conta esta explicita.
- **Orcamento de contexto:** atendido; o documento calcula `128K - 2K = 126K`, chega a `252 chunks` de `500` tokens no limite teorico e converte isso numa recomendacao pratica menor.
- **Chunking justificado:** atendido; a estrategia nao e "512 fixo para tudo", mas sim orientada por tipo de pergunta, tipo de conteudo e pelo risco de `lost in the middle`.
- **Qualidade visivel da iteracao:** parcial; a evolucao de v1 para a versao final aparece, mas a rastreabilidade e mais fraca do que o ideal porque falta evidencia primaria do Claude e o historico esta resumido.

### Pontos Fortes
- Traduz bem problemas de ingestao em decisoes de arquitetura, especialmente para OCR, tabelas e planilhas com formula.
- Faz uma boa leitura de contexto budget: separa limite matematico de limite pratico e justifica retrieval curto.
- E altamente especifico para a NovaTech, com bons exemplos de autoridade, vigencia e conflito entre fontes.

### Pontos de Melhoria
- Anexar evidencia primaria da iteracao exigida no enunciado (export, print ou transcricao literal do chat) em vez de apenas um resumo.
- Se a substituicao de Claude por Copilot CLI foi autorizada, registrar essa autorizacao de forma verificavel no proprio entregavel.
- Tornar as premissas das planilhas ainda mais auditaveis, por exemplo decompondo melhor de onde vem a estimativa de `~15.000 palavras equivalentes por planilha`.

### Classificacao
Aprovado com distincao

### Topicos da Trilha para Reforco
Nao ha lacuna conceitual critica. O principal reforco e processual: evidenciar melhor o uso da ferramenta exigida e manter rastreabilidade entre prompt, saida bruta da IA e versao final do entregavel.

