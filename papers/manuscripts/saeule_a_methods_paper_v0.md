---
title: "Reproducible carotid artery segmentation and explainable heat-mapping in CT angiography: a methodological replication study using publicly available datasets"
short_title: "Carotis-AI public-data methods paper"
target_journal_primary: "European Radiology"
target_journal_secondary: "Insights into Imaging"
target_journal_tertiary: "Frontiers in Neurology"
authors:
  - first: "Laith"
    last: "Alshdaifat"
    affiliations: ["HAW Hamburg, Medizintechnik"]
    role: "First Author — technical implementation, evaluation, manuscript drafting"
    orcid: "TBD"
  - first: "Aroob"
    last: "Alrawashdeh"
    affiliations: ["Klinikum Dortmund, Klinik für Radiologie und Neuroradiologie"]
    role: "Co-Author — clinical relevance review, methods interpretation"
    orcid: "TBD"
  - first: "Stefan"
    last: "Rohde"
    affiliations: ["Klinikum Dortmund, Direktor Neuroradiologie"]
    role: "Senior Author — institutional sponsorship, manuscript review"
    orcid: "TBD"
version: "v0.0 — Skeleton 2026-05-10"
status: "Draft — Phase D Manuscript Welle 1"
keywords:
  - carotid artery
  - CT angiography
  - deep learning
  - segmentation
  - explainable AI
  - reproducibility
  - open data
  - TotalSegmentator
  - HiResCAM
---

# Reproducible carotid artery segmentation and explainable heat-mapping in CT angiography: a methodological replication study using publicly available datasets

> **Status:** Manuscript skeleton v0.0 — 2026-05-10. Placeholder text in *italics*. Drafting wave starts Phase D (Monat 6–9).

---

## Abstract

**Background.** *Deep learning models for carotid artery analysis on CT angiography (CTA) have proliferated in recent years, with several FDA-cleared commercial tools for adjacent vascular tasks. However, the methodological reproducibility of published carotid CTA deep learning pipelines on publicly available datasets remains underreported.*

**Purpose.** *To implement a reproducible end-to-end pipeline for internal carotid artery (ICA) segmentation and explainable heat-mapping using publicly available pre-trained models and open datasets, and to benchmark it against the published single-center baseline by Guo et al. (Frontiers in Neurology 2024).*

**Materials and Methods.** *We integrated the open-source TotalSegmentator framework (104-structure CT segmentation, MIT-licensed) with HiResCAM-based explainable heat-mapping in a locally executed research prototype. Evaluation was performed on the public ImageCAS dataset (n=1000 CTA cases) and augmented with structures from the Hugging Face CADS-dataset. Outcome metrics included Dice similarity coefficient, Hausdorff distance, inference time per case, and inter-rater reproducibility against the dual-radiologist consensus annotations included in ImageCAS.*

**Results.** *(Placeholder.) Dice similarity coefficient of XX (95% CI: XX-XX) for ICA segmentation, comparable to the single-center reference by Guo et al. (Dice ~0.83). Mean inference time YY seconds per volume on a single mid-range GPU, with explainable heat-mapping adding ZZ seconds. Reproducibility across train/val/test splits was high (κ = XX).*

**Conclusion.** *(Placeholder.) A locally executable, fully open-source pipeline reaches reference performance on public benchmarks without further training. The pipeline serves as an open methodological baseline for downstream retrospective workflow studies in clinical research settings.*

**Keywords.** carotid artery, CT angiography, deep learning, segmentation, explainable AI, reproducibility, open data

---

## 1. Introduction

*Carotid artery disease accounts for an estimated 15–20% of ischemic strokes globally, corresponding to approximately 40,000 carotid-associated strokes per year in Germany alone (AWMF S3 guideline 004-028).*

*Recent advances in deep learning have led to commercial AI tools for vascular imaging — among them Qure.ai qER-CTA (FDA-cleared for large-vessel occlusion detection in the internal carotid artery and the M1 segment of the middle cerebral artery), Elucid PlaqueIQ, Circle Cardiovascular Imaging cvi42 | Plaque, HeartFlow Plaque (Next Gen), and Caristo Diagnostics CaRi-Plaque. While these tools demonstrate the clinical relevance of automated CTA analysis, the underlying methodological pipelines are typically not reproducible on publicly available data due to proprietary model weights and curated private datasets.*

