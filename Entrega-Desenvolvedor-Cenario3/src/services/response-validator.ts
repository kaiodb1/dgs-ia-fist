import { z } from 'zod';

import { logger as defaultLogger, type Logger } from '../shared/logger';

export const assistantResponseSchema = z
  .object({
    answer: z.string().trim().min(1),
    source_document: z.string().trim().min(1),
    confidence_score: z.number().min(0).max(1)
  })
  .strict();

export type AssistantResponse = z.infer<typeof assistantResponseSchema>;

export interface ValidationResult {
  accepted: boolean;
  response: AssistantResponse;
  rejectionReason?: string;
}

interface GuardrailOutcome {
  ok: boolean;
  reason?: string;
}

const missingSourcePatterns = [
  /^[-—]+$/,
  /^(na|n\/a|none|null|undefined)$/,
  /^nenhum[ao]?$/,
  /^sem\s+(fonte|documento)$/,
  /^nao\s+(encontrad\w*|disponivel\w*|informad\w*)$/,
  /^desconhecid[ao]$/
];

export const safeFallbackResponse: AssistantResponse = {
  answer:
    'Nao consigo responder com seguranca no momento. Por favor, confirme a solicitacao com um supervisor.',
  source_document: 'SYSTEM-GUARDRAIL',
  confidence_score: 0
};

function normalizeText(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

function reject(
  log: Logger,
  reason: string,
  metadata?: Record<string, unknown>
): ValidationResult {
  log.warn({ reason, ...metadata }, 'Resposta rejeitada pelo response validator');

  return {
    accepted: false,
    response: safeFallbackResponse,
    rejectionReason: reason
  };
}

export function hasUsableSourceDocument(value: string): boolean {
  const normalizedSource = normalizeText(value);
  return (
    normalizedSource.length > 0 &&
    !missingSourcePatterns.some((pattern) => pattern.test(normalizedSource))
  );
}

function validateSourceDocument(response: AssistantResponse): GuardrailOutcome {
  if (!hasUsableSourceDocument(response.source_document)) {
    return {
      ok: false,
      reason: 'source_document ausente ou com placeholder invalido'
    };
  }

  return { ok: true };
}

export function violatesDangerousCargoReturnGuardrail(answer: string): boolean {
  const normalizedAnswer = normalizeText(answer);
  const dangerousCargoPattern =
    /\b(cargas?\s+(classificadas?\s+como\s+|consideradas?\s+)?perigosas?|materiais?\s+perigosos?|mercadorias?\s+perigosas?|produtos?\s+perigosos?)\b/;
  const returnPattern = /\bdevolucao\b|\bdevolver\b|\bdevolv\w*\b/;

  const mentionsDangerousCargo = dangerousCargoPattern.test(normalizedAnswer);
  const mentionsReturn = returnPattern.test(normalizedAnswer);

  if (!mentionsDangerousCargo || !mentionsReturn) {
    return false;
  }

  const relevantSentences = normalizedAnswer
    .split(/[.!?;:]/)
    .map((sentence) => sentence.trim())
    .filter(Boolean)
    .filter((sentence) => dangerousCargoPattern.test(sentence) || returnPattern.test(sentence));

  const denialPattern =
    /\bnao\b.{0,24}\b(devolv\w*|pode\w*|e\s+possivel|ser\w*\s+permitid[ao]s?|ser\w*\s+autorizad[ao]s?)\b|\b(impossivel|proibid[ao]s?|vedad[ao]s?)\b.{0,24}\bdevolv\w*\b/;
  const approvalPattern =
    /\b(pode\w*|permitid[ao]s?|autorizad[ao]s?|possivel)\b.{0,24}\bdevolv\w*\b|\bdevolv\w*\b.{0,24}\b(pode\w*|permitid[ao]s?|autorizad[ao]s?|possivel)\b/;

  const hasExplicitDenial = relevantSentences.some((sentence) => denialPattern.test(sentence));

  const hasExplicitApproval = relevantSentences.some(
    (sentence) => approvalPattern.test(sentence) && !denialPattern.test(sentence)
  );

  return !hasExplicitDenial || hasExplicitApproval;
}

function validateDangerousCargoReturn(response: AssistantResponse): GuardrailOutcome {
  if (violatesDangerousCargoReturnGuardrail(response.answer)) {
    return {
      ok: false,
      reason: 'resposta sobre devolucao de carga perigosa sem negativa explicita'
    };
  }

  return { ok: true };
}

export function validateAssistantResponse(
  candidate: unknown,
  log: Logger = defaultLogger
): ValidationResult {
  const parsedResponse = assistantResponseSchema.safeParse(candidate);

  if (!parsedResponse.success) {
    const issues = parsedResponse.error.issues.map((issue) => {
      const path = issue.path.length > 0 ? issue.path.join('.') : 'root';
      return `${path}: ${issue.message}`;
    });

    return reject(log, 'structured output invalido', { issues });
  }

  const sourceOutcome = validateSourceDocument(parsedResponse.data);
  if (!sourceOutcome.ok) {
    return reject(log, sourceOutcome.reason ?? 'source_document invalido', {
      response: parsedResponse.data
    });
  }

  const dangerousCargoOutcome = validateDangerousCargoReturn(parsedResponse.data);
  if (!dangerousCargoOutcome.ok) {
    return reject(log, dangerousCargoOutcome.reason ?? 'guardrail violado', {
      response: parsedResponse.data
    });
  }

  return {
    accepted: true,
    response: parsedResponse.data
  };
}
