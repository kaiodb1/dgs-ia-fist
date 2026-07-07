import { describe, expect, it, vi } from 'vitest';

import {
  safeFallbackResponse,
  validateAssistantResponse
} from '../src/services/response-validator';

function createLoggerMock() {
  return {
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn()
  };
}

describe('validateAssistantResponse', () => {
  it('accepts a valid structured response', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'Nao. Cargas perigosas nao podem ser devolvidas pelo processo padrao.',
        source_document: 'POL-001',
        confidence_score: 0.92
      },
      logger
    );

    expect(result.accepted).toBe(true);
    expect(result.response.source_document).toBe('POL-001');
    expect(logger.warn).not.toHaveBeenCalled();
  });

  it('rejects placeholder source documents', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'A politica depende do tipo de cliente.',
        source_document: '—',
        confidence_score: 0.7
      },
      logger
    );

    expect(result.accepted).toBe(false);
    expect(result.response).toEqual(safeFallbackResponse);
    expect(result.rejectionReason).toContain('source_document');
    expect(logger.warn).toHaveBeenCalledTimes(1);
  });

  it('rejects semantic placeholders such as "sem fonte"', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'A politica depende do tipo de cliente.',
        source_document: 'sem fonte',
        confidence_score: 0.7
      },
      logger
    );

    expect(result.accepted).toBe(false);
    expect(result.response).toEqual(safeFallbackResponse);
  });

  it('rejects dangerous cargo return answers without an explicit denial', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'Sim, a devolucao de carga perigosa pode ser feita com autorizacao previa.',
        source_document: 'POL-001',
        confidence_score: 0.88
      },
      logger
    );

    expect(result.accepted).toBe(false);
    expect(result.response).toEqual(safeFallbackResponse);
    expect(result.rejectionReason).toContain('carga perigosa');
  });

  it('rejects paraphrased approvals about dangerous cargo returns', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'A carga classificada como perigosa pode ser devolvida com autorizacao previa.',
        source_document: 'POL-001',
        confidence_score: 0.8
      },
      logger
    );

    expect(result.accepted).toBe(false);
    expect(result.response).toEqual(safeFallbackResponse);
  });

  it('accepts compliant denials with alternate verb conjugation', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer:
          'Nao podemos devolver carga classificada como perigosa pelo processo padrao; escale para o supervisor.',
        source_document: 'POL-001',
        confidence_score: 0.95
      },
      logger
    );

    expect(result.accepted).toBe(true);
    expect(result.response.source_document).toBe('POL-001');
  });

  it('rejects extra fields because the schema is strict', () => {
    const logger = createLoggerMock();

    const result = validateAssistantResponse(
      {
        answer: 'Nao. Cargas perigosas nao podem ser devolvidas pelo processo padrao.',
        source_document: 'POL-001',
        confidence_score: 0.92,
        extra: true
      },
      logger
    );

    expect(result.accepted).toBe(false);
    expect(result.response).toEqual(safeFallbackResponse);
    expect(result.rejectionReason).toContain('structured output');
  });
});
