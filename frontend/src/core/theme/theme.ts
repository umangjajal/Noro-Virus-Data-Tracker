import { alpha, createTheme } from '@mui/material/styles';

const shellShadow = '0 20px 55px rgba(21, 49, 60, 0.12)';

export const appTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0C3B4A',
      light: '#1F5B6E',
      dark: '#07232C',
      contrastText: '#F8F2E7',
    },
    secondary: {
      main: '#F26A4B',
      light: '#FF8D74',
      dark: '#BA4429',
      contrastText: '#111827',
    },
    success: {
      main: '#2E8B57',
    },
    warning: {
      main: '#CC8A1D',
    },
    error: {
      main: '#C44D3B',
    },
    background: {
      default: '#F6EFDF',
      paper: alpha('#FFFFFF', 0.8),
    },
    text: {
      primary: '#15313C',
      secondary: '#4D636D',
    },
  },
  typography: {
    fontFamily: '"IBM Plex Sans", "Segoe UI", sans-serif',
    h1: {
      fontFamily: '"Space Grotesk", "IBM Plex Sans", sans-serif',
      fontSize: 'clamp(2.6rem, 5vw, 4.5rem)',
      lineHeight: 0.95,
      fontWeight: 700,
    },
    h2: {
      fontFamily: '"Space Grotesk", "IBM Plex Sans", sans-serif',
      fontSize: 'clamp(2rem, 4vw, 3rem)',
      fontWeight: 700,
      lineHeight: 1.02,
    },
    h3: {
      fontFamily: '"Space Grotesk", "IBM Plex Sans", sans-serif',
      fontWeight: 700,
    },
    h4: {
      fontFamily: '"Space Grotesk", "IBM Plex Sans", sans-serif',
      fontWeight: 700,
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 24,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundAttachment: 'fixed',
        },
        '::selection': {
          backgroundColor: alpha('#F26A4B', 0.32),
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundImage: `linear-gradient(135deg, ${alpha('#0C3B4A', 0.96)}, ${alpha(
            '#12354F',
            0.86,
          )})`,
          backdropFilter: 'blur(18px)',
          boxShadow: shellShadow,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: shellShadow,
          border: `1px solid ${alpha('#0C3B4A', 0.08)}`,
          backgroundImage:
            'linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(250,245,236,0.88) 100%)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 999,
          paddingInline: 18,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 999,
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        rounded: {
          borderRadius: 24,
        },
      },
    },
  },
});
