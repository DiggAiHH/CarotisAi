import { useEffect, useRef, useState } from "react";
import { useDebouncedCallback } from "use-debounce";
import { apiClient } from "@/lib/apiClient";

interface PIISpan {
  start: number;
  end: number;
  label: string;
}

interface FreeTextFieldProps {
  value: string;
  onChange: (v: string) => void;
  maxLength?: number;
  placeholder?: string;
  hintText?: string;
}

export function FreeTextField({
  value,
  onChange,
  maxLength = 2000,
  placeholder = 'z.B. "Plaque-Form unklar, wuerde Verlaufskontrolle in 6 Monaten machen wenn Symptome zunehmen."',
  hintText = "Was ist offen oder unsicher? Was wuerdest du noch klaeren? Keine Patientennamen — wir filtern automatisch und lehnen den Eintrag ab, wenn welche drin sind.",
}: FreeTextFieldProps) {
  const [spans, setSpans] = useState<PIISpan[]>([]);
  const [checking, setChecking] = useState(false);
  const taRef = useRef<HTMLTextAreaElement>(null);

  const checkText = useDebouncedCallback(async (text: string) => {
    if (!text) {
      setSpans([]);
      return;
    }
    setChecking(true);
    try {
      const r = await apiClient.checkText(text);
      setSpans(r.pii_spans);
    } catch {
      // Silent fail — Frontend-Check is UX-Hint, Backend is autoritativ (B-14)
      setSpans([]);
    } finally {
      setChecking(false);
    }
  }, 500);

  useEffect(() => {
    checkText(value);
  }, [value, checkText]);

  // Auto-Save in localStorage (5s debounced)
  const saveDraft = useDebouncedCallback((text: string) => {
    localStorage.setItem("dt:free_text_draft", text);
  }, 5000);
  useEffect(() => saveDraft(value), [value, saveDraft]);

  const counterColor =
    value.length > 1900 ? "text-orange-400" : "text-slate-400";
  const hasPII = spans.length > 0;

  return (
    <div className="space-y-2">
      <label className="block text-sm text-slate-200">
        Was ist offen / unsicher?{" "}
        <span className="text-slate-500">(optional)</span>
      </label>
      <div className="relative">
        <textarea
          ref={taRef}
          value={value}
          onChange={(e) => onChange(e.target.value.slice(0, maxLength))}
          placeholder={placeholder}
          rows={4}
          maxLength={maxLength}
          className={`w-full bg-slate-900 border ${
            hasPII ? "border-red-500" : "border-slate-700"
          } rounded p-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 resize-none`}
        />
        <div className={`absolute bottom-2 right-3 text-xs ${counterColor}`}>
          {value.length}/{maxLength}
          {checking && <span className="ml-2 text-cyan-400">pruefe...</span>}
        </div>
      </div>
      <p className="text-xs text-slate-400">{hintText}</p>
      {hasPII && (
        <div className="bg-red-950 border border-red-800 rounded p-2 text-xs text-red-200">
          <strong>Moegliche personenbezogene Daten gefunden:</strong>{" "}
          {spans.map((s, i) => (
            <span key={i} className="mx-1 px-1 bg-red-900 rounded">
              {s.label}
            </span>
          ))}
          <br />
          Bitte umformulieren — wir koennen den Eintrag sonst nicht speichern.
        </div>
      )}
    </div>
  );
}
