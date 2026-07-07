import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Landing } from './pages/Landing';
import { Servicios } from './pages/Servicios';
import { PortafolioLista, PortafolioDetalle } from './pages/Portafolio';
import { BlogLista, BlogDetalle } from './pages/Blog';
import { ErrorBoundary } from './components/shared/ErrorBoundary';
import { ConfigNotice } from './components/shared/ConfigNotice';
import { isSupabaseConfigured } from './lib/supabase';

function App() {
  if (!isSupabaseConfigured) {
    return <ConfigNotice />;
  }

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/servicios" element={<Servicios />} />
          <Route path="/portafolio" element={<PortafolioLista />} />
          <Route path="/portafolio/:slug" element={<PortafolioDetalle />} />
          <Route path="/blog" element={<BlogLista />} />
          <Route path="/blog/:slug" element={<BlogDetalle />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
