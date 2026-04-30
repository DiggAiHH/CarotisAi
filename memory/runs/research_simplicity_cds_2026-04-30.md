---
name: research_simplicity_cds_2026-04-30
type: run
date: 2026-04-30
---
# Research: Simplicity & Usability in Clinical Decision Support Systems / Medical AI Interfaces

**Context:** Carotis-AI -- local-first medical AI for carotid stenosis quantification.
**Stack:** React 19 + Vite + TypeScript + Tailwind + Cornerstone3D + FastAPI.
**Goal:** Extract evidence-based design principles for low-friction, high-adoption radiology AI interfaces.

---

## 1. Cognitive Load Theory Applied to Radiology Workstations

### Source 1 ? AHRQ Issue Brief
- **Citation:** Agency for Healthcare Research and Quality (AHRQ), *Cognitive Load Theory and Its Impact on Diagnostic Accuracy* (2023/2024). Available at ahrq.gov/diagnostic-safety/resources/issue-briefs/dxsafety-cognitive-load3.html.
- **Core Finding:** When working memory is overloaded by extrinsic distractions (poorly organized EHR data, interruptions, multitasking), clinicians lose the cognitive bandwidth required for effortful Type 2 (analytical) thinking and default to intuitive Type 1 processing, increasing diagnostic error risk.
- **Actionable Design Principle:** Design radiology AI interfaces to minimize *extraneous* cognitive load -- remove non-essential visual clutter, avoid interruptive alerts for low-severity findings, and keep all relevant decision data spatially aligned so clinicians do not need to mentally integrate fragmented information.

### Source 2 ? De Riddere et al. (PACS E-Learning Study)
- **Citation:** De Riddere et al., *Optimizing Physicians Instruction of PACS Through E-Learning*, Journal of Digital Imaging (PMC3043672, 2011).
- **Core Finding:** Applying Cognitive Load Theory (CLT) techniques -- weeding (cutting away extraneous visual information), aligning (placing related text/images close together), and signaling (highlighting key aspects with color boxes) -- measurably reduced mental burden when learning PACS interfaces.
- **Actionable Design Principle:** In the Carotis-AI DICOM viewer, **weed** non-relevant UI elements during analysis (e.g., gray out unrelated tools), **align** AI findings text directly adjacent to the relevant image region, and **signal** high-risk stenosis findings with pre-attentive color cues (e.g., red overlay) rather than separate pop-ups.

### Source 3 ? Education Theory Made Practical (CLT in Healthcare)
- **Citation:** University of Saskatchewan, *Education Theory Made Practical: Volume 4* (2023). Fraser et al. review on CLT in healthcare simulation.
- **Core Finding:** Extraneous load in clinical environments includes buzzers, interruptions, poor printouts, and time pressure -- each increases cognitive load and makes primary tasks (e.g., ECG reading, image interpretation) harder.
- **Actionable Design Principle:** Adopt the **split-attention principle**: provide one integrated source of information rather than distributing it across space/time. For Carotis-AI, embed AI results (stenosis %, plaque vulnerability score, Grad-CAM heatmap) directly in the viewer canvas rather than forcing the radiologist to look at a separate side panel or browser tab.

---

## 2. Low-Friction UI Patterns for AI-Assisted Diagnosis

### Source 4 ? Wang et al. (RSNA 2019, AI Structured Reporting)
- **Citation:** Wang X. et al., *Implementation of AI Structured Reporting to Smooth Workflow in Radiology Department Daily Practice*, RSNA 2019 Scientific Assembly (Q1120-ED-TUB3).
- **Core Finding:** Integrating AI into structured reporting reduced interpretation and reporting time by **8.9-56.1%**; acceptance rates for AI-generated findings/measurements were **84.3-100%**; **96.9%** of radiologists preferred the AI-integrated workflow over traditional reporting.
- **Actionable Design Principle:** Auto-populate structured report fields (findings, measurements, key images) from AI output and let the radiologist **verify and revise** rather than type from scratch. In Carotis-AI, offer a one-click Accept and Populate Report button that inserts stenosis quantification and plaque descriptors into a predefined structured report template.

