import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { createProxyMiddleware, fixRequestBody } from 'http-proxy-middleware';
import type { ServerResponse } from 'node:http';

const app = express();

const DJANGO_API_URL = process.env.DJANGO_API_URL || 'http://localhost:8000';
const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'http://localhost:5173')
  .split(',')
  .map((o) => o.trim());

app.use(cors({ origin: allowedOrigins }));

// Solo parsea application/json. Los bodies multipart/form-data no los toca
// (express.json() hace next() sin leer el stream), asi que el proxy los
// streamea crudos hacia Django: eso es lo que habilita subir imagenes.
app.use(express.json({ limit: '1mb' }));

// Rutas locales del BFF. Deben quedar antes del proxy: Django solo expone
// /health, no /api/health.
app.get('/health', (_req, res) => res.json({ ok: true }));
app.get('/api/health', (_req, res) => res.json({ ok: true }));

// Proxy fino: reenvia /api/* a Django conservando metodo, query string,
// headers del cliente (incluido Authorization) y body (JSON o binario).
app.use(
  createProxyMiddleware({
    target: DJANGO_API_URL,
    changeOrigin: true,
    pathFilter: '/api',
    xfwd: true,
    timeout: 30_000,
    proxyTimeout: 30_000,
    on: {
      // express.json() ya consumio el stream en los requests JSON:
      // fixRequestBody lo reescribe y recalcula Content-Length.
      proxyReq: (proxyReq, req) => {
        // GET/HEAD no llevan body. express.json() deja req.body = {} y
        // fixRequestBody lo serializaria como "{}", desincronizando el
        // framing de la respuesta upstream: Node abortaba el HEAD con
        // "Parse Error: Data after `Connection: close`" -> 502.
        const metodo = (req.method || '').toUpperCase();
        if (metodo === 'GET' || metodo === 'HEAD') return;
        fixRequestBody(proxyReq, req);
      },
      error: (err, _req, res) => {
        console.error('[bff] error de proxy:', err.message);
        const response = res as ServerResponse;
        if (typeof response.writeHead !== 'function' || response.headersSent) return;
        response.writeHead(502, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify({ error: 'Error contactando el API de datos' }));
      },
    },
  }),
);

const port = Number(process.env.PORT) || 3001;
app.listen(port, () => {
  console.log(`Orion BFF escuchando en http://localhost:${port} -> ${DJANGO_API_URL}`);
});
