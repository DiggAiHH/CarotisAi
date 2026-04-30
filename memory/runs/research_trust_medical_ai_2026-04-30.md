---
name: 2026-04-30_research_trust_medical_ai
type: research-run
date: 2026-04-30
project: Carotis-AI
---

# Research Synthesis: Trust in Medical AI Systems
> **Scope:** Trust calibration, XAI, confidence communication, human-AI interaction patterns in radiology  
> **Sources:** 14 high-quality studies (2020–2026) from *Radiology*, *European Radiology*, *Radiology: Artificial Intelligence*, *Nature* family, *JMIR*, *PMC*, *arXiv*, *medRxiv*  
> **Context:** Carotis-AI — local-first edge AI for carotid stenosis quantification from CTA (MFSD-UNet + Grad-CAM/SHAP + trust-score service)

---

## 1. Trust Calibration: Over-Trust vs. Under-Trust

### 1.1 Core Finding
Trust calibration is the correspondence between a clinician’s subjective trust and the AI’s objective reliability. The gap manifests as **automation bias** (over-trust ? misuse) and **algorithm aversion** (under-trust ? disuse). Both increase false positives and false negatives.

### 1.2 Key Sources

**A. Prinster, Mahmood, Yi et al. (2024)**  
- *Journal:* **Radiology** (RSNA)  
- *Title:* "Care to Explain? AI Explanation Types Differentially Impact Chest Radiograph Diagnostic Performance and Physician Trust in AI"  
- *DOI:* doi.org/10.1148/radiol.233261  
- **Core finding:** Local explanations (bounding boxes / heatmaps) improved diagnostic accuracy to **92.8%** when the AI was correct, but when the AI was *incorrect*, physician accuracy collapsed to **23.6%** (vs. 26.1% for global explanations). Local explanations accelerated agreement regardless of accuracy — a classic over-reliance signal.  
- **Actionable insight:** *Grad-CAM overlays must be paired with explicit uncertainty indicators or case-level confidence gating. When AI confidence is low, suppress or flag saliency maps rather than presenting them as authoritative.*

**B. Goldsmith-Pinkham, Tan, Zentefis (2026)**  
- *Journal:* **arXiv** (forthcoming; real-world deployment study)  
- *Title:* "Human-AI Collaboration in Radiology: The Case of Pulmonary Embolism"  
- **Core finding:** Analysis of **117,063 CTPA scans** interpreted by **389 radiologists** with an FDA-approved PE-AI tool. Radiologists showed **asymmetric agreement**: they overread AI-positive flags (high sensitivity) but underread AI-negative screens (lower specificity). Disagreement declined after initial deployment but substantial heterogeneity persisted. Diagnostic speed remained stable despite doubled workload.  
- **Actionable insight:** *Implement a "second-read" nudge for AI-negative cases where the model’s confidence sits in an intermediate band. Radiologists need differential cues for positive vs. negative AI outputs.*

**C. Ming Yin / HCI Meta-Literature (cited in multiple 2024–2025 reviews)**  
- *Concept:* Trust calibration framework  
- **Core finding:** Over-trust is highest at trust levels 9–10; under-trust is highest below 5. Extreme trust values act as cognitive biases.  
- **Actionable insight:** *Design the Carotis-AI trust-score UI to avoid a 0–100 linear scale. Use a 3-zone visualization (Low / Uncertain / High) centered on calibrated probability thresholds, with explicit color breaks at the 5 and 9 boundaries.*

---

## 2. Explainable AI (XAI) Impact on Clinician Trust

### 2.1 Core Finding
XAI increases clinician confidence and diagnostic accuracy **when explanations align with clinical intuition**. However, explanations can become heuristics that *reinforce* automation bias if the AI is wrong. Method effectiveness is specialty-dependent: radiologists prefer visual heatmaps (Grad-CAM), while pathologists and EHR-based diagnosticians prefer feature attributions (SHAP).

### 2.2 Key Sources

**D. Systematic Review — PMC (2025/2026)**  
- *Journal:* **PMC / Frontiers** (systematic review, PMC12809972)  
- *Title:* "Explainable artificial intelligence (XAI) in medical imaging"  
- **Core finding:** In controlled studies, **87%** of clinicians found AI outputs interpretable and actionable when supplemented with XAI visualizations. **Grad-CAM received 89% clinician approval** for imaging tasks; SHAP received 85% for EHR/tabular data. Attention maps were noted as potentially misleading ("attention ? explanation").  
- **Actionable insight:** *Carotis-AI should present Grad-CAM/HiResCAM as the primary visual explanation (radiology-native) and reserve SHAP for supplementary feature-level metadata (e.g., plaque composition scores if multimodal inputs are added later).*