### Source 5 ? Sectra Reporting / AI Auto-Impressions
- **Citation:** Sectra Medical Systems, *Sectra Reporting* product documentation (2025). medical.sectra.com/product/sectra-reporting/
- **Core Finding:** One-click AI impression tools that summarize dictated findings and auto-populate templates significantly reduce report turnaround time while maintaining radiologist control.
- **Actionable Design Principle:** Provide **one-click AI impressions** that generate a draft impression from the AI analysis, but keep the radiologist in full control to edit or discard. The action should be a single button press within the existing reporting pane, not a separate application.

### Source 6 ? AI to SR Pipeline (Insights into Imaging, 2024)
- **Citation:** T. et al., *A novel reporting workflow for automated integration of artificial intelligence results into structured radiology reports*, Insights into Imaging (SpringerOpen, 2024). DOI: 10.1186/s13244-024-01660-5.
- **Core Finding:** An automated pipeline converting AI findings into DICOM Structured Reports (SR) enabled standardized, time-efficient, high-quality chest X-ray reporting with strong synergy between AI and structured reporting.
- **Actionable Design Principle:** Use **DICOM SR** as the exchange format for AI results -- it is machine-readable (enables worklist reprioritization) and human-renderable (enables accept/reject/adjust workflows directly in the viewer). Avoid static DICOM secondary captures which freeze AI results into non-interactive images.

---

## 3. CDS Usability Heuristics -- What Makes Clinicians Actually USE the AI

### Source 7 ? JMIR Systematic Review on CDSS HCI Elements
- **Citation:** *Optimizing Clinical Decision Support System Functionality by Leveraging Specific Human-Computer Interaction Elements: Insights From a Systematic Review*, JMIR Human Factors (2025). DOI: 10.2196/69333.
- **Core Finding:** Alert fatigue poses a significant challenge because users neglect or override frequent alerts; usability flaws include dense information, low signal-to-noise ratio, missing practical recommendations, and lack of transparency. Five solutions were identified: (1) augment alert specificity, (2) tier alerts by severity, (3) apply human factors principles (format, color, legibility), (4) customize based on patient attributes, (5) tailor for practitioners.
- **Actionable Design Principle:** For Carotis-AI, **tier findings by severity**: only interruptive (modal) alerts for critical findings (e.g., high-grade stenosis >70%); non-interruptive badges/labels for moderate/low-grade findings. Always pair alerts with actionable next steps (e.g., Recommend CTA follow-up in 3 months).

### Source 8 ? Olakotan et al. (CDSS Alert Appropriateness Systematic Review)
- **Citation:** Olufisayo Olusegun Olakotan et al., *The appropriateness of clinical decision support systems alerts in supporting clinical workflows: A systematic review*, Health Informatics Journal (2021). DOI: 10.1177/14604582211007536.
- **Core Finding:** Most CDSS alerts were **not properly designed based on human factor methods and principles**, explaining high alert overrides in clinical practice. Alerts interrupt workflow and are often silenced or disabled.
- **Actionable Design Principle:** Before deploying any AI alert or notification in Carotis-AI, validate it against **human factors / Lean principles** -- ask: does this alert appear at the right time? Is it actionable? Can the user override it without penalty? If the answer to any is no, redesign before release.

### Source 9 ? AI-CDSS Systematic Review (PJLSS, 2025)
- **Citation:** *A Systematic Review of AI-based Clinical Decision Support Systems: From Development and Implementation to Applications*, Pakistan Journal of Life and Social Sciences (2025).
- **Core Finding:** Standalone or weakly integrated CDSS increases cognitive load and task completion time. **Clinicians ignore ~95% of alerts** because common, low-priority alerts cause desensitization and loss of trust, leading genuinely critical alerts to be missed.
- **Actionable Design Principle:** **Embed Carotis-AI directly into the PACS/viewer workflow** -- do not build a separate web app radiologists must open. Adaptive alerting (context-aware, urgency-ranked, personalized to clinician history) dramatically improves relevance and reduces ignore rates.

---

## 4. Simplicity Metrics -- How to Measure UI Simplicity in Medical Software

### Source 10 ? Visual Perception and Pre-Attentive Attributes in Oncological Data Visualisation
- **Citation:** *Visual Perception and Pre-Attentive Attributes in Oncological Data Visualisation*, Frontiers in Oncology / PMC12292122 (2025).
- **Core Finding:** Pre-attentive attributes (color, shape, orientation, size) guide user attention before conscious processing. Reliable evaluation requires quantitative methods: visual search task performance, eye-tracking (gaze fixation, time to first fixation, scan paths), Signal Detection Theory metrics, NASA-TLX, and SUS.
- **Actionable Design Principle:** When evaluating Carotis-AI prototypes, use a **combined metric battery**: (1) **NASA-TLX** for cognitive workload, (2) **SUS** for subjective usability, (3) **eye-tracking** to verify radiologists look at AI findings quickly (time to first fixation), and (4) **task completion time** for stenosis assessment workflows.

