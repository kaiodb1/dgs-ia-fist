import { CosmosClient, type Container } from '@azure/cosmos';
import { app, type HttpRequest, type HttpResponseInit } from '@azure/functions';
import { z } from 'zod';

import { logger as defaultLogger, type Logger } from '../../shared/logger';

const feedbackRequestSchema = z
  .object({
    queryId: z.string().trim().min(1),
    rating: z.number().int().min(1).max(5),
    comment: z.string().trim().max(2000).optional().default(''),
    attendantEmail: z.string().trim().email()
  })
  .strict();

export type FeedbackRequestBody = z.infer<typeof feedbackRequestSchema>;

export interface FeedbackDocument {
  queryId: string;
  rating: number;
  comment: string;
  receivedAt: string;
}

export interface FeedbackHandlerDependencies {
  container: Pick<Container, 'items'>;
  logger?: Logger;
  now?: () => Date;
}

export class InvalidFeedbackRequestError extends Error {
  constructor(
    message: string,
    public readonly issues: string[] = []
  ) {
    super(message);
    this.name = 'InvalidFeedbackRequestError';
  }
}

async function readRequestBody(request: Pick<HttpRequest, 'json'>): Promise<unknown> {
  try {
    return await request.json();
  } catch {
    throw new InvalidFeedbackRequestError('O corpo da requisicao precisa ser um JSON valido.');
  }
}

export async function parseFeedbackRequest(
  request: Pick<HttpRequest, 'json'>
): Promise<FeedbackRequestBody> {
  const requestBody = await readRequestBody(request);
  const parsedBody = feedbackRequestSchema.safeParse(requestBody);

  if (!parsedBody.success) {
    throw new InvalidFeedbackRequestError(
      'Payload de feedback invalido.',
      parsedBody.error.issues.map((issue) => {
        const path = issue.path.length > 0 ? issue.path.join('.') : 'root';
        return `${path}: ${issue.message}`;
      })
    );
  }

  return parsedBody.data;
}

export function buildFeedbackDocument(
  feedback: FeedbackRequestBody,
  now: () => Date = () => new Date()
): FeedbackDocument {
  return {
    queryId: feedback.queryId,
    rating: feedback.rating,
    comment: feedback.comment,
    receivedAt: now().toISOString()
  };
}

export function createFeedbackHandler(dependencies: FeedbackHandlerDependencies) {
  const log = dependencies.logger ?? defaultLogger;
  const now = dependencies.now ?? (() => new Date());

  return async function feedbackHandler(
    request: Pick<HttpRequest, 'json'>
  ): Promise<HttpResponseInit> {
    try {
      const feedback = await parseFeedbackRequest(request);
      const feedbackDocument = buildFeedbackDocument(feedback, now);

      await dependencies.container.items.create(feedbackDocument);

      log.info(
        {
          queryId: feedbackDocument.queryId,
          rating: feedbackDocument.rating
        },
        'Feedback recebido e persistido'
      );

      return {
        status: 201,
        jsonBody: {
          message: 'Feedback registrado com sucesso.'
        }
      };
    } catch (error) {
      if (error instanceof InvalidFeedbackRequestError) {
        log.warn(
          {
            issues: error.issues
          },
          'Payload de feedback rejeitado'
        );

        return {
          status: 400,
          jsonBody: {
            error: error.message,
            issues: error.issues
          }
        };
      }

      throw error;
    }
  };
}

function getCosmosConnectionString(): string {
  const connectionString = process.env.COSMOS_CONNECTION_STRING;

  if (!connectionString) {
    throw new Error('A variavel de ambiente COSMOS_CONNECTION_STRING e obrigatoria.');
  }

  return connectionString;
}

let cachedContainer: Container | undefined;

export function getFeedbackContainer(
  clientFactory: (connectionString: string) => CosmosClient = (connectionString) =>
    new CosmosClient(connectionString)
): Container {
  if (!cachedContainer) {
    const client = clientFactory(getCosmosConnectionString());
    cachedContainer = client.database('novatech').container('feedbacks');
  }

  return cachedContainer;
}

export async function feedbackHandler(request: HttpRequest): Promise<HttpResponseInit> {
  const handler = createFeedbackHandler({
    container: getFeedbackContainer()
  });

  return handler(request);
}

app.http('feedback', {
  methods: ['POST'],
  handler: feedbackHandler
});
