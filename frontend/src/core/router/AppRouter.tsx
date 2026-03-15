import { lazy, Suspense, type ReactNode } from 'react';

import { Container, LinearProgress } from '@mui/material';
import { Navigate, useRoutes } from 'react-router-dom';

import { AppShell } from '@/core/layouts/AppShell';

const HomePage = lazy(() =>
  import('@/lib/features/dashboard/presentation/HomePage').then((module) => ({ default: module.HomePage })),
);
const AboutPage = lazy(() =>
  import('@/lib/features/about/presentation/AboutPage').then((module) => ({ default: module.AboutPage })),
);
const SymptomsPage = lazy(() =>
  import('@/lib/features/symptoms/presentation/SymptomsPage').then((module) => ({ default: module.SymptomsPage })),
);
const SelfCheckPage = lazy(() =>
  import('@/lib/features/self-check/presentation/SelfCheckPage').then((module) => ({ default: module.SelfCheckPage })),
);
const GraphsPage = lazy(() =>
  import('@/lib/features/graphs/presentation/GraphsPage').then((module) => ({ default: module.GraphsPage })),
);
const ContactPage = lazy(() =>
  import('@/lib/features/contact/presentation/ContactPage').then((module) => ({ default: module.ContactPage })),
);

const withSuspense = (page: ReactNode) => (
  <Suspense
    fallback={
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <LinearProgress color="secondary" />
      </Container>
    }
  >
    {page}
  </Suspense>
);

export function AppRouter() {
  return useRoutes([
    {
      path: '/',
      element: <AppShell />,
      children: [
        { index: true, element: withSuspense(<HomePage />) },
        { path: 'about', element: withSuspense(<AboutPage />) },
        { path: 'symptoms', element: withSuspense(<SymptomsPage />) },
        { path: 'self-check', element: withSuspense(<SelfCheckPage />) },
        { path: 'graphs', element: withSuspense(<GraphsPage />) },
        { path: 'contact', element: withSuspense(<ContactPage />) },
      ],
    },
    { path: '*', element: <Navigate replace to="/" /> },
  ]);
}