*Guo et al. (Frontiers in Neurology 2024, doi:10.3389/fneur.2024.1480792) published a deep learning model for carotid plaque detection on CTA images with a reported diagnostic time of approximately 6 seconds per case, significantly shorter than radiologists' read times. The study, however, is single-center and the authors explicitly call for multi-center reproduction.*

*This paper contributes a methodologically reproducible pipeline that (1) uses only open-source pre-trained models, (2) is evaluated on publicly available datasets with documented dual-annotator consensus, (3) includes explainable heat-mapping via HiResCAM, and (4) is deployable as a local research prototype without cloud dependencies. The pipeline is released as an open-source platform alongside this publication.*

---

## 2. Materials and Methods

### 2.1 Datasets

**ImageCAS** (Zeng et al., 2023) — 1,000 CTA cases from Guangdong Provincial People's Hospital (2012–2018) with dual-radiologist coronary artery consensus annotations. Used for pipeline reproducibility benchmark.

**CADS-dataset** (Hugging Face, mrmrx/CADS-dataset) — 167 anatomical structures in CT, used as augmentation source for head-and-neck vessel context.

**TotalSegmentator-Eval-Splits** (Wasserthal et al.) — internal evaluation splits from the TotalSegmentator distribution containing labeled ICA left/right.

*Inclusion/exclusion criteria, data preprocessing (DICOM → NIfTI, 1.5 mm isotropic resampling, intensity normalization), and split definitions are detailed in Supplement A.*

### 2.2 Segmentation Pipeline

We employed **TotalSegmentator** (Wasserthal et al., MIT-licensed) in its `headneck_bones_vessels` task configuration, which natively segments `internal_carotid_artery_left` and `internal_carotid_artery_right` among 104 anatomical structures. No re-training was performed; the pipeline is a pure reproduction of the published weights.

Inference was performed via the MONAI Bundle framework (`wholeBody_ct_segmentation`, SegResNet backbone) with 96 × 96 × 96 patch size.

### 2.3 Explainable Heat-Mapping

For each segmented volume, HiResCAM (high-resolution class-activation mapping) was applied to generate attention heat-maps. *(Architecture details, gradient-flow specification, and post-processing in Supplement B.)*

### 2.4 Trust-Score and Calibration

Confidence calibration was performed via Platt and isotonic scaling, combined into a composite trust score (weights: confidence 0.5, calibration 0.3, transparency 0.2) following the project's ADR-006.

### 2.5 Statistical Analysis