**E. Springer Comprehensive Review (2025)**  
- *Journal:* **Cluster Computing** (Springer)  
- *Title:* "Explainable artificial intelligence for medical imaging systems using deep learning: a comprehensive review"  
- **Core finding:** Longitudinal multi-hospital studies found that after **6 months** of AI-assisted diagnosis, clinicians were significantly more likely to accept AI recommendations than during initial trials. Hybrid models combining Grad-CAM heatmaps with structured textual explanations improved usability in emergency departments, whereas LIME alone was too inconsistent for stroke CT.  
- **Actionable insight:** *Plan a 6-month onboarding / trust-acclimatization phase at Klinikum Dortmund. Provide textual rationales alongside heatmaps (e.g., "Stenosis severity driven by calcified plaque at ICA bulb") to match emergency-medicine best practices.*

**F. Tonekaboni et al. (cited in Springer review, 2023)**  
- *Journal:* **Original study referenced in review**  
- **Core finding:** Survey of 200 physicians: clinicians trust AI decisions **when explanations align with their diagnostic reasoning**. Excessively complex or ambiguous explanations reduced trust, especially when outputs conflicted with human intuition.  
- **Actionable insight:** *Keep explanations simple and anatomically grounded. If Grad-CAM highlights a region that contradicts the radiologist’s visual assessment, the system should flag itself for uncertainty rather than forcing a complex explanation.*

**G. MDPI Meta-Analysis (2025)**  
- *Journal:* **Healthcare** (MDPI)  
- *Title:* "Explainable AI in Clinical Decision Support Systems: A Meta-Analysis of Methods, Applications, and Usability Challenges"  
- **Core finding:** Counterfactual explanations ("what would need to change for a different diagnosis?") showed promise in psychiatry and risk prediction but are underexplored in radiology. SHAP + Grad-CAM multimodal combinations yielded highest acceptance in multimodal CDSS.  
- **Actionable insight:** *For Carotis-AI Phase P4+, consider adding a lightweight counterfactual module: "If this plaque were non-calcified, the model would predict moderate rather than severe stenosis." This encourages critical reflection rather than passive acceptance.*

---

## 3. Trust Scores / Confidence Indicators

### 3.1 Core Finding
Raw model probabilities are poorly calibrated in medical deep learning. **Isotonic regression** consistently outperforms Platt scaling and temperature scaling for post-hoc calibration in clinical settings, especially when calibration sets are small to moderate. Uncalibrated high-confidence predictions are a major driver of automation bias.

### 3.2 Key Sources

**H. Post-Hoc Calibration for Heart Disease (2025)**  
- *Journal:* **medRxiv** (preprint)  
- *Title:* "A post hoc calibration approach for heart disease prediction"  
- *DOI:* doi.org/10.1101/2025.09.28.25336834  
- **Core finding:** Despite perfect test-set discrimination (100% accuracy for RF/XGBoost), reliability diagrams revealed **overconfidence pre-calibration**. Isotonic calibration consistently improved probability quality: Random Forest Brier score dropped from 0.007 ? 0.002, ECE from 0.051 ? 0.011. Platt scaling occasionally worsened calibration (e.g., KNN ECE increased).  
- **Actionable insight:** *Carotis-AI’s confidence_calibration_service.py should prioritize Isotonic Regression as the default post-hoc calibrator. Validate with Spiegelhalter’s Z-test on a held-out clinical validation set before deployment.*

**I. "Making Machine Learning Predictions Trustworthy" (2025)**  
- *Journal:* **arXiv** (2509.23665)  
- **Core finding:** Rigorous 50-run cross-validation on Random Forest: Isotonic Regression achieved **80.4% ECE improvement** (ECE 0.0340 ± 0.0080) vs. **74.1% for Platt Scaling** (ECE 0.0449 ± 0.0094). Both were statistically significant (p < 0.001), but isotonic had superior reliability scores (0.9660 vs. 0.9551).  
- **Actionable insight:** *Use isotonic regression for the trust-score computation. Display the calibrated probability alongside a qualitative label (e.g., "Calibrated Confidence: 78% — Moderate Certainty") rather than raw softmax outputs.*

**J. Emergent Mind Synthesis / Calibration Methodologies (2025)**  
- *Concept:* Dynamic trust calibration frameworks  
- **Core finding:** Multicalibration (calibration across patient subgroups) is a sufficient condition for utility-monotonic, human-aligned trust policies. LinUCB and decision-tree bandit variants yielded **10–38% increases in task rewards** by adaptively learning when to recommend trusting AI predictions.  
- **Actionable insight:** *For Carotis-AI P5+, implement subgroup-aware calibration: separate isotonic regressors for different CTA scanner protocols or patient age groups to avoid systematic miscalibration on underrepresented subpopulations.*

---

## 4. Human-AI Interaction Patterns That Maximize Appropriate Trust

