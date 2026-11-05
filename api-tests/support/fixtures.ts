import { test as base } from '@playwright/test';
import { ApiClient, PASSWORD, uniqueName } from './api-client';

export interface TestUser {
  client: ApiClient;
  username: string;
  password: string;
}

interface Fixtures {
  /** Factory: creates a brand-new client with its own empty cookie jar. */
  newClient: () => Promise<ApiClient>;
  /** Factory: registers a brand-new user and logs them in. */
  newUser: (prefix?: string) => Promise<TestUser>;
  /** An anonymous client (nobody is logged in). */
  api: ApiClient;
  /** A freshly registered, logged-in user. */
  user: TestUser;
}

export const test = base.extend<Fixtures>({
  newClient: async ({ playwright, baseURL }, use) => {
    const created: ApiClient[] = [];
    await use(async () => {
      const ctx = await playwright.request.newContext({
        baseURL,
        extraHTTPHeaders: { Accept: 'application/json' },
      });
      const client = new ApiClient(ctx, baseURL as string);
      created.push(client);
      return client;
    });
    // TEARDOWN: runs after every test, even failed ones.
    for (const client of created) {
      await client.cleanup();
    }
  },

  newUser: async ({ newClient }, use) => {
    await use(async (prefix = 'user') => {
      const client = await newClient();
      const username = uniqueName(prefix);
      const reg = await client.register(username, PASSWORD);
      if (reg.status() !== 201) throw new Error(`setup: register failed (${reg.status()})`);
      const login = await client.login(username, PASSWORD);
      if (login.status() !== 200) throw new Error(`setup: login failed (${login.status()})`);
      return { client, username, password: PASSWORD };
    });
  },

  api: async ({ newClient }, use) => {
    await use(await newClient());
  },

  user: async ({ newUser }, use) => {
    await use(await newUser('alice'));
  },
});

export { expect } from '@playwright/test';