import { test, expect } from '../support/fixtures';
import { PASSWORD, uniqueName } from '../support/api-client';

const BOOK = { title: 'CSRF Test Book', author: 'Test Author' };

test.describe('CSRF protection for session-authenticated writes', () => {
  test('/api/csrf/ returns a token and sets a readable, Secure csrftoken cookie', async ({ api }) => {
    const res = await api.ctx.get('/api/csrf/');

    expect(res.status()).toBe(200);
    expect((await res.json()).csrfToken).toBeTruthy();
    const cookie = await api.cookie('csrftoken');
    expect(cookie).toMatchObject({ secure: true, httpOnly: false, sameSite: 'Lax' });
  });

  test('logged in, but no X-CSRFToken header -> 403', async ({ user }) => {
    const res = await user.client.ctx.post('/api/books/', {
      data: BOOK,
      headers: { Origin: user.client.origin }, // Origin present, token missing
    });

    expect(res.status()).toBe(403);
    expect((await res.json()).detail).toContain('CSRF');
  });

  test('logged in, wrong token -> 403', async ({ user }) => {
    const res = await user.client.ctx.post('/api/books/', {
      data: BOOK,
      headers: await user.client.unsafeHeaders('this-is-not-the-token'),
    });

    expect(res.status()).toBe(403);
  });

  test('valid token but no Origin/Referer header over HTTPS -> 403', async ({ user }) => {
    const res = await user.client.ctx.post('/api/books/', {
      data: BOOK,
      headers: { 'X-CSRFToken': await user.client.csrfToken() }, // no Origin
    });

    expect(res.status()).toBe(403);
    expect((await res.json()).detail).toMatch(/Referer|Origin/);
  });

  test('valid token but Origin from another site -> 403', async ({ user }) => {
    const res = await user.client.ctx.post('/api/books/', {
      data: BOOK,
      headers: {
        'X-CSRFToken': await user.client.csrfToken(),
        Origin: 'https://evil.example',
      },
    });

    expect(res.status()).toBe(403);
    expect((await res.json()).detail).toContain('Origin');
  });

  test('valid token and matching Origin -> 201', async ({ user }) => {
    const res = await user.client.createBook(BOOK);

    expect(res.status()).toBe(201);
  });

  test('a token fetched BEFORE login stops working AFTER login (token rotation)', async ({ newClient }) => {
    const client = await newClient();
    const username = uniqueName('rotate');
    await client.register(username, PASSWORD);

    const before = await client.csrfToken(); // token issued to an anonymous visitor
    const login = await client.ctx.post('/api/login/', {
      data: { username, password: PASSWORD },
      headers: { 'X-CSRFToken': before, Origin: client.origin },
    });
    expect(login.status()).toBe(200); // login itself accepted the pre-login token

    // Django rotated the token during login, so the old one is now stale:
    const stale = await client.ctx.post('/api/books/', {
      data: BOOK,
      headers: { 'X-CSRFToken': before, Origin: client.origin },
    });
    expect(stale.status()).toBe(403);

    // Asking for a fresh token fixes it (createBook does this for us):
    expect((await client.createBook(BOOK)).status()).toBe(201);
  });

  test('login and register are protected too', async ({ api }) => {
    const login = await api.ctx.post('/api/login/', {
      data: { username: 'x', password: 'y' },
      headers: { Origin: api.origin },
    });
    const register = await api.ctx.post('/api/register/', {
      data: { username: 'x', password: 'y' },
      headers: { Origin: api.origin },
    });

    expect(login.status()).toBe(403);
    expect(register.status()).toBe(403);
  });

  test('safe methods (GET) never need a token', async ({ api }) => {
    expect((await api.ctx.get('/api/books/')).status()).toBe(200);
  });
});