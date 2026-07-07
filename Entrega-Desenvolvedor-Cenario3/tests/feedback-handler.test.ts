import { describe, expect, it, vi } from 'vitest';

import { createFeedbackHandler } from '../src/functions/feedback/handler';

function createLoggerMock() {
  return {
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn()
  };
}

describe('createFeedbackHandler', () => {
  it('persists validated feedback without logging attendantEmail', async () => {
    const create = vi.fn().mockResolvedValue({ resource: { id: 'f1' } });
    const logger = createLoggerMock();
    const handler = createFeedbackHandler({
      container: {
        items: {
          create
        }
      },
      logger,
      now: () => new Date('2026-07-07T12:00:00.000Z')
    });

    const response = await handler({
      json: async () => ({
        queryId: 'q-123',
        rating: 5,
        comment: 'Resposta muito util.',
        attendantEmail: 'atendente@novatech.com'
      })
    });

    expect(response.status).toBe(201);
    expect(create).toHaveBeenCalledWith({
      queryId: 'q-123',
      rating: 5,
      comment: 'Resposta muito util.',
      receivedAt: '2026-07-07T12:00:00.000Z'
    });
    expect(logger.info).toHaveBeenCalledWith(
      {
        queryId: 'q-123',
        rating: 5
      },
      'Feedback recebido e persistido'
    );
    expect(JSON.stringify(logger.info.mock.calls)).not.toContain('attendantEmail');
  });

  it('returns 400 when the payload is invalid', async () => {
    const create = vi.fn();
    const logger = createLoggerMock();
    const handler = createFeedbackHandler({
      container: {
        items: {
          create
        }
      },
      logger
    });

    const response = await handler({
      json: async () => ({
        queryId: '',
        rating: 10,
        comment: 'fora da faixa',
        attendantEmail: 'email-invalido'
      })
    });

    expect(response.status).toBe(400);
    expect(create).not.toHaveBeenCalled();
    expect(logger.warn).toHaveBeenCalledTimes(1);
  });
});
