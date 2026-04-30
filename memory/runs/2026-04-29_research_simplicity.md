---
name: 2026-04-29_research_simplicity
type: run
---

# Research Review: Simplicity in Medical AI Software

**Date:** 2026-04-29
**Topic:** UI/UX Simplicity and Architectural Simplicity in Medical AI
**Sources consulted:** 12+ peer-reviewed and industry sources

---

## Executive Summary

1. **Cognitive burden, not speed, is the primary bottleneck in radiology.** A 2025 survey across 8 institutions found that radiologists experience a **60% reduction in cognitive burden** when using well-integrated AI tools that automate repetitive microtasks and unify fragmented workflows (RapidAI, 2025). The equation is simple: mental strain + workflow friction = cognitive burden.

2. **Visual adjacency and low-density explanations outperform dense information displays.** A Frontiers in Neuroscience study (2022) confirmed that adjacent, low "mental computation" (MC) visualizations produced the highest user confidence and lowest cognitive load — counterintuitively, high-density explanations reduced trust and increased mental demand.

3. **Monolithic and "modulithic" architectures are strongly favored for early-stage medical AI.** Multiple sources converge on starting with a modular monolith for clinical AI proof-of-concepts, prioritizing observability, debuggability, and data sovereignty over distributed complexity (Oxford RAG dissertation, 2025; Thinkitive, 2026).

4. **Complex UIs measurably increase medical errors.** Nearly 70% of physicians in surveyed hospitals struggled to find critical information due to information overload. Simplified interfaces with clear visual hierarchy reduce medication errors, data entry mistakes, and perceptual misses (SaaS Factor, 2026; FuseLab, 2023).

5. **XAI explanations can trigger information overload and overreliance.** The "transparency-comprehension paradox" means that overly detailed explanations (e.g., 30 SHAP plots) obscure more than they reveal. Progressive disclosure and plain-language summaries outperform raw technical explainability for clinical users (UCL, 2022; PMC, 2024; arXiv, 2025).

---

## 1. UI Simplicity for Radiologists: The Cognitive Load Evidence

### The Core Finding
Radiologists consistently report that "it's not the reading, it's everything around the reading" — app switching, manual measurements, alert fatigue, and fragmented PACS/EHR workflows compound into unsustainable cognitive load (RapidAI, 2025). Nearly 40% of radiologists express desire to leave the profession due to sustained cognitive overload.

### What Makes an AI Tool "Simple Enough"
- **Workflow integration over feature count:** Patel et al. (2021) found that poorly integrated AI tools *increase* cognitive load and interrupt diagnostic processes, negating efficiency gains.
- **Automation of microtasks:** AI that handles lesion tracking, volumetric measurements, and longitudinal comparisons allows radiologists to focus on interpretation rather than manual preparation.
- **Unified workspace:** Eliminating toggling between PACS, reporting tools, and communication platforms is the single biggest lever for reducing mental switching costs.
- **PACS-native integration:** AI tools embedded directly into the PACS viewer — rather than standalone apps — achieve significantly higher adoption and lower time-to-decision (RSNA, 2020; ScienceDirect review, 2025).

### Time-to-Decision Data
- AI-enhanced PACS reduced diagnostic times by up to **90%** for critical conditions like intracranial hemorrhages (ScienceDirect review, 2025).
- NLP-based reporting tools reduced radiology reporting times by **30–50%** while improving consistency.
- AI-assisted screening workflows achieved up to **50% workload reduction** without loss of diagnostic integrity (WOS-EMR, 2025).

---

## 2. Decision Support UI Patterns

### Key Evidence

| Pattern | Evidence | Implementation Effort |
|---------|----------|----------------------|
| **Adjacent, low-density visual overlays** (e.g., bounding boxes directly on image) | Frontiers study (2022): adjacent EVs significantly outperformed non-adjacent ones; low-MC visualizations produced highest confidence and lowest cognitive load. | Low — native canvas overlays in DICOM viewer |
| **Progressive disclosure** (summary first, details on demand) | arXiv (2025): experts described raw XAI outputs as "complete information overload"; progressive disclosure emerged as the preferred solution. | Medium — requires structured response schemas |
| **Confidence scores with calibrated thresholds** (e.g., ≥90% = high, <90% = low) | arXiv breast-cancer study (2025): dichotomized confidence scores reduced mental demand and stress vs. raw probability distributions. | Low — simple UI badge/color coding |
| **Actionable insight cards** (not raw probability lists) | Physician AI Handbook (2025): presenting actionable insights (highlighted abnormalities + clear recommendation) reduces cognitive load vs. raw data. | Medium — requires NLP/structured output pipeline |
| **Smart triage / worklist prioritization** | Multiple studies: automated triage of critical findings (ICH, LVO) to the top of the worklist improves turnaround time and reduces missed findings. | Medium — integration with RIS/PACS worklist |
| **Two-click rule** for any AI interaction | Physician AI Handbook: every additional click reduces compliance; ideal AI tasks require ≤2 clicks. | Low — UX constraint, no new tech |
| **Graceful degradation** (UI works even if AI fails) | Physician AI Handbook: workflows must continue seamlessly if the AI service is unavailable. | Medium — requires fallback UI states |

