# Análise de problemas observados e correções propostas

## Contexto rápido
O protótipo final executou **7 cenários** do Anexo B com resultado agregado de **6 corretos, 1 parcial e 0 incorretos** (`resultados-testes.md`).

Durante a primeira iteração, o retrieval ficou bem pior (**2 corretos, 1 parcial, 4 incorretos**). O principal ajuste aplicado foi:
- **normalizar tabelas markdown em texto semântico** antes de gerar embeddings;
- **reranquear localmente** os chunks do ChromaDB com score híbrido (denso + lexical + metadados).

Esse ajuste já foi incorporado ao código final porque resolveu um problema real observado, especialmente nas perguntas de SLA e multiplicadores.

---

## Problema 1 — versões v1 e v2 da PROC-042 aparecem juntas

### Evidência
Nos cenários abaixo, a v1 continuou aparecendo junto da v2:
- **Cenário 4 — `Frete para 600kg para Manaus?`**
  - rank 1: `PROC-042v2-B` com similaridade `0.7084`
  - rank 2: `PROC-042-B` com similaridade `0.6785`
- **Cenário 5 — `Qual o multiplicador para o Sudeste?`**
  - rank 1: `PROC-042v2-B` com similaridade `0.6977`
  - rank 2: `PROC-042-B` com similaridade `0.6688`
- **Cenário 6 — `Frete para 300kg para Salvador?`**
  - rank 1: `PROC-042v2-B`
  - rank 2: `PROC-042-B`

### Risco
O LLM pode misturar multiplicadores antigos e novos na mesma resposta, exatamente a armadilha descrita no Anexo B.

### Correções propostas
1. **Filtro por vigência na família documental**  
   Armazenar metadados explícitos de vigência (`vigencia_inicio`, `vigencia_fim`, `substitui_documento`) e, no retrieval, privilegiar só a versão vigente por padrão.
2. **Deduplicação por família antes do prompt**  
   Se `PROC-042` e `PROC-042-v2` aparecerem juntas, manter apenas a mais nova, salvo quando a pergunta mencionar histórico, transição ou chamados anteriores a `01/12/2023`.
3. **Guardrail no prompt**  
   Instruir o LLM a nunca consolidar regras de duas versões diferentes sem explicitar o conflito.

---

## Problema 2 — perguntas sem cobertura ainda recebem chunks “plausíveis”

### Evidência
No **cenário 6 — `Frete para 300kg para Salvador?`**, o gabarito diz que **não há chunk formal aplicável**, porque a base só cobre frete especial acima de `500kg`.  
Mesmo assim, o protótipo recuperou:
- `PROC-042v2-B` (`0.6841`)
- `PROC-042-B` (`0.6487`)
- `PROC-042v2-C` (`0.5640`)

### Risco
Isso cria a ilusão de cobertura e incentiva o LLM a responder algo sobre frete especial, quando a resposta correta deveria ser “não encontrei documentação para frete padrão abaixo de 500kg”.

### Correções propostas
1. **Regra de abstenção / no-answer**  
   Criar um classificador simples de cobertura com limiar mínimo de confiança e diversidade de fontes.
2. **Filtro por regra de negócio estruturada**  
   Se a pergunta contiver peso `< 500kg`, evitar chunks da família `PROC-042*` como resposta final, porque a própria documentação define que ela é para frete especial.
3. **Resposta controlada quando só houver match parcial**  
   Se todos os chunks recuperados forem apenas parcialmente relevantes, o prompt deve forçar o modelo a responder com incerteza explícita.

---

## Problema 3 — FAQ informal ainda pode vencer documento normativo

### Evidência
No **cenário 2 — `Posso devolver carga perigosa?`**, o chunk correto (`POL-001-B`) foi recuperado, mas ficou em **rank 2**:
- rank 1: `FAQ-03` com similaridade `0.7553`
- rank 2: `POL-001-B` com similaridade `0.6279`

### Risco
Para regras críticas, o FAQ pode “contaminar” a resposta com uma exceção prática antes da regra formal (“não é elegível pelo processo padrão”).

### Correções propostas
1. **Re-rank por autoridade de fonte mais agressivo**  
   Separar as classes de fonte em:
   - normativo/contratual;
   - procedimento;
   - FAQ informal.
2. **Uso do FAQ só como complemento**  
   Em perguntas de política, compliance, SLA e cálculo, o FAQ só deveria entrar se já existir ao menos um chunk formal equivalente na seleção final.
3. **Campo de confiabilidade no prompt**  
   Passar para o LLM a classificação da fonte para que ele cite FAQ como observação operacional, nunca como base principal da regra.

---

## Priorização recomendada
1. **Primeiro:** resolver o conflito v1/v2 da `PROC-042`.  
2. **Segundo:** implementar abstenção para perguntas fora da cobertura documental.  
3. **Terceiro:** endurecer a priorização de autoridade para FAQ.

Essa ordem reduz diretamente o risco de resposta errada com alta confiança, que é o problema mais grave em produção.
