# Entrega — Papel Desenvolvedor / Cenario 1

Esta pasta concentra todos os artefatos gerados para a pratica do papel **Desenvolvedor** no **Cenario 1 — Fase de Entendimento e Contexto**.

## Estrutura

| Pasta | Conteudo |
|---|---|
| `01-exercicio-1-1\` | Analise tecnica de viabilidade, iteracao em formato de transcricao e evidencias de aderencia a rubrica |
| `02-exercicio-1-2\` | System prompts v1/v2, mapa de contexto, testes em duas rodadas e evidencias |
| `03-exercicio-1-3\` | Prototipo local de RAG em Python, resultados de retrieval, prompts montados, avaliacao das respostas do LLM e evidencias |
| `04-avaliacao\` | Insumos de avaliacao (foundation, rubricas, prompt padrao e enunciado consolidado) e avaliacoes finais |
| `05-consolidado\` | Arquivos de fechamento e sintese final da entrega |

## Principais entregaveis por exercicio

### Exercicio 1.1
- `01-exercicio-1-1\analise-tecnica-final.md`
- `01-exercicio-1-1\transcricao-iteracao.md`
- `01-exercicio-1-1\evidencias.md`

### Exercicio 1.2
- `02-exercicio-1-2\system-prompt-v1.md`
- `02-exercicio-1-2\system-prompt-v2.md`
- `02-exercicio-1-2\mapa-contexto-e-analise.md`
- `02-exercicio-1-2\transcricao-testes.md`
- `02-exercicio-1-2\evidencias.md`

### Exercicio 1.3
- `03-exercicio-1-3\README.md`
- `03-exercicio-1-3\requirements.txt`
- `03-exercicio-1-3\run.py`
- `03-exercicio-1-3\resultados-testes.md`
- `03-exercicio-1-3\avaliacao-respostas-llm.md`
- `03-exercicio-1-3\analise-problemas-e-correcoes.md`
- `03-exercicio-1-3\evidencias-copilot.md`

## Validacoes executadas
- Montagem dos artefatos textuais dos exercicios 1.1 e 1.2 com revisao critica frente a rubrica.
- Execucao do prototipo do exercicio 1.3 com:
  - `python .\run.py run-tests`
  - `python .\run.py query --question "Qual o multiplicador para o Sudeste?" --top-k 5`
  - `python .\run.py prompt --question "..."`

## Observacao sobre Claude
Onde o enunciado exigia uso do **Claude**, foi usado o **GitHub Copilot CLI como substituto pratico**, conforme autorizacao explicita do usuario, e essa premissa foi registrada nos entregaveis e nas evidencias.
