import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { serviciosRouter } from './routes/servicios.js';
import { portafolioRouter } from './routes/portafolio.js';
import { blogRouter } from './routes/blog.js';
import { cotizacionesRouter } from './routes/cotizaciones.js';

const app = express();

const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'http://localhost:5173')
  .split(',')
  .map((o) => o.trim());

app.use(cors({ origin: allowedOrigins }));
app.use(express.json());

app.get('/health', (_req, res) => res.json({ ok: true }));

app.use('/api/servicios', serviciosRouter);
app.use('/api/portafolio', portafolioRouter);
app.use('/api/blog', blogRouter);
app.use('/api/cotizaciones', cotizacionesRouter);

const port = Number(process.env.PORT) || 3001;
app.listen(port, () => {
  console.log(`Orion API escuchando en http://localhost:${port}`);
});
