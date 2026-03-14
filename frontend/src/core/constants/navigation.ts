export interface NavigationItem {
  label: string;
  path: string;
  description: string;
}

export const navigationItems: NavigationItem[] = [
  {
    label: 'Home',
    path: '/',
    description: 'Live overview of outbreak activity and current signals.',
  },
  {
    label: 'About',
    path: '/about',
    description: 'Project goals, evidence model, and response workflow.',
  },
  {
    label: 'Symptoms',
    path: '/symptoms',
    description: 'Quick symptom guide and risk indicators.',
  },
  {
    label: 'Self-check',
    path: '/self-check',
    description: 'Guided triage questions for personal screening.',
  },
  {
    label: 'Graphs',
    path: '/graphs',
    description: 'Exploratory charts built on the case API.',
  },
  {
    label: 'Contact',
    path: '/contact',
    description: 'Send feedback, questions, or data quality notes.',
  },
];

export const footerHighlights = [
  'Case monitoring aligned to the Django API.',
  'Reusable Zustand state for auth, dashboard, and triage.',
  'Feature folders split into data, domain, and presentation layers.',
];