### Anti-Patterns to Avoid in Decision Support UI
- **Raw probability dumps:** Long lists of classification probabilities increase cognitive load without improving decisions.
- **Non-adjacent explanations:** Explanations in side panels or separate windows disrupt visual attention and reduce confidence.
- **Alert fatigue:** Excessive false positives force radiologists to develop filter habits that cause important findings to be skipped (HealthManagement, 2026).
- **Opaque confidence presentation:** Un-calibrated or missing confidence scores reduce appropriate trust calibration.

---

## 3. Software Architecture Simplicity

### The Consensus: Start Simple, Stay Observable
Multiple 2025–2026 architecture reviews for healthcare systems converge on a clear recommendation: **begin with a modular monolith**, not microservices, unless you have >10 developers and proven product-market fit.

### Monolith vs. Microservices in Medical AI

| Factor | Monolithic / Modular Monolith | Microservices |
|--------|------------------------------|---------------|
| **Initial development speed** | Faster — single codebase, no distributed complexity | Slower — service boundaries, inter-service communication |
| **Debuggability** | Centralized logs, single process, easier tracing | Requires distributed tracing, service mesh, mature DevOps |
| **Data sovereignty / Local-First** | Easier — single SQLite/PostgreSQL instance, no network egress | Harder — inter-service communication increases attack surface |
| **AI integration flexibility** | Tightly coupled; model updates require full redeploy | AI services can be updated independently |
| **Operational overhead** | Low — suitable for small teams | High — demands container orchestration, monitoring |
| **Regulatory validation (MDR/FDA)** | Simpler — single validation artifact | Complex — each service may require separate validation |
| **Best for** | Early-stage clinical AI, edge deployment, small teams | Large hospital networks, multi-tenant SaaS, >15 devs |

### Local-First as an Architectural Simplicity Pattern
The Oxford RAG dissertation (2025) explicitly validated local-first architecture for clinical AI prototypes:
- **Privacy:** Patient data never leaves the device; eliminates HIPAA/GDPR cloud-complexity.
- **Latency:** Local inference removes network round-trips.
- **Simplicity:** SQLite + single-process monolith enabled deep observability and rapid iteration.
- **Trade-off:** Horizontal scalability is sacrificed. For single-clinic or edge deployments, this is acceptable.

### Key Architectural Recommendations
1. **Use a modular monolith** with clear internal boundaries (a "modulith") to enable future extraction without distributed-system complexity.
2. **Keep AI inference as a local service** (ONNX Runtime, edge GPU) to avoid cloud dependency and maintain data sovereignty.
3. **SQLite is sufficient** for single-user or small-clinic deployments; avoid premature migration to client-server databases.
4. **Modular adapter layers** for external APIs allow future substitution with local models without architectural rewrite.
5. **Observability > Scalability** in early phases: structured logging and evaluation-driven development matter more than horizontal scaling.

---

## 4. Error Prevention Through Simplicity

### The Evidence Base
- **70% of physicians** at surveyed Midwestern hospitals had difficulty finding needed information due to information overload (SaaS Factor, 2026).
- Poorly designed EHR interfaces directly contribute to medication errors, data entry mistakes, and diagnostic delays (FuseLab, 2023).
- Minimalist GUI design in medical devices is explicitly linked to **faster decision-making, fewer user errors, and better patient safety** (Creanova, 2025).

### How Simplicity Reduces Errors
1. **Visual hierarchy:** Critical alerts at the top, active problems below, administrative data at the bottom. Screens should reflect the order in which clinicians actually need things.
2. **Reduced clicks:** Every additional click reduces compliance and increases error risk. The "two-click rule" should govern AI interactions.
3. **Distinct formatting:** Drug names, dosing values, and units must be readable at a glance. Consistent formatting prevents interpretation errors.
4. **Color + shape + text:** Never rely on color alone — red-green color blindness affects ~8% of male clinicians.
5. **Smart defaults:** Pre-populated fields and intelligent defaults reduce data entry burden and manual transcription errors.
6. **Minimalism:** Strip out anything that does not serve the immediate clinical task. Administrative metadata should not compete for attention on diagnostic screens.

