# Resultados dos testes do protótipo RAG

- Gerado em: `2026-07-07T16:27:30`
- Diretório dos documentos ingeridos: `C:\Users\kaiop\Desktop\Prática 1\Prática 1`
- Modelo de embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Chunks indexados no ChromaDB: `34`
- Cenários executados: `7`
- Veredictos: `6` corretos, `1` parciais, `0` incorretos

## Estratégia de leitura dos resultados
- `Chunks esperados`: gabarito do Anexo B.
- `Recuperado`: IDs de referência encontrados nos chunks retornados.
- O corpo do chunk abaixo mostra o trecho realmente recuperado pelo protótipo.

## 1. prazo-devolucao
- Pergunta: `Qual o prazo de devolução?`
- Chunks esperados (Anexo B): `POL-001-A, POL-001-B`
- Chunks opcionais / risco: `POL-001-C`
- Recuperado: `POL-001-A, POL-001-B, POL-001-C, POL-001-D, PROC-042v2-C`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Chunks opcionais/risco também apareceram: POL-001-C.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.7776 | `pol-001__3-regras-de-devolucao-3-1-prazo-geral__part-01` | `POL-001-A` | `POL-001` | `3. Regras de Devolução > 3.1. Prazo geral` |
| 2 | 0.6709 | `pol-001__3-regras-de-devolucao-3-2-excecoes-ao-prazo-geral__part-01` | `POL-001-B` | `POL-001` | `3. Regras de Devolução > 3.2. Exceções ao prazo geral` |
| 3 | 0.6294 | `pol-001__3-regras-de-devolucao-3-3-procedimento-de-devolucao__part-01` | `POL-001-C` | `POL-001` | `3. Regras de Devolução > 3.3. Procedimento de devolução` |
| 4 | 0.6025 | `pol-001__3-regras-de-devolucao-3-5-custos-de-devolucao__part-01` | `POL-001-D` | `POL-001` | `3. Regras de Devolução > 3.5. Custos de devolução` |
| 5 | 0.6017 | `proc-042-v2__3-prazo-de-entrega-para-frete-especial__part-01` | `PROC-042v2-C` | `PROC-042-v2` | `3. Prazo de entrega para frete especial` |

### Chunk rank 1
- Similaridade: `0.7776`
- Documento: `POL-001`
- Referência(s) do Anexo B: `POL-001-A`

> Documento: POL-001 | Tipo: normativo | Seção: 3. Regras de Devolução > 3.1. Prazo geral
> O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking. A contagem de dias úteis exclui sábados, domingos e feriados nacionais.

### Chunk rank 2
- Similaridade: `0.6709`
- Documento: `POL-001`
- Referência(s) do Anexo B: `POL-001-B`

> Documento: POL-001 | Tipo: normativo | Seção: 3. Regras de Devolução > 3.2. Exceções ao prazo geral
> As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão:
> 
> - Cargas perigosas classificadas nas classes 1 a 6 da ANTT (Agência Nacional de Transportes Terrestres), conforme Resolução ANTT nº 5.947/2021. Inclui: explosivos (classe 1), gases (classe 2), líquidos inflamáveis (classe 3), sólidos inflamáveis (classe 4), oxidantes e peróxidos (classe 5), substâncias tóxicas e infectantes (classe 6).
> - Cargas refrigeradas que tenham rompido a cadeia de frio (temperatura fora da faixa especificada na nota fiscal por mais de 30 minutos contínuos, conforme registro do sensor IoT).
> - Cargas com lacre de segurança violado, salvo quando a violação for documentada no ato de entrega com assinatura do motorista e do recebedor.
> 
> Para essas categorias, o cliente deve entrar em contato com o setor de Gestão de Riscos (ramal 4500) para tratamento individual.

### Chunk rank 3
- Similaridade: `0.6294`
- Documento: `POL-001`
- Referência(s) do Anexo B: `POL-001-C`

