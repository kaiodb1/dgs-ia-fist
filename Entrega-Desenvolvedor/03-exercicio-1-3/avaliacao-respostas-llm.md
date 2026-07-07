# Avaliacao das respostas do LLM — Exercício 1.3

## Metodo adotado
- Ferramenta usada para a etapa de geracao: **GitHub Copilot CLI como substituto pratico do Claude**, conforme autorizacao explicita do usuario.
- Base de cada teste: **prompt montado automaticamente pelo pipeline** e salvo em `artifacts\prompt_*.txt`.
- Criterios de avaliacao por resposta:
  1. a resposta esta correta frente aos chunks recuperados e ao gabarito do Anexo B?;
  2. a resposta cita a fonte?;
  3. a resposta respeita os guardrails (nao inventar, explicitar conflito, abster-se quando faltar cobertura)?

## 1. Posso devolver carga perigosa?

**Prompt usado:** `artifacts\prompt_devolucao_carga_perigosa.txt`

**Resposta gerada**
> Nao pelo processo padrao. Cargas perigosas classificadas nas classes 1 a 6 da ANTT nao sao elegiveis para devolucao padrao [POL-001 | 3. Regras de Devolucao > 3.2. Excecoes ao prazo geral].  
> O FAQ recuperado so reforca que, na pratica, o caso pode receber tratamento especial pela area de Riscos, mas essa observacao e complementar e nao substitui a politica formal [FAQ-ATENDIMENTO | Item 3].  
> **Encaminhamento:** direcionar o caso para Gestao de Riscos (ramal 4500) [POL-001 | 3. Regras de Devolucao > 3.2. Excecoes ao prazo geral].

**Avaliacao**
- **Correta?** Sim.
- **Citou fonte?** Sim, com prioridade da fonte normativa.
- **Respeitou guardrails?** Sim. Nao inventou prazo e tratou o FAQ apenas como apoio operacional.

## 2. Qual o SLA do cliente Gold?

**Prompt usado:** `artifacts\prompt_sla_gold.txt`

**Resposta gerada**
> Para **chamados gerais**, cliente Gold tem **ate 2h uteis de primeira resposta** e **ate 24h uteis de resolucao** [SLA-2024 | 2. Tabela de SLAs].  
> Como os chunks recuperados tambem trazem o recorte de **incidentes criticos**, nesses casos o cliente Gold tem **ate 30min de primeira resposta** e **ate 4h de resolucao** [SLA-2024 | 2. Tabela de SLAs].

**Avaliacao**
- **Correta?** Sim.
- **Citou fonte?** Sim.
- **Respeitou guardrails?** Sim. A resposta separa chamados gerais de incidentes criticos e nao inventa tiers nem penalidades.

## 3. Frete para 600kg para Manaus?

**Prompt usado:** `artifacts\prompt_frete_manaus.txt`

**Resposta gerada**
> Os chunks recuperados trazem conflito entre a `PROC-042` v1 e a `PROC-042-v2`. Pela prioridade definida no prompt, a referencia principal e a versao mais recente, `PROC-042-v2`, que informa multiplicador **1.8** para a regiao Norte [PROC-042-v2 | 2. Formula de calculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)].  
> Para uma carga de **600kg**, a mesma versao informa **fator de peso 1.0** para a faixa de 500kg a 1.000kg [PROC-042-v2 | 2. Formula de calculo].  
> **Nao e possivel calcular o valor final** com seguranca porque o **valor base da rota** nao foi recuperado nos chunks [PROC-042-v2 | 2. Formula de calculo].

**Avaliacao**
- **Correta?** Sim.
- **Citou fonte?** Sim.
- **Respeitou guardrails?** Sim. Explicita o conflito, prioriza a versao mais nova e nao inventa preco final.

## 4. Frete para 300kg para Salvador?

**Prompt usado:** `artifacts\prompt_frete_salvador_300kg.txt`

**Resposta gerada**
> A base recuperada **nao cobre com seguranca** o frete para **300kg**. Os procedimentos recuperados tratam de **frete especial acima de 500kg**, entao eles nao bastam para responder sobre frete padrao abaixo desse limite [PROC-042-v2 | 2. Formula de calculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)] [PROC-042 | 2. Formula de calculo > 2.1. Multiplicadores regionais].  
> **Encaminhamento:** consultar a documentacao de frete padrao ou validar com a area responsavel antes de orientar o cliente.

**Avaliacao**
- **Correta?** Sim, e este e um dos testes mais importantes do conjunto.
- **Citou fonte?** Sim.
- **Respeitou guardrails?** Sim. A resposta nao usa chunks parcialmente relevantes para fingir cobertura documental.

## 5. Qual o multiplicador para o Sudeste?

**Prompt usado:** `artifacts\prompt_multiplicador_sudeste.txt`

**Resposta gerada**
> Ha conflito entre as versoes recuperadas. A `PROC-042-v2` informa multiplicador **1.1** para o Sudeste [PROC-042-v2 | 2. Formula de calculo > 2.1. Multiplicadores regionais (atualizados em novembro/2023)], enquanto a `PROC-042` v1 informa **1.0** [PROC-042 | 2. Formula de calculo > 2.1. Multiplicadores regionais].  
> Pela hierarquia do prompt, a referencia principal deve ser a versao mais recente, entao o valor a usar como padrao e **1.1**, com observacao de que contratos ou situacoes de transicao podem exigir validacao adicional.

**Avaliacao**
- **Correta?** Sim.
- **Citou fonte?** Sim.
- **Respeitou guardrails?** Sim. Expos o conflito em vez de consolidar silenciosamente informacoes contraditorias.

## 6. O que acontece com carga danificada?

**Prompt usado:** `artifacts\prompt_carga_danificada.txt`

**Resposta gerada**
> A base recuperada traz principalmente uma orientacao **informal** do FAQ: registrar a ocorrencia em ate **48h** apos o recebimento, com fotos e laudo se possivel, e encaminhar para `sinistros@novatech.com.br` [FAQ-ATENDIMENTO | Item 38].  
> Como essa informacao vem de **FAQ informal**, ela deve ser tratada como apoio operacional e nao como politica normativa completa. Entre os chunks recuperados, a fonte formal mais proxima so confirma que avaria em transito gera devolucao sem custo para o cliente, mas nao descreve o fluxo completo [POL-001 | 3. Regras de Devolucao > 3.5. Custos de devolucao].  
> **Encaminhamento:** orientar o registro do caso com cautela e validar o procedimento formal com a area responsavel.

**Avaliacao**
- **Correta?** Parcialmente correta e prudente.
- **Citou fonte?** Sim.
- **Respeitou guardrails?** Sim. O ponto forte aqui foi explicitar que a base principal e informal e que a cobertura formal esta incompleta.

## Conclusao da etapa de geracao
O pipeline nao ficou restrito a retrieval. Ele tambem montou prompts utilizaveis e sustentou respostas que:
- citam fonte;
- respeitam conflito entre versoes;
- rejeitam responder com seguranca quando a base nao cobre o caso;
- e tratam FAQ informal como apoio, nao como verdade normativa principal.

O melhor resultado apareceu nos cenarios em que a resposta depende de **restricao explicita** (carga perigosa), **dado contratual tabular** (SLA Gold) ou **abstencao por falta de cobertura** (frete de 300kg). O risco residual continua sendo a presenca simultanea de `PROC-042` v1 e v2 no topo do retrieval, ponto ja coberto em `analise-problemas-e-correcoes.md`.
