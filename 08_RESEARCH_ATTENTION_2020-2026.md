# 08_RESEARCH — Attention-Mechanism in Medical Imaging (2020–2026)

> Inventar der relevanten Literatur für die Promotion. Wird zur Methodik-Sektion und zum Stand-der-Forschung-Kapitel. Stand 2026-04-27.

---

## 1. Foundational Papers (Pre-2020, Pflicht-Zitate)

| # | Autor / Jahr | Titel | Warum relevant |
|---|--------------|-------|----------------|
| F1 | Vaswani et al. 2017 | *Attention Is All You Need* | Definition Self-Attention; Grundlage aller Transformer-basierten Architekturen |
| F2 | Ronneberger et al. 2015 | *U-Net: Convolutional Networks for Biomedical Image Segmentation* | Goldstandard für medizinische Bild-Segmentierung; Backbone unseres MFSD-UNet |
| F3 | Selvaraju et al. 2017 | *Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization* | XAI-Komponente unseres Systems |
| F4 | Lundberg & Lee 2017 | *A Unified Approach to Interpreting Model Predictions* (SHAP) | Erklärbarkeit für die Vulnerability-Klassifikation |

---

## 2. Vision Transformer in Medical Imaging (2020–2024)

| # | Autor / Jahr | Titel | Beitrag | Quelle |
|---|--------------|-------|---------|--------|
| T1 | Liu et al. 2021 | *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows* | Backbone für Multi-Scale-Imaging — Basis für Swin-UNet | ICCV 2021 |
| T2 | Cao et al. 2022 | *Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation* | Erste reine Transformer-U-Net-Hybride für Med. Imaging | ECCV Workshops 2022 |
| T3 | Hatamizadeh et al. 2022 | *Swin UNETR: Swin Transformers for Semantic Segmentation of Brain Tumors in MRI Images* | Brain-Tumor-Anwendung — Methodik übertragbar | BrainLes / MICCAI |
| T4 | He et al. 2023 | *Transforming medical imaging with Transformers? A comparative review* | Comprehensive Review für Stand-der-Forschung-Kapitel | [PMC10010286](https://pmc.ncbi.nlm.nih.gov/articles/PMC10010286/) |
| T5 | Shamshad et al. 2023 | *Transformers in medical imaging: A survey* | Encyclopedic Review aller ViT-Anwendungen in Medizin | Medical Image Analysis 2023 |

---

## 3. Carotid-Specific (2022–2026) — Direkt relevant für die Promotion

| # | Autor / Jahr | Titel | Beitrag | Quelle |
|---|--------------|-------|---------|--------|
| C1 | Xie et al. 2024 | *Carotid artery segmentation in CTA using multi-scale deep supervision with Swin-UNet and advanced data augmentation* | **Direkter Benchmark — Dice 0.91, Sensitivity 0.99 auf CTA-Daten. Unser Pixel-Modell-Reference.** | [QIMS](https://qims.amegroups.org/article/view/135680/html) |
| C2 | Le et al. 2024 | *Machine Learning Detects Symptomatic Plaques in Patients With Carotid Atherosclerosis on CT Angiography* | Symptomatic-Plaque-Detection mit ML, AUC 0.90+ — Methodik-Referenz für unsere Plaque-Vulnerability-Klassifikation | [PMC11186714](https://pmc.ncbi.nlm.nih.gov/articles/PMC11186714/) / [Circ Imaging](https://www.ahajournals.org/doi/10.1161/CIRCIMAGING.123.016274) |
| C3 | Frontiers Neurology 2024 | *A deep learning model for carotid plaques detection based on CTA images: a two stepwise early-stage clinical validation study* | Klinische Validierungs-Methodik — Vorbild für unser P5-Studiendesign | [Frontiers](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2024.1480792/full) |
| C4 | Springer Neuroradiology 2026 | *Plaque-level machine-learning prediction of carotid plaque vulnerability on CTA* | Sehr aktuelle Vulnerability-Prädiktion — Direkt-Vergleich für unsere Resultate | [Springer](https://link.springer.com/article/10.1007/s00234-026-03984-z) |
| C5 | Frontiers Cardiovascular Med 2024 | *Diagnostic value of artificial intelligence-assisted CTA for the assessment of atherosclerosis plaque: a systematic review and meta-analysis* | Pooled AUC 0.96, Sens. 0.90, Spec. 0.93 — Benchmark-Erwartung für unsere Performance | [Frontiers](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2024.1398963/full) |
| C6 | Frontiers Neurology 2025 | *An Explainable CT-Based Machine Learning Model Integrating Carotid Plaque and Perivascular Adipose Tissue for Predicting Symptomatic Plaques* | XAI + Plaque + PVAT — direkter Methodik-Vergleich | [Frontiers](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1679861/abstract) |
| C7 | PubMed 2025 | *Artificial intelligence in carotid CTA plaque detection: Decade of progress and future perspectives* | Decade-Review — perfekte Stand-der-Forschung-Quelle | [PubMed 41025057](https://pubmed.ncbi.nlm.nih.gov/41025057/) |
| C8 | OAE Vulnerable Plaque 2024 | *Applications of artificial intelligence-based models in vulnerable carotid plaque* | Modell-Übersicht für Vulnerability-Detection | [OAE](https://www.oaepublish.com/articles/2574-1209.2023.78) |

---

## 4. Attention Mechanism Reviews (für Methodik-Kapitel)

| # | Autor / Jahr | Titel | Quelle |
|---|--------------|-------|--------|
| A1 | ScienceDirect 2024 | *Advances in attention mechanisms for medical image segmentation* | [SD](https://www.sciencedirect.com/science/article/pii/S1574013724001047) |
| A2 | ScienceDirect 2023 | *Advances in medical image analysis with vision Transformers: A comprehensive review* | [SD](https://www.sciencedirect.com/science/article/abs/pii/S1361841523002608) |
| A3 | arXiv 2023 | *A Recent Survey of Vision Transformers for Medical Image Segmentation* | [arXiv 2312.00634](https://arxiv.org/pdf/2312.00634) |
| A4 | medRxiv 2024 | *Systematic Review of Hybrid Vision Transformer Architectures* | [medRxiv](https://www.medrxiv.org/content/10.1101/2024.06.21.24309265v1.full.pdf) |
| A5 | PMC 2024 | *From CNN to Transformer: A Review of Medical Image Segmentation Models* | [PMC11300773](https://pmc.ncbi.nlm.nih.gov/articles/PMC11300773/) |

---

## 5. Hybrid Architectures + Multi-Scale (für unsere MFSD-UNet-Wahl)

| # | Autor / Jahr | Titel | Beitrag | Quelle |
|---|--------------|-------|---------|--------|
| H1 | Nature SciRep 2024 | *Enhancing medical image segmentation with a multi-transformer U-Net* | Multi-Transformer + UNet Hybride | [PMC10909362](https://pmc.ncbi.nlm.nih.gov/articles/PMC10909362/) |
| H2 | Nature SciRep 2025 | *Medical image segmentation by combining feature enhancement Swin Transformer and UperNet* | FE-SwinUper-Architektur | [Nature](https://www.nature.com/articles/s41598-025-97779-6) |
| H3 | Nature SciRep 2025 | *A multi-scale attention-based Swin transformer model for medical images segmentation* | Multi-Scale-Attention für Med. Imaging | [Nature](https://www.nature.com/articles/s41598-025-22649-0) |
| H4 | Nature SciRep 2025 | *Multi-scheme cross-level attention embedded U-shape transformer for MRI semantic segmentation* | Cross-Level-Attention für MRT — übertragbar auf CTA | [Nature](https://www.nature.com/articles/s41598-025-06966-y) |

---

## 6. Speziell Carotis + Ultraschall (für Sarah-Hospital-Daten)

| # | Autor / Jahr | Titel | Quelle |
|---|--------------|-------|--------|
| U1 | ScienceDirect 2022 | *Method for Carotid Artery 3-D Ultrasound Image Segmentation Based on CSWin Transformer* | [SD](https://www.sciencedirect.com/science/article/abs/pii/S0301562922006342) |
| U2 | SGS Engineering 2024 | *An Evolution of Automated Segmentation Techniques of Carotid Artery Structures in Ultrasound Imaging* | [SGS](https://spast.org/techrep/article/view/5775) |
| U3 | ScienceDirect 2026 | *Attention/Transformer-based AI models for carotid segmentation and intima media Thickness/Plaque area measurements in Japanese ultrasound scans* | Multi-Ethnizitäts-Aspekt | [SD](https://www.sciencedirect.com/science/article/abs/pii/S0263224126000205) |
| U4 | PMC 2025 | *Transformer and Attention-Based Architectures for Segmentation of Coronary Arterial Walls in IVUS: A Narrative Review* | Methodik-übertragbar Coronary→Carotid | [PMC11988294](https://pmc.ncbi.nlm.nih.gov/articles/PMC11988294/) |

---

## 7. Explainability + Reasoning Capture (für unser Decision-Tree-Harvesting)

| # | Autor / Jahr | Titel | Beitrag | Quelle |
|---|--------------|-------|---------|--------|
| E1 | Komorowski et al. CVPR 2023 | *Towards Evaluating Explanations of Vision Transformers for Medical Imaging* | XAI-Evaluation-Framework | [CVPR](https://openaccess.thecvf.com/content/CVPR2023W/XAI4CV/papers/Komorowski_Towards_Evaluating_Explanations_of_Vision_Transformers_for_Medical_Imaging_CVPRW_2023_paper.pdf) |
| E2 | Bock et al. 2024 (PMC) | *Explainable machine-learning model to classify culprit calcified carotid plaque in embolic stroke of undetermined source* | Explainable ML in Carotis — Methodik-Vergleich | [PMC11581071](https://pmc.ncbi.nlm.nih.gov/articles/PMC11581071/) |
| E3 | PMC 2024 | *A multimodal vision transformer for interpretable fusion of functional and structural neuroimaging data* | Multimodal + Interpretable | [PMC11599617](https://pmc.ncbi.nlm.nih.gov/articles/PMC11599617/) |

---

## 8. KAN / Newer Attention Variants (für späte Phasen)

| # | Autor / Jahr | Titel | Quelle |
|---|--------------|-------|--------|
| N1 | arXiv 2025 | *Medical Image Classification with KAN-Integrated Transformers* | [arXiv 2502.13693](https://arxiv.org/pdf/2502.13693) |
| N2 | Nature SciRep 2025 | *Hierarchical multi-scale vision transformer model for accurate detection and classification of brain tumors in MRI* | [Nature](https://www.nature.com/articles/s41598-025-23100-0) |

---

## 9. Lücken in der bisherigen Literatur (= unser Beitrag)

Die folgenden Punkte sind **unser Differenzierungs-Argument** im Methodik-Paper:

1. **Kein Paper kombiniert Local-First-Architektur mit Carotis-Vulnerability-Klassifikation** — alle vorhandenen Lösungen sind cloud-basiert.
2. **Kein Paper trainiert systematisch auf den Begründungs-Strukturen der Befunder** — das ist die Lücke, die Decision-Tree-Harvesting füllt.
3. **Keine transnationale Validierung DE/JO existiert** — Multi-Ethnizität kommt vor (U3 für Japan), aber kein DACH↔MENA-Vergleich.
4. **Keine systematische EU-AI-Act-konforme Implementation publiziert** — das wird ab 2026 zur regulatorischen Pflicht und ist daher publizier-attraktiv.
5. **Keine Daily-Learning-Loop-Implementierung mit Auto-Rollback** — alle Federated-Learning-Ansätze in der Carotis-Literatur sind episodisch (monatliches Re-Training), nicht kontinuierlich.

---

## 10. Wie diese Liste pflegen

- **Bei jedem neuen Paper-Fund** in P1–P5: Eintrag hier ergänzen + 1-Zeile in `memory/domain/refs_papers.md`.
- **Quartalsweise Sweep:** Opus 4.7 mit Template 7-Variante: *„Suche neue Papers seit <Datum> zu Carotis + AI + Local-First. Update 08_RESEARCH."*
- **Vor Submission:** Sonnet 4.6 generiert daraus die BibTeX-Datei für Zotero.

---

## Sources

- [Carotid artery segmentation in CTA using multi-scale deep supervision with Swin-UNet (Xie 2024 QIMS)](https://qims.amegroups.org/article/view/135680/html)
- [Machine Learning Detects Symptomatic Plaques in Patients With Carotid Atherosclerosis on CTA (Le 2024 Circulation Imaging)](https://www.ahajournals.org/doi/10.1161/CIRCIMAGING.123.016274)
- [A deep learning model for carotid plaques detection based on CTA images (Frontiers Neurology 2024)](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2024.1480792/full)
- [Plaque-level machine-learning prediction of carotid plaque vulnerability on CTA (Springer Neuroradiology 2026)](https://link.springer.com/article/10.1007/s00234-026-03984-z)
- [Diagnostic value of AI-assisted CTA for atherosclerosis plaque: systematic review and meta-analysis (Frontiers CV Med 2024)](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2024.1398963/full)
- [Explainable CT-Based ML Integrating Carotid Plaque and PVAT (Frontiers Neurology 2025)](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1679861/abstract)
- [AI in carotid CTA plaque detection: Decade of progress (PubMed 2025)](https://pubmed.ncbi.nlm.nih.gov/41025057/)
- [Applications of AI-based models in vulnerable carotid plaque (OAE 2024)](https://www.oaepublish.com/articles/2574-1209.2023.78)
- [Advances in attention mechanisms for medical image segmentation (ScienceDirect 2024)](https://www.sciencedirect.com/science/article/pii/S1574013724001047)
- [Advances in medical image analysis with vision Transformers (ScienceDirect 2023)](https://www.sciencedirect.com/science/article/abs/pii/S1361841523002608)
- [A Recent Survey of Vision Transformers for Medical Image Segmentation (arXiv 2312.00634)](https://arxiv.org/pdf/2312.00634)
- [Transforming medical imaging with Transformers (PMC 2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10010286/)
- [From CNN to Transformer: A Review of Medical Image Segmentation Models (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11300773/)
- [Multi-transformer U-Net for medical image segmentation (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10909362/)
- [Feature Enhancement Swin Transformer + UperNet (Nature SciRep 2025)](https://www.nature.com/articles/s41598-025-97779-6)
- [Multi-scale attention-based Swin transformer (Nature SciRep 2025)](https://www.nature.com/articles/s41598-025-22649-0)
- [Multi-scheme cross-level attention U-shape transformer (Nature SciRep 2025)](https://www.nature.com/articles/s41598-025-06966-y)
- [3-D Carotid Ultrasound Segmentation with CSWin Transformer (ScienceDirect 2022)](https://www.sciencedirect.com/science/article/abs/pii/S0301562922006342)
- [Evolution of Carotid Segmentation in Ultrasound (SGS Engineering 2024)](https://spast.org/techrep/article/view/5775)
- [Attention/Transformer AI for Japanese Carotid Ultrasound (ScienceDirect 2026)](https://www.sciencedirect.com/science/article/abs/pii/S0263224126000205)
- [Transformer + Attention for Coronary IVUS Segmentation Review (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11988294/)
- [Evaluating Explanations of ViTs for Medical Imaging (CVPR 2023 XAI4CV)](https://openaccess.thecvf.com/content/CVPR2023W/XAI4CV/papers/Komorowski_Towards_Evaluating_Explanations_of_Vision_Transformers_for_Medical_Imaging_CVPRW_2023_paper.pdf)
- [Explainable ML for culprit calcified carotid plaque (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11581071/)
- [Multimodal ViT for Interpretable Neuroimaging Fusion (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11599617/)
- [KAN-Integrated Transformers for Medical Image Classification (arXiv 2502.13693)](https://arxiv.org/pdf/2502.13693)
- [Hierarchical Multi-Scale ViT for Brain Tumor Detection (Nature SciRep 2025)](https://www.nature.com/articles/s41598-025-23100-0)
- [Systematic Review of Hybrid ViT Architectures (medRxiv 2024)](https://www.medrxiv.org/content/10.1101/2024.06.21.24309265v1.full.pdf)
