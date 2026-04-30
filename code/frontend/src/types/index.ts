// ---- API response types ----

export interface VulnerabilityMarkers {
  intraplaque_hemorrhage: number;
  thin_fibrous_cap: number;
  lipid_rich_necrotic_core: number;
  systolic_motion_anomaly: number;
}

export interface InferenceResponse {
  case_id: string;
  stenosis_pct_nascet: number;
  confidence: number;
  confidence_bucket: string | null;
  trust_score: number | null;
  calibrated: boolean;
  vulnerability_markers: VulnerabilityMarkers;
  model_version: string;
  model_sha: string;
  audit_id: string;
  captured_at: string;
  heatmap_b64: string | null;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean | null;
  db_ok: boolean | null;
  ollama_reachable: boolean | null;
  timestamp: string;
}

// ---- Decision-Tree capture ----

export type AgreementVerdict =
  | "full_agreement"
  | "partial_agreement"
  | "disagreement"
  | "physician_override";

export type ConfidenceLevel = "low" | "medium" | "high" | "very_high";

export type OverrideReason =
  | "patient_specific"
  | "clinical_judgment"
  | "insufficient_evidence"
  | "alert_fatigue"
  | "other";

export type StenosisVerdict = "normal" | "mild" | "moderate" | "severe" | "critical";

export interface Disagreement {
  ai_verdict: StenosisVerdict;
  physician_verdict: StenosisVerdict;
  override_reason: OverrideReason;
  override_free_text?: string;
}

export interface DecisionTreeRequest {
  case_id: string;
  captured_at: string;
  physician_role_hash: string;
  ai_prediction: {
    stenosis_pct_nascet: number;
    confidence: number;
    vulnerability_markers: VulnerabilityMarkers;
    model_version: string;
    model_sha: string;
  };
  physician_decision: {
    stenosis_pct_nascet: number;
    confidence_self_reported?: ConfidenceLevel | null;
    confirmed_markers: string[];
    rejected_markers: string[];
    added_markers: string[];
  };
  reasoning?: {
    deciding_feature?: string | null;
    ruled_out: string[];
    ruled_out_reason?: string | null;
    would_consult?: string | null;
    would_re_image_if?: string | null;
    free_text_notes?: string | null;
  } | null;
  agreement_with_ai: {
    verdict: AgreementVerdict;
    delta_pct: number;
    delta_markers: string[];
    trust_score_for_this_case: number;
  };
  anonymisation: {
    method: "DICOM_PS_3.15_basic" | "DICOM_PS_3.15_research" | "custom_v1";
    salt_version: string;
    audit_id: string;
    k_anonymity_min: number;
  };
  disagreement?: Disagreement | null;
}

export interface DecisionTreeResponse {
  id: number;
  case_id: string;
  captured_at: string;
  agreement_verdict: AgreementVerdict;
  delta_pct: number | null;
}

// ---- UI state ----

export type AnalysisStatus = "idle" | "uploading" | "analysing" | "done" | "error";
