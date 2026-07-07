# Saída registrada do Claude — Exercício 3.1

Trecho literal consolidado da revisão executada sobre `src/services/response-validator.ts`:

## Problemas encontrados

1. **O guardrail de "carga perigosa" era burlável por paráfrases**  
   Exemplos como `a carga classificada como perigosa pode ser devolvida` ou `cargas consideradas perigosas podem ser devolvidas` não eram capturados pelo matcher inicial.

2. **O regex de negativa não cobria conjugações comuns**  
   Formulações como `não podemos devolver` ou `a devolução não poderá ser feita` podiam ser tratadas como ausência de negativa explícita e gerar bloqueio indevido.

3. **A validação de `source_document` era estreita demais**  
   Placeholders semânticos como `null`, `undefined`, `sem fonte` ou `não encontrado` ainda passavam como fonte "útil".

## Correções aplicadas a partir da revisão

- expansão do reconhecimento de carga perigosa para sinônimos e paráfrases;
- detecção de negativa baseada em stems e contexto textual;
- rejeição semântica de placeholders de fonte em vez de uma lista mínima fixa.
