import { test, expect } from '../support/fixtures';

test.describe('session cookie behaviour', () => {
  test('the session cookie is HttpOnly, Secure and SameSite=Lax', async ({ user }) => {
    const cookie = await user.client.cookie('sessionid');

    expect(cookie).toBeDefined();
    expect(cookie).toMatchObject({ httpOnly: true, secure: true, sameSite: 'Lax', path: '/' });
    expect(cookie!.value.length).toBeGreaterThan(20);
  });

  test('the cookie jar is reused automatically on later requests', async ({ user }) => {
    // We never copy the cookie by hand: Playwright stores and resends it for us.
    for (let i = 0; i < 3; i++) {
      expect((await user.client.me()).status()).toBe(200);
    }
  });

  test('a new client (empty jar) is NOT logged in', async ({ user, newClient }) => {
    expect((await user.client.me()).status()).toBe(200);

    const stranger = await newClient();

    expect((await stranger.me()).status()).toBe(401);
  });

  test('each login creates a different session id', async ({ user, newClient }) => {
    const second = await newClient();
    await second.login(user.username, user.password);

    const a = await user.client.cookie('sessionid');
    const b = await second.cookie('sessionid');

    expect(a!.value).not.toBe(b!.value);
    expect((await second.me()).status()).toBe(200); // both sessions work at once
  });

  test('two users never see each other\'s identity', async ({ user, newUser }) => {
    const bob = await newUser('bob');

    expect((await (await user.client.me()).json()).username).toBe(user.username);
    expect((await (await bob.client.me()).json()).username).toBe(bob.username);
  });

  test('a tampered session cookie is rejected', async ({ user, playwright, baseURL }) => {
    const real = (await user.client.cookie('sessionid'))!;
    const forged = { ...real, value: real.value.slice(0, -4) + 'xxxx' };
    const ctx = await playwright.request.newContext({
      baseURL,
      storageState: { cookies: [forged], origins: [] },
    });

    expect((await ctx.get('/api/me/')).status()).toBe(401);

    await ctx.dispose();
  });
});

test.describe('logout', () => {
  test('logout returns 204 and the same client is no longer authenticated', async ({ user }) => {
    expect((await user.client.me()).status()).toBe(200);

    const res = await user.client.logout();

    expect(res.status()).toBe(204);
    expect((await user.client.me()).status()).toBe(401);
  });

  test('after logout the client can no longer write', async ({ user }) => {
    await user.client.logout();

    const res = await user.client.createBook({ title: 'Ghost', author: 'Nobody' });

    expect(res.status()).toBe(401);
  });

  test('the OLD session cookie is dead on the server after logout (replay attack fails)', async ({
    user,
    playwright,
    baseURL,
  }) => {
    const oldCookie = (await user.client.cookie('sessionid'))!;
    await user.client.logout();

    // An attacker who copied the cookie before logout tries to use it:
    const attacker = await playwright.request.newContext({
      baseURL,
      storageState: { cookies: [oldCookie], origins: [] },
    });

    expect((await attacker.get('/api/me/')).status()).toBe(401);

    await attacker.dispose();
  });

  test('logging out when not logged in returns 401', async ({ api }) => {
    expect((await api.logout()).status()).toBe(401);
  });
});