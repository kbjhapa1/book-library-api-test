import { test, expect } from '../support/fixtures';

const DUNE = { title: 'Dune', author: 'Frank Herbert', published_year: 1965 };

test.describe('reading books (public)', () => {
  test('anonymous user can list books', async ({ api }) => {
    const res = await api.listBooks();

    expect(res.status()).toBe(200);
    expect(Array.isArray(await res.json())).toBe(true);
  });

  test('a created book appears in the list and can be fetched by id', async ({ user, api }) => {
    const created = await user.client.createBook(DUNE);
    expect(created.status()).toBe(201);
    const book = await created.json();

    const list = await api.listBooks(); // anonymous reader
    expect((await list.json()).map((b: { id: number }) => b.id)).toContain(book.id);

    const one = await api.getBook(book.id);
    expect(one.status()).toBe(200);
    expect(await one.json()).toMatchObject({ ...DUNE, owner: user.username });
  });

  test('unknown id returns 404', async ({ api }) => {
    const res = await api.getBook(999_999_999);

    expect(res.status()).toBe(404);
    expect(await res.json()).toHaveProperty('detail');
  });
});

test.describe('creating books', () => {
  test('authenticated user gets 201 and becomes the owner', async ({ user }) => {
    const res = await user.client.createBook(DUNE);

    expect(res.status()).toBe(201);
    expect(await res.json()).toEqual({
      id: expect.any(Number),
      ...DUNE,
      owner: user.username,
      created_at: expect.any(String),
    });
  });

  test('anonymous user gets 401', async ({ api }) => {
    const res = await api.createBook(DUNE);

    expect(res.status()).toBe(401);
  });

  test('client cannot choose the owner', async ({ user, newUser }) => {
    const other = await newUser('other');

    const res = await user.client.createBook({ ...DUNE, owner: other.username });

    expect((await res.json()).owner).toBe(user.username);
  });

  test('missing title returns 400 naming the field', async ({ user }) => {
    const res = await user.client.createBook({ author: 'Someone' });

    expect(res.status()).toBe(400);
    expect((await res.json()).title).toEqual(['This field is required.']);
  });

  test('absurd year returns 400', async ({ user }) => {
    const res = await user.client.createBook({ ...DUNE, published_year: 99 });

    expect(res.status()).toBe(400);
    expect(await res.json()).toHaveProperty('published_year');
  });

  test('non-JSON body returns 415', async ({ user }) => {
    const res = await user.client.ctx.post('/api/books/', {
      data: 'title=Dune',
      headers: { ...(await user.client.unsafeHeaders()), 'Content-Type': 'text/plain' },
    });

    expect(res.status()).toBe(415);
  });
});

test.describe('deleting books', () => {
  test('owner can delete: 204, then 404', async ({ user, api }) => {
    const id = (await (await user.client.createBook(DUNE)).json()).id as number;

    const del = await user.client.deleteBook(id);
    expect(del.status()).toBe(204);
    expect(await del.text()).toBe('');

    expect((await api.getBook(id)).status()).toBe(404);
  });

  test('another logged-in user gets 403 and the book survives', async ({ user, newUser, api }) => {
    const id = (await (await user.client.createBook(DUNE)).json()).id as number;
    const intruder = await newUser('intruder');

    const del = await intruder.client.deleteBook(id);

    expect(del.status()).toBe(403);
    expect((await api.getBook(id)).status()).toBe(200);
  });

  test('anonymous user gets 401', async ({ user, api }) => {
    const id = (await (await user.client.createBook(DUNE)).json()).id as number;

    expect((await api.deleteBook(id)).status()).toBe(401);
  });

  test('deleting an unknown id returns 404', async ({ user }) => {
    expect((await user.client.deleteBook(999_999_999)).status()).toBe(404);
  });

  test('PUT is not offered: 405 Method Not Allowed', async ({ user }) => {
    const id = (await (await user.client.createBook(DUNE)).json()).id as number;

    const res = await user.client.ctx.put(`/api/books/${id}/`, {
      data: DUNE,
      headers: await user.client.unsafeHeaders(),
    });

    expect(res.status()).toBe(405);
    expect(res.headers()['allow']).toContain('GET');
  });
});