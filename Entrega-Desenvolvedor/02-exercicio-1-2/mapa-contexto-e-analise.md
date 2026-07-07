# Mapa de contexto e análise crítica

## 1. Escopo e método
Exercício: **Desenvolvedor 1.2 — Prototipação de prompt com engenharia de contexto**.  
Ambiente adotado: **Copilot CLI como substituto prático do Claude**, conforme premissa aprovada.  
Objetivo: versionar um `system prompt`, separar contexto estático de contexto dinâmico, testar com 3 perguntas reais do cenário NovaTech e iterar a partir das falhas observadas.

---

## 2. Anatomia do contexto

### 2.1 Ordem recomendada de composição por query
1. **System prompt estático**  
   Identidade, hierarquia de fontes, guardrails e formato de resposta.
2. **Metadados dinâmicos da query**  
   Tipo da pergunta, tier do cliente (quando houver), observações de risco.
3. **Chunks recuperados**  
   Ordenados por autoridade e risco: exceções/proibições antes de regra geral.
4. **Pergunta atual do atendente**  
   Curta e explícita.
5. **Histórico resumido (opcional)**  
   Só quando realmente necessário; prioridade menor que os chunks atuais.

### 2.2 Regra de poda quando o contexto crescer
- Remover primeiro o **histórico**.
- Remover depois FAQs de **baixa autoridade**.
- **Nunca** remover o chunk formal que contém uma exceção crítica (ex.: carga perigosa não elegível).
- Em perguntas com risco regulatório ou financeiro, manter a resposta curta e exigir dados faltantes em vez de alongar contexto.

### 2.3 Mapa estático vs. dinâmico com estimativa de tokens

> Heurística usada: **tokens ≈ palavras / 0,75**. São estimativas de engenharia, não contagem exata de tokenizer.  
> Contagem observada do prompt completo: **v1 ≈ 373 tokens** e **v2 ≈ 671 tokens**.

| Parte | Tipo | Conteúdo | Estimativa v1 | Estimativa v2 | Observações |
|---|---|---|---:|---:|---|
| Preâmbulo e objetivo geral | Estático | Missão do assistente e escopo da query | ~60 tokens | ~55 tokens | Curto, mas útil para ancorar o papel |
| Identidade e papel | Estático | Quem é o assistente, público-alvo, objetivo operacional | ~45 tokens | ~50 tokens | v2 reforça uso interno e auditabilidade |
| Hierarquia + regras e guardrails | Estático | Não inventar, conflito, exceções, fallback | ~130 tokens | ~350 tokens | v2 adiciona precedência de exceção, carga perigosa e cálculo incompleto |
| Formato de resposta | Estático | Estrutura de saída | ~40 tokens | ~50 tokens | v2 força campos de limites e encaminhamento |
| Instruções de uso dos chunks + tom | Estático | Como ler, combinar e priorizar contexto | ~100 tokens | ~165 tokens | v2 formaliza hierarquia e conflito |
| **Total do system prompt** | **Estático** | **Prompt completo por query** | **~375 tokens** | **~670 tokens** | Continua baixo; custo extra é justificável pelo ganho de segurança |
| Metadados da query | Dinâmico | Tipo de pergunta, tier, flags | ~15-40 tokens | ~15-40 tokens | Não usei nos testes, mas faz parte do design de produção |
| Pergunta do atendente | Dinâmico | Ex.: "Qual o prazo..." | ~10-18 tokens | ~10-18 tokens | Muito barata em tokens |
| Chunks de devolução | Dinâmico | POL-001-A + POL-001-B | ~95 + ~165 = ~260 tokens | ~260 tokens | Caso mais sensível; manter a exceção acima do prazo geral |
| Chunk de SLA | Dinâmico | SLA-2024-B | ~60 tokens | ~60 tokens | Contexto simples e suficiente |
| Chunk de frete | Dinâmico | Chunk C / PROC-042-v2 seção 2 | ~60 tokens | ~60 tokens | Deliberadamente insuficiente para custo final, porque não traz a tarifa base |
| Histórico resumido | Dinâmico | Último turno ou resumo curto | 0 nos testes; teto ~120 tokens | 0 nos testes; teto ~120 tokens | Deve ser a primeira peça podada |

### 2.4 Leitura prática do orçamento
Mesmo com a v2, a montagem de contexto dos testes ficou em algo entre **~760 e ~1.000 tokens totais por query**, muito abaixo da janela de 128K. O ponto aqui não é capacidade bruta, e sim **qualidade da ordem e da prioridade**:
- Se o chunk da exceção vier diluído atrás do prazo geral, a resposta tende a começar pela regra errada.
- Se a instrução disser "responda com o melhor dado disponível", o modelo pode completar lacunas com excesso de confiança.
- Em perguntas numéricas, um único chunk parcial já é suficiente para induzir uma resposta errada se o prompt não exigir **completude da fórmula**.

---

## 3. Análise crítica das respostas

### 3.1 Gabarito esperado por pergunta

