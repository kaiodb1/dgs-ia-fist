# Analise tecnica final - Desenvolvedor 1.1

## Parecer executivo
O assistente da NovaTech e tecnicamente viavel, mas nao como um RAG ingenuo de "indexar tudo e mandar para o GPT-4o". O risco dominante aqui nao e a falta de janela de contexto; e perder estrutura, autoridade, vigencia e excecoes durante ingestao e retrieval. Para a NovaTech, a solucao precisa combinar extracao multimodal, metadados fortes de versao/vigencia, retrieval pequeno e bem ordenado, e tratamento especial para planilhas com calculo.

Dois pontos tornam isso especialmente critico no caso NovaTech:
1. a base ja contem contradicoes reais, como **PROC-042 vs PROC-042-v2**;
2. existe conteudo informal (**FAQ-Atendimento**) que pode ser util como apoio operacional, mas nao pode ter o mesmo peso de **POL-001**, **PROC-042-v2** ou **SLA-2024**.

## 1. Desafios por tipo de fonte

| Tipo de fonte | Desafio de ingestao/RAG | Impacto provavel na qualidade da resposta | Estrategia de mitigacao recomendada |
|---|---|---|---|
| **PDFs com tabelas complexas** | PDFs com tabelas largas (ex.: frete com 15+ colunas) costumam perder a relacao linha/coluna na extracao. Cabecalhos multi-linha, celulas mescladas e tabelas quebradas em varias paginas viram texto linear confuso. | O modelo pode associar o valor errado a linha errada. No contexto NovaTech, isso pode trocar multiplicadores por regiao, misturar SLAs por tier ou ignorar notas de rodape que mudam a regra. | Usar extracao **layout-aware** (ex.: Azure Document Intelligence, aderente ao stack Azure ja aceito pela NovaTech), preservar pagina/bounding boxes, e normalizar tabelas em formato estruturado (JSON ou Markdown tabular). Quando a tabela for grande, quebrar por blocos logicos de linhas, **repetindo cabecalhos e unidades em cada chunk**. |
| **PDFs escaneados** | O gargalo passa a ser OCR: rotacao, baixa resolucao, carimbo, contraste ruim e segmentacao de colunas podem apagar palavras criticas. | Erros de OCR nao so reduzem recall; eles podem inverter regra. Ex.: perder o "NAO" em "cargas perigosas NAO sao elegiveis" muda completamente a resposta para devolucao de carga perigosa. | Pipeline com pre-processamento (deskew/denoise), OCR com score de confianca por pagina, reprocessamento das paginas ruins e fila de validacao humana para documentos criticos. Chunks de baixa confianca devem entrar no indice com flag de risco ou ficar fora da base principal ate revisao. |
| **Wiki com links e macros (Confluence)** | Exportar so o HTML/texto bruto pode perder conteudo renderizado por macro (include, excerpt, status, tabela embutida) e tambem a hierarquia de paginas e links internos. | A resposta pode sair incompleta ou fora de contexto: a pagina encontrada parece correta, mas omite um quadro gerado por macro ou a pagina mae que explica vigencia/escopo. Isso e perigoso num cenario com versoes convivendo em paralelo. | Ingerir pela API do Confluence, expandir macros antes do chunking e armazenar metadados de **titulo, espaco, hierarquia, links internos, labels e ultima atualizacao**. Indexar tanto o conteudo renderizado quanto o contexto da pagina para rerank por autoridade e recencia. |
| **Planilhas com formulas interdependentes** | Em planilhas, o significado nao esta so no texto visivel: esta em formulas, ranges nomeados, abas ocultas e dependencias entre celulas/abas. No caso NovaTech, isso afeta diretamente arquivos como `frete-base-AAAAMM.xlsx`, citados pelos procedimentos de frete. | Um RAG puramente textual pode devolver um numero sem explicar a base de calculo, usar o mes errado ou ignorar que o valor depende de formula e versao. Para perguntas como "quanto custa o frete para 600kg em Manaus?", retrieval puro tende a ser insuficiente. | Tratar planilha como **fonte semiestruturada**, nao como texto corrido: extrair por aba/faixa, preservar cabecalhos, data de vigencia, formula e valor calculado. Para perguntas numericas, combinar RAG para achar a politica correta com uma **camada deterministica de calculo** sobre o snapshot vigente da planilha. |

## 2. Decisao transversal: autoridade, vigencia e conflito de versoes

Mesmo com boa extracao, a NovaTech ainda tem um risco estrutural: **fontes conflitantes e sem revisao unificada**. Isso aparece de forma explicita em:
- **PROC-042 vs PROC-042-v2** (multiplicadores, fatores de peso e prazo adicional diferentes);
- **FAQ-Atendimento**, que e util operacionalmente, mas esta marcado como informal e nao validado.

