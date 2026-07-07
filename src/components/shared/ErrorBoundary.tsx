import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Unhandled error rendering the app:', error, info.componentStack);
  }

  render() {
    if (!this.state.error) {
      return this.props.children;
    }

    return (
      <div className="min-h-screen flex items-center justify-center bg-surface text-text px-6">
        <div className="max-w-lg text-center">
          <h1 className="text-3xl font-bebas tracking-wider mb-4">Algo salió mal</h1>
          <p className="text-text/70 mb-2">
            La aplicación no pudo cargar correctamente. Intenta recargar la página.
          </p>
          <p className="text-xs text-text/40 mt-6">{this.state.error.message}</p>
        </div>
      </div>
    );
  }
}
