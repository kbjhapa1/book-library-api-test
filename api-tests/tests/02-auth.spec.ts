import { test, expect } from '../support/fixtures';
import { PASSWORD, uniqueName } from '../support/api-client';

test.describe('registration', () => {
  test('register returns 201 and never echoes the password', async ({ api }) => {
    const username = uniqueName('reg');

    const res = await api.register(username, PASSWORD);

    expect(res.status()).toBe(201);
    const body = await res.json();
    expect(body).toEqual({ id: expect.any(Number), username });
    expect(JSON.stringify(body)).not.toContain(PASSWORD);
  });

  test('duplicate username returns 400', async ({ api }) => {
    const username = uniqueName('dup');
    expect((await api.register(username, PASSWORD)).status()).toBe(201);

    const res = await api.register(username, PASSWORD);

    expect(res.status()).toBe(400);
    expect(await res.json()).toHaveProperty('username');
  });

  test('weak password returns 400 with a password error', async ({ api }) => {
    const res = await api.register(uniqueName('weak'), '12345678');

    expect(res.status()).toBe(400);
    expect(await res.json()).toHaveProperty('password');
  });

  test('missing password returns 400', async ({ api }) => {
    const res = await api.ctx.post('/api/register/', {
      data: { username: uniqueName('nopw') },
      headers: await api.unsafeHeaders(),
    });

    expect(res.status()).toBe(400);
    expect((await res.json()).password).toEqual(['This field is required.']);
  });
});

test.describe('login', () => {
  test('valid credentials return 200 and a session cookie', async ({ api }) => {
    const username = uniqueName('login');
    await api.register(username, PASSWORD);

    const res = await api.login(username, PASSWORD);

    expect(res.status()).toBe(200);
    expect(await res.json()).toEqual({ id: expect.any(Number), username });
    expect(res.headers()['set-cookie']).toContain('sessionid=');
    expect(await api.cookie('sessionid')).toBeDefined();
  });

  test('wrong password returns 401 and sets no session cookie', async ({ api }) => {
    const username = uniqueName('wrongpw');
    await api.register(username, PASSWORD);

    const res = await api.login(username, 'not-the-password');

    expect(res.status()).toBe(401);
    expect(await res.json()).toEqual({ detail: 'Invalid username or password.' });
    expect(await api.cookie('sessionid')).toBeUndefined();
  });

  test('unknown user gets exactly the same answer as a wrong password', async ({ api }) => {
    const res = await api.login(uniqueName('ghost'), PASSWORD);

    expect(res.status()).toBe(401);
    expect(await res.json()).toEqual({ detail: 'Invalid username or password.' });
  });

  test('missing fields return 400', async ({ api }) => {
    const res = await api.ctx.post('/api/login/', {
      data: { username: 'someone' },
      headers: await api.unsafeHeaders(),
    });

    expect(res.status()).toBe(400);
  });
});

test.describe('who am I (authenticated vs unauthenticated requests)', () => {
  test('logged-in user is recognised from the cookie alone', async ({ user }) => {
    const res = await user.client.me();

    expect(res.status()).toBe(200);
    expect((await res.json()).username).toBe(user.username);
  });

  test('anonymous request gets 401 and a WWW-Authenticate challenge', async ({ api }) => {
    const res = await api.me();

    expect(res.status()).toBe(401);
    expect(res.headers()['www-authenticate']).toBe('Session');
    expect(await res.json()).toHaveProperty('detail');
  });
});