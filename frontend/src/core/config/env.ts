const trimTrailingSlash = (value: string) => value.replace(/\/+$/, '');

export const appEnv = {
  apiBaseUrl: trimTrailingSlash(import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'),
  appName: 'NoroWatch',
  defaultLocale: 'en-US',
} as const;