---

## 5. The "Less is More" Paradox: When XAI Explanations Harm

### The Core Paradox
As AI models grow more sophisticated, transparency efforts often fail to enhance human comprehension. This is the **complexity-comprehension paradox**: explaining complex models requires simplification, but simplification inevitably sacrifices the ability to capture complex relationships (Lancashire, 2026).

### Evidence That More Explanation Can Hurt
1. **Information overload in XAI:** UCL research (2022) found that "the more detailed the explanation, the less useful and trustworthy it was considered to be." Non-numerical explanations in plain English outperformed SHAP models for non-technical users.
2. **Overwhelmed and angry:** Experts receiving "30 plots slapped down from XAI" reported being "overwhelmed and angry at the AI, and then I don't trust it either way" (arXiv, 2025).
3. **Cognitive overreliance:** A PMC study (2024) of 41 medical practitioners found that some explanation types increased cognitive overreliance on AI — providers were more inclined to accept AI recommendations when accompanied by explanations, even when the recommendations were wrong.
4. **XAI doesn't explain like radiologists:** UC Merced research found that radiology practitioners explain impressions in levels of increasing abstraction, sensitive to the explainee's knowledge. Current XAI heatmaps "give no guidance on how to attend to features, how to make sense of the relations between features, and what features mean in the larger clinical context."
5. **Long explanations get skipped:** The PMC study noted that "long and redundant explanations make participants skip them" — defeating the purpose of transparency.

### When to Show Less
- **High time pressure:** Emergency decisions (stroke, trauma) cannot accommodate lengthy explanations.
- **High model confidence:** When AI confidence is ≥90%, a simple highlight or one-sentence rationale suffices.
- **Expert users performing routine tasks:** Experienced radiologists need triage, not tutorials.
- **Cognitive fatigue periods:** Late in shifts, explanations increase rather than reduce mental demand.

### When to Show More
- **Low confidence predictions:** Uncertain cases warrant deeper inspection.
- **Training / educational contexts:** Residents and students benefit from detailed explanations.
- **Novel or rare pathologies:** Unusual findings require richer context to build appropriate mental models.
- **Discrepancy cases:** When AI and radiologist disagree, detailed explanation supports reconciliation.

### Design Principle: Progressive Disclosure
The evidence consistently supports **progressive disclosure** as the resolution:
- **Level 1:** Visual highlight on image (lowest cognitive load).
- **Level 2:** One-sentence plain-language rationale (e.g., "Stenosis indicated by calcified plaque at bifurcation").
- **Level 3:** Confidence score + key metrics.
- **Level 4 (on demand):** Full Grad-CAM/SHAP visualization + technical details.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Source Evidence |
|--------------|-------------|-----------------|
| **Standalone AI apps** requiring separate login/PACS toggling | Increases cognitive load, disrupts workflow, reduces adoption | Patel et al. (2021); RapidAI (2025) |
| **Raw probability lists / SHAP dumps** | Information overload; less trustworthy than simple explanations | UCL (2022); arXiv (2025) |
| **Non-adjacent explanations** (side panels, pop-ups) | Breaks visual attention; lower confidence and higher cognitive load | Frontiers in Neuroscience (2022) |
| **Microservices for small teams / early stage** | Operational complexity distracts from clinical validation; harder to debug | Thinkitive (2026); GetDX (2025) |
| **Color-only coding** for critical alerts | Excludes colorblind users; increases error risk | SaaS Factor (2026); Creanova (2025) |
| **Alert fatigue** from excessive false positives | Clinicians develop filtering habits; important findings get skipped | HealthManagement (2026) |
| **Forced workflow changes** | "Technology adapts to users, not users to technology" — every disruption reduces adoption | Physician AI Handbook (2025) |
| **Overselling XAI transparency** | Creates false confidence; explanations can be misleading or persuasive in unpredictable ways | UCL (2022); PMC (2024) |

---

## Sources

