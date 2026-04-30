---
name: 2026-04-29_research_deep_dive
type: run
model: Sonnet 4.6
---
# Deep Research: State-of-the-Art Verbesserungen fuer Carotis-AI
*Generated: 2026-04-29 | Quellen: 35+ | Confidence: High*

## Executive Summary

Diese Recherche deckt sechs Schluesselbereiche ab, in denen Carotis-AI von neuester Methodik profitieren kann:

1. **MFSD-UNet ist weiterhin State-of-the-Art** fuer Carotis-CTA-Segmentierung (Dice 0.912 in 2025 veroeffentlicht), aber **Vision-Mamba-Architekturen** (U-Mamba, VM-UNet) bieten lineare statt quadratische Komplexitaet und koennten bei 3D-CTA-Volumina deutlich effizienter sein.

2. **XAI: Grad-CAM + SHAP bleiben Standard**, aber **TCAV (Testing with Concept Activation Vectors)** koennte uns ermoeglichen, nicht nur *wo* das Modell hinschaut, sondern *welche medizinischen Konzepte* (z.B. "duenne Fibrokappe", "lipidreiche Nekrose") die Entscheidung beeinflussen.

3. **Reasoning Capture: Die AHRQ-CDSiC-Taxonomie fuer Override-Reasons** ist ein uebersehener Standard, der unsere Decision-Tree-Harvesting-Struktur verbessern koennte.

4. **Privacy: Federated Learning ist reif fuer P3** -- Frameworks wie NVIDIA FLARE, Flower und PySyft ermoeglichen Multi-Site-Training ohne Daten-Export.

5. **NLP: BERTopic ist weiterhin valide**, aber **BioGottBERT** (deutsches klinisches BERT) koennte unsere PII-Detection und Keyword-Extraktion aus freien Arzttexten erheblich verbessern.

6. **Regulatory: EU AI Act + MDR -- entscheidender Deadline-Shift**. Medizinprodukte (Class IIa) haben bis **2. August 2027** Zeit (nicht 2026!). Unser Audit-Trail + Decision-Tree-Harvesting deckt bereits zentrale AI-Act-Anforderungen ab.

---

## 1. Deep Learning Architekturen fuer Carotis-Stenose & Plaque

### 1.1 MFSD-UNet Bestaetigung (unsere aktuelle Architektur)

Eine 2025 in *Quantitative Imaging in Medicine and Surgery* veroeffentlichte Studie (Xie et al.) evaluiert genau unseren Ansatz:

- **MFSD-UNet** erreicht **Dice 0.9119**, Accuracy 0.9819, Sensitivity 0.9924
- Verglichen mit Swin-UNet (0.8910), MFD-UNet (0.8770), RA-UNet (0.8371)
- **Ablation:** Entfernen des Swin Transformers reduziert Dice auf 0.8630
- Entfernen von Deep Supervision reduziert auf 0.8371
- Evaluation time: **27.3s (AI) vs. 296.8s (Arzt)** -- 10x schneller

> Quelle: [Xie et al., QIMS 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11994491/)

**Fazit:** Unsere Architekturwahl ist wissenschaftlich validiert und fuehrend. Kein dringender Wechsel noetig.

### 1.2 Vision Mamba: Die naechste Generation?

2024-2025 hat eine Welle von **State Space Models (SSMs)** -- insbesondere **Mamba** -- die Medical Image Segmentation erreicht:

| Modell | Jahr | Innovation | Vorteil |
|--------|------|------------|---------|
| U-Mamba | 2024 | Hybrid CNN+SSM Block | Lineare Komplexitaet, 3D-tauglich |
| VM-UNet | 2024 | Reiner SSM-Encoder-Decoder | 3.49% besser als U-Net |
| H-VMUNet | 2025 | High-order 2D Selective Scanning | 67% weniger Parameter als VM-UNet |
| VMAXL-UNet | 2025 | SSM + xLSTM Hybrid | Beste Segmentation auf multiplen Datasets |
| SegMamba | 2025 | 3D Vision Mamba | 7% Dice-Improvement, stabileres Training |
| Weak-Mamba-UNet | 2026 | CNN + ViT + VMamba Ensemble | Scribble-based weak supervision |

