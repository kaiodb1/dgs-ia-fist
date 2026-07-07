# Evidência MCP

## Resumo

- Data/hora: 2026-07-07T19:57:03.740Z
- Pergunta de domínio usada no corpus: Qual o multiplicador para o Sudeste?

## filesystem-workspace

- Tools: read_file, read_text_file, read_media_file, read_multiple_files, write_file, edit_file, create_directory, list_directory, list_directory_with_sizes, directory_tree, move_file, search_files, get_file_info, list_allowed_directories
- Allowed directories:

```json
{
  "ok": true,
  "value": {
    "content": [
      {
        "type": "text",
        "text": "Allowed directories:\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\.mcp\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\deliverables\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\prompts\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\skills\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\specs\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\src\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\tests"
      }
    ],
    "structuredContent": {
      "content": "Allowed directories:\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\.mcp\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\deliverables\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\prompts\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\skills\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\specs\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\src\nC:\\Users\\kaiop\\Desktop\\Prática 2 - V2\\entrega-desenvolvedor\\novatech-assistant\\tests"
    }
  }
}
```

## filesystem-docs

- Tools: read_file, read_text_file, read_media_file, read_multiple_files, write_file, edit_file, create_directory, list_directory, list_directory_with_sizes, directory_tree, move_file, search_files, get_file_info, list_allowed_directories
- Exemplo de leitura do documento oficial:

```
# POL-001 — Política de Devolução de Mercadorias

**Versão:** 3.1
**Última atualização:** 15/01/2024
**Responsável:** Diretoria de Operações
**Classificação:** Documento normativo — uso obrigatório pelo time de atendimento

## 1. Objetivo

Esta política define as regras e procedimentos para devolução de mercadorias transportadas pela NovaTech, aplicável a todos os tipos de cliente e categorias de carga, salvo exceções explicitamente listadas na seção 3.

## 2. Escopo

Aplica-se a todas as devoluções solicitadas por clientes da NovaTech após a entrega da mercadoria. Não se aplica a mercadorias ainda em trânsito (para essas, consultar PROC-088: Procedimento de Interceptação de Carga).

## 3. Regras de Devolução

### 3.1. Prazo geral

O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking. A contagem de dia
...[truncated]
```

## filesystem-corpus

- Tools: read_file, read_text_file, read_media_file, read_multiple_files, write_file, edit_file, create_directory, list_directory, list_directory_with_sizes, directory_tree, move_file, search_files, get_file_info, list_allowed_directories
- Chunk recuperado para a pergunta "Qual o multiplicador para o Sudeste?":

```
Chunk PROC-042v2-B** — Seção 2.1: Multiplicadores regionais atualizados
> Multiplicadores regionais atualizados (novembro/2023): Sul 1.3, Sudeste 1.1, Centro-Oeste 1.4, Nordeste 1.5, Norte 1.8.
```

## git

- Tools: git_status, git_diff_unstaged, git_diff_staged, git_diff, git_commit, git_add, git_reset, git_log, git_create_branch, git_checkout, git_show, git_branch
- Exemplo de histórico/status:

```
Commit history:
Commit: 'bbdd03aeecd7e349a2bfc93849e0552a0b766ac6'
Author: <git.Actor "Trilha AI First <trilha@db1.local>">
Date: 2026-06-09 18:13:30+00:00
Message: 'chore: starter repo (Anexo D) — estrutura + dados semeados dos Anexos A e B\n'

```

## memory

- Tools: create_entities, create_relations, add_observations, delete_entities, delete_observations, delete_relations, read_graph, search_nodes, open_nodes
- Resources:

```json
{
  "ok": true,
  "value": {
    "resources": [
      {
        "name": "knowledge-graph",
        "title": "Knowledge Graph",
        "uri": "memory://knowledge-graph",
        "description": "The full knowledge graph with all entities and relations",
        "mimeType": "application/json"
      }
    ]
  }
}
```

## everything

- Tools: echo, get-annotated-message, get-env, get-resource-links, get-resource-reference, get-structured-content, get-sum, get-tiny-image, gzip-file-as-resource, toggle-simulated-logging, toggle-subscriber-updates, trigger-long-running-operation, simulate-research-query
- Resources: demo://resource/static/document/architecture.md, demo://resource/static/document/extension.md, demo://resource/static/document/features.md, demo://resource/static/document/how-it-works.md, demo://resource/static/document/instructions.md, demo://resource/static/document/startup.md, demo://resource/static/document/structure.md
- Prompts: simple-prompt, args-prompt, completable-prompt, resource-prompt
