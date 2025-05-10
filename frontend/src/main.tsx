import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { ThemeProvider } from './components/ThemeProvider';
import { QueryClientProvider } from '@tanstack/react-query';
import queryClient from './client/queryClient';

createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem={false}
      disableTransitionOnChange
  >
    <App />
  </ThemeProvider>
  </QueryClientProvider>
);
