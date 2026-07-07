# Enunciado consolidado — Desenvolvedor / Cenario 1

## O cenario

A NovaTech e uma empresa de medio porte do setor de logistica com 1.200 funcionarios. Sua operacao depende de um conjunto extenso de documentacao interna: manuais de procedimento operacional, politicas de compliance, tabelas de SLA por tipo de cliente, regras de calculo de frete e normas de seguranca de carga.

Hoje, essa documentacao esta espalhada em tres fontes: um SharePoint corporativo com ~800 documentos (PDFs e Word), uma wiki interna no Confluence com ~400 paginas e uma pasta de rede com planilhas de referencia atualizadas mensalmente.

O problema: a equipe de atendimento ao cliente (45 pessoas) gasta em media 12 minutos por chamado buscando informacoes nessas fontes para responder duvidas de clientes sobre prazos, regras de frete, politicas de devolucao e procedimentos de reclamacao. Isso gera atrasos, respostas inconsistentes e frustracao tanto dos atendentes quanto dos clientes.

A NovaTech contratou a DB1 para construir um assistente de IA que permita aos atendentes fazer perguntas em linguagem natural e receber respostas fundamentadas na documentacao oficial da empresa, com indicacao da fonte. O assistente sera integrado ao ambiente Microsoft da NovaTech (Teams + SharePoint).

### Informacoes adicionais fornecidas pela NovaTech

- O volume medio e de 320 chamados/dia, dos quais ~60% envolvem consulta a documentacao.
- A documentacao e atualizada mensalmente por 3 areas diferentes (Operacoes, Compliance, Comercial), sem processo unificado de revisao.
- Alguns documentos se contradizem entre versoes - a equipe de atendimento hoje resolve isso "perguntando para quem sabe".
- A NovaTech ja tem licencas Microsoft 365 E3 e esta disposta a provisionar Azure AI Services.
- O projeto tem orcamento para 3 meses de discovery + desenvolvimento + go-live.
- A expectativa da diretoria e reduzir o tempo medio de busca de 12 para menos de 2 minutos por chamado.

---

## Desenvolvedor

### Exercicio 1.1 — Analise de viabilidade tecnica com fundamentos de LLM e engenharia de contexto

**Contexto:** O Tech Lead pediu que voce avalie a viabilidade tecnica do assistente considerando as caracteristicas da documentacao da NovaTech e o impacto do gerenciamento de contexto na arquitetura.

**Ferramentas a utilizar:** Claude (chat)

**Inputs fornecidos:**
- O cenario completo.
- Informacoes tecnicas adicionais: *"Os PDFs do SharePoint incluem documentos com tabelas complexas (tabelas de frete com 15+ colunas), fluxogramas embutidos como imagens, e alguns documentos escaneados (OCR necessario). A wiki do Confluence tem links internos entre paginas e usa macros customizadas. As planilhas tem formulas interdependentes."*
- Conceito de context engineering aplicado a RAG: *"O contexto que o LLM recebe a cada pergunta e limitado pela janela de contexto do modelo. A qualidade da resposta depende de: quais chunks sao selecionados (relevancia), quantos chunks cabem no contexto (orcamento de atencao), onde ficam posicionados no prompt (informacao no meio de contextos longos e 'esquecida' - o efeito 'lost in the middle'), e o que mais esta no contexto competindo por atencao (system prompt, historico de conversa, instrucoes)."*

**Tarefa:**
1. Usando o **Claude**, produza uma analise tecnica que cubra:
   - Para cada tipo de fonte (PDFs com tabelas, PDFs escaneados, wiki com links, planilhas com formulas): qual o desafio para o pipeline de RAG, como isso afeta a qualidade das respostas, e uma estrategia de tratamento.
   - Estimativa do tamanho aproximado da base em tokens considerando ~800 documentos PDF (media de 10 paginas cada), ~400 paginas wiki (media de 1.500 palavras cada), e ~50 planilhas. Use a regra pratica de ~0.75 palavras por token.
   - Analise de orcamento de contexto: dado que o GPT-4o tem 128K tokens de janela e o system prompt + instrucoes consomem ~2K tokens, quantos chunks de ~500 tokens cabem em cada query? Como isso afeta a estrategia de chunking e retrieval?
   - Recomendacao de estrategia de chunking justificada pelo tipo de pergunta que o usuario fara e pelo conceito de *lost in the middle*.
2. Peca ao **Claude** que revise sua analise: forneca o documento e peca que identifique pontos fracos, estimativas otimistas demais ou riscos que voce nao considerou. Incorpore o feedback.

**Entregavel:** A analise tecnica final e o historico de iteracao com o Claude.

---

### Exercicio 1.2 — Prototipacao de prompt com engenharia de contexto

**Contexto:** Voce precisa prototipar o system prompt do assistente e testar com cenarios reais. Alem do conteudo do prompt, voce precisa pensar em como o contexto e estruturado: o que e estatico, o que e dinamico, e como a ordem da informacao afeta a resposta.

**Ferramentas a utilizar:** Claude (chat) - o proprio Claude serve como ambiente de teste do prompt

