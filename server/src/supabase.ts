import { createAdminClient } from '@supabase/server/core';

const url = process.env.SUPABASE_URL;
const secretKey = process.env.SUPABASE_SECRET_KEY;

if (!url || !secretKey) {
  throw new Error('Faltan SUPABASE_URL o SUPABASE_SECRET_KEY en el entorno');
}

// Cliente admin (secret key): bypassea RLS. Cada query DEBE filtrar contenido publicado.
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- sin tipos de DB generados
export const supabase = createAdminClient<any>({
  env: {
    url,
    secretKeys: { default: secretKey },
  },
  supabaseOptions: {
    auth: { persistSession: false, autoRefreshToken: false },
  },
});
