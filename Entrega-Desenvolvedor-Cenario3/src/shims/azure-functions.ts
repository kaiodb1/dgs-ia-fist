export interface HttpRequest {
  json(): Promise<unknown>;
}

export interface HttpResponseInit {
  status: number;
  body?: string;
  jsonBody?: unknown;
  headers?: Record<string, string>;
}

export interface HttpHandlerConfig {
  methods: string[];
  handler: (request: HttpRequest) => Promise<HttpResponseInit> | HttpResponseInit;
}

export interface RegisteredHttpFunction {
  name: string;
  methods: string[];
  handler: HttpHandlerConfig['handler'];
}

const registeredHttpFunctions: RegisteredHttpFunction[] = [];

export const app = {
  http(name: string, config: HttpHandlerConfig): void {
    registeredHttpFunctions.push({
      name,
      methods: config.methods,
      handler: config.handler
    });
  }
};

export function getRegisteredHttpFunctions(): RegisteredHttpFunction[] {
  return [...registeredHttpFunctions];
}