Por isso, eu incluiria no indice, em todos os chunks relevantes, pelo menos estes metadados:
- `doc_id` (ex.: PROC-042-v2);
- `versao`;
- `data_emissao` / `ultima_atualizacao`;
- `vigencia` (quando existir);
- `area_responsavel`;
- `tipo_de_fonte` (normativa, procedimento, contratual, FAQ informal);
- `nivel_de_autoridade`.

Regra operacional de retrieval/resposta para a NovaTech:
1. **normativo/contratual** vence FAQ informal;
2. em conflito entre versoes, priorizar a versao mais recente **se houver regra de transicao explicita**;
3. se o conflito permanecer, o assistente deve **expor a divergencia e citar as duas fontes**, nao mesclar numeros.

Sem isso, o problema nao sera "falta de contexto", e sim **contexto contraditorio sem governanca**.

## 3. Estimativa do volume total em tokens

Vou usar a regra pratica pedida no exercicio: **~0,75 palavras por token** (ou seja, `tokens ~= palavras / 0,75`).

### 3.1 PDFs
- Quantidade: `800 PDFs`
- Media: `10 paginas por PDF`
- Total de paginas: `800 x 10 = 8.000 paginas`
- Assuncao de trabalho: `~600 palavras por pagina`
  - Essa media e defensavel para a NovaTech porque a extracao de tabelas e legendas costuma **inflar** o texto final em relacao a um PDF puramente narrativo.
- Total de palavras: `8.000 x 600 = 4.800.000 palavras`
- Tokens: `4.800.000 / 0,75 = 6.400.000 tokens`

### 3.2 Wiki
- Quantidade: `400 paginas`
- Media: `1.500 palavras por pagina`
- Total de palavras: `400 x 1.500 = 600.000 palavras`
- Tokens: `600.000 / 0,75 = 800.000 tokens`

### 3.3 Planilhas
- Quantidade: `50 planilhas`
- Assuncao de trabalho: `~15.000 palavras equivalentes por planilha`
  - Aqui estou considerando nao so valores visiveis, mas tambem **nomes de abas, cabecalhos, formulas, ranges e explicacoes textuais normalizadas**. Se eu indexasse so os valores, o numero cairia, mas a utilidade para auditoria e calculo cairia junto.
- Total de palavras equivalentes: `50 x 15.000 = 750.000 palavras`
- Tokens: `750.000 / 0,75 = 1.000.000 tokens`

### 3.4 Total estimado
- Palavras totais: `4.800.000 + 600.000 + 750.000 = 6.150.000 palavras`
- Tokens totais: `6.150.000 / 0,75 = 8.200.000 tokens`

**Estimativa de trabalho:** eu planejaria a base da NovaTech como algo na ordem de **~8,2 milhoes de tokens**.

Se o chunk medio tiver `~500 tokens`, isso gera aproximadamente:
- `8.200.000 / 500 = 16.400 chunks` sem considerar overlap;
- com overlap de 10% a 15%, o total real tende a subir para algo entre **18 mil e 19 mil chunks**.

Ou seja: o desafio principal nao e "caber no modelo"; e **selecionar muito bem poucos chunks dentro de uma base grande e heterogenea**.

## 4. Orcamento de contexto no GPT-4o 128K

### 4.1 Limite matematico
- Janela total: `128.000 tokens`
- Reserva para system prompt + instrucoes: `~2.000 tokens`
- Contexto util restante: `126.000 tokens`
- Com chunks de `~500 tokens`: `126.000 / 500 = 252 chunks`

**Matematicamente, caberiam ~252 chunks.**

### 4.2 O que isso significa na pratica
Esse numero e enganoso se usado como meta operacional. Em producao, ainda competem por atencao:
- pergunta do atendente;
- metadados/citacoes das fontes;
- resumo de historico de conversa (se houver);
- espaco para a propria resposta;
- e, principalmente, o efeito **lost in the middle**.

No cenario NovaTech, mandar 100+ chunks seria contraproducente por tres motivos:
1. enterraria excecoes criticas no meio do contexto;
2. aumentaria a chance de misturar **PROC-042** com **PROC-042-v2**;
3. daria peso indevido ao **FAQ informal** se ele viesse junto com documentos normativos.

### 4.3 Recomendacao pratica
Minha recomendacao nao e "usar o maximo que cabe", e sim **usar o minimo que resolve bem**:
- **5 a 8 chunks** para a maioria das perguntas de atendimento;
- **ate 10 chunks** quando a pergunta cruza regra + excecao + versao/calculo.

Em tokens, isso representa algo como:
- `5 chunks ~= 2.500 tokens`
- `8 chunks ~= 4.000 tokens`
- `10 chunks ~= 5.000 tokens`

Ou seja: mesmo tendo 126K uteis, eu deliberadamente operaria com **uma fracao pequena** disso para preservar precisao e evitar competicao de atencao.

## 5. Estrategia de chunking recomendada