### 4.1 Core Finding
Appropriate trust is not a static property — it evolves with exposure, feedback, and system design. Key patterns: (1) onboarding tutorials that set realistic expectations *before* first use; (2) confidence scores + visual evidence + feature explanations presented together; (3) forced deliberation (cognitive forcing) when trust is high; (4) decision-referral systems that route uncertain cases to human experts.

### 4.2 Key Sources

**K. Bergquist, Rolandsson, Gryska et al. (2023)**  
- *Journal:* **European Radiology**  
- *Title:* "Trust and stakeholder perspectives on the implementation of AI tools in clinical radiology"  
- *DOI:* 10.1007/s00330-023-09967-5  
- **Core finding:** Semi-structured interviews with 25 stakeholders identified **four aspects of trust**: reliability, transparency, quality verification, and inter-organizational compatibility. Substantial and procedural requirements must both be met.  
- **Actionable insight:** *Carotis-AI should document its quality verification pipeline (external validation, DICOM anonymization, model signing) in a transparent "trust dashboard" visible to radiologists. Trust is not just about the model — it is about the entire socio-technical system.*

**L. Expectation Management & Model Transparency Study (Wiley, 2024)**  
- *Journal:* **Journal of Medical Imaging and Radiation Oncology**  
- **Core finding:** An onboarding tutorial setting realistic expectations before initial use + AI model explainability during use both significantly affected radiologists’ trust calibration in lung nodule CT assessment. Trust is dynamic and influenced by system design, personal characteristics, workload, and prior interactions.  
- **Actionable insight:** *Build a 5-minute interactive onboarding module into the Carotis-AI frontend before radiologists can submit their first case. Include explicit failure-mode examples (e.g., "AI may underestimate stenosis in heavily calcified vessels").*

**M. Adaptive Explanations / Trust Calibration Cues (2025)**  
- *Journal:* **arXiv** (2502.13321)  
- **Core finding:** User studies with doctors (Diagnosis task, 20 physicians) showed that **supporting explanations** reduced under-reliance when trust was low (< 5), while **counter-explanations** reduced over-reliance when trust was high (> 8). Forced deliberation (10-second wait) when trust was high improved final decision accuracy.  
- **Actionable insight:** *Implement an adaptive explanation layer in Carotis-AI: if the radiologist overrides the AI frequently (low trust), show supporting evidence (similar past cases, guideline citations). If the radiologist accepts AI advice rapidly on high-confidence cases (potential over-trust), trigger a lightweight cognitive forcing function (e.g., "Please confirm you have reviewed the contralateral artery").*

**N. Linguraru, Bakas, Chang et al. / RSNA & MICCAI (2024)**  
- *Journal:* **Radiology: Artificial Intelligence**  
- *Title:* "Clinical, Cultural, Computational, and Regulatory Considerations to Deploy AI in Radiology: Perspectives of RSNA and MICCAI Experts"  
- *DOI:* 10.1148/ryai.240225  
- **Core finding:** Experts emphasized that trust, reproducibility, explainability, and accountability are intertwined. Clinical penetration depends on **collaboration** between radiologists and AI scientists, integration of clinical and imaging data, and smooth workflow integration.  
- **Actionable insight:** *Position Carotis-AI as a "collaborative second reader" rather than a diagnostic authority. Ensure PACS integration and HL7/FHIR connectivity are part of the trust architecture, not just technical nice-to-haves.*

---

## 5. Top 5 Findings — Executive Summary for Carotis-AI

| # | Finding | Direct Evidence | Implementation for Carotis-AI |
|---|---------|-----------------|------------------------------|
| **1** | **Local visual explanations (Grad-CAM) boost accuracy when AI is right but dangerously amplify over-reliance when AI is wrong.** | Prinster et al., *Radiology* 2024: accuracy 92.8% (correct AI + local expl.) vs. 23.6% (incorrect AI + local expl.) | Pair every Grad-CAM overlay with a **calibrated confidence band**; suppress or watermark saliency when confidence < threshold. |
| **2** | **Isotonic regression outperforms Platt scaling for clinical probability calibration.** | medRxiv 2025 (heart disease) + arXiv 2509.23665: Isotonic achieves 80.4% ECE improvement vs. 74.1% for Platt; Platt can worsen calibration on some models. | Set **Isotonic Regression as the default** in `confidence_calibration_service.py`; validate with Spiegelhalter’s Z-test. |
| **3** | **Trust is dynamic and specialty-specific; radiologists prefer visual heatmaps, but only when aligned with anatomical expectation.** | PMC systematic review 2025: 89% clinician approval for Grad-CAM; Tonekaboni et al. 2023: trust drops when explanations conflict with intuition. | Run a **radiologist validation study** at Klinikum Dortmund: do Grad-CAM highlights for carotid plaques align with expert annotations? If not, retrain or adjust attribution thresholds. |
| **4** | **Real-world deployment shows asymmetric reliance: radiologists overread AI positives and underread AI negatives.** | Goldsmith-Pinkham et al. 2026 (117,063 CTPA scans): AI-positive flags get high agreement; AI-negative screens do not. | Implement **differential UI treatment** for positive vs. negative findings. For AI-negative intermediate-confidence cases, add a "second look required" badge. |
| **5** | **Adaptive explanations + cognitive forcing functions simultaneously combat under-trust and over-trust.** | arXiv 2502.13321: supporting expl. for low trust, counter-explanations for high trust, and forced deliberation both reduced inappropriate reliance. | Build a **decision-tree-harvesting layer** that adapts: (a) show guideline citations when radiologist disagrees with AI (under-trust), (b) show counterfactuals / require confirmation when radiologist agrees too quickly with high-confidence AI (over-trust). |

