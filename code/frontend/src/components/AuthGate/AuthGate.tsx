import { useState, useEffect } from "react";
import { t } from "@/lib/i18n";
import { useStore } from "@/store";
import { useDemoToken } from "./useDemoToken";

interface Props {
  children: React.ReactNode;
}

export function AuthGate({ children }: Props) {
  const { token, setToken } = useDemoToken();
  const setPhysicianRoleHash = useStore((s) => s.setPhysicianRoleHash);
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [checking, setChecking] = useState(false);

  // Validate token against backend /demo/whoami
  const validate = async (raw: string) => {
    setChecking(true);
    setError("");
    try {
      const baseUrl = import.meta.env.VITE_API_URL as string;
      const res = await fetch(`${baseUrl}/api/v1/demo/whoami`, {
        headers: {
          "X-API-Key": import.meta.env.VITE_API_KEY as string,
          "X-Demo-Token": raw,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setToken(raw);
        if (data.role_hash) {
          setPhysicianRoleHash(data.role_hash);
        }
      } else {
        setError("Ungueltiger oder abgelaufener Demo-Token.");
        setToken(null);
      }
    } catch {
      setError("Server nicht erreichbar. Bitte spaeter erneut versuchen.");
      setToken(null);
    } finally {
      setChecking(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim().length < 8) {
      setError("Token zu kurz.");
      return;
    }
    validate(input.trim());
  };

  // Re-validate stored token on mount
  useEffect(() => {
    if (token) validate(token);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (token) return <>{children}</>;

  return (
    <div className="h-screen flex items-center justify-center bg-slate-950 text-slate-100">
      <div className="w-full max-w-md rounded-xl border border-slate-700 bg-slate-900 p-8 shadow-2xl">
        <div className="mb-6 text-center">
          <h1 className="text-xl font-bold mb-1">{t("app.title")}</h1>
          <p className="text-sm text-slate-400">Demo-Zugang — Token erforderlich</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Demo-Token</label>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Token eingeben..."
              className="w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
              autoFocus
            />
          </div>

          {error && (
            <p className="text-xs text-red-400 bg-red-950/40 border border-red-900/50 rounded px-3 py-2">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={checking || !input.trim()}
            className="w-full rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-2.5 text-sm transition-colors"
          >
            {checking ? "Wird geprueft..." : "Zugang freischalten"}
          </button>
        </form>

        <p className="mt-4 text-xs text-slate-600 text-center">
          Diese Demo enthaelt ausschliesslich synthetische Daten.
          <br />
          Keine Patientendaten werden verarbeitet.
        </p>
      </div>
    </div>
  );
}
