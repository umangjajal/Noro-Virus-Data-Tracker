import { Navigate, useRoutes } from 'react-router-dom';

import { AppShell } from '@/core/layouts/AppShell';
import { AboutPage } from '@/lib/features/about/presentation/AboutPage';
import { ContactPage } from '@/lib/features/contact/presentation/ContactPage';
import { HomePage } from '@/lib/features/dashboard/presentation/HomePage';
import { GraphsPage } from '@/lib/features/graphs/presentation/GraphsPage';
import { SelfCheckPage } from '@/lib/features/self-check/presentation/SelfCheckPage';
import { SymptomsPage } from '@/lib/features/symptoms/presentation/SymptomsPage';

export function AppRouter() {
  return useRoutes([
    {
      path: '/',
      element: <AppShell />,
      children: [
        { index: true, element: <HomePage /> },
        { path: 'about', element: <AboutPage /> },
        { path: 'symptoms', element: <SymptomsPage /> },
        { path: 'self-check', element: <SelfCheckPage /> },
        { path: 'graphs', element: <GraphsPage /> },
        { path: 'contact', element: <ContactPage /> },
      ],
    },
    { path: '*', element: <Navigate replace to="/" /> },
  ]);
}