---

## 6. Full Source Bibliography

1. **Prinster D, Mahmood A, Yi PH, Huang C-M, et al.** (2024). "Care to Explain? AI Explanation Types Differentially Impact Chest Radiograph Diagnostic Performance and Physician Trust in AI." *Radiology*. doi:10.1148/radiol.233261
2. **Goldsmith-Pinkham P, Tan C, Zentefis AK.** (2026). "Human-AI Collaboration in Radiology: The Case of Pulmonary Embolism." *arXiv:2601.13379*.
3. **Hasani N, Morris MA, Rahmim A, Summers RM, et al.** (2022). "Trustworthy Artificial Intelligence in Medical Imaging." *PET Clinics*, 17(1):1–12. PMID: 34809860
4. **Bergquist M, Rolandsson B, Gryska E, Laesser M, et al.** (2023). "Trust and stakeholder perspectives on the implementation of AI tools in clinical radiology." *European Radiology*. doi:10.1007/s00330-023-09967-5
5. **Linguraru MG, Bakas S, Aboian M, Chang PD, et al.** (2024). "Clinical, Cultural, Computational, and Regulatory Considerations to Deploy AI in Radiology: Perspectives of RSNA and MICCAI Experts." *Radiology: Artificial Intelligence*. doi:10.1148/ryai.240225
6. **Systematic Review** (2025). "Explainable artificial intelligence (XAI) in medical imaging." *PMC12809972* / *Frontiers in Artificial Intelligence*.
7. **Springer Review** (2025). "Explainable artificial intelligence for medical imaging systems using deep learning: a comprehensive review." *Cluster Computing*. doi:10.1007/s10586-025-05281-5
8. **MDPI Meta-Analysis** (2025). "Explainable AI in Clinical Decision Support Systems: A Meta-Analysis of Methods, Applications, and Usability Challenges." *Healthcare*, 13(17):2154.
9. **medRxiv Preprint** (2025). "A post hoc calibration approach for heart disease prediction." doi:10.1101/2025.09.28.25336834
10. **arXiv** (2025). "Making Machine Learning Predictions Trustworthy." *arXiv:2509.23665*.
11. **arXiv** (2025). "Adaptive Explanations for Trust Calibration in Human-AI Decision Making." *arXiv:2502.13321*.
12. **Wiley / Journal of Medical Imaging and Radiation Oncology** (2024). "The Impact of Expectation Management and Model Transparency on Radiologists' Trust and Utilization of AI Recommendations for Lung Nodule Assessment on CT."
13. **Zhang Z, et al.** (2021). "Patients' perceptions of using artificial intelligence (AI)-based technology to comprehend radiology imaging data." *Health Informatics J*, 27(2). PMID: 33913359
14. **Dratsch et al.** (2023). Automation bias in mammography CAD. Referenced in multiple 2024–2025 review papers.

---

## 7. Next Steps for Carotis-AI

| Priority | Action | Owner | Phase |
|----------|--------|-------|-------|
| High | Replace Platt scaling default with Isotonic Regression in calibration service; add Spiegelhalter test | ML/Backend | P1 |
| High | Design 3-zone trust-score UI (Low/Uncertain/High) with color breaks at calibrated thresholds | Frontend | P2 |
| Medium | Add lightweight cognitive forcing: confirmation prompt for rapid acceptance of high-confidence AI | Frontend | P2 |
| Medium | Draft radiologist validation protocol: Grad-CAM alignment with expert plaque annotations | Clinical/Lou | P3 |
| Medium | Build onboarding tutorial with explicit failure-mode examples (calcification artifacts, etc.) | Frontend | P2 |
| Low | Explore counterfactual explanations for Phase P4+ ("What if plaque were non-calcified?") | ML/Hermes | P4 |

---

*Compiled by: Research Agent*  
*Date: 2026-04-30*  
*Relevant to: T-XXX (trust-score UI design), backend confidence calibration, ethics/DSA arguments*
