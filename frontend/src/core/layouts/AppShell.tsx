import { useState } from 'react';

import MenuRounded from '@mui/icons-material/MenuRounded';
import MessageRounded from '@mui/icons-material/MessageRounded';
import VirusOutlined from '@mui/icons-material/VaccinesOutlined';
import {
  AppBar,
  Box,
  Button,
  Container,
  Drawer,
  IconButton,
  Stack,
  Toolbar,
  Typography,
} from '@mui/material';
import { Link as RouterLink, Outlet, useLocation } from 'react-router-dom';

import { footerHighlights, navigationItems } from '@/core/constants/navigation';
import { useRouteEffects } from '@/core/hooks/useRouteEffects';
import { useFeedbackModalStore } from '@/lib/components/feedback-modal/data/feedbackModalStore';
import { FeedbackModal } from '@/lib/components/feedback-modal/presentation/FeedbackModal';
import { AuthIdentity } from '@/lib/features/auth/presentation/AuthIdentity';

export function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const openModal = useFeedbackModalStore((state) => state.openModal);
  const location = useLocation();

  useRouteEffects();

  return (
    <Box sx={{ minHeight: '100vh', pb: 6 }}>
      <AppBar position="sticky" elevation={0}>
        <Container maxWidth="xl">
          <Toolbar disableGutters sx={{ gap: 2, py: 1 }}>
            <Stack direction="row" spacing={1.5} alignItems="center" sx={{ flexGrow: 1 }}>
              <Box
                component="img"
                src="/virus-mark.svg"
                alt="NoroWatch"
                sx={{ width: 42, height: 42, borderRadius: 3 }}
              />
              <Box>
                <Typography variant="h6" sx={{ fontFamily: '"Space Grotesk", sans-serif' }}>
                  NoroWatch
                </Typography>
                <Typography variant="caption" sx={{ color: 'rgba(248,242,231,0.8)' }}>
                  Norovirus intelligence and self-check
                </Typography>
              </Box>
            </Stack>

            <Stack
              direction="row"
              spacing={1}
              sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center' }}
            >
              {navigationItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Button
                    key={item.path}
                    component={RouterLink}
                    to={item.path}
                    color="inherit"
                    sx={{
                      bgcolor: isActive ? 'rgba(248,242,231,0.14)' : 'transparent',
                      color: 'primary.contrastText',
                    }}
                  >
                    {item.label}
                  </Button>
                );
              })}
            </Stack>

            <Stack
              direction="row"
              spacing={1}
              alignItems="center"
              sx={{ display: { xs: 'none', lg: 'flex' } }}
            >
              <Button
                variant="contained"
                color="secondary"
                startIcon={<MessageRounded />}
                onClick={openModal}
              >
                Share feedback
              </Button>
              <AuthIdentity />
            </Stack>

            <IconButton
              color="inherit"
              sx={{ display: { xs: 'inline-flex', md: 'none' } }}
              onClick={() => setMobileOpen(true)}
            >
              <MenuRounded />
            </IconButton>
          </Toolbar>
        </Container>
      </AppBar>

      <Drawer anchor="right" open={mobileOpen} onClose={() => setMobileOpen(false)}>
        <Box sx={{ width: 300, p: 3 }}>
          <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 3 }}>
            <VirusOutlined color="secondary" />
            <Typography variant="h6">NoroWatch</Typography>
          </Stack>
          <Stack spacing={1.25}>
            {navigationItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Button
                  key={item.path}
                  component={RouterLink}
                  to={item.path}
                  variant={isActive ? 'contained' : 'text'}
                  color={isActive ? 'secondary' : 'inherit'}
                  onClick={() => setMobileOpen(false)}
                  sx={{ justifyContent: 'flex-start' }}
                >
                  {item.label}
                </Button>
              );
            })}
          </Stack>
          <Button
            fullWidth
            variant="contained"
            color="secondary"
            startIcon={<MessageRounded />}
            onClick={() => {
              openModal();
              setMobileOpen(false);
            }}
            sx={{ mt: 3 }}
          >
            Share feedback
          </Button>
          <Box sx={{ mt: 3 }}>
            <AuthIdentity compact />
          </Box>
        </Box>
      </Drawer>

      <Box component="main">
        <Outlet />
      </Box>

      <Container maxWidth="xl" sx={{ mt: 8 }}>
        <Box
          component="footer"
          sx={{
            borderTop: '1px solid rgba(12,59,74,0.1)',
            pt: 3,
            display: 'grid',
            gap: 1,
          }}
        >
          <Typography variant="h6" sx={{ fontFamily: '"Space Grotesk", sans-serif' }}>
            Build once, extend by feature.
          </Typography>
          {footerHighlights.map((highlight) => (
            <Typography key={highlight} variant="body2" color="text.secondary">
              {highlight}
            </Typography>
          ))}
        </Box>
      </Container>

      <FeedbackModal />
    </Box>
  );
}