| Pergunta | Comportamento esperado |
|---|---|
| Qual o prazo de devolução para carga perigosa? | Dizer explicitamente que **não é elegível para devolução padrão** e encaminhar para **Gestão de Riscos (ramal 4500)**. Não inventar nem reaproveitar o prazo geral de 7 dias. |
| Meu cliente é Gold, qual o SLA de resolução? | Informar **24h úteis** para chamados gerais, com citação de **SLA-2024-B**. |
| Quanto custa o frete para 600kg para Manaus? | Com o chunk fornecido, só é possível afirmar que o frete especial usa **valor base × multiplicador regional** e que, para a região Norte/Manaus, o multiplicador é **1,8**. O **preço exato não pode ser calculado** sem o valor base da rota. |

### 3.2 Comparativo v1 vs. v2

| Pergunta | Avaliação da v1 | Julgamento crítico | Avaliação da v2 | Julgamento crítico |
|---|---|---|---|---|
| Prazo de devolução para carga perigosa | **Inadequada** | A resposta abriu com "7 dias úteis", apesar de o chunk **POL-001-B** dizer que carga perigosa **não é elegível** para devolução padrão. Houve mistura de regra geral com exceção, sem dizer "não pode no fluxo padrão". Também perdeu o encaminhamento explícito para Gestão de Riscos. | **Correta** | A v2 responde pela exceção primeiro, nega a elegibilidade no fluxo padrão e encaminha para Gestão de Riscos. Esse é exatamente o comportamento pedido pela rubrica. |
| SLA de resolução do cliente Gold | **Adequada, mas simples demais** | O conteúdo central está certo (24h úteis), porém a citação ficou genérica ("SLA-2024"). Em produção, vale exigir citação granular de chunk/seção. | **Correta** | Mantém a resposta curta, cita **SLA-2024-B** e não extrapola para incidente crítico, já que isso não foi perguntado nem recuperado. |
| Custo do frete para 600kg para Manaus | **Inadequada por completude** | A resposta menciona o multiplicador 1,8, mas não declara a limitação principal: **falta o valor base**, então o preço final não pode ser dado. Isso viola o guardrail "não inventar valores". Mesmo sem chutar um número em reais, a resposta trata a pergunta "quanto custa" como se estivesse suficientemente respondida. | **Correta** | A v2 admite insuficiência de contexto e responde só com o que está documentado: multiplicador regional 1,8. Faz a ressalva crítica de que o valor base da rota está ausente. |

### 3.3 Falhas-raiz identificadas na v1
1. **A instrução "responda com o melhor dado disponível" era permissiva demais.**  
   Em vez de proteger contra alucinação, ela incentivava respostas "meio certas" em perguntas que exigiam resposta binária (pode/não pode) ou cálculo completo.

2. **Não havia precedência explícita de exceção sobre regra geral.**  
   Isso ficou evidente no caso de carga perigosa: o modelo viu "7 dias úteis" e "não elegível" ao mesmo tempo, mas sem uma regra forte priorizou o prazo geral.

3. **Faltava política clara para dados numéricos incompletos.**  
   O caso do frete mostrou que um chunk parcial pode induzir uma resposta aparentemente útil, porém incompleta para a pergunta feita.

4. **A hierarquia de autoridade entre fontes não estava formalizada.**  
   A v1 falava em "fontes" genericamente; a v2 passa a separar documento formal de FAQ, reduzindo risco de usar orientação informal como regra.

### 3.4 O que mudou materialmente da v1 para a v2
- **Exceção antes da regra geral** deixou de ser implícito e virou regra explícita.
- **Carga perigosa** passou a ter um guardrail estático de alto risco: não elegível + Gestão de Riscos.
- **Perguntas de custo** passaram a exigir todas as variáveis da fórmula; sem isso, a resposta correta é declarar insuficiência.
- **Formato de saída** ganhou os campos `Limites/condições` e `Encaminhamento`, o que força o modelo a externalizar incerteza e próxima ação.
- **Hierarquia de fontes** foi explicitada: documentos formais (POL/PROC/SLA) acima de FAQ e histórico.

---

## 4. O que o prompt resolve e o que o produto deve validar fora do prompt

### 4.1 Enforcements probabilísticos (via prompt)
- Responder em português formal e acessível.
- Citar a fonte usada.
- Priorizar exceção sobre regra geral.
- Não dar preço exato sem fórmula completa.
- Diferenciar documento formal de FAQ.

### 4.2 Enforcements determinísticos recomendados no produto

| Regra | Como validar fora do prompt |
|---|---|
| Toda resposta deve citar fonte | Regex simples exigindo `Fonte:` ou `Fonte(s):` + identificador de documento |
| Pergunta sobre carga perigosa | Se a pergunta contiver `carga perigosa`, falhar a resposta que não contenha simultaneamente ideia de **não elegibilidade** + **Gestão de Riscos** |
| Pergunta de custo com contexto incompleto | Se a resposta trouxer valor final ou `R$` sem `valor base` presente nos chunks recuperados, bloquear ou sinalizar |
| Tier não documentado | Se a pergunta mencionar tier fora de `Gold/Silver/Standard`, exigir resposta negativa ou escalonamento |

Essa separação é importante: **prompt reduz risco, mas não substitui validação de aplicação**.
