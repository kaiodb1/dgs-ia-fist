# Protótipo local de RAG — Exercício 1.3 (Desenvolvedor)

## Objetivo
Entregar uma prova de conceito local que:
- ingere os 5 documentos `.md` da NovaTech;
- faz chunking com sensibilidade a seções, listas e tabelas;
- gera embeddings com modelo open-source;
- persiste vetores localmente em ChromaDB;
- recupera top-N chunks por similaridade;
- monta um prompt pronto para colar em um LLM;
- executa cenários de teste baseados no Anexo B.

## Stack escolhida
- **Python 3.12**
- **ChromaDB** como vector store local persistente
- **sentence-transformers / all-MiniLM-L6-v2** para embeddings open-source
- **argparse + código manual** para orquestração (sem LangChain, para deixar o pipeline explícito)
- **Reranqueamento híbrido local** sobre os vetores persistidos (similaridade densa + TF-IDF + heurísticas de autoridade/versionamento)

## Estratégia de chunking
O chunking foi implementado por **seção markdown**, preservando:
1. **Cabeçalhos** (`##`, `###`) como fronteiras naturais.
2. **Tabelas markdown** como blocos indivisíveis, evitando cortar linhas no meio.
3. **Listas** como blocos completos, evitando separar passos de procedimento.
4. **Tabela de SLA** com uma heurística adicional: a seção é quebrada em subchunks temáticos (SLA geral, incidente crítico e linhas complementares), o que melhora a recuperação para perguntas sobre Gold/Silver/Standard.

Essa estratégia foi escolhida porque o corpus é pequeno, estruturado e com forte semântica por seção. Assim, o protótipo evita o anti-padrão de “512 tokens fixos sem justificativa”.

## Estratégia de retrieval
1. **Embeddings locais** com `all-MiniLM-L6-v2`.
2. **Persistência vetorial** em `artifacts\chroma_db`.
3. **Reranqueamento híbrido** para melhorar perguntas curtas e tabeladas:
   - score denso do embedding;
   - score lexical TF-IDF;
   - bônus por autoridade da fonte;
   - bônus para versão preferencial (`PROC-042-v2`);
   - pequenas expansões de query para casos como cidade → região (`Manaus` → `Norte`, `Salvador` → `Nordeste`).

O objetivo foi manter o armazenamento no ChromaDB, mas corrigir dois problemas típicos do corpus: tabelas em markdown “frias” para embeddings e ambiguidades entre versões de procedimento.

## Estrutura
```text
03-exercicio-1-3\
├── README.md
├── avaliacao-respostas-llm.md
├── requirements.txt
├── run.py
├── resultados-testes.md
├── analise-problemas-e-correcoes.md
├── evidencias-copilot.md
├── artifacts\
│   ├── chroma_db\
│   ├── ingestion_manifest.json
│   ├── model_cache\
│   ├── prompt_exemplo_frete_manaus.txt
│   └── test_results.json
└── src\
    └── rag_prototype\
        ├── cli.py
        ├── chunking.py
        ├── config.py
        ├── markdown_loader.py
        ├── models.py
        ├── pipeline.py
        ├── reporting.py
        └── scenarios.py
```

## Como executar
No diretório desta entrega:

```powershell
python -m pip install -r .\requirements.txt
python .\run.py ingest
python .\run.py query --question "Qual o multiplicador para o Sudeste?" --top-k 5
python .\run.py prompt --question "Frete para 600kg para Manaus?" --top-k 5 --output .\artifacts\prompt_exemplo_frete_manaus.txt
python .\run.py run-tests
```

## O que o protótipo grava localmente
- `artifacts\chroma_db\`: índice vetorial persistido
- `artifacts\model_cache\`: cache local do modelo de embeddings
- `artifacts\ingestion_manifest.json`: inventário da ingestão
- `artifacts\test_results.json`: resultados estruturados dos testes
- `artifacts\prompt_exemplo_frete_manaus.txt`: exemplo de prompt montado

## Limitações conhecidas
- O corpus é pequeno e foi tratado com heurísticas específicas para markdown; um pipeline corporativo precisaria lidar com PDFs, OCR e versionamento mais forte.
- O protótipo ainda não filtra automaticamente chunks contraditórios da `PROC-042` v1 quando a v2 também aparece.
- Ainda falta uma regra de **abstenção forte** para perguntas sem cobertura documental (ex.: frete padrão abaixo de 500kg).
- A geração final no LLM fica fora do código, mas foi executada e avaliada em `avaliacao-respostas-llm.md` usando o Copilot CLI como substituto prático do Claude.
