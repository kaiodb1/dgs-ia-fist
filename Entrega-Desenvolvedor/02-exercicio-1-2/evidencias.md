# Evidências do exercício 1.2

## 1. Premissa operacional adotada
Conforme a autorização explícita do usuário, usei **GitHub Copilot CLI como substituto prático do Claude** e registrei as interações em **formato de transcrição**.

## 2. Fontes consultadas
- `C:\Users\kaiop\Desktop\Prática 1\Prática 1\exercicio-fase-1-entendimento.md`
- `C:\Users\kaiop\Desktop\Prática 1\Prática 1\anexo-b-chunks-referencia-rag.md`
- `C:\Users\kaiop\Desktop\Prática 1\Correção\cenario-1-avaliacao-desenvolvedor.md`
- `C:\Users\kaiop\Desktop\Prática 1\Correção\cenario-1-avaliacao-foundation.md`

## 3. Artefatos gerados
- `system-prompt-v1.md` — primeira versão do prompt.
- `system-prompt-v2.md` — versão iterada com melhorias materiais.
- `transcricao-testes.md` — duas rodadas de perguntas/respostas com os três cenários obrigatórios.
- `mapa-contexto-e-analise.md` — anatomia do contexto, estimativa de tokens e análise crítica.
- `evidencias.md` — este arquivo, com rastreabilidade dos requisitos.

## 4. Protocolo de iteração executado
1. Leitura do enunciado do exercício 1.2 e da rubrica de correção.
2. Leitura do Anexo B para identificar os chunks corretos e as armadilhas intencionais.
3. Escrita do **system prompt v1** com foco em grounding, citação e fallback.
4. Teste da v1 com as 3 perguntas obrigatórias:
   - devolução para carga perigosa;
   - SLA de resolução para cliente Gold;
   - frete para 600kg com destino Manaus.
5. Análise crítica das falhas da v1 contra chunks e guardrails.
6. Escrita do **system prompt v2** com melhorias explícitas.
7. Repetição dos 3 testes com a v2.
8. Consolidação das conclusões e da anatomia de contexto.

## 5. Matriz requisito → evidência

| Requisito do usuário | Evidência |
|---|---|
| Prompt completo v1 e v2 em português | `system-prompt-v1.md` e `system-prompt-v2.md` |
| Seções claras: identidade, regras, formato, chunks | Ambos os arquivos de prompt, no bloco `Prompt completo` |
| Contexto estático vs dinâmico + tokens | `mapa-contexto-e-analise.md`, seção 2 |
| 3 perguntas testadas em duas rodadas | `transcricao-testes.md`, rodadas 1 e 2 |
| Análise crítica de cada resposta | `mapa-contexto-e-analise.md`, seção 3 |
| Capturar armadilha de carga perigosa | `mapa-contexto-e-analise.md`, seções 3.1 e 3.2 |
| Capturar limitação do custo de frete sem tarifa base | `mapa-contexto-e-analise.md`, seções 3.1 e 3.2 |
| Evidência do uso do Copilot CLI como substituto do Claude | `transcricao-testes.md` (método) + este arquivo |
| Melhoria material da v2 | `system-prompt-v2.md` (melhorias centrais) + `mapa-contexto-e-analise.md`, seção 3.4 |

## 6. Principais correções aplicadas na v2
- Regra explícita de que **exceções/proibições prevalecem sobre a regra geral**.
- Guardrail fixo para **carga perigosa**: não elegível para devolução padrão + encaminhamento à **Gestão de Riscos**.
- Regra de **completude de fórmula** para perguntas de custo: sem valor base, sem preço final.
- Estrutura de resposta mais auditável: `Resposta objetiva`, `Limites/condições`, `Fonte(s)` e `Encaminhamento`.
- Hierarquia de fontes: **POL/PROC/SLA > FAQ > histórico**.

## 7. Conclusão de evidência
O exercício foi tratado como um artefato de engenharia de prompt versionado e testado. A v1 não foi aceita de forma acrítica: ela falhou nos dois pontos mais perigosos do cenário (carga perigosa e custo de frete com contexto incompleto), e a v2 foi redesenhada especificamente para corrigir essas falhas.
