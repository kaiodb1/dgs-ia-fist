# Transcrição de testes — Copilot CLI como substituto do Claude

## Método de teste
- Ferramenta usada: GitHub Copilot CLI, conforme a premissa aprovada pelo usuário para substituir o Claude no exercício.
- Cada rodada foi pensada como uma conversa limpa: `system prompt` + chunks dinâmicos da consulta + pergunta do atendente.
- Para isolar o comportamento do prompt, não usei histórico de conversa nas rodadas abaixo.
- Os chunks reproduzem o enunciado e o Anexo B/gabarito do exercício; no caso do frete, o contexto foi propositalmente limitado à regra geral do frete especial + multiplicador regional, sem tarifa base da rota, para testar alucinação por lacuna de dados.

---

## Rodada 1 — system prompt v1

### Teste 1 — "Qual o prazo de devolução para carga perigosa?"

**Chunks injetados**
- **POL-001-A**: "O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking."
- **POL-001-B**: "As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão: Cargas perigosas classificadas nas classes 1 a 6 da ANTT (...) Para essas categorias, o cliente deve entrar em contato com o setor de Gestão de Riscos (ramal 4500) para tratamento individual."

**Pergunta**
> Qual o prazo de devolução para carga perigosa?

**Resposta gerada (v1)**
> Resposta: O prazo geral de devolução é de até 7 dias úteis após o recebimento. Em casos de carga perigosa, a documentação indica tratamento individual pelo setor responsável.  
> Base documental: POL-001-A e POL-001-B.  
> Observação: Oriente o cliente a abrir o caso para análise específica.

### Teste 2 — "Meu cliente é Gold, qual o SLA de resolução?"

**Chunks injetados**
- **SLA-2024-B**: "SLAs para chamados gerais — Gold: resposta em até 2h úteis, resolução em até 24h úteis. Silver: resposta em até 4h úteis, resolução em até 48h úteis. Standard: resposta em até 8h úteis, resolução em até 72h úteis."

**Pergunta**
> Meu cliente é Gold, qual o SLA de resolução?

**Resposta gerada (v1)**
> Resposta: Para cliente Gold, o SLA de resolução é de até 24h úteis.  
> Base documental: SLA-2024.  
> Observação: Nenhuma.

### Teste 3 — "Quanto custa o frete para 600kg para Manaus?"

**Chunks injetados**
- **Chunk C do exercício / PROC-042-v2, seção 2**: "Frete especial para cargas acima de 500kg: valor base × multiplicador regional. Região Sul: 1.3. Região Sudeste: 1.1. Região Norte: 1.8. Região Nordeste: 1.5. Região Centro-Oeste: 1.4."

**Pergunta**
> Quanto custa o frete para 600kg para Manaus?

**Resposta gerada (v1)**
> Resposta: Para Manaus, o frete especial usa multiplicador regional 1,8 sobre o valor base. Como a carga tem 600kg, aplica-se a regra de frete especial acima de 500kg.  
> Base documental: PROC-042-v2, seção 2 (chunk C).  
> Observação: Nenhuma.

**Resumo da rodada 1**
- 1 resposta adequada no conteúdo principal (SLA Gold).
- 2 respostas inadequadas por falta de precedência da exceção e por excesso de confiança com dado incompleto.

---

## Rodada 2 — system prompt v2

### Teste 1 — "Qual o prazo de devolução para carga perigosa?"

**Chunks injetados**
- **POL-001-A**: "O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking."
- **POL-001-B**: "As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão: Cargas perigosas classificadas nas classes 1 a 6 da ANTT (...) Para essas categorias, o cliente deve entrar em contato com o setor de Gestão de Riscos (ramal 4500) para tratamento individual."

**Pergunta**
> Qual o prazo de devolução para carga perigosa?

**Resposta gerada (v2)**
> Resposta objetiva: Carga perigosa classes 1 a 6 da ANTT não é elegível para devolução pelo processo padrão; portanto, o prazo geral de 7 dias úteis não se aplica a esse caso.  
> Limites/condições: O tratamento é individual para esse tipo de carga.  
> Fonte(s): POL-001-B; apoio contextual de POL-001-A para o prazo geral que não se aplica aqui.  
> Encaminhamento: Direcionar o caso para Gestão de Riscos (ramal 4500).

### Teste 2 — "Meu cliente é Gold, qual o SLA de resolução?"

**Chunks injetados**
- **SLA-2024-B**: "SLAs para chamados gerais — Gold: resposta em até 2h úteis, resolução em até 24h úteis. Silver: resposta em até 4h úteis, resolução em até 48h úteis. Standard: resposta em até 8h úteis, resolução em até 72h úteis."

**Pergunta**
> Meu cliente é Gold, qual o SLA de resolução?

**Resposta gerada (v2)**
> Resposta objetiva: Para chamados gerais de cliente Gold, o SLA de resolução é de até 24h úteis.  
> Limites/condições: Nenhum.  
> Fonte(s): SLA-2024-B.  
> Encaminhamento: Nenhum.

### Teste 3 — "Quanto custa o frete para 600kg para Manaus?"

**Chunks injetados**
- **Chunk C do exercício / PROC-042-v2, seção 2**: "Frete especial para cargas acima de 500kg: valor base × multiplicador regional. Região Sul: 1.3. Região Sudeste: 1.1. Região Norte: 1.8. Região Nordeste: 1.5. Região Centro-Oeste: 1.4."

**Pergunta**
> Quanto custa o frete para 600kg para Manaus?

**Resposta gerada (v2)**
> Resposta objetiva: Não é possível calcular o custo exato com segurança apenas com o contexto recuperado. O que a documentação confirma é que Manaus, por estar na região Norte, usa multiplicador regional 1,8 no frete especial.  
> Limites/condições: Falta o valor base da rota; sem esse dado, o preço final não pode ser informado com segurança.  
> Fonte(s): PROC-042-v2, seção 2 (chunk C).  
> Encaminhamento: Consultar a tarifa base da rota antes de fechar o cálculo.

**Resumo da rodada 2**
- 3 respostas adequadas ao contexto disponível.
- A v2 ficou mais conservadora e auditável.
- O ganho principal foi impedir que o modelo "complete" a resposta quando a documentação recuperada não basta.
