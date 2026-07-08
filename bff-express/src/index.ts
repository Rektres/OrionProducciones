import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import axios from 'axios';

const app = express();

const DJANGO_API_URL = process.env.DJANGO_API_URL || 'http://localhost:8000';
const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'http://localhost:5173')
  .split(',')
  .map((o) => o.trim());

app.use(cors({ origin: allowedOrigins }));
app.use(express.json());

app.get('/health', (_req, res) => res.json({ ok: true }));

// Proxy fino: reenvia cualquier /api/* a Django conservando metodo, query y body.
app.use('/api', async (req, res) => {
  try {
    const upstream = await axios({
      method: req.method,
      url: DJANGO_API_URL + req.originalUrl,
      data: req.body,
      headers: { 'Content-Type': 'application/json' },
      validateStatus: () => true,
    });
    res.status(upstream.status).json(upstream.data);
  } catch (err) {
    res.status(502).json({ error: 'Error contactando el API de datos' });
  }
});

const port = Number(process.env.PORT) || 3001;
app.listen(port, () => {
  console.log(`Orion BFF escuchando en http://localhost:${port} -> ${DJANGO_API_URL}`);
});
