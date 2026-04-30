import { useState } from "react";

const TOKEN_KEY = "carotis:demoToken";

function getStoredToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

function setStoredToken(token: string | null) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch { /* ignore */ }
}

export function useDemoToken() {
  const [token, setToken] = useState<string | null>(getStoredToken);

  const save = (value: string | null) => {
    setStoredToken(value);
    setToken(value);
  };

  return { token, setToken: save };
}
