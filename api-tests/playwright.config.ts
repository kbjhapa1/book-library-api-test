import { defineConfig } from '@playwright/test';

// This project tests an HTTP API. There are no browsers, pages or locators here.
// Every test receives an APIRequestContext (a tiny HTTP client with a cookie jar).

export default defineConfig({
  testDir: './tests',
  globalSetup: './global-setup.ts',

  // One test at a time keeps the SQLite database calm and the output easy to read.
  // The tests do NOT depend on order: each one creates its own users and books.
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 30_000,

  reporter: [['list'], ['html', { open: 'never' }]],

  use: {
    baseURL: process.env.BASE_URL ?? 'https://localhost:8443',

    // NEVER turn this on. We trust our development certificate explicitly instead
    // (NODE_EXTRA_CA_CERTS in package.json), so TLS validation stays ENABLED.
    ignoreHTTPSErrors: false,

    extraHTTPHeaders: { Accept: 'application/json' },
  },
});