### Source 11 ? EdgeFlow CW10 Plus Usability Study
- **Citation:** *Usability Validation of an Integrated Hemodynamic and Pulmonary Monitoring Device*, PMC13073963 (2024/2025).
- **Core Finding:** A multi-method approach (task success rate + SUS + NASA-TLX + eye-tracking heat maps) revealed that even experienced clinicians showed more dispersed gaze patterns and higher workload when interacting with a new, non-optimized interface.
- **Actionable Design Principle:** Set a **SUS benchmark >= 68** (good usability) and **NASA-TLX overall task load < 30** for Carotis-AI. Use heat-map analysis during usability testing to ensure radiologists gaze is directed efficiently toward the AI panel and relevant image regions, not scattered across the UI.

### Source 12 ? Predicting EHR Usability (JMIR Human Factors, 2025)
- **Citation:** *Predicting Electronic Health Record Usability: Scoping Review of Adoption Models, Metrics, and Future Directions*, JMIR Human Factors (2026/2025). DOI: 10.2196/86076.
- **Core Finding:** 70% of physicians cite usability concerns. Audit-log metrics (clicks per task, error rates, task completion time, alert fatigue peaks) provide objective quantification of usability but are rarely used predictively.
- **Actionable Design Principle:** Instrument Carotis-AI with **telemetry** (clicks per task, time-to-accept, override rate, time spent in viewer vs. AI panel). Monitor these continuously; a rising override rate or increased time-to-accept signals UI friction or model misalignment.

---

## 5. Best Practices from Successful Medical AI Deployments (Aidoc, Viz.ai, Floy)

### Source 13 ? Aidoc Blog: What is Missing from AI Marketplaces?
- **Citation:** Aidoc, *What is Missing from AI Marketplaces? Workflow, Trust and Clinical Impact* (2025). aidoc.com/learn/blog/whats-missing-from-ai-marketplaces-workflow-trust-and-clinical-impact/
- **Core Finding:** Algorithms are not solutions. Marketplaces provide minimal integration, leading to poor workflow support and low adoption. Health systems need an **operating system** with workflow awareness, dedicated AI interfaces (findings summary, explainability, worklist integration), and trust infrastructure.
- **Actionable Design Principle:** Build Carotis-AI as a **workflow-native layer**, not a plugin. Provide: (a) a findings summary panel with explainability (Grad-CAM + SHAP), (b) direct worklist integration (prioritize urgent stenosis cases), and (c) transparent confidence scoring so radiologists know when to trust vs. verify.

### Source 14 ? Viz.ai Platform and Radiology Workflow
- **Citation:** Viz.ai, *AI for Radiology, on the proven Viz.ai platform* (2021) and *Viz Radiology* product materials (2025). viz.ai/blog/ai-for-radiology-on-the-proven-viz-ai-platform
- **Core Finding:** Viz.ai achieved **73% faster time to treatment decision** and **24% decreased time to notification** by pairing AI detection with **care coordination** (mobile alerts, team communication, image sharing) -- not just image analysis.
- **Actionable Design Principle:** Beyond detection, Carotis-AI should offer **one-click communication** of confirmed critical findings to the referring clinician (e.g., neurologist, vascular surgeon) and embed the AI result with a single click into the final report. Speed of *action* matters more than speed of *detection*.

### Source 15 ? Floy (German Radiology AI)
- **Citation:** Floy / Hollmann Medical, *Radiology-AI* product overview (2024). hollmann-medical.com/en/radiology-ai/
- **Core Finding:** Floy adoption in German radiology practices is driven by three factors: **easy integration into work processes**, **relief when reading images**, and **additional security** (second-opinion validation). It is positioned as an optional IGeL service that generates additional practice revenue.
- **Actionable Design Principle:** Position Carotis-AI as a **second set of eyes** that reduces liability and reading stress, not as a replacement. Emphasize seamless PACS integration and frame the AI as augmenting radiologist confidence, especially for subtle plaque findings that are easy to overlook under time pressure.

