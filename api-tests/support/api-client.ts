import { expect, type APIRequestContext, type APIResponse } from '@playwright/test';
import { randomBytes } from 'node:crypto';

export const PASSWORD = 'S3cure-Lab-Passw0rd!';

/** unique_name('alice') -> 'alice_3fa9c2d1'  (avoids clashes between tests and runs) */
export function uniqueName(prefix: string): string {
  return `${prefix}_${randomBytes(4).toString('hex')}`;
}

export interface BookInput {
  title?: string;
  author?: string;
  published_year?: number | null;
  [extra: string]: unknown;
}

/**
 * A thin helper around one APIRequestContext.
 * The context owns a COOKIE JAR: cookies from Set-Cookie headers are stored
 * automatically and sent back on later requests, exactly like a browser would.
 */
export class ApiClient {
  readonly createdBookIds: number[] = [];

  constructor(
    readonly ctx: APIRequestContext,
    readonly baseURL: string,
  ) {}

  get origin(): string {
    return new URL(this.baseURL).origin;
  }

  // ---- CSRF -------------------------------------------------------------

  /** Asks the server for a CSRF token (the server also sets the csrftoken cookie). */
  async csrfToken(): Promise<string> {
    const res = await this.ctx.get('/api/csrf/');
    expect(res.status(), 'GET /api/csrf/').toBe(200);
    return (await res.json()).csrfToken as string;
  }

  /**
   * Headers every "unsafe" request (POST, DELETE, ...) needs:
   *  - X-CSRFToken: proves we read the token from this site
   *  - Origin: Django checks it on HTTPS requests. Browsers add it automatically,
   *            Playwright's API client does not, so we send it ourselves.
   */
  async unsafeHeaders(token?: string): Promise<Record<string, string>> {
    return { 'X-CSRFToken': token ?? (await this.csrfToken()), Origin: this.origin };
  }

  // ---- Auth endpoints -----------------------------------------------------

  async register(username: string, password: string): Promise<APIResponse> {
    return this.ctx.post('/api/register/', {
      data: { username, password },
      headers: await this.unsafeHeaders(),
    });
  }

  async login(username: string, password: string): Promise<APIResponse> {
    // Login rotates the CSRF token, so we fetch a fresh one *before* each call.
    return this.ctx.post('/api/login/', {
      data: { username, password },
      headers: await this.unsafeHeaders(),
    });
  }

  async logout(): Promise<APIResponse> {
    return this.ctx.post('/api/logout/', { headers: await this.unsafeHeaders() });
  }

  async me(): Promise<APIResponse> {
    return this.ctx.get('/api/me/');
  }

  // ---- Book endpoints -----------------------------------------------------

  async listBooks(): Promise<APIResponse> {
    return this.ctx.get('/api/books/');
  }

  async getBook(id: number): Promise<APIResponse> {
    return this.ctx.get(`/api/books/${id}/`);
  }

  async createBook(book: BookInput): Promise<APIResponse> {
    const res = await this.ctx.post('/api/books/', {
      data: book,
      headers: await this.unsafeHeaders(),
    });
    if (res.status() === 201) {
      this.createdBookIds.push((await res.json()).id as number);
    }
    return res;
  }

  async deleteBook(id: number): Promise<APIResponse> {
    return this.ctx.delete(`/api/books/${id}/`, { headers: await this.unsafeHeaders() });
  }

  // ---- Cookie jar -----------------------------------------------------------

  async cookies() {
    return (await this.ctx.storageState()).cookies;
  }

  async cookie(name: string) {
    return (await this.cookies()).find((c) => c.name === name);
  }

  // ---- Teardown ---------------------------------------------------------------

  /** Best-effort cleanup: remove books we created, log out, close the context. */
  async cleanup(): Promise<void> {
    for (const id of this.createdBookIds) {
      try {
        await this.deleteBook(id);
      } catch {
        /* already gone or not logged in: fine */
      }
    }
    try {
      await this.logout();
    } catch {
      /* not logged in: fine */
    }
    await this.ctx.dispose();
  }
}