1. RapidAI. (2025). *Radiology's real challenge isn't speed, it's cognitive burden.* https://www.rapidai.com/blog/radiologys-real-challenge-isnt-speed-its-cognitive-burden
2. Müller et al. (2022); Patel et al. (2021). Cited in: *Integrating Ultrasound into Clinical Practice* (2025). https://impactfactor.org/PDF/IJDDT/16/IJDDT,Vol16,Issue11s,Article85.pdf
3. Frontiers in Neuroscience. (2022). *The Impact of Visualizing Artificial Intelligence Decisions.* https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.883385/full
4. arXiv. (2025). *Explainability and AI Confidence in Clinical Decision Support Systems: Effects on Trust, Diagnostic Performance, and Cognitive Load in Breast Cancer Care.* https://arxiv.org/html/2501.16693v1
5. Physician AI Handbook. (2025). *Integration into Clinical Workflow — Human Factors Engineering for AI.* https://physicianaihandbook.com/implementation/workflow.html
6. HealthManagement.org. (2026). *AI Decision Support Faces Adoption Barriers in Radiology.* https://healthmanagement.org/c/imaging/News/ai-decision-support-faces-adoption-barriers-in-radiology
7. Thinkitive. (2026). *EHR Software Architecture Comparison: Microservices vs Monolithic.* https://www.thinkitive.com/blog/microservices-vs-monolithic-architecture-for-ehr-development/
8. Digicleft Solutions. (2026). *Microservices vs Monolithic for EHR.* https://digicleftsolutionsllc.com/architecture-which-best-ehr-development/
9. GetDX. (2025). *Monolithic vs microservices architecture: When to choose each approach.* https://getdx.com/blog/monolithic-vs-microservices/
10. Meleka, M. (2025). *Retrieval-Augmented AI Assistants for Healthcare: System Design and Evaluation.* University of Oxford. https://ora.ox.ac.uk/objects/uuid:9add0c17-f4fe-4051-9a2a-027f8818a5aa
11. SaaS Factor. (2026). *User Interface Design for Healthcare Applications.* https://www.saasfactor.co/blogs/user-interface-design-for-healthcare-applications
12. FuseLab Creative. (2023). *EHR Interface Design Principles, UX, And Usability Challenges.* https://fuselabcreative.com/ehr-interface-design-principles-ux-and-usability-challenges/
13. Creanova. (2025). *GUI Trends in Medical Devices.* https://creanova.com/2025/09/19/gui-graphic-user-interface-trends-in-medical-devices-how-interfaces-are-evolving/
14. UCL / Discovery. (2022). *Human-AI Interaction Paradigm for Evaluating Explainable Artificial Intelligence.* https://discovery.ucl.ac.uk/id/eprint/10195997/1/Evaluatory%20XAI.pdf
15. arXiv. (2025). *Experts on XAI overload and progressive disclosure.* https://arxiv.org/pdf/2508.06352
16. PMC / NCBI. (2024). *How Explainable Artificial Intelligence Can Increase or Decrease Trust.* https://pmc.ncbi.nlm.nih.gov/articles/PMC11561425/
17. UC Merced / eScholarship. (2024). *Inadequacies of Explainable AI for Radiological Interpretations.* https://escholarship.org/content/qt9p24077n/qt9p24077n.pdf
18. Lancashire / Shared Minds. (2026). *The Cognitive Parallels Between Humans and AI — complexity-comprehension paradox.* https://knowledge.lancashire.ac.uk/id/eprint/58705/
19. RSNA. (2020). *Integrating AI with PACS Key to Improving Workflow Efficiency.* https://www.rsna.org/news/2020/march/integrating-ai-with-pacs
20. ScienceDirect / Current Medical Imaging. (2025). *Transforming Medical Imaging: The Role of AI Integration in PACS.* https://www.sciencedirect.com/org/science/article/pii/S1573405625000670
21. WOS-EMR / Data Science. (2025). *AI-driven workload reduction in radiology.* https://www.wos-emr.net/

---

## Implications for Carotis-AI

1. **UI:** Keep the DICOM viewer integration tight — Grad-CAM overlays must be adjacent (on-image), not side-panel. Default to low-density explanation (highlight + 1-sentence rationale). Full SHAP only on explicit user request.
2. **Confidence presentation:** Use a simple dichotomized badge (high/low) rather than raw probability distributions.
3. **Architecture:** The current modular monolith (FastAPI + SQLite + local ONNX) is the right choice for P0–P3. Resist microservices until multi-clinic deployment is proven necessary.
4. **Error prevention:** Apply the "two-click rule" — any AI insight must be reachable in ≤2 clicks from the main viewer.
5. **XAI design:** Implement progressive disclosure (Level 1–4) from day one. The default view should be as simple as possible; technical explanations are opt-in.
