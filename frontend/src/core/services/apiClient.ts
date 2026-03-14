import { appEnv } from '@/core/config/env';

export interface ApiRequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
}

export class AppApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = 'AppApiError';
  }
}

const isAbsoluteUrl = (path: string) => /^https?:\/\//.test(path);

const resolveUrl = (path: string) =>
  isAbsoluteUrl(path) ? path : `${appEnv.apiBaseUrl}${path.startsWith('/') ? path : `/${path}`}`;

const parseJsonSafely = async (response: Response) => {
  try {
    return await response.json();
  } catch {
    return null;
  }
};

async function request<TResponse>(path: string, options: ApiRequestOptions = {}): Promise<TResponse> {
  const headers = new Headers(options.headers);

  if (options.body !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(resolveUrl(path), {
    ...options,
    headers,
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const details = await parseJsonSafely(response);
    throw new AppApiError(`Request failed with status ${response.status}`, response.status, details);
  }

  if (response.status === 204) {
    return undefined as TResponse;
  }

  const contentType = response.headers.get('content-type') ?? '';
  if (contentType.includes('application/json')) {
    return (await response.json()) as TResponse;
  }

  return (await response.text()) as TResponse;
}

export const apiClient = {
  get: <TResponse>(path: string, options?: Omit<ApiRequestOptions, 'body' | 'method'>) =>
    request<TResponse>(path, { ...options, method: 'GET' }),
  post: <TResponse>(
    path: string,
    body?: unknown,
    options?: Omit<ApiRequestOptions, 'body' | 'method'>,
  ) => request<TResponse>(path, { ...options, method: 'POST', body }),
};