**Kernargument:** Swin Transformer hat **quadratische Komplexitaet** O(n^2) bezueglich der Patch-Anzahl. Mamba hat **lineare Komplexitaet** O(n). Bei 3D-CTA-Volumina (512x512x200+ Voxel) kann dies den Unterschied zwischen "laeuft auf Edge-Hardware" und "braucht GPU-Cluster" ausmachen.

> Quellen: [Nature Sci Rep 2025](https://www.nature.com/articles/s41598-025-88967-5), [Neurocomputing 2025](https://www.sciencedirect.com/science/article/abs/pii/S0925231225001195), [IJCAI 2025](https://www.ijcai.org/proceedings/2025/0245.pdf)

**Empfehlung fuer Carotis-AI:**
- **P2/P3:** Experimentiere mit **U-Mamba** als MFSD-UNet-Nachfolger. Der Hybrid-CNN+SSM-Ansatz behaelt lokale Feature-Extraktion bei (wie U-Net) und verbessert globale Kontext-Modellierung.
- **Vorteil:** U-Mamba basiert auf nnUNet -- unserer bestehenden Codebasis sehr aehnlich.

### 1.3 Plaque Vulnerability: Was ist der SOTA?

Eine 2025 Scoping Review (Saba et al., Medicina) analysiert 12 Studien (2021-2025):

| Modalitaet | Beste AUC | Methode |
|------------|-----------|---------|
| Ultrasound (CEUS) | 0.87 | Contrast-enhanced videomics |
| CTA | 0.987 | Histology-referenced DL pilot |
| CTA | 0.89 | Symptomatic-plaque ML model |
| MRI (HR-MRI) | 0.984 | Multi-contrast radiomics |

**Wichtige Erkenntnis:** Die Kombination von **Radiomics + Deep Learning** (sog. "Deep Radiomics") uebertrifft reine DL-Ansaetze bei Plaque-Vulnerability. Features wie **perivaskulaeres Fettgewebe (PVAT)** und texturale CTA-Features sind praediktiv.

> Quelle: [Saba et al., Medicina 2025](https://www.mdpi.com/1648-9144/61/12/2082)

**Empfehlung fuer Carotis-AI:**
- **P4/P5:** Erweitere das Modell um einen **Radiomics-Branch** neben dem CNN-Branch. Das MFSD-UNet segmentiert die Plaque; ein paralleler Radiomics-Extraktor (Haralick, Laws, LBP) berechnet texturale Features aus der ROI. Kombiniert mit dem Deep-Learning-Feature-Vector vor der Klassifikationsschicht.

---

## 2. Explainable AI (XAI): Jenseits von Grad-CAM

### 2.1 Aktueller Stand der XAI-Methoden (2025-2026)

Eine 2026 Uebersicht in *Sensors* systematisiert XAI fuer Medical Imaging:

| Methode | Typ | Beste fuer | Limitation |
|---------|-----|------------|------------|
| Grad-CAM / EigenGrad-CAM | Gradient-based | Echtzeit-Diagnostik (<3s) | Moderate raeumliche Praezision |
| Integrated Gradients | Gradient-based | Hohe Kontrast-Modalitaeten (CT) | Rechnet fuer jede Pixelreihe |
| LIME / SHAP | Perturbation-based | Modell-agnostisch | Hohe Rechenkosten |
| **TCAV** | **Concept-based** | **Semantische Erklaerungen** | **Benutzerdefinierte Konzepte noetig** |
| StylEx | Counterfactual | Confounding-Feature-Detection | Uninterpretierbare latente Attribute |
| Attention Rollout | Attention-based | Transformer-Modelle | Modell-spezifisch |

> Quelle: [Sensors 2026](https://www.mdpi.com/1424-8220/26/7/2131), [ACM 2026](https://dl.acm.org/doi/10.1145/3788112.3788141)

### 2.2 TCAV fuer Plaque-Vulnerability-Erklaerungen

**Testing with Concept Activation Vectors (TCAV, Kim et al. 2018)** ist fuer Carotis-AI besonders relevant:

- Statt zu fragen "welche Pixel sind wichtig?" (Grad-CAM), fragt TCAV: "wie wichtig ist das medizinische Konzept X fuer die Vorhersage?"
- Beispiel-Konzepte fuer uns: "lipidreiche Nekrose", "verkalkte Region", "duenne Fibrokappe", "irregulaere Oberflaeche", "intraplaque Blutung"
- Das Modell lernt einen "Konzeptvektor" fuer jedes annotierte Konzept und quantifiziert dessen Einfluss auf die Klassifikation

> Quelle: [Transparency of Medical AI, PMC 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13102313/)

**Fuer Carotis-AI:**
- **P3/P4:** Implementiere **TCAV-lite** -- nicht als Echtzeit-Erklaerung (zu rechenintensiv), sondern als **Qualitaetssicherung waehrend Modell-Training**.
- Wir koennen pruefen, ob das Modell tatsaechlich die erwarteten medizinischen Konzepte gelernt hat, bevor es deployed wird.
- Das ergaenzt Grad-CAM (pixel-level) und SHAP (feature-level) um **semantic-level explanations**.

### 2.3 FastSHAP: Echtzeit-SHAP

**FastSHAP** erreicht **100x Speedup** gegenueber KernelSHAP nach einmaligem Training eines Explanation-Models. Fuer unsere tabellarischen Features (Stenose-%, Plaque-Features) koennte dies Echtzeit-SHAP-Werte ermoeglichen, ohne die Inferenz zu verzoegern.

> Quelle: [Sensors 2026](https://www.mdpi.com/1424-8220/26/7/2131)

---

## 3. Tacit Knowledge Capture & Clinical Decision Support

### 3.1 CDSiC Override Taxonomie

Die AHRQ (Agency for Healthcare Research and Quality) hat 2024 eine **standardisierte Taxonomie fuer Override-Reasons** in Clinical Decision Support entwickelt. Diese wird jetzt durch HL7 CDS Hooks standardisiert.

**Relevanz fuer Carotis-AI:**
- Unsere Decision-Tree-Harvesting-Struktur erfasst bisher: `verdict`, `stenosis_pct`, `confidence`, `deciding_feature`, `trust`, `free_text_notes`
- **Erweiterungsmoeglichkeit:** Wenn der Arzt die AI-Empfehlung ablehnt (override), koennen wir nach einem **standardisierten Grund** fragen (basierend auf der CDSiC-Taxonomie):
  - "Patient-spezifische Umstaende" (z.B. Komorbiditaeten)
  - "Widerspruch zu klinischem Urteil"
  - "Unzureichende Evidenz"
  - "Alert-Fatigue / irrelevant"
  - "Anderer Grund (Freitext)"

> Quelle: [CDSiC Annual Meeting 2025](https://www.ncbi.nlm.nih.gov/books/NBK618402/), [Override Taxonomy PDF](https://cdsic.ahrq.gov/sites/default/files/2024-07/SRF_Taxonomy%20of%20PC%20CDS%20Override%20Recommendations_508_0.pdf)

### 3.2 AI-Native CDS: Die dritte Welle

Eine 2026 Analyse beschreibt drei Wellen von CDS:
1. **Regelbasiert** (MYCIN, EHR-alerts) -- hohe Override-Raten
2. **Referenz-basiert** (UpToDate, DynaMed) -- erfordert aktive Suche
3. **Reasoning-basiert** (AI-native) -- versteht klinischen Kontext

Carotis-AI ist bereits in der 3. Welle angekommen: Wir segmentieren, quantifizieren und erklaeren -- aber wir **lernen vom Arzt zurueck**.

> Quelle: [Glass Health 2026](https://glass.health/resources/best-clinical-decision-support)

**Empfehlung:**
- **P1/P2:** Erweitere `DecisionTreeCreate` um ein **Override-Feld**: Wenn der Arzt die AI-Einschaetzung ablehnt, erfassen wir:
  - `ai_verdict` (was die AI sagte)
  - `physician_verdict` (was der Arzt entschied)
  - `override_reason` (Taxonomie-kodiert)
  - `override_free_text` (optional, PII-gefiltert)
- Diese Daten sind **Gold fuer Continual Learning** -- sie zeigen, wo das Modell systematisch falsch liegt.

---

## 4. Privacy-Preserving Machine Learning

### 4.1 Federated Learning fuer Medical Imaging

Eine 2025 RSNA-Review analysiert den Stand von FL in der Radiologie:

**Frameworks (produktionsreif):**
- **NVIDIA FLARE** -- enterprise-grade, medizinische Validierung
- **Flower (flwr)** -- Python-native, flexibel, gut dokumentiert
- **PySyft** -- OpenMined, stark auf Privacy fokussiert
- **TensorFlow Federated** -- Google, aber TF-spezifisch

**Wichtige Erkenntnis:** FL ist **nicht automatisch privat**. Model-Updates koennen durch **Model-Inversion-Attacken** und **Gradient-Leakage** teilweise rekonstruiert werden. Abwehr:
- Differential Privacy (DP) -- Noise in Gradienten
- Secure Aggregation (SMPC) -- verschlüsselte Update-Aggregation
- Homomorphe Verschluesselung -- rechenintensiv

> Quellen: [RSNA 2025](https://pubs.rsna.org/doi/10.1148/ryai.240637), [PMC FL Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10546441/)

**Empfehlung fuer Carotis-AI:**
- **P5/P6:** Plane **Federated Learning** als Multi-Site-Feature ein. Das Klinikum Dortmund koennte mit anderen Haendlern kooperieren, ohne Patientendaten zu teilen.
- **P0-Blocker:** Noch nicht relevant, da kein Multi-Site-Training vor Rohde-Approval.

### 4.2 ONNX Model Integrity & Edge Security

Eine 2026 Arbeit demonstriert **ONNX Runtime in Intel SGX Enclaves** -- das Modell wird verschluesselt gespeichert, nur im Enclave entschluesselt, mit SHA-256-Integritaetspruefung vor dem Load.

**Relevant fuer uns:**
- Wir pruefen bereits ONNX-Modelle via SHA-256 (optional in Config)
- **Erweiterung:** SigStore/Cosign fuer Modell-Signing (statt nur SHA-256)
- **Erweiterung:** Modell-Verschlusselung im Ruhezustand (AES-GCM)

> Quellen: [ONNX Signing Issue](https://github.com/onnx/onnx/issues/4046), [MDPI TEEs 2026](https://www.mdpi.com/2624-800X/6/1/23), [WJARR 2025](https://wjarr.com/sites/default/files/fulltext_pdf/WJARR-2025-1832.pdf)

---

## 5. NLP fuer Medizinische Freitexte

### 5.1 BERTopic: Weiterhin valide

Eine 2025 systematische Review in PMC bestaetigt: BERTopic bleibt das fuehrende **unsupervised** Topic-Modeling fuer Clinical Text. KeyBERTInspired und MaximalMarginalRelevance liefern die besten automatischen Labels.

> Quelle: [PMC Systematic Review 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840768/)

### 5.2 BioGottBERT: Deutsches Klinisches NER

Eine 2025 Studie (Diaz Ochoa et al., Frontiers in Digital Health) vergleicht **BioGottBERT** mit zero-shot LLMs (GLiNER, Mistral) fuer deutsche Klinik-Freitexte:

| Modell | Symptom NER F1 | Negation Detection | Lokal deploybar? |
|--------|---------------|-------------------|------------------|
| BioGottBERT (fine-tuned) | **0.84** | **Sehr gut** | **Ja** |
| GLiNER (zero-shot) | ~0.65 | Schlecht | Ja |
| Mistral (zero-shot) | ~0.50 | Sehr schlecht | Ja |

**Kritische Erkenntnis:** Fine-tuned BERT-Modelle schlagen zero-shot LLMs bei spezifischen NER-Aufgaben -- **auch wenn die LLMs lokal laufen**. German clinical NLP ist ein "low-resource"-Gebiet.

> Quelle: [Frontiers Digital Health 2025](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1623922/full)

**Empfehlung fuer Carotis-AI:**
- **P1/P2:** Ersetze Spacy `de_core_news_lg` durch **BioGottBERT** oder zumindest **GottBERT** fuer die PII-Detection und Keyword-Extraktion.
  - `de_core_news_lg` ist ein allgemeines deutsches Modell
  - BioGottBERT ist auf **biomedizinischen Text** trainiert und erkennt medizinische Entitaeten besser
  - Auch fuer die Nightly-Aggregation: Medizinische Keywords werden praeziser extrahiert
- Alternative: **scai-bio/BioGottBERT** auf HuggingFace (open source)

### 5.3 Clinical Concept Extraction

Tools wie **cTAKES** und **MedSpacy** (fuer Englisch) bzw. **BioGottBERT** (fuer Deutsch) koennen aus freien Arzttexten strukturierte Entitaeten extrahieren: Diagnosen, Symptome, Anatomie, Negationen.

Fuer unsere `free_text_notes` koennte dies bedeuten:
- Extraktion von: `plaque_type`, `stenosis_description`, `symptom_mentions`
- Automatische **Negationserkennung**: "keine signifikante Stenose" vs. "signifikante Stenose"
- Diese extrahierten Entitaeten koennen als **zusaetzliche Features** fuer das ML-Modell dienen

---

## 6. EU AI Act & MDR: Regulatory Landscape

### 6.1 Kritische Timeline-Korrektur

Die wichtigste Erkenntnis fuer uns: **Medizinprodukte haben bis 2. August 2027!**

| Datum | Was gilt? | Relevanz fuer Carotis-AI |
|-------|-----------|-------------------------|
| 2 Aug 2026 | High-Risk AI (Annex III, ohne NB) | Nicht direkt relevant |
| **2 Aug 2027** | **Art. 6(1): CE-markierte MDR/IVDR-Geraete** | **Unsere Deadline!** |
| 2 Aug 2028 | Erste AI-Act-Review | Feedback-Gelegenheit |

> Quelle: [MDxCRO 2026](https://mdxcro.com/eu-ai-act-medical-devices-samd/)

### 6.2 Anforderungen, die unser System bereits erfuellt

| AI-Act-Anforderung | Carotis-AI Implementierung | Status |
|-------------------|---------------------------|--------|
| Art. 11: Technische Dokumentation | ADRs, Risk-Register, Schemas | GUT |
| Art. 12: Automatisches Logging | AuditEvent-Tabelle (append-only) | **SEHR GUT** |
| Art. 14: Human Oversight | Decision-Tree-Harvesting + Override | **SEHR GUT** |
| Art. 10: Daten-Governance | DICOM-Anonymisierung (PS 3.15) | GUT |
| Art. 9: Risikomanagement | Risk-Register + ISO 14971 Alignment | IN ARBEIT |
| Post-Market Monitoring | Nightly Aggregator + Anomalien-Reports | GUT |

**Wichtig:** "Continuous learning of even a high-risk model does not constitute a significant change" -- unser Daily-Learning-Loop erfordert **keine Re-Zertifizierung** bei jedem Update.

### 6.3 Noetige Ergaenzungen

- **FRIA (Fundamental Rights Impact Assessment)** -- wird fuer Public-Sector-Deployer gefordert; fuer uns (Klinikum) moeglicherweise relevant
- **Transparency/Labeling** -- Klarstellung, dass die Diagnose "AI-unterstuetzt" ist
- **Bias Assessment** -- Nachweis, dass das Modell ueber verschiedene Patientengruppen hinweg fair ist

---

## Zusammenfassung: Empfohlene Verbesserungen nach Phase

### Sofort umsetzbar (P0 / vor Rohde-Meeting)

| # | Verbesserung | Aufwand | Impact |
|---|-------------|---------|--------|
| 1 | **BioGottBERT statt Spacy** fuer PII-Detection + Keyword-Extraction | M | HOCH |
| 2 | **Override-Capture** in Decision Tree Schema (CDSiC-Taxonomie) | S | HOCH |
| 3 | **TCAV-Research** -- Paper lesen, Konzept fuer Plaque-Vulnerability skizzieren | S | MITTEL |

### P1-P2 (nach Rohde-Approval)

| # | Verbesserung | Aufwand | Impact |
|---|-------------|---------|--------|
| 4 | **Clinical Concept Extraction** aus free_text_notes via BioGottBERT | M | HOCH |
| 5 | **FastSHAP** fuer Echtzeit-SHAP anstelle KernelSHAP | M | MITTEL |
| 6 | **EU AI Act FRIA-Dokument** erstellen | M | HOCH |

### P3-P4 (Entwicklungsphase)

| # | Verbesserung | Aufwand | Impact |
|---|-------------|---------|--------|
| 7 | **U-Mamba** als MFSD-UNet-Nachfolger evaluieren | L | HOCH |
| 8 | **Radiomics-Branch** neben CNN-Branch fuer Plaque-Vulnerability | L | SEHR HOCH |
| 9 | **TCAV-lite** fuer Modell-Validierung implementieren | L | MITTEL |

### P5-P6 (Multi-Site / Skalierung)

| # | Verbesserung | Aufwand | Impact |
|---|-------------|---------|--------|
| 10 | **Federated Learning** mit NVIDIA FLARE / Flower planen | L | HOCH |
| 11 | **ONNX SigStore-Signing** fuer Modell-Integrity | S | MITTEL |
| 12 | **TEE-basierte Inferenz** (Intel SGX) evaluieren | L | MITTEL |

---

## Quellen

1. [Xie et al., Carotid CTA Segmentation with MFSD-UNet, QIMS 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11994491/)
2. [Saba et al., AI in Vulnerable Carotid Plaque Assessment, Medicina 2025](https://www.mdpi.com/1648-9144/61/12/2082)
3. [VMAXL-UNet: Vision Mamba + xLSTM, Nature Sci Rep 2025](https://www.nature.com/articles/s41598-025-88967-5)
4. [H-VMUNet: High-order Vision Mamba, Neurocomputing 2025](https://www.sciencedirect.com/science/article/abs/pii/S0925231225001195)
5. [Mamba Survey for Medical Imaging, arXiv 2026](https://arxiv.org/html/2408.01129v8)
6. [XAI in Medical Imaging Comprehensive Review, Springer 2025](https://link.springer.com/article/10.1007/s10586-025-05281-5)
7. [XAI for Medical Imaging Systems, PMC 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13102313/)
8. [TAXAI Framework, Nature Sci Rep 2026](https://www.nature.com/articles/s41598-026-44167-3)
9. [XAI Methods Comparative Analysis, Sensors 2026](https://www.mdpi.com/1424-8220/26/7/2131)
10. [CDSiC Annual Meeting 2025, NCBI](https://www.ncbi.nlm.nih.gov/books/NBK618402/)
11. [CDSiC Override Taxonomy, AHRQ 2024](https://cdsic.ahrq.gov/sites/default/files/2024-07/SRF_Taxonomy%20of%20PC%20CDS%20Override%20Recommendations_508_0.pdf)
12. [AI-Native CDS Analysis, Glass Health 2026](https://glass.health/resources/best-clinical-decision-support)
13. [Privacy-Preserving FL in Medical Imaging, RSNA 2025](https://pubs.rsna.org/doi/10.1148/ryai.240637)
14. [FL in Medical Imaging: State of Practice, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10546441/)
15. [ONNX in Intel SGX Enclaves, MDPI 2026](https://www.mdpi.com/2624-800X/6/1/23)
16. [ONNX Model Signing Feature Request, GitHub](https://github.com/onnx/onnx/issues/4046)
17. [Secure ML Deployment, WJARR 2025](https://wjarr.com/sites/default/files/fulltext_pdf/WJARR-2025-1832.pdf)
18. [BERTopic Systematic Review for EHRs, PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12840768/)
19. [BioGottBERT vs Zero-Shot LLMs, Frontiers 2025](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1623922/full)
20. [BioGottBERT German Clinical NER, PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12689901/)
21. [EU AI Act Medical Devices, MDxCRO 2026](https://mdxcro.com/eu-ai-act-medical-devices-samd/)
22. [EU AI Act Timeline, Kennedys Law 2026](https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-eu-ai-act-implementation-timeline/)
23. [EU AI Act 2025-2026 Outlook, AI Act Blog](https://www.aiactblog.nl/en/posts/eu-ai-act-2025-review-2026-outlook)
24. [Federated Learning Market 2025, Dialzara](https://dialzara.com/blog/federated-learning-vs-edge-ai-preserving-privacy)
25. [Edge AI Deployment Best Practices, Promwad 2025](https://promwad.com/news/edge-ai-model-deployment)
26. [Carotid Plaque Detection CTA, PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11769795/)
27. [Deep Learning Radiomics Carotid Meta-Analysis, PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12826653/)
28. [Weak-Mamba-UNet, IEEE T-BME 2026](https://pubmed.ncbi.nlm.nih.gov/41770954/)
29. [VM-UNet for Medical Segmentation, MDPI 2025](https://www.mdpi.com/2076-3417/15/14/7821)
30. [U-Mamba for Biomedical Segmentation, arXiv 2024](https://arxiv.org/abs/2401.04722)
31. [Task-Specific Transformers in Healthcare, JMIR 2024](https://medinform.jmir.org/2024/1/e49724/)
32. [LLMs for Healthcare Text Classification, PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC12936667/)
33. [Patient-Reported Care BERTopic Study, JMIR 2025](https://medinform.jmir.org/2025/1/e63466)
34. [Federated Learning Brain Tumor, Nature Sci Rep 2025](https://www.nature.com/articles/s41598-025-07807-8)
35. [OpenMined Privacy-Preserving AI](https://openmined.org/blog/federated-learning-differential-privacy-and-encrypted-computation-for-medical-imaging/)
