import { test, expect } from '@playwright/test';

test.describe('HTTPS and certificate validation', () => {
  test('server answers over HTTPS and our certificate is trusted', async ({ request, baseURL }) => {
    expect(baseURL).toMatch(/^https:\/\//);

    const res = await request.get('/api/health/');

    expect(res.status()).toBe(200);
    expect(res.headers()['content-type']).toContain('application/json');
    expect(await res.json()).toEqual({ status: 'ok' });
  });

  test('certificate validation is NOT disabled in this project', async ({}, testInfo) => {
    // If someone "fixes" TLS errors by switching validation off, this test fails.
    expect(testInfo.project.use.ignoreHTTPSErrors ?? false).toBe(false);
  });

  test('a host name that is NOT in the certificate is rejected', async ({ playwright, baseURL }) => {
    // Our certificate only says "localhost". The numeric address 127.0.0.1 reaches the
    // very same server, but the certificate does not vouch for that name.
    const port = new URL(baseURL as string).port;
    const ctx = await playwright.request.newContext({ baseURL: `https://127.0.0.1:${port}` });

    await expect(ctx.get('/api/health/')).rejects.toThrow(/altname|certificate|not in the cert/i);

    await ctx.dispose();
  });

  test('speaking plain HTTP to the HTTPS port fails', async ({ playwright, baseURL }) => {
    const port = new URL(baseURL as string).port;
    const ctx = await playwright.request.newContext({ baseURL: `http://localhost:${port}` });

    await expect(ctx.get('/api/health/')).rejects.toThrow();

    await ctx.dispose();
  });
});