---
name: 2026-04-29_research_xai_radiology
type: run
---

# Explainable AI (XAI) Best Practices for Medical Image Analysis / Radiology

## Executive Summary

This research review synthesizes peer-reviewed evidence on Explainable AI (XAI) best practices specifically for radiology and medical image analysis, with direct applicability to the Carotis-AI project (carotid plaque/stenosis quantification from CTA).

**Key findings:**

1. **No single CAM method dominates.** A large comparative study of 11 CAM methods in veterinary radiography (n=7,362 images) found **EigenGradCAM** achieved the highest mean clinician rating (2.571 ± 1.256), followed by EigenCAM (2.519) and GradCAM++ (2.512). However, **no method universally improved diagnostic confidence**, and inter-rater reliability was only moderate (Kendall's Tau 0.12–0.38). HiResCAM and LayerCAM showed pathology-dependent strengths but were not consistently top-ranked across all classes.

2. **Heatmaps improve diagnostic accuracy, but the effect is task-dependent.** A tuberculosis chest-X-ray study found **77% of physicians improved diagnostic accuracy when using XAI visual explanations** vs. without. However, a meta-analysis of 83 studies revealed overall AI diagnostic accuracy of only 52.1% with no significant difference vs. physicians, highlighting that explanation quality and model quality are tightly coupled.

3. **SHAP alone is insufficient for clinical acceptance.** A controlled study with 63 clinicians found that **"results + SHAP + clinical narrative explanation" significantly outperformed** both "results only" and "results + SHAP" in weight of advice (0.73 vs. 0.61 vs. 0.50), trust, satisfaction, and usability. Pure SHAP visualizations without clinical framing are less effective than narrative explanations.

4. **Multimodal XAI is measurably better than single-modality.** In critical care, multimodal AI achieved a **mean 4.4% relative AUC improvement** (95% CI: 3.2–5.7) over unimodal models, with 94.6% of studies reporting superior performance. The HAIM framework demonstrated **6–30% performance gains** when combining imaging + tabular + text + time-series data. For explainability, multimodal attention mechanisms allow clinicians to see which modality contributed most to a decision.

5. **XAI evaluation requires clinically aligned metrics.** The proposed **XAlign** metric (integrating Weighted Relevance Overlap, Boundary Agreement Score, and Dispersion Penalty) quantitatively discriminates explanation quality. On brain MRI and breast ultrasound, Grad-CAM scored 0.662–0.742, LIME 0.459–0.474, SHAP 0.256–0.348, while native explanation mechanisms scored 0.884–0.929. Traditional metrics like AOPC and Max-Sensitivity favor faithful methods (e.g., HiResCAM), whereas HAAS is less reliable for complex medical patterns.

---

## 1. Grad-CAM vs HiResCAM vs LayerCAM in Radiology: User Studies

### 1.1 Comparative Evidence

| Study | Domain | Methods Compared | N | Key Finding |
|-------|--------|------------------|---|-------------|
| Dias et al. (2025), *Sci Rep* | Veterinary radiography | 11 CAMs incl. Grad-CAM, HiResCAM, LayerCAM, EigenGradCAM, ScoreCAM | 7,362 images, 3 veterinarians | EigenGradCAM highest mean score (2.571). HiResCAM ranked 8th of 11 by global average (2.179). LayerCAM ranked 4th (2.460). **No method consistently improved diagnostic confidence.** |
| Lamprou et al. (2023) | Medical datasets (CRC, COVID-19, HAM10000, BreakHis) | Grad-CAM vs HiResCAM | 4 datasets | HiResCAM achieved higher AOPC and lower Max-Sensitivity (better faithfulness) in 7/8 model cases. Pixel-level gradient preservation yields finer-grained maps. |
| Rafati et al. (2025) | Brain hemorrhage CT (Hemorica) | 10 CAMs incl. Grad-CAM, HiResCAM, AblationCAM | Hemorica dataset | HiResCAM achieved bounding-box Dice 0.572, IoU 0.401, loose hit-rate 0.975 — outperforming Grad-CAM and approaching AblationCAM with much lower compute. |
| Jiang et al. (2021), *IEEE TIP* | General localization (PASCAL VOC) | Grad-CAM, Grad-CAM++, LayerCAM | PASCAL VOC | LayerCAM (ResNet101) achieved 64.5% mIoU in weakly-supervised segmentation, outperforming Grad-CAM (56.3%) and Grad-CAM++ (56.1%) by >5%. Hierarchical fusion of multi-layer maps improves localization. |
| Almeida et al. (2025), *PMC* | Chest radiology (pneumonia, COVID-19) | Grad-CAM vs LIME | 2 datasets, clinician survey | Grad-CAM preferred over LIME for **coherency and trust**. However, concerns raised about clinical usability. SHAP deemed less stable for local image accuracy. |

### 1.2 Radiologist Preference Insights

From the Dias et al. veterinary radiography study (the largest clinician-evaluated CAM comparison to date):

- **ScoreCAM** achieved the highest score in "Alveolar pattern" (3.361) but with high variance (SD=1.073).
- **EigenCAM/EigenGradCAM** were most consistent across "Cardiomegaly", "Interstitial pattern", and "Bronchial pattern" classes.
- **HiResCAM** performed well in absolute "best performing" rankings (3rd by Borda count = 6.796) but poorly in relative mean scores, suggesting clinicians appreciated its precision when it worked but found it inconsistent.
- **Grad-CAM** was middle-of-the-pack (global average 2.068), with broad activation areas that were "helpful in certain situations" but lacked precision for small anomalies.

From the chest radiology user study (Almeida et al.):
- Grad-CAM was rated more coherent and trustworthy than LIME.
- Clinicians expressed **lack of awareness** about XAI potential uses.
- **Multi-modal explainability** was identified as a crucial need.

### 1.3 Resolution and Localization Trade-offs

| Method | Resolution Mechanism | Known Limitation in Radiology |
|--------|---------------------|------------------------------|
| **Grad-CAM** | Averages gradients per feature map → 7×7 grid upsampled | Coarse localization; blurs small pathologies; boundary overreach |
| **HiResCAM** | Element-wise (Hadamard) product of activations × gradients at each spatial location | Higher resolution but may produce "spiky" activations covering less of the object; exact faithfulness only guaranteed for single-FC-layer architectures |
| **LayerCAM** | Uses pixel-level positive gradients as weights; aggregates hierarchical maps from multiple layers | Better fine-grained localization, especially in lower layers where spatial info is preserved; requires multi-layer fusion for best results |

**Clinical implication:** For small, confined pathologies (e.g., early plaque vulnerability features), LayerCAM's hierarchical fusion or HiResCAM's pixel-level fidelity may be preferable to standard Grad-CAM. However, EigenGradCAM showed the most consistent clinician approval across pathology types.

---

## 2. Heatmap Effectiveness: Do Heatmaps Improve Diagnostic Accuracy?

### 2.1 Evidence Summary

| Study | Modality | Finding |
|-------|----------|---------|
| TB diagnosis study (cited in Almeida et al.) | Chest X-ray | **77% of 13 physicians showed enhanced diagnostic accuracy** with XAI visual explanations vs. without |
| Meta-analysis (Liu et al., 2019, *Lancet Digit Health*) | Multiple imaging modalities | Deep learning performance comparable to healthcare professionals; AI-assisted imaging superior in certain studies but with inconsistencies |
| Nature npj Digital Medicine (2025) | Multiple | Analysis of 83 studies: overall AI diagnostic accuracy **52.1%** — no significant difference vs. physicians; highlights need for standardized implementation |
| Grad-CAM wrist/elbow study (2024) | Musculoskeletal radiographs | Average test accuracy 0.81 (wrist), 0.60 (elbow); DSC showed **only minimal agreement for fractures** — heatmaps aligned on metal implants but not subtle pathology |
| Alzheimer's heatmap validation (2023) | Brain MRI (ADNI) | LRP, Integrated Gradients, and Guided Grad-CAM all captured brain regions overlapping with meta-analysis VBM maps; **IG showed most promising results**; heatmaps from deep nonlinear models outperformed linear SVM maps |

### 2.2 Meta-Analytic Conclusion

Heatmaps **can** improve diagnostic accuracy, but the effect is **moderated by:**
- **Pathology visibility:** Heatmaps work better for large, obvious findings (cardiomegaly, pneumothorax) than for subtle or diffuse patterns (interstitial lung disease, early plaque).
- **Explanation quality:** Low-fidelity heatmaps (blurred, mislocalized) do not improve — and may reduce — clinician trust.
- **Clinician AI literacy:** Studies consistently find low awareness of XAI among practitioners; without training, heatmaps may be misinterpreted.
- **Task complexity:** In high-stakes tasks requiring precise localization, heatmap utility depends heavily on spatial fidelity.

**Key quote from Dias et al.:**
> "Despite variations in saliency visualization, no single method universally improved veterinarians' diagnostic confidence... CAM-generated heatmaps lack semantic understanding, limiting their utility."

---

## 3. SHAP for Tabular Medical Data: Best Practices

### 3.1 Key Evidence

| Study | Application | SHAP Best Practice Identified |
|-------|-------------|------------------------------|
| Hur et al. (2025), *npj Digit Med* | Perioperative transfusion prediction | **Clinical narrative + SHAP > SHAP alone > results alone.** WOA: 0.73 vs 0.61 vs 0.50. Top-3 SHAP features translated into natural language explanations significantly improved acceptance. |
| Lundberg et al. (2020+) / SHAP tutorial | Drug development / clinical ML | Use **TreeSHAP** for tree-based models (XGBoost, LightGBM, Random Forest) for computational efficiency. Use **KernelSHAP** or **DeepSHAP** for neural networks. |
| Practical SHAP guide (PMC11513550) | General clinical tabular data | Beeswarm plots for global feature importance; dependence plots for feature interactions; scatter plots for temporal trends. **Bar plots for top-N feature ranking** most intuitive for clinicians. |
| SHAP stroke prediction (2025) | Stroke risk (tabular clinical) | SHAP-weighted hybrid ensemble: use SHAP as **adaptive feature weighting** rather than just post-hoc explanation. Age, avg glucose, BMI were top features — aligned with clinical findings. |
| Appendix cancer prediction (2025) | Cancer prediction | SHAP-based **feature engineering** (selection → construction → weighting) improved F1 to 0.8877. Composite features derived from SHAP interaction values identified high-risk patients missed by individual indicators. |

### 3.2 Best Practices for Clinical SHAP

1. **Always pair SHAP with clinical narrative.** Raw SHAP beeswarm plots are less effective than rule-based natural language summaries (e.g., "The top 3 factors increasing this patient's risk are: Age (72), Hb (8.2 g/dL), and PT-INR (1.4).").

2. **Use TreeSHAP for structured clinical data.** It is exact and orders of magnitude faster than model-agnostic approximations. For deep learning on tabular data, DeepSHAP or GradientSHAP are preferred.

3. **Show global + local explanations.** Clinicians need both: (a) population-level feature importance to understand model behavior, and (b) patient-specific SHAP values to understand individual predictions.

4. **Beware correlated features.** SHAP can distribute importance across correlated clinical variables (e.g., BMI and weight). Use SHAP interaction values or group correlated features.

5. **Temporal SHAP requires caution.** Aggregating SHAP values over time points loses temporal information. Use time-dependent SHAP variants for longitudinal clinical data.

---

## 4. Combining XAI Methods: Multi-Modal Explanation

### 4.1 Evidence That Multi-Modal XAI > Single-Modality

| Study | Modalities | Performance Gain | Explainability Approach |
|-------|-----------|------------------|------------------------|
| Soenksen et al. (HAIM framework), *Nature* | Imaging + tabular + text + time-series | **6–30% outperformance** vs unimodal | Modality-specific embeddings → XGBoost; SHAP for all inputs |
| Critical care scoping review (PMC13084062) | Structured data + text + imaging + waveforms | **4.4% relative AUC improvement** (95% CI 3.2–5.7); 94.6% of studies favored multimodal | 14 explainability techniques identified; intermediate fusion predominant |
| Alzheimer's multimodal (PMC12876535) | MRI + PET + clinical + genetic | 93.26% accuracy (vs lower unimodal) | Hierarchical attention + SHAP for clinical features |
| Multimodal NSCLC (2025) | CT imaging + clinical data | Substantial MCC increase over unimodal CT or clinical alone | Grad-CAM for images + feature importance for clinical; multimodal heatmaps showed **higher intensity and more refined lesion focus** |
| AMD ophthalmology (PMC11554086) | OCT + infrared reflectance | 0.94 accuracy (better than unimodal) | **Grad-CAM + Guided Grad-CAM combined** for coarse + fine-grained analysis |

### 4.2 Why Multi-Modal XAI Works Better

1. **Complementary information:** Imaging captures anatomical/functional features; tabular data captures demographics, labs, history; text captures narrative clinical reasoning.
2. **Robustness to missing data:** If one modality is unavailable or noisy, the model can still reason from others.
3. **Richer explanations:** Clinicians see not just "where" (image heatmap) but also "why based on history" (SHAP values for labs/age/symptoms).
4. **Cross-modal validation:** When image heatmap and tabular SHAP both point to the same pathology, clinician confidence increases.

### 4.3 Carotis-AI Relevance

For Carotis-AI, a multi-modal explanation would combine:
- **CTA image explanation:** Grad-CAM/LayerCAM highlighting plaque regions and stenosis segments.
- **Tabular explanation:** SHAP values for patient age, cardiovascular risk factors, prior TIA/stroke history, lab values.
- **Decision-tree harvesting:** The physician's own clinical reasoning (captured via the decision-tree interface) provides a third, human-generated explanation layer.

This three-layer explanation (visual + tabular + physician reasoning) aligns with the finding that **RSC (results + SHAP + clinical narrative) outperforms RS or RO alone**.

---

## 5. XAI Evaluation Metrics: Measuring "Good" Explanations in Medicine

### 5.1 Clinically Oriented Metrics

| Metric | What It Measures | Best For | Source |
|--------|-----------------|---------|--------|
| **XAlign** (novel) | Regional concentration + boundary agreement + dispersion penalty | Saliency map alignment with expert tumor annotations | SpikeNet paper (Front Med Tech 2025) |
| **Weighted Relevance Overlap (WRO)** | Proportion of explanation relevance inside annotated ROI | Localization accuracy of heatmaps | SpikeNet paper |
| **Boundary Agreement Score (BAS)** | Normalized inverse Hausdorff distance between explanation and GT contours | Boundary precision (critical for surgical planning) | SpikeNet paper |
| **Dispersion Penalty (DP)** | Attribution scattered outside annotated region | Penalizing clinically irrelevant activations | SpikeNet paper |
| **AOPC** (Area Over Perturbation Curve) | Prediction change when most important pixels removed/inserted | Faithfulness of attribution ranking | Lamprou et al. (2023) |
| **Max-Sensitivity** | Stability of explanations to input perturbations | Robustness/consistency | Lamprou et al. (2023) |
| **HAAS** (Heatmap Assisted Accuracy Score) | Accuracy change when masking heatmap regions | Machine-centric explainability | IEEE Xplore (2022) — but **less reliable for complex medical patterns** |
| **IoU / Dice** | Overlap between explanation mask and ground truth | Simple segmentation tasks | Multiple studies |
| **Pointing Game** | Whether maximum attribution point falls inside GT | Coarse localization check | Multiple studies |

### 5.2 Human-Centered Evaluation Framework

Per Almeida et al. and Hoffman et al., clinical XAI evaluation should assess:

| Criterion | Definition | How to Measure |
|-----------|-----------|----------------|
| **Clinical Relevance** | Useful, usable, accurate for medical decision-making | Clinician rating scales (1–5), decision change (WOA) |
| **Comprehensibility** | Coherent presentation; no technical expertise required | Likert scales, think-aloud protocols, SUS scores |
| **Confidence/Trust** | Explanation truthfully reflects model reasoning | Trust Scale Recommended for XAI, preference rankings |
| **Truthfulness** | Explanation actually corresponds to model computation | Fidelity metrics (AOPC, correlation with model gradients) |
| **Informative Plausibility** | Explanation aligns with clinical/pathophysiological knowledge | Expert panel review against clinical guidelines |
| **Computational Efficiency** | Explanation generated within clinically acceptable time | Per-image latency (ms), throughput (images/sec) |

### 5.3 Key Metric Benchmarks from Literature

From the SpikeNet XAlign evaluation (brain MRI + breast ultrasound):

| Method | TCGA-LGG (MRI) | BUSI (Ultrasound) | Interpretation |
|--------|---------------|-------------------|----------------|
| SHAP | 0.348 ± 0.029 | 0.256 ± 0.027 | Poor localization; fragmented, anatomically irrelevant |
| LIME | 0.459 ± 0.026 | 0.474 ± 0.030 | Moderate alignment; noisy due to perturbation approximations |
| Grad-CAM | 0.662 ± 0.031 | 0.742 ± 0.028 | High alignment; correct region but boundary overreach |
| Native (SpikeNet) | **0.884 ± 0.021** | **0.929 ± 0.018** | Very high alignment; sharp, localized, boundary-adherent |

**Insight:** Post-hoc methods (Grad-CAM, LIME, SHAP) all underperform compared to architectures with **native explanation mechanisms**. For Carotis-AI, if explainability is a core requirement, consider integrating explanation heads into the MFSD-UNet architecture rather than relying solely on post-hoc Grad-CAM.

---

## 6. Method Comparison Table

| Method | Resolution | Speed | User Preference | Best For | Key Limitation |
|--------|-----------|-------|----------------|----------|----------------|
| **Grad-CAM** | Low (7×7 upsampled) | Fast (~ms) | Moderate (2.068/5 in vet study; preferred over LIME in chest study) | Quick screening; broad region identification; standard baseline | Blurs small pathologies; boundary overreach; coarse localization |
| **HiResCAM** | High (pixel-level Hadamard product) | Fast (single backward pass) | Mixed (3rd in Borda count; 8th in mean scores) | Precise localization where exact faithfulness matters; brain hemorrhage; CT anomalies | "Spiky" activations; may cover less of object; approximate faithfulness for deep heads |
| **LayerCAM** | High (hierarchical multi-layer fusion) | Moderate (multiple layers) | Moderate (4th of 11; 2.460/5) | Small, confined pathologies; weakly-supervised segmentation; fine-grained localization | Requires multi-layer aggregation; shallow-layer noise without fusion |
| **EigenGradCAM** | Medium | Fast | **Highest mean score (2.571/5)** | Consistent performance across diverse pathologies; cardiomegaly; bronchial patterns | Less spatial precision than HiResCAM/LayerCAM |
| **ScoreCAM** | Medium | Slow (forward passes per channel) | High in specific classes (alveolar pattern: 3.361) | Pathologies with strong activation signatures; gradient-free scenarios | High variance; computationally expensive |
| **SHAP (images)** | Low (patch-based) | Very slow | Poor for images (0.256–0.348 XAlign) | Tabular/feature data; global model behavior | Fragmented saliency; poor localization; unstable for complex images |
| **SHAP (tabular)** | N/A (feature scores) | Fast (TreeSHAP) | High when paired with clinical narrative | Structured clinical data; EHR features; risk factors | Correlated feature distribution; requires clinical translation |
| **LIME** | Medium (superpixel) | Slow (perturbation) | Lower than Grad-CAM in chest study | Model-agnostic local explanations; quick prototyping | Noisy; unstable; poor boundary adherence |

---

## 7. Recommended XAI Stack for Carotis-AI

Based on the evidence, the following stack is recommended for Carotis-AI's carotid stenosis/plaque analysis pipeline:

### 7.1 Image Explanations (CTA)

| Priority | Method | Use Case | Implementation Notes |
|----------|--------|----------|---------------------|
| **Primary** | **LayerCAM** (hierarchical, multi-layer) | Main diagnostic heatmap for plaque localization and stenosis grading | Fuse maps from last 2–3 decoder stages of MFSD-UNet to preserve both coarse plaque extent and fine surface irregularities. Evaluate with XAlign using radiologist-drawn plaque ROIs. |
| **Secondary** | **HiResCAM** | High-resolution focal analysis of vulnerable plaque features (calcification, lipid core, ulceration) | Use when precise pixel-level attribution is needed (e.g., explaining why a specific region was flagged as high-risk). Computed only on-demand to save inference time. |
| **Baseline** | **Grad-CAM** | Fallback; compatibility with standard pytorch-grad-cam library; broad context | Keep for baseline comparisons and integration tests. Useful for showing general carotid bifurcation attention. |

**Rationale:** LayerCAM's multi-layer fusion provides the best compromise between fine-grained localization (needed for plaque morphology) and stable clinician approval. HiResCAM adds pixel precision for specific vulnerability markers. Grad-CAM serves as a robust fallback.

### 7.2 Tabular Explanations (Patient Data)

| Priority | Method | Use Case |
|----------|--------|----------|
| **Primary** | **TreeSHAP** (via XGBoost/LightGBM) | For the clinical risk stratification component (if separate tree-based model) or for explaining aggregated patient features |
| **Secondary** | **DeepSHAP / GradientSHAP** | If tabular features are processed through the neural network (MFSD-UNet auxiliary classifier) |
| **Presentation** | **Clinical narrative generation** | Convert top-3 SHAP features into German natural language: *"Das Modell gewichtet: (1) Stenosegrad 78%, (2) Alter 72 Jahre, (3) Vorheriger TIA."* |

### 7.3 Multi-Modal Explanation Architecture

```
Input: CTA image + Patient tabular data (age, risk factors, labs, history)
         ↓
    ┌────┴────┐
    ↓         ↓
MFSD-UNet   Tabular Encoder
(image)     (clinical features)
    ↓         ↓
LayerCAM    SHAP values
heatmap     (top-N features)
    ↓         ↓
    └────┬────┘
         ↓
   Fusion / Orchestration
   (decision-tree harvesting captures physician reasoning)
         ↓
   Unified Explanation Dashboard:
   - CTA with LayerCAM overlay (plaque region)
   - Side panel: Top SHAP clinical factors
   - Bottom: Physician's captured decision tree logic
```

### 7.4 Evaluation Protocol

| Level | Metric | Threshold / Target |
|-------|--------|-------------------|
| **Model-centric** | XAlign (vs. radiologist plaque ROI) | > 0.75 (approaching Grad-CAM's 0.662–0.742 baseline; native mechanisms should exceed) |
| | AOPC | Higher is better; benchmark against HiResCAM on same architecture |
| | Max-Sensitivity | Lower is better; indicates stable explanations |
| **Human-centric** | Weight of Advice (WOA) | > 0.65 when explanations provided vs. without |
| | Trust Scale (XAI-recommended) | > 28/35 |
| | System Usability Scale (SUS) | > 68 ("good" threshold) |
| | Clinical relevance rating | > 4/5 from participating radiologists |
| **Regulatory** | Fidelity to model computation | Correlation > 0.8 between explanation and internal attention weights |
| | PII safety | No patient-identifiable information in explanation logs |

---

## 8. Open Questions / Future Work

### 8.1 Technical Gaps

1. **Native explanation for UNet/Swin architectures:** Most XAI evaluation literature focuses on classification CNNs (ResNet, VGG). The MFSD-UNet (U-Net + Swin Transformer + Deep Supervision) requires adapted LayerCAM/HiResCAM implementations for encoder-decoder structures with skip connections. *Action: Validate that gradients flow meaningfully through the Swin Transformer blocks.*

2. **3D CTA explanation:** Carotis-AI processes 3D CTA volumes, but most CAM literature evaluates 2D slices. How to aggregate 3D attribution maps across slices while preserving spatial coherence is an open question. *Action: Evaluate 3D Grad-CAM extensions or slice-aggregation strategies.*

3. **Real-time explanation latency:** The Carotis-AI backend must generate explanations within the clinical workflow. HiResCAM and LayerCAM add computation; native explanation heads (like SpikeNet's) reduce latency by ~80%. *Action: Benchmark explanation generation time on target Edge hardware (CPU-only ONNX Runtime).*

4. **SHAP for multi-modal fusion:** How to attribute importance across image features and tabular features jointly? Current SHAP libraries process modalities separately. *Action: Investigate Captum's multimodal attribution or custom Shapley value computation for the fusion layer.*

### 8.2 Clinical Validation Needs

1. **Radiologist reader study:** No published study specifically compares CAM methods for **carotid CTA** or **plaque characterization**. A controlled reader study with 5–10 neuroradiologists/vascular surgeons is needed to validate which explanation type improves stenosis grading accuracy and inter-rater agreement.

2. **Decision impact measurement:** Most studies measure explanation preference, not actual decision change. Carotis-AI should measure **weight of advice** (WOA) — do explanations change the physician's stenosis grade or treatment recommendation?

3. **Long-term trust evolution:** Initial studies show skepticism toward AI explanations. Does trust increase with sustained use? Does over-reliance (automation bias) emerge? *Action: Design longitudinal usability study post-deployment.*

4. **Plaque-type-specific explanations:** Different CAM methods may perform differently for calcified vs. lipid-rich vs. ulcerated plaques. *Action: Stratify XAlign evaluation by plaque type (if ground-truth labels available).*

### 8.3 Regulatory and Ethical

1. **Explanation audit trail:** For MDR compliance, explanations must be reproducible and logged. How to version-control explanation methods so that regulatory submissions remain valid when XAI methods are updated?

2. **Explanation fairness:** Do explanations highlight different regions for different demographic groups (age, sex)? If the model has demographic bias, will the explanation reveal or conceal it?

3. **LLM-generated clinical narratives:** The Hur et al. study suggests LLM-translated SHAP narratives improve acceptance. Can this be done locally (LLaMA-3.1, as mentioned in JMIR 2025) without cloud data export, satisfying Carotis-AI's local-first requirement?

---

## Sources (Peer-Reviewed)

1. Dias et al. (2025). *Comparative evaluation of CAM methods for enhancing explainability in CNN outputs in veterinary radiography.* Scientific Reports, PMC12350829.
2. Almeida et al. (2024). *Evaluating Explainable Artificial Intelligence (XAI) techniques in chest radiology imaging through a human-centered Lens.* PMC11463756.
3. Lamprou et al. (2023). *Grad-CAM vs HiResCAM: A comparative study via evaluation metrics.* University of Piraeus thesis / related works.
4. Rafati et al. (2025). *Benchmarking Class Activation Map Methods for Explainable Brain Hemorrhage Classification on Hemorica Dataset.* arXiv:2508.17699.
5. Jiang et al. (2021). *LayerCAM: Exploring Hierarchical Class Activation Maps for Localization.* IEEE Transactions on Image Processing.
6. Hur et al. (2025). *Comparison of SHAP and clinician friendly explanations reveals effects on clinical decision behaviour.* npj Digital Medicine, PMC12475050.
7. SpikeNet / XAlign (2025). *More than just a heatmap: elevating XAI with rigorous evaluation metrics.* Frontiers in Medical Technology, PMC12602234.
8. Soenksen et al. / HAIM framework (2024). *Orchestrating explainable artificial intelligence for multimodal and longitudinal data in medical imaging.* npj Digital Medicine, Nature s41746-024-01190-w.
9. Multimodal AI in Critical Care (2026). *Multimodal Artificial Intelligence for Precision Critical Care.* PMC13084062.
10. Practical SHAP guide (2024). *Practical guide to SHAP analysis: Explaining supervised machine learning model predictions in drug development.* PMC11513550.
11. Explainable AI in Medical Imaging (2025). *Explainable artificial intelligence (XAI) in medical imaging: A systematic review.* PMC12809972.
12. Draelos & Carin (2020). *HiResCAM: High-Resolution Class Activation Mapping.* Original HiResCAM method.
13. Liu et al. (2019). *A comparison of deep learning performance against health-care professionals in detecting diseases from medical imaging: a systematic review and meta-analysis.* Lancet Digital Health.
14. Prinster et al. (2024). *Care to Explain? AI explanation types differentially impact chest radiograph diagnostic performance and physician trust in AI.* Radiology, e233261.
15. JMIR Formative Research (2025). *Explainable AI-Driven Analysis of Radiology Reports Using Text and Image Data: Experimental Study.* e77482.

---

## Memory Updates

- **XAI stack decision:** Carotis-AI should adopt **LayerCAM as primary** image explanation (hierarchical, multi-layer fusion) with **HiResCAM as secondary** on-demand option, backed by **TreeSHAP + clinical narrative** for tabular data.
- **Evaluation framework:** Adopt **XAlign** (or its components: WRO, BAS, DP) for quantitative explanation evaluation against radiologist plaque annotations. Do not rely solely on AOPC or HAAS for medical images.
- **Multi-modal evidence:** Strong quantitative evidence (4.4–30% AUC improvement) supports Carotis-AI's planned multi-modal approach (CTA + clinical data + physician decision-tree harvesting).
- **Clinical narrative necessity:** Raw SHAP/heatmaps are insufficient. Every explanation must include **German natural-language clinical context** to maximize physician acceptance (WOA +46% vs. results-only).
- **Gap identified:** No published XAI comparison exists specifically for **carotid CTA plaque analysis**. A reader study is a critical future step for P3/P4 validation.