> Documento: POL-001 | Tipo: normativo | Seção: 3. Regras de Devolução > 3.3. Procedimento de devolução
> 1. O cliente abre chamado no Portal do Cliente (portal.novatech.com.br), selecionando a categoria "Devolução de Mercadoria".
> 2. O chamado deve incluir: número do CT-e (Conhecimento de Transporte Eletrônico), fotos da mercadoria no estado atual (mínimo 3 fotos: embalagem externa, etiqueta de identificação, e conteúdo), e motivo da devolução.
> 3. O time de atendimento tem 4 horas úteis para triagem do chamado (verificar elegibilidade, documentação e prazo).
> 4. Se elegível, a coleta reversa é agendada em até 2 dias úteis após aprovação.
> 5. O reembolso ou crédito é processado em até 5 dias úteis após o recebimento da mercadoria devolvida no centro de distribuição.

## 2. devolucao-carga-perigosa
- Pergunta: `Posso devolver carga perigosa?`
- Chunks esperados (Anexo B): `POL-001-B`
- Chunks opcionais / risco: `FAQ-03, POL-001-A`
- Recuperado: `FAQ-03, POL-001-B, FAQ-32, SLA-2024-D, POL-001-D`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Chunks opcionais/risco também apareceram: FAQ-03. FAQ informal apareceu nos resultados; isso pede priorização por autoridade da fonte.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.7553 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-3-cliente-perguntou-se-pode-devolver-carga-perigosa-o-que-respondo__part-01` | `FAQ-03` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"` |
| 2 | 0.6279 | `pol-001__3-regras-de-devolucao-3-2-excecoes-ao-prazo-geral__part-01` | `POL-001-B` | `POL-001` | `3. Regras de Devolução > 3.2. Exceções ao prazo geral` |
| 3 | 0.5652 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-32-pode-enviar-carga-perigosa-com-frete-expresso__part-01` | `FAQ-32` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 32 — "Pode enviar carga perigosa com frete expresso?"` |
| 4 | 0.5637 | `sla-2024__3-definicao-de-incidente-critico__part-01` | `SLA-2024-D` | `SLA-2024` | `3. Definição de incidente crítico` |
| 5 | 0.5519 | `pol-001__3-regras-de-devolucao-3-5-custos-de-devolucao__part-01` | `POL-001-D` | `POL-001` | `3. Regras de Devolução > 3.5. Custos de devolução` |

### Chunk rank 1
- Similaridade: `0.7553`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-03`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"
> Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.

### Chunk rank 2
- Similaridade: `0.6279`
- Documento: `POL-001`
- Referência(s) do Anexo B: `POL-001-B`

> Documento: POL-001 | Tipo: normativo | Seção: 3. Regras de Devolução > 3.2. Exceções ao prazo geral
> As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão:
> 
> - Cargas perigosas classificadas nas classes 1 a 6 da ANTT (Agência Nacional de Transportes Terrestres), conforme Resolução ANTT nº 5.947/2021. Inclui: explosivos (classe 1), gases (classe 2), líquidos inflamáveis (classe 3), sólidos inflamáveis (classe 4), oxidantes e peróxidos (classe 5), substâncias tóxicas e infectantes (classe 6).
> - Cargas refrigeradas que tenham rompido a cadeia de frio (temperatura fora da faixa especificada na nota fiscal por mais de 30 minutos contínuos, conforme registro do sensor IoT).
> - Cargas com lacre de segurança violado, salvo quando a violação for documentada no ato de entrega com assinatura do motorista e do recebedor.
> 
> Para essas categorias, o cliente deve entrar em contato com o setor de Gestão de Riscos (ramal 4500) para tratamento individual.

### Chunk rank 3
- Similaridade: `0.5652`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-32`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 32 — "Pode enviar carga perigosa com frete expresso?"
> Sim, mas precisa de autorização do Compliance e a documentação ANTT tem que estar atualizada. Na prática, demora uns 2 dias para conseguir a autorização, então o 'expresso' acaba não sendo tão expresso. Avise o cliente sobre isso.

