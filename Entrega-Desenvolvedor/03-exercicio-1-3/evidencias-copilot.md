# Evidências de uso do GitHub Copilot

## Ferramenta utilizada
Implementação feita com **GitHub Copilot CLI** nesta sessão de terminal.

## Prompt principal usado para gerar o entregável
Resumo do pedido dado ao Copilot:

> Implementar o entregável completo do exercício 1.3 (Desenvolvedor), criando um protótipo local em Python com ingestão dos 5 documentos markdown, chunking justificado, embeddings open-source, armazenamento vetorial local, retrieval top-N, montagem de prompt, CLI, documentação e testes comparados ao gabarito do Anexo B.

## Artefatos gerados com apoio do Copilot
O Copilot foi usado para estruturar e refinar os seguintes arquivos:
- `run.py`
- `src\rag_prototype\config.py`
- `src\rag_prototype\markdown_loader.py`
- `src\rag_prototype\chunking.py`
- `src\rag_prototype\pipeline.py`
- `src\rag_prototype\cli.py`
- `src\rag_prototype\reporting.py`
- `src\rag_prototype\scenarios.py`
- `README.md`
- `avaliacao-respostas-llm.md`

## Ciclo real de geração → teste → refinamento

### Iteração 1
Após a primeira geração do pipeline, rodei:

```powershell
python .\run.py run-tests
```

Resultado observado:
- **2 cenários corretos**
- **1 parcial**
- **4 incorretos**

Principais falhas detectadas nessa rodada:
- tabelas markdown não estavam boas para embeddings;
- consultas curtas (“SLA Gold”, “multiplicador Sudeste”) recuperavam chunks errados;
- “Manaus” não puxava naturalmente a chunk de região Norte.

### Iteração 2
Com base no teste real, o Copilot foi usado para refinar o código com:
- **normalização de tabelas para texto semântico**;
- **reranqueamento híbrido** (embedding + TF-IDF + autoridade + versão preferida);
- **expansão de query** para casos como cidade → região;
- preservação da tabela original no texto final do chunk para manter rastreabilidade.

Nova execução:

```powershell
python .\run.py run-tests
```

Resultado observado:
- **6 cenários corretos**
- **1 parcial**
- **0 incorretos**

## Evidência objetiva de iteração
Essa diferença entre a primeira e a segunda execução mostra que o Copilot não foi usado só para “gerar boilerplate”; houve um ciclo real de:
1. gerar código,
2. executar,
3. analisar falhas,
4. refinar a solução,
5. revalidar.

## Saídas operacionais geradas
Como evidência adicional, o protótipo produziu:
- `artifacts\ingestion_manifest.json`
- `artifacts\test_results.json`
- `artifacts\prompt_exemplo_frete_manaus.txt`
- `artifacts\query_multiplicador_sudeste.json`
- `artifacts\prompt_multiplicador_sudeste.txt`
- `artifacts\prompt_devolucao_carga_perigosa.txt`
- `artifacts\prompt_sla_gold.txt`
- `artifacts\prompt_frete_manaus.txt`
- `artifacts\prompt_frete_salvador_300kg.txt`
- `artifacts\prompt_carga_danificada.txt`

Esses arquivos mostram que o código não ficou em nível de pseudocódigo: ele foi executado e gerou artefatos concretos.