### Source 16 ? PMC11208735 ? Integrating and Adopting AI in the Radiology Workflow
- **Citation:** *Integrating and Adopting AI in the Radiology Workflow*, Radiographics / PMC11208735 (2024).
- **Core Finding:** Effective AI integration requires conforming to a practice routine workflow with **minimal disruption**. AI results must be easily accessed without additional steps. DICOM structured reports allow dynamic interaction (accept/reject/adjust calipers), while secondary captures do not.
- **Actionable Design Principle:** Ensure Carotis-AI results appear **in the existing viewer** with zero extra logins. Use DICOM SR for results so radiologists can accept, reject, or adjust AI measurements (e.g., stenosis calipers) directly inside their native PACS environment.

---

## 6. Trust Calibration, Automation Bias and Override Design

### Source 17 ? Automation Bias Literature (Parasuraman & Manzey 2010; Goddard et al. 2012)
- **Citation:** Parasuraman R., Manzey D.H., *Complacency and Bias in Human Use of Automation: An Attentional Integration*, Human Factors (2010); Goddard K. et al., *Automation bias: a systematic review of frequency, effect mediators, and mitigators*, JAMIA (2012).
- **Core Finding:** Automation bias (over-reliance on AI) is strongest when systems have high accuracy track records. Clinicians develop glance-and-click approval habits. Requiring brief justifications for overrides creates implicit pressure to comply; conversely, random deliberation prompts and calibration cases restore vigilance.
- **Actionable Design Principle:** **Do not require lengthy override justifications** -- this penalizes disagreement. Instead: (1) display confidence levels prominently, (2) show Grad-CAM/SHAP evidence so the radiologist can *see* the basis for the AI recommendation, and (3) track disagreement patterns in the decision-tree harvesting module to calibrate trust over time.

### Source 18 ? Human-AI Interaction Design (Sequential vs. Simultaneous)
- **Citation:** Liu et al. (2025), cited in *Physician AI Handbook: Emerging AI Technologies in Healthcare* (2025). physicianaihandbook.com/future/emerging.html
- **Core Finding:** Simultaneous display of AI recommendations increases performance augmentation but raises automation bias risk, especially for junior clinicians. Sequential mode (clinician forms initial impression first, then sees AI) preserves independent judgment and is preferred for experienced clinicians.
- **Actionable Design Principle:** Offer a **sequential mode** in Carotis-AI: let the radiologist review the CTA study first, record their independent assessment, then reveal the AI analysis. This preserves clinical agency and provides clean disagreement data for the decision-tree harvesting loop.

---

## Summary Matrix

| # | Source | Year | Key Metric / Finding | Carotis-AI Design Principle |
|---|--------|------|----------------------|----------------------------|
| 1 | AHRQ CLT Brief | 2023 | Extraneous load reduces Type 2 thinking | Weed non-essential UI; align data spatially |
| 2 | De Riddere et al. | 2011 | CLT weeding/aligning/signaling reduces PACS learning burden | Gray out unrelated tools; place AI text adjacent to image |
| 3 | Wang et al. (RSNA) | 2019 | AI structured reporting cut time 8.9-56.1%; 96.9% preferred | One-click Accept and Populate Report into structured template |
| 4 | AI to SR Pipeline | 2024 | DICOM SR enables interactive AI result workflows | Export AI results as DICOM SR; avoid static secondary captures |
| 5 | JMIR HCI Review | 2025 | 95% alert ignore rate due to low specificity | Tier findings: interruptive only for >70% stenosis; badges for rest |
| 6 | Olakotan et al. | 2021 | Alerts not designed with human factors = high override | Validate every alert against human factors / Lean principles |
| 7 | PJLSS AI-CDSS Review | 2025 | Weakly integrated CDSS increases cognitive load + task time | Embed AI directly in PACS/viewer; no separate browser app |
| 8 | Visual Perception / Oncology | 2025 | Pre-attentive attributes guide attention before consciousness | Use color/size for severity; evaluate with NASA-TLX + SUS + eye-tracking |
| 9 | EdgeFlow Usability Study | 2024 | Multi-method (SUS + NASA-TLX + heat maps) catches expert friction | Benchmark SUS >=68, NASA-TLX <30; heat-map test gaze efficiency |
| 10 | Aidoc Blog | 2025 | Marketplaces fail without workflow OS layer | Build workflow-native findings summary + explainability + worklist integration |
| 11 | Viz.ai Platform | 2021/25 | 73% faster treatment decision via care coordination | One-click communication of critical findings + report embedding |
| 12 | Floy / Hollmann Medical | 2024 | Adoption driven by easy integration + relief + second-opinion security | Position as second set of eyes; reduce liability and reading stress |
| 13 | PMC11208735 (Radiographics) | 2024 | Minimal disruption + DICOM SR dynamic interaction = adoption | Zero extra logins; accept/reject/adjust calipers in native viewer |
| 14 | Parasuraman & Manzey | 2010 | High accuracy increases automation bias | Show confidence + XAI evidence; no punitive override requirements |
| 15 | Liu et al. (Physician AI Handbook) | 2025 | Sequential display preserves independent judgment | Offer my assessment first mode before revealing AI results |
| 16 | EHR Usability Scoping Review | 2025 | 70% of physicians cite usability concerns; audit logs underused | Instrument telemetry (clicks, time-to-accept, override rate) |
| 17 | Scoping Review AI UI Radiology | 2025 | Simple, non-complicated designs preferred over complex UIs | Keep AI panel simple; avoid information density |
| 18 | CLT Education Theory | 2023 | Split-attention principle: integrate info sources | Embed AI results in viewer canvas, not separate side panel/tab |