## 3. sla-cliente-gold
- Pergunta: `Qual o SLA do cliente Gold?`
- Chunks esperados (Anexo B): `SLA-2024-B`
- Chunks opcionais / risco: `SLA-2024-A, SLA-2024-C`
- Recuperado: `SLA-2024-B, FAQ-41, SLA-2024-C, SLA-2024-E`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Chunks opcionais/risco também apareceram: SLA-2024-C. FAQ informal apareceu nos resultados; isso pede priorização por autoridade da fonte.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.8026 | `sla-2024__2-tabela-de-slas__sla-geral` | `SLA-2024-B` | `SLA-2024` | `2. Tabela de SLAs` |
| 2 | 0.6373 | `sla-2024__5-medicao-e-reportes__part-01` | `—` | `SLA-2024` | `5. Medição e reportes` |
| 3 | 0.6133 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-41-qual-a-diferenca-entre-sla-de-resposta-e-sla-de-resolucao__part-01` | `FAQ-41` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"` |
| 4 | 0.6017 | `sla-2024__2-tabela-de-slas__sla-critico` | `SLA-2024-C` | `SLA-2024` | `2. Tabela de SLAs` |
| 5 | 0.5788 | `sla-2024__4-penalidades-por-descumprimento__part-01` | `SLA-2024-E` | `SLA-2024` | `4. Penalidades por descumprimento` |

### Chunk rank 1
- Similaridade: `0.8026`
- Documento: `SLA-2024`
- Referência(s) do Anexo B: `SLA-2024-B`

> Documento: SLA-2024 | Tipo: contratual | Seção: 2. Tabela de SLAs
> Tabela normalizada:
> Subtema: SLAs para chamados gerais.
> - Gold: Tempo de primeira resposta (chamados gerais): Até 2h úteis; Tempo de resolução (chamados gerais): Até 24h úteis.
> - Silver: Tempo de primeira resposta (chamados gerais): Até 4h úteis; Tempo de resolução (chamados gerais): Até 48h úteis.
> - Standard: Tempo de primeira resposta (chamados gerais): Até 8h úteis; Tempo de resolução (chamados gerais): Até 72h úteis.
> 
> Tabela original markdown:
> | Métrica | Gold | Silver | Standard |
> |---------|------|--------|----------|
> | Tempo de primeira resposta (chamados gerais) | Até 2h úteis | Até 4h úteis | Até 8h úteis |
> | Tempo de resolução (chamados gerais) | Até 24h úteis | Até 48h úteis | Até 72h úteis |

### Chunk rank 2
- Similaridade: `0.6373`
- Documento: `SLA-2024`
- Referência(s) do Anexo B: `sem mapeamento`

> Documento: SLA-2024 | Tipo: contratual | Seção: 5. Medição e reportes
> Os SLAs são medidos pelo sistema de chamados (Azure DevOps) a partir do timestamp de abertura do chamado. O relógio de SLA pausa fora do horário comercial (08h-18h, dias úteis) para chamados gerais, mas não pausa para incidentes críticos de clientes Gold.