### 5.1 Principio geral
As perguntas da NovaTech tendem a ser curtas e operacionais, por exemplo:
- "Posso devolver carga perigosa?"
- "Qual o SLA do cliente Gold?"
- "Quanto custa o frete para 600kg em Manaus?"
- "Existe tier Platinum?"

Essas perguntas nao pedem o documento inteiro; pedem **uma unidade de regra de negocio fechada**. Entao eu nao faria chunking cego de 500 tokens em tudo.

### 5.2 Como eu quebraria por tipo de conteudo

#### a) Politicas e procedimentos (POL/PROC)
- Chunk por **secao logica** com cabecalho do documento, versao e data.
- Faixa alvo: **250-400 tokens por chunk textual**.
- Regra importante: quando a pergunta tipica combina **regra geral + excecao**, eu manteria esses dois elementos no mesmo "grupo recuperavel".

**Exemplo NovaTech:**
- Para "qual o prazo de devolucao?", nao basta recuperar so a regra geral de 7 dias; e perigoso separar isso da excecao de **carga perigosa nao elegivel**.
- Portanto, **POL-001 secao 3.1** e **3.2** devem ficar no mesmo chunk ampliado ou em dois chunks adjacentes, sempre recuperados juntos.

#### b) Tabelas (SLA e frete)
- Nao quebrar no meio de uma relacao linha/coluna.
- Quando a tabela for grande, quebrar por **blocos de linhas** ou por **subtabela tematica**, repetindo cabecalhos.
- Cada chunk precisa repetir: documento, versao, data e unidade.

**Exemplos NovaTech:**
- `SLA-2024`: um chunk para "chamados gerais", outro para "incidentes criticos", ambos com os tiers completos.
- `PROC-042-v2`: um chunk para a formula/faixas de peso, outro para a tabela de multiplicadores, e outro para a regra transitoria da secao 5.

#### c) Wiki do Confluence
- Chunk por secao renderizada da pagina, preservando **titulo + hierarquia + macro expandida + links principais**.
- Se uma macro gerar tabela ou checklist importante, indexar tambem esse conteudo como chunk proprio, ligado a pagina original.

#### d) Planilhas
- Chunk por **aba + faixa nomeada/tabela**.
- Preservar `mes de vigencia`, `nome da aba`, `cabecalhos`, `formula`, `valor calculado` e `unidade`.
- Para perguntas de calculo, o LLM nao deve "deduzir" a matematica do Excel lendo texto; ele deve usar a planilha normalizada ou uma funcao de calculo em cima do snapshot vigente.

### 5.3 Como combater o lost in the middle
1. **Poucos chunks por vez**: 5-8 na maioria dos casos.
2. **Ordenacao por autoridade e relevancia**, nao so por similaridade semantica.
3. **Excecoes criticas nunca no meio de um pacote grande**.
4. **Chunks conflitantes explicitamente rotulados** quando houver mais de uma versao.
5. **FAQ informal so entra como apoio**, e idealmente depois das fontes normativas.

**Exemplo pratico:**
- Para uma pergunta de frete especial, eu nao enviaria 8 chunks misturando PROC-042, PROC-042-v2 e FAQ.
- Eu enviaria primeiro o chunk de `PROC-042-v2` com formula/faixa de peso, depois o chunk de multiplicadores regionais, e, se necessario, o chunk de transicao (`chamados antes de 01/12/2023`).
- Se o FAQ aparecer, ele entraria como contexto secundario e rotulado como informal.

## 6. Recomendacao final para a arquitetura NovaTech

Minha recomendacao tecnica e:
1. **ingestao multimodal e orientada a estrutura** para PDFs e wiki;
2. **OCR com controle de confianca** para PDFs escaneados;
3. **metadados fortes de autoridade/versao/vigencia** em todos os chunks;
4. **retrieval curto** (5-8 chunks, ate 10 no maximo);
5. **chunking semantico por regra de negocio**, nao chunking fixo e cego;
6. **tratamento especial para planilhas**, com camada deterministica de calculo para perguntas numericas.

## Conclusao
O projeto e viavel para a NovaTech, mas **nao** com a expectativa de que o modelo "vai saber tudo" so porque a janela do GPT-4o e grande. O desenho correto e um sistema que:
- sabe distinguir fonte oficial de fonte informal;
- sabe separar versao antiga de versao vigente;
- sabe recuperar poucas evidencias fortes;
- e sabe quando retrieval puro nao basta, como no caso das planilhas com formula.

Se esses cuidados forem adotados, a arquitetura tem boa chance de atender o objetivo de reduzir o tempo de busca do atendimento. Se nao forem, os erros mais provaveis serao justamente os mais perigosos para a NovaTech: **misturar PROC-042 com PROC-042-v2, citar FAQ informal como politica oficial e inverter excecoes criticas como a devolucao de carga perigosa**.