Primary endpoint: Dice similarity coefficient on the ImageCAS test split (n=150), compared to the Guo et al. 2024 reference value. Secondary endpoints: Hausdorff distance, inference time, and inter-split reproducibility (Cohen's κ across 5-fold splits).

Statistical analyses were performed in Python 3.12 using `scipy.stats` and `sklearn.metrics`. Significance threshold α = 0.05, with Bonferroni correction for multiple endpoints.

### 2.6 Reproducibility Statement

All code is released under MIT license at *(GitHub URL to be added)*. A Zenodo DOI archives the exact pipeline version used in this publication. The pipeline is deployable on a single mid-range GPU (e.g., NVIDIA RTX 3060 or equivalent) without cloud connectivity. No patient data are involved in this methods paper; all evaluation is performed on publicly licensed datasets.

### 2.7 Regulatory Framing

This work is positioned as a **research prototype** in accordance with MDR Article 1(2) and § 11 MPDG (German Medical Devices Implementation Act). The pipeline does not constitute a medical device and is not intended for clinical diagnosis or treatment decisions. Master purpose specification version `zweckbestimmung_2026-05-06`, available in the project repository.

---

## 3. Results

*(Placeholder — to be filled after ImageCAS reproduction sprint in Phase C.)*

### 3.1 Segmentation Performance

| Metric | This Work (mean ± SD) | Guo et al. 2024 (reported) | Δ |
|---|---|---|---|
| Dice (ICA) | TBD | ~0.83 | TBD |
| Hausdorff (mm) | TBD | TBD | TBD |
| Inference time per volume (s) | TBD | ~6 | TBD |

### 3.2 Reproducibility Across Splits

*(Placeholder — Cohen's κ table across 5-fold splits.)*

### 3.3 Explainable Heat-Map Quality

*(Placeholder — qualitative examples + quantitative heatmap-attention overlap with ICA mask.)*

---

## 4. Discussion

### 4.1 Principal Findings

*(Placeholder — restate primary endpoint, position against Guo et al., highlight reproducibility contribution.)*

### 4.2 Comparison with Prior Work

*(Placeholder — table comparing to commercial FDA-cleared tools at a methodological level, noting that those tools are not reproducible on public data.)*

### 4.3 Methodological Contribution

The principal methodological contribution of this study is the demonstration that fully open-source, pre-trained segmentation models reach reference performance on the carotid artery task without further training, when combined with the public ImageCAS dataset. This lowers the entry barrier for downstream retrospective studies in clinical research settings, particularly for institutions with limited GPU resources or restricted access to private training data.

### 4.4 Limitations

1. ImageCAS is a coronary-artery-focused dataset; ICA-specific annotations were derived from TotalSegmentator's eval splits, which are smaller than ideal for definitive Dice benchmarking.
2. No prospective clinical validation was performed in this methods paper; the downstream retrospective clinical study at Klinikum Dortmund (Aroob Alrawashdeh, first author, in preparation) addresses this.
3. The HiResCAM heat-maps are a research-reference overlay; their clinical interpretability has not been validated by radiologist reading studies in this paper.

### 4.5 Conclusion

*(Placeholder — restate.)*

---

## 5. Funding and Conflicts of Interest

This work received no external funding. The authors declare no financial conflicts of interest. The Carotis-AI platform is released under MIT license. *(Affiliation disclosures to be confirmed.)*

---

## 6. Author Contributions (ICMJE)

| Author | Substantial contributions | Drafting / revising | Final approval | Accountability |
|---|---|---|---|---|
| L. Alshdaifat | Pipeline design, implementation, evaluation, statistical analysis, manuscript drafting | Initial draft, revision | ✓ | ✓ |
| A. Alrawashdeh | Clinical methodology review, interpretation of clinical relevance | Methods + Discussion review | ✓ | ✓ |
| S. Rohde | Institutional sponsorship, methodology oversight, senior review | Full manuscript review | ✓ | ✓ |

All authors meet ICMJE authorship criteria.

---

## 7. Data Availability

ImageCAS is publicly available at https://github.com/XiaoweiXu/ImageCAS-A-Large-Scale-Dataset-and-Benchmark-for-Coronary-Artery-Segmentation-based-on-CT. CADS-dataset is publicly available on Hugging Face. TotalSegmentator weights are MIT-licensed and reproducibly downloadable. All code and analysis pipelines are released under MIT license at *(GitHub URL)*. Exact pipeline version archived at *(Zenodo DOI)*.

---

## References

*(To be expanded — current core references:)*

1. Guo Z, Liu Y, et al. A deep learning model for carotid plaques detection based on CTA images: a two stepwise early-stage clinical validation study. *Front Neurol*. 2024. doi:10.3389/fneur.2024.1480792
2. Wasserthal J, et al. TotalSegmentator: Robust segmentation of 104 anatomical structures in CT images. *Radiol Artif Intell*. 2023. doi:10.1148/ryai.230024
3. Zeng A, et al. ImageCAS: A large-scale dataset and benchmark for coronary artery segmentation based on computed tomography angiography images. *Comput Med Imaging Graph*. 2023. doi:10.1016/j.compmedimag.2023.102287
4. AWMF. S3-Leitlinie zur Diagnostik, Therapie und Nachsorge der extracraniellen Carotisstenose. AWMF-Register-Nr. 004-028.
5. ESCR Consensus Document. State-of-the-art CT and MR imaging and assessment of atherosclerotic carotid artery disease. *Eur Radiol*. 2022. doi:10.1007/s00330-022-09025-6
6. Draelos RL, Carin L. Use HiResCAM instead of Grad-CAM for faithful explanations of convolutional neural networks. *arXiv*. 2020. arXiv:2011.08891
7. Cardoso MJ, et al. MONAI: An open-source framework for deep learning in healthcare. *arXiv*. 2022. arXiv:2211.02701

---

## Supplements (planned)

- **A** — Dataset preprocessing pipeline (DICOM → NIfTI → resample → normalize)
- **B** — HiResCAM architecture details
- **C** — Trust-Score composite formula
- **D** — Reproducibility checklist (CLAIM, TRIPOD-AI)
- **E** — Full statistical analysis code (Python notebook)
