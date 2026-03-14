import { useEffect } from 'react';

import { useLocation } from 'react-router-dom';

import { appEnv } from '@/core/config/env';
import { navigationItems } from '@/core/constants/navigation';

const pageTitleMap = Object.fromEntries(navigationItems.map((item) => [item.path, item.label]));

export function useRouteEffects() {
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
    const currentTitle = pageTitleMap[location.pathname] ?? 'Tracker';
    document.title = `${currentTitle} | ${appEnv.appName}`;
  }, [location.pathname]);
}
