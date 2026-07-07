export function ConfigNotice() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-surface text-text px-6">
      <div className="max-w-lg text-center">
        <h1 className="text-3xl font-bebas tracking-wider mb-4">Configuración pendiente</h1>
        <p className="text-text/70">
          Faltan las variables de entorno de Supabase (<code>VITE_SUPABASE_URL</code> y{' '}
          <code>VITE_SUPABASE_ANON_KEY</code>). Configúralas en Site settings → Environment
          variables y vuelve a desplegar el sitio.
        </p>
      </div>
    </div>
  );
}
