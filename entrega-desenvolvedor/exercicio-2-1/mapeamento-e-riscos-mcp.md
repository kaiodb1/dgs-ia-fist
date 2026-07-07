# Exercício 2.1 — Mapeamento MCP, least privilege e riscos

## Mapeamento necessidade -> server local

| Necessidade do projeto | Server | O que expõe | Quem consome | Escopo configurado | Justificativa de least privilege |
|---|---|---|---|---|---|
| Ler/escrever código, specs, prompts, testes, skills e a própria config MCP | `filesystem-workspace` | Ferramentas de filesystem (listar, ler, escrever, editar, mover, buscar) | Dev, Tech Lead, QA e agentes de implementação | `.mcp`, `deliverables`, `prompts`, `skills`, `specs`, `src`, `tests` | Evita expor o repositório inteiro, `.git`, documentos de negócio e corpus RAG ao mesmo server de escrita. |
| Ler documentação de negócio oficial da NovaTech | `filesystem-docs` | Ferramentas de filesystem, usadas apenas em modo leitura | Agentes de atendimento, Product Specialist, Dev, QA | `docs/novatech` | Restringe o acesso a somente a fonte normativa do domínio. O diretório é isolado do restante do repo para não misturar leitura de negócio com escrita de código. |
| Ler o corpus de chunks do RAG | `filesystem-corpus` | Ferramentas de filesystem, usadas apenas em modo leitura | Agentes de retrieval/prompting e testes de domínio | `data/retrieval-corpus` | O corpus fica separado da documentação fonte e do código. Isso reduz risco de um agente alterar a base usada nos testes de retrieval. |
| Ler histórico, branches, diff e estado do repositório | `git` | Ferramentas do server Git (histórico, status, diff, branches/tags, show) | Dev, Tech Lead e agentes de revisão | Repositório local `novatech-assistant` | Resolve histórico/branches sem depender de GitHub remoto, token ou serviço externo. |
| Persistir linguagem ubíqua e decisões recorrentes | `memory` | Resource `memory://knowledge-graph` + tools de criação/edição de entidades, relações e observações | Agentes multi-etapa do projeto | Arquivo local `deliverables/desenvolvedor/evidencias/memory/memory.jsonl` | A memória fica local e versionável na pasta de evidências, sem vazar para serviços externos. |
| Explorar recursos do protocolo e validar comportamento do cliente | `everything` | Tools, resources e prompts de exemplo do protocolo MCP | Mantenedores do setup MCP | Sem acesso ao repo | Server de aprendizado/diagnóstico; não recebe nenhum path do projeto. |

## Decisão para as fontes somente leitura

Os paths `docs/novatech` e `data/retrieval-corpus` ficam em **instâncias separadas** do server `filesystem` para evitar mistura com o server de escrita do workspace.

Como o reference server de filesystem via `npx` não oferece flag nativa de read-only por path em Windows, a mitigação concreta desta entrega é:

1. manter docs e corpus em servers dedicados;
2. usar apenas ferramentas com `readOnlyHint=true` nesses servers;
3. aplicar proteção local de escrita nos dois diretórios antes da execução da evidência real.

## Riscos de segurança do setup local e mitigação

### 1. Exposição acidental de segredos por escopo amplo no filesystem

- **Risco:** se o server de escrita apontar para a raiz do repositório, o agente pode acessar `.git`, arquivos temporários, configs locais ou futuros `.env`.
- **Mitigação:** separar `filesystem-workspace` em paths explícitos e não expor a raiz inteira.

### 2. Alteração indevida da documentação oficial ou do corpus de avaliação

- **Risco:** um agente com write access em `docs/novatech` ou `data/retrieval-corpus` pode contaminar a fonte de verdade do domínio ou o corpus usado nos testes.
- **Mitigação:** usar servers dedicados para leitura e endurecer permissão local de escrita nesses diretórios antes da demonstração.

### 3. Vazamento de contexto sensível via histórico Git

- **Risco:** commits e mensagens podem carregar detalhes internos que não deveriam ser copiados automaticamente para prompts externos.
- **Mitigação:** manter o server Git somente no repositório local, sem remotos configurados, e revisar o conteúdo de commits antes de persisti-lo no histórico.

### 4. Memória persistente armazenar fatos errados ou obsoletos

- **Risco:** o knowledge graph local pode guardar decisões antigas e influenciar respostas futuras de forma incorreta.
- **Mitigação:** usar a memória só para linguagem ubíqua/decisões estáveis, registrar origem das observações e limpar fatos desatualizados nas revisões do projeto.

## Evidências geradas nesta entrega

- Configuração final: `.mcp/mcp.json`
- Endurecimento local das pastas somente leitura:
  - `deliverables/desenvolvedor/evidencias/mcp/set-readonly-sources.ps1`
  - `deliverables/desenvolvedor/evidencias/mcp/readonly-setup.log`
  - `deliverables/desenvolvedor/evidencias/mcp/readonly-write-check.log`
- Execução real dos servers e leitura via MCP:
  - `deliverables/desenvolvedor/evidencias/mcp/mcp-evidence.md`
  - `deliverables/desenvolvedor/evidencias/mcp/mcp-evidence.json`
