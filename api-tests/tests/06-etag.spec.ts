import { test, expect } from '../support/fixtures';

// OPTIONAL (Lab 7, Part B): only meaningful after you enable ConditionalGetMiddleware.
test.describe('conditional requests with ETag', () => {
  test('If-None-Match with the current ETag returns 304 Not Modified', async ({ api }) => {
    const first = await api.listBooks();
    const etag = first.headers()['etag'];
    test.skip(!etag, 'ETag middleware not enabled yet (see Lab 7, Part B)');

    const second = await api.ctx.get('/api/books/', { headers: { 'If-None-Match': etag } });

    expect(second.status()).toBe(304);
    expect(await second.text()).toBe('');
  });

  test('after the data changes, the old ETag no longer matches', async ({ api, user }) => {
    const first = await api.listBooks();
    const etag = first.headers()['etag'];
    test.skip(!etag, 'ETag middleware not enabled yet (see Lab 7, Part B)');

    await user.client.createBook({ title: 'ETag Book', author: 'Someone' });
    const second = await api.ctx.get('/api/books/', { headers: { 'If-None-Match': etag } });

    expect(second.status()).toBe(200);
    expect(second.headers()['etag']).not.toBe(etag);
  });
});