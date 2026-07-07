# Exercício 2.2 — Revisão crítica do código gerado

## Resumo

A primeira implementação cobre corretamente o contrato HTTP inicial do endpoint, mas o trabalho exigiu revisão crítica real em cima do código/testes gerados. Abaixo estão os principais pontos encontrados.

## Pontos encontrados

| Ponto | Impacto | Ação |
|---|---|---|
| O harness de teste usava `body` como string crua no `HttpRequest` do `@azure/functions`. Em modo de teste, o pacote espera `body.string` ou `body.bytes`. | Requisições válidas caiam falsamente em `INVALID_JSON`, mascarando defeitos reais do handler. | Corrigido em `tests/unit/functions/query/handler.test.ts` para usar `body: { string: ... }`. |
| O registro `app.http()` rejeitou `["POST"] as const` porque a API espera `HttpMethod[]` mutável. | O build quebrava mesmo com a lógica do endpoint correta. | Corrigido em `src/functions/query/handler.ts` com tipagem explícita `HttpMethod[]`. |
| O endpoint ainda não limita tamanho de payload nem emite um correlation/request id explícito nos logs. | Antes das tasks de integração com Azure, troubleshooting e proteção contra payload excessivo ainda ficam fracos para produção. | Mantido como ajuste pendente para a próxima iteração do endpoint (idealmente junto com config/env e retry das integrações). |
| O `handler.ts` hoje acumula validação e resposta-placeholder no mesmo arquivo. | Se as próximas tasks forem adicionadas diretamente ali, o arquivo tende a crescer e misturar orchestration com integração. | Próxima etapa deve introduzir um serviço de aplicação para manter o handler fino quando search/completion entrarem. |

## Conclusão

Os dois primeiros pontos foram defeitos concretos encontrados durante a implementação e já corrigidos. Os dois últimos são ajustes reais que eu exigiria antes de considerar o endpoint pronto para um code review de produção.