### Chunk rank 3
- Similaridade: `0.6133`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-41`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
> Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

## 4. frete-600kg-manaus
- Pergunta: `Frete para 600kg para Manaus?`
- Chunks esperados (Anexo B): `PROC-042v2-B, PROC-042v2-A`
- Chunks opcionais / risco: `PROC-042-B`
- Recuperado: `PROC-042v2-B, PROC-042-B, PROC-042v2-A, PROC-042-A, FAQ-08`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Chunks opcionais/risco também apareceram: PROC-042-B. FAQ informal apareceu nos resultados; isso pede priorização por autoridade da fonte. Versões v1 e v2 da PROC-042 foram recuperadas juntas, criando risco real de contradição.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.7084 | `proc-042-v2__2-formula-de-calculo-2-1-multiplicadores-regionais-atualizados-em-novembro-2023__part-01` | `PROC-042v2-B` | `PROC-042-v2` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)` |
| 2 | 0.6785 | `proc-042__2-formula-de-calculo-2-1-multiplicadores-regionais__part-01` | `PROC-042-B` | `PROC-042` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais` |
| 3 | 0.5989 | `proc-042-v2__2-formula-de-calculo__part-01` | `PROC-042v2-A` | `PROC-042-v2` | `2. Fórmula de cálculo` |
| 4 | 0.5734 | `proc-042__2-formula-de-calculo__part-01` | `PROC-042-A` | `PROC-042` | `2. Fórmula de cálculo` |
| 5 | 0.5669 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-8-como-funciona-o-frete-especial__part-01` | `FAQ-08` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 8 — "Como funciona o frete especial?"` |

### Chunk rank 1
- Similaridade: `0.7084`
- Documento: `PROC-042-v2`
- Referência(s) do Anexo B: `PROC-042v2-B`

> Documento: PROC-042-v2 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.3.
> - Região: Sudeste; Multiplicador: 1.1.
> - Região: Centro-Oeste; Multiplicador: 1.4.
> - Região: Nordeste; Multiplicador: 1.5.
> - Região: Norte; Multiplicador: 1.8.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.3 |
> | Sudeste | 1.1 |
> | Centro-Oeste | 1.4 |
> | Nordeste | 1.5 |
> | Norte | 1.8 |

### Chunk rank 2
- Similaridade: `0.6785`
- Documento: `PROC-042`
- Referência(s) do Anexo B: `PROC-042-B`

> Documento: PROC-042 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.2.
> - Região: Sudeste; Multiplicador: 1.0.
> - Região: Centro-Oeste; Multiplicador: 1.3.
> - Região: Nordeste; Multiplicador: 1.4.
> - Região: Norte; Multiplicador: 1.6.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.2 |
> | Sudeste | 1.0 |
> | Centro-Oeste | 1.3 |
> | Nordeste | 1.4 |
> | Norte | 1.6 |

### Chunk rank 3
- Similaridade: `0.5989`
- Documento: `PROC-042-v2`
- Referência(s) do Anexo B: `PROC-042v2-A`

> Documento: PROC-042-v2 | Tipo: procedimento | Seção: 2. Fórmula de cálculo
> O frete especial é calculado como:
> 
> Valor do frete = Valor base × Multiplicador regional × Fator de peso
> 
> Onde:
> 
> - Valor base = tarifa publicada na tabela mensal de fretes.
> - Multiplicador regional = fator aplicado conforme a região de destino (seção 2.1).
> - Fator de peso = 1.0 para cargas de 500kg a 1.000kg; 1.15 para cargas de 1.001kg a 3.000kg; 1.4 para cargas acima de 3.000kg.

## 5. multiplicador-sudeste
- Pergunta: `Qual o multiplicador para o Sudeste?`
- Chunks esperados (Anexo B): `PROC-042v2-B`
- Chunks opcionais / risco: `PROC-042-B`
- Recuperado: `PROC-042v2-B, PROC-042-B, FAQ-08, PROC-042v2-C, PROC-042-C`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Chunks opcionais/risco também apareceram: PROC-042-B. FAQ informal apareceu nos resultados; isso pede priorização por autoridade da fonte. Versões v1 e v2 da PROC-042 foram recuperadas juntas, criando risco real de contradição.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.6977 | `proc-042-v2__2-formula-de-calculo-2-1-multiplicadores-regionais-atualizados-em-novembro-2023__part-01` | `PROC-042v2-B` | `PROC-042-v2` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)` |
| 2 | 0.6688 | `proc-042__2-formula-de-calculo-2-1-multiplicadores-regionais__part-01` | `PROC-042-B` | `PROC-042` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais` |
| 3 | 0.5521 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-8-como-funciona-o-frete-especial__part-01` | `FAQ-08` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 8 — "Como funciona o frete especial?"` |
| 4 | 0.5383 | `proc-042-v2__3-prazo-de-entrega-para-frete-especial__part-01` | `PROC-042v2-C` | `PROC-042-v2` | `3. Prazo de entrega para frete especial` |
| 5 | 0.5234 | `proc-042__3-prazo-de-entrega-para-frete-especial__part-01` | `PROC-042-C` | `PROC-042` | `3. Prazo de entrega para frete especial` |

### Chunk rank 1
- Similaridade: `0.6977`
- Documento: `PROC-042-v2`
- Referência(s) do Anexo B: `PROC-042v2-B`

> Documento: PROC-042-v2 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.3.
> - Região: Sudeste; Multiplicador: 1.1.
> - Região: Centro-Oeste; Multiplicador: 1.4.
> - Região: Nordeste; Multiplicador: 1.5.
> - Região: Norte; Multiplicador: 1.8.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.3 |
> | Sudeste | 1.1 |
> | Centro-Oeste | 1.4 |
> | Nordeste | 1.5 |
> | Norte | 1.8 |

### Chunk rank 2
- Similaridade: `0.6688`
- Documento: `PROC-042`
- Referência(s) do Anexo B: `PROC-042-B`

> Documento: PROC-042 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.2.
> - Região: Sudeste; Multiplicador: 1.0.
> - Região: Centro-Oeste; Multiplicador: 1.3.
> - Região: Nordeste; Multiplicador: 1.4.
> - Região: Norte; Multiplicador: 1.6.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.2 |
> | Sudeste | 1.0 |
> | Centro-Oeste | 1.3 |
> | Nordeste | 1.4 |
> | Norte | 1.6 |

### Chunk rank 3
- Similaridade: `0.5521`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-08`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 8 — "Como funciona o frete especial?"
> Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.