**Inputs fornecidos:**
- O cenario completo.
- Guardrails definidos pelo Product Specialist: *"O assistente deve (1) sempre citar a fonte do documento, (2) nunca inventar prazos ou valores que nao estejam na documentacao, (3) quando nao encontrar resposta, dizer explicitamente que nao encontrou e sugerir escalar para o supervisor, (4) responder em portugues formal mas acessivel."*
- 3 chunks simulados de documentacao (extraidos do **Anexo B** - o Anexo B contem o conjunto completo de chunks e o mapa de cobertura para validacao):
  - Chunk A: *"Politica de Devolucao POL-001, secao 3.2: Mercadorias podem ser devolvidas em ate 7 dias uteis apos o recebimento, exceto cargas classificadas como perigosas (classes 1 a 6 da ANTT). O cliente deve abrir chamado no portal e anexar fotos da mercadoria."*
  - Chunk B: *"Tabela SLA-2024: Cliente Gold - resposta em ate 2h, resolucao em ate 24h. Cliente Silver - resposta em ate 4h, resolucao em ate 48h. Cliente Standard - resposta em ate 8h, resolucao em ate 72h."*
  - Chunk C: *"PROC-042-v2, secao 2: Frete especial para cargas acima de 500kg: valor base × multiplicador regional. Regiao Sul: 1.3. Regiao Sudeste: 1.1. Regiao Norte: 1.8. Regiao Nordeste: 1.5. Regiao Centro-Oeste: 1.4."*
- Conceito de contexto estatico vs dinamico: *"Em um prompt de producao, algumas partes sao estaticas (system prompt, guardrails - raramente mudam) e outras sao dinamicas (chunks recuperados, dados do cliente, historico da conversa - mudam a cada query). A engenharia de contexto decide como essas partes se compoem: em que ordem, com que prioridade, e o que fazer quando o contexto total ultrapassa o orcamento."*

**Tarefa:**
1. Escreva um system prompt completo para o assistente, incorporando os guardrails e o contexto do projeto. Organize o prompt em secoes claras: identidade, regras, formato de resposta e instrucoes para uso dos chunks. Defina explicitamente a ordem de prioridade quando houver conflito entre fontes.
2. Documente a estrutura de contexto do prompt: identifique quais partes sao estaticas (vao em toda query) e quais sao dinamicas (mudam por query). Estime o tamanho em tokens de cada parte.
3. Teste o prompt diretamente no **Claude**: abra uma conversa nova, cole o system prompt como instrucao inicial junto com os chunks simulados, e faca estas 3 perguntas como se fosse o atendente:
   - "Qual o prazo de devolucao para carga perigosa?"
   - "Meu cliente e Gold, qual o SLA de resolucao?"
   - "Quanto custa o frete para 600kg para Manaus?"
4. Analise cada resposta: esta correta? Citou a fonte? Respeitou os guardrails? Onde errou?
5. Itere o system prompt: reescreva partes que geraram respostas inadequadas e teste novamente.

**Entregavel:** O system prompt v1 com mapeamento de contexto estatico/dinamico, as respostas obtidas, a analise critica, o system prompt v2 (iterado), e as respostas da segunda rodada.

---

### Exercicio 1.3 — Construcao de pipeline de RAG com ferramentas open-source

**Contexto:** O Tech Lead quer uma prova de conceito funcional do pipeline de RAG usando ferramentas gratuitas e open-source, antes de investir em licencas Azure. Voce precisa construir um prototipo que ingira documentos, crie embeddings, armazene num vector store, e responda perguntas com base nos documentos.

**Ferramentas a utilizar:** Claude (chat) + GitHub Copilot

**Inputs fornecidos:**
- O cenario completo.
- Os documentos da NovaTech como arquivos individuais para ingestao (ver **Anexo A**, pasta `anexo-a-documentos-individuais/` - 5 arquivos .md, um por documento, prontos para processamento por scripts).
- Os chunks de referencia (ver **Anexo B**) - use o mapa de cobertura como gabarito para validar se o pipeline recupera os chunks corretos.
- Stack sugerida (todas gratuitas/open-source):
  - **Python** como linguagem.
  - **ChromaDB** como vector store local (`pip install chromadb`).
  - **sentence-transformers** para embeddings open-source (`pip install sentence-transformers` - modelo sugerido: `all-MiniLM-L6-v2`).
  - **LangChain** ou codigo manual para orquestracao (`pip install langchain`).
  - Para geracao: usar o **Claude** (via chat manual, nao via API) ou qualquer modelo local via **Ollama** (gratuito).
- Alternativa: se o participante preferir, pode usar outra stack free (FAISS em vez de ChromaDB, Ollama para embeddings locais, etc). O que importa e que funcione e seja gratuito.

**Tarefa:**
1. Usando o **GitHub Copilot**, implemente um pipeline de RAG minimo com estas etapas:
   - **Ingestao:** Um script que le os documentos do Anexo A (como texto), divide em chunks (defina a estrategia de chunking e justifique), gera embeddings, e armazena no ChromaDB.
   - **Busca:** Uma funcao que recebe uma pergunta, gera o embedding da pergunta, busca os N chunks mais similares no ChromaDB, e retorna os chunks com score de similaridade.
   - **Montagem de prompt:** Uma funcao que recebe os chunks recuperados e a pergunta, e monta o prompt completo (system prompt + chunks + pergunta) pronto para enviar ao LLM.
2. Teste o pipeline com ao menos 5 perguntas do mapa de cobertura do Anexo B. Para cada pergunta, documente: quais chunks foram recuperados, se sao os chunks corretos (compare com o gabarito), e o score de similaridade.
3. Usando o **Claude** (chat), cole o prompt montado pelo pipeline e obtenha a resposta. Avalie: esta correta? Citou fonte? Respeitou guardrails?
4. Identifique ao menos 2 problemas encontrados (ex: chunk errado recuperado, documento irrelevante no topo, chunking que cortou uma tabela no meio) e proponha correcoes.

**Entregavel:** O codigo do pipeline (com evidencia do Copilot), os resultados dos 5 testes com analise, e as propostas de correcao.
