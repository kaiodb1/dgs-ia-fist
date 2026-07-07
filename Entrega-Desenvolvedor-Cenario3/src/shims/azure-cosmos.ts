export interface Container {
  items: {
    create(item: unknown): Promise<{ resource: unknown }>;
  };
}

class Database {
  container(_name: string): Container {
    return {
      items: {
        async create(item: unknown): Promise<{ resource: unknown }> {
          return { resource: item };
        }
      }
    };
  }
}

export class CosmosClient {
  constructor(_connectionString: string) {}

  database(_name: string): Database {
    return new Database();
  }
}
