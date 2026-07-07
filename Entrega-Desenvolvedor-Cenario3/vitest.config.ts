import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

const rootDirectory = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      '@azure/functions': path.resolve(rootDirectory, 'src/shims/azure-functions.ts'),
      '@azure/cosmos': path.resolve(rootDirectory, 'src/shims/azure-cosmos.ts')
    }
  },
  test: {
    environment: 'node'
  }
});
