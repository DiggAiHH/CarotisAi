import { Component, type ReactNode } from "react";
import { t } from "@/lib/i18n";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to backend for demo tracking (best-effort)
    try {
      const baseUrl = import.meta.env.VITE_API_URL as string;
      fetch(`${baseUrl}/api/v1/demo/log-error`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": import.meta.env.VITE_API_KEY as string,
        },
        body: JSON.stringify({
          message: error.message,
          stack: error.stack?.slice(0, 500),
          componentStack: errorInfo.componentStack?.slice(0, 500),
        }),
      }).catch(() => {});
    } catch {
      // ignore
    }
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="h-screen flex items-center justify-center bg-slate-950 text-slate-100">
          <div className="max-w-md text-center p-8">
            <h2 className="text-xl font-bold text-red-400 mb-2">
              {t("error.title")}
            </h2>
            <p className="text-sm text-slate-400 mb-4">
              {t("error.description")}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-medium px-6 py-2.5 text-sm transition-colors"
            >
              {t("error.reload")}
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
