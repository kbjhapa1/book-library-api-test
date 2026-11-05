import { request, type FullConfig } from '@playwright/test';

/**
 * Runs once before all tests. If the server is not reachable we stop right away
 * with a helpful message instead of 40 confusing failures.
 */
export default async function globalSetup(config: FullConfig): Promise<void> {
  const baseURL = config.projects[0].use.baseURL as string;
  const ctx = await request.newContext({ baseURL });

  try {
    const res = await ctx.get('/api/health/');
    if (!res.ok()) {
      throw new Error(`GET /api/health/ answered ${res.status()}`);
    }
  } catch (err) {
    const caHint = process.env.NODE_EXTRA_CA_CERTS
      ? `NODE_EXTRA_CA_CERTS = ${process.env.NODE_EXTRA_CA_CERTS}`
      : 'NODE_EXTRA_CA_CERTS is NOT set (run tests with "npm test", not "npx playwright test")';
    throw new Error(
      [
        `Cannot reach the API at ${baseURL}.`,
        '  1. Is the HTTPS server running in another terminal?',
        '  2. Did you generate the certificate in ../certs ?',
        `  3. ${caHint}`,
        `Original error: ${String(err)}`,
      ].join('\n'),
    );
  } finally {
    await ctx.dispose();
  }
}