## 6. frete-300kg-salvador
- Pergunta: `Frete para 300kg para Salvador?`
- Chunks esperados (Anexo B): `Nenhum chunk formal esperado`
- Chunks opcionais / risco: `PROC-042v2-B`
- Recuperado: `PROC-042v2-B, PROC-042-B, PROC-042v2-C, FAQ-08, PROC-042-C`
- Faltantes: `—`
- Veredito: **Parcial**
- Observações: A pergunta não tem cobertura formal; mesmo assim apareceram chunks parciais sobre frete especial (>500kg). Chunks opcionais/risco também apareceram: PROC-042v2-B. Versões v1 e v2 da PROC-042 foram recuperadas juntas, criando risco real de contradição.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.6841 | `proc-042-v2__2-formula-de-calculo-2-1-multiplicadores-regionais-atualizados-em-novembro-2023__part-01` | `PROC-042v2-B` | `PROC-042-v2` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)` |
| 2 | 0.6487 | `proc-042__2-formula-de-calculo-2-1-multiplicadores-regionais__part-01` | `PROC-042-B` | `PROC-042` | `2. Fórmula de cálculo > 2.1. Multiplicadores regionais` |
| 3 | 0.5640 | `proc-042-v2__3-prazo-de-entrega-para-frete-especial__part-01` | `PROC-042v2-C` | `PROC-042-v2` | `3. Prazo de entrega para frete especial` |
| 4 | 0.5582 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-8-como-funciona-o-frete-especial__part-01` | `FAQ-08` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 8 — "Como funciona o frete especial?"` |
| 5 | 0.5494 | `proc-042__3-prazo-de-entrega-para-frete-especial__part-01` | `PROC-042-C` | `PROC-042` | `3. Prazo de entrega para frete especial` |

### Chunk rank 1
- Similaridade: `0.6841`
- Documento: `PROC-042-v2`
- Referência(s) do Anexo B: `PROC-042v2-B`

> Documento: PROC-042-v2 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.3.
> - Região: Sudeste; Multiplicador: 1.1.
> - Região: Centro-Oeste; Multiplicador: 1.4.
> - Região: Nordeste; Multiplicador: 1.5.
> - Região: Norte; Multiplicador: 1.8.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.3 |
> | Sudeste | 1.1 |
> | Centro-Oeste | 1.4 |
> | Nordeste | 1.5 |
> | Norte | 1.8 |

### Chunk rank 2
- Similaridade: `0.6487`
- Documento: `PROC-042`
- Referência(s) do Anexo B: `PROC-042-B`

> Documento: PROC-042 | Tipo: procedimento | Seção: 2. Fórmula de cálculo > 2.1. Multiplicadores regionais
> Tabela normalizada:
> - Região: Sul; Multiplicador: 1.2.
> - Região: Sudeste; Multiplicador: 1.0.
> - Região: Centro-Oeste; Multiplicador: 1.3.
> - Região: Nordeste; Multiplicador: 1.4.
> - Região: Norte; Multiplicador: 1.6.
> 
> Tabela original markdown:
> | Região | Multiplicador |
> |--------|--------------|
> | Sul | 1.2 |
> | Sudeste | 1.0 |
> | Centro-Oeste | 1.3 |
> | Nordeste | 1.4 |
> | Norte | 1.6 |

### Chunk rank 3
- Similaridade: `0.5640`
- Documento: `PROC-042-v2`
- Referência(s) do Anexo B: `PROC-042v2-C`

> Documento: PROC-042-v2 | Tipo: procedimento | Seção: 3. Prazo de entrega para frete especial
> O prazo de entrega para frete especial é calculado como o prazo padrão da rota + 3 dias úteis adicionais para manuseio e roteirização de carga pesada (anteriormente era + 2 dias na versão anterior).

## 7. carga-danificada
- Pergunta: `O que acontece com carga danificada?`
- Chunks esperados (Anexo B): `FAQ-38`
- Chunks opcionais / risco: `—`
- Recuperado: `FAQ-38, SLA-2024-D, FAQ-22, POL-001-D, FAQ-32`
- Faltantes: `—`
- Veredito: **Correto**
- Observações: Sem ressalvas relevantes neste cenário.

| Rank | Similaridade | Chunk interno | Referência(s) | Documento | Seção |
|---:|---:|---|---|---|---|
| 1 | 0.6308 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-38-cliente-quer-saber-a-politica-para-carga-que-chegou-danificada__part-01` | `FAQ-38` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 38 — "Cliente quer saber a política para carga que chegou danificada."` |
| 2 | 0.5626 | `sla-2024__3-definicao-de-incidente-critico__part-01` | `SLA-2024-D` | `SLA-2024` | `3. Definição de incidente crítico` |
| 3 | 0.5554 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-22-cliente-quer-saber-sobre-seguro-de-carga-o-que-falar__part-01` | `FAQ-22` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"` |
| 4 | 0.5410 | `pol-001__3-regras-de-devolucao-3-5-custos-de-devolucao__part-01` | `POL-001-D` | `POL-001` | `3. Regras de Devolução > 3.5. Custos de devolução` |
| 5 | 0.5397 | `faq-atendimento__perguntas-selecionadas-das-47-do-documento-original-item-32-pode-enviar-carga-perigosa-com-frete-expresso__part-01` | `FAQ-32` | `FAQ-ATENDIMENTO` | `Perguntas selecionadas (das 47 do documento original) > Item 32 — "Pode enviar carga perigosa com frete expresso?"` |

### Chunk rank 1
- Similaridade: `0.6308`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-38`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 38 — "Cliente quer saber a política para carga que chegou danificada."
> Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Chunk rank 2
- Similaridade: `0.5626`
- Documento: `SLA-2024`
- Referência(s) do Anexo B: `SLA-2024-D`

> Documento: SLA-2024 | Tipo: contratual | Seção: 3. Definição de incidente crítico
> Um incidente é classificado como crítico quando atende a pelo menos um dos seguintes critérios:
> 
> - Carga com valor declarado acima de R$ 100.000 está com status desconhecido há mais de 6 horas.
> - Carga perigosa com qualquer irregularidade de documentação ou rastreamento.
> - Mais de 5 chamados do mesmo cliente nas últimas 24 horas sobre o mesmo problema.
> - Qualquer situação que envolva risco à segurança de pessoas.

### Chunk rank 3
- Similaridade: `0.5554`
- Documento: `FAQ-ATENDIMENTO`
- Referência(s) do Anexo B: `FAQ-22`

> Documento: FAQ-ATENDIMENTO | Tipo: informal | Seção: Perguntas selecionadas (das 47 do documento original) > Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"
> A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.