---

## Top 5 Findings with Direct Quotes / Key Insights

### 1. The 95% Alert Ignore Rate -- Relevance Beats Volume
> *It has been reported that clinicians ignore 95% of these alerts because common, low-priority alerts result in desensitization and loss of trust in the system.* -- PJLSS Systematic Review (2025)

**Insight:** Volume of AI output is the enemy of adoption. Carotis-AI must aggressively filter what it surfaces. A single high-confidence, high-severity finding with an actionable recommendation is worth more than ten low-confidence suggestions. Design for **signal-to-noise ratio**, not feature count.

### 2. Structured Reporting Integration Slashes Reporting Time
> *The average interpretation and reporting time reduced 8.9%-56.1%. In questionnaire survey, 96.9% radiologists considered the workflow of structured reporting with integration of AI was better than the traditional reporting workflow.* -- Wang et al., RSNA 2019

**Insight:** The biggest usability win is not a better viewer -- it is eliminating re-typing. Auto-populating structured report fields with AI-generated measurements and letting radiologists verify (not create) transforms the AI from a reference tool into a workflow accelerator.

### 3. DICOM Structured Reports Enable Dynamic Interaction; Static Captures Do Not
> *Results encoded as DICOM structured reports... allows radiologists to interact with AI results. Radiologists can see a list of indexed pulmonary nodules and accept (yellow arrow) or reject findings. Radiologists may adjust lesion calipers... before accepting.* -- PMC11208735, Radiographics (2024)

**Insight:** Static screenshots of AI results are dead-ends. Machine-readable, interactive formats (DICOM SR) let radiologists correct AI measurements (e.g., adjust stenosis calipers) and feed those corrections back into the report and the learning loop.

### 4. Automation Bias Is a Predictable Cognitive Pattern, Not a Character Failure
> *Automation bias, documented by Parasuraman and Manzey (2010), is the tendency for human operators to rely on automated outputs even when contradictory information is available. The bias is strongest when the automated system has a track record of accuracy -- which, perversely, means that the better the AI system performs, the less likely the human reviewer is to override it.* -- Physician AI Handbook / Automation Bias Analysis (2025)

**Insight:** As Carotis-AI improves, radiologists will trust it more -- and scrutinize it less. The UI must actively combat this: show confidence levels, display Grad-CAM evidence by default, and design the decision-tree capture to record *independent* clinician judgment before AI is revealed.

### 5. Workflow Awareness Is the Defining Factor for Adoption
> *Algorithms are not solutions. Marketplaces, for all their choice and ease of purchase, only provide minimal integration capabilities and accountability, which eventually leads to poor workflow support, low adoption and performance issues. At Aidoc, we have seen where these models break down. Why? Because health systems do not need more algorithms, they require an operating system.* -- Aidoc Blog (2025)

**Insight:** The technical accuracy of the MFSD-UNet model is necessary but insufficient. If Carotis-AI requires radiologists to open a separate app, copy-paste measurements, or manually alert referring physicians, adoption will fail. The product must be a **workflow-native operating system** -- embedded in PACS, integrated with reporting, and connected to care teams.

---

*End of research synthesis. Ready for translation into Carotis-AI design tickets / ADRs.*
