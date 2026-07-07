# Registro de prompts usados no Copilot

## Exercício 3.1

1. `Defina um schema Zod strict para { answer, source_document, confidence_score } e rejeite campos extras.`
2. `Implemente src/services/response-validator.ts para validar o structured output, aplicar os dois guardrails do cenário e devolver fallback seguro quando houver falha.`
3. `Refine o validator após o code review: cubra paráfrases de carga perigosa, conjugação de negativas e placeholders semânticos de source_document.`

## Exercício 3.2

1. `Reescreva o feedback handler em TypeScript strict usando Zod na fronteira, pino para logging e imports estáticos.`
2. `Remova console.log, require dinâmico e qualquer log de attendantEmail; mantenha o handler testável com injeção de dependências.`
3. `Adicione testes Vitest para garantir que attendantEmail não seja persistido nem logado e que payload inválido retorne 400.`
