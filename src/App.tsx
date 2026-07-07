import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Landing } from './pages/Landing';
import { Servicios } from './pages/Servicios';
import { PortafolioLista, PortafolioDetalle } from './pages/Portafolio';
import { BlogLista, BlogDetalle } from './pages/Blog';

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/servicios" element={<Servicios />} />
        <Route path="/portafolio" element={<PortafolioLista />} />
        <Route path="/portafolio/:slug" element={<PortafolioDetalle />} />
        <Route path="/blog" element={<BlogLista />} />
        <Route path="/blog/:slug" element={<BlogDetalle />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
