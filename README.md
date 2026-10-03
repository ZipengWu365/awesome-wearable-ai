<div align="center">

# Awesome Wearable AI

**An evidence-aware, machine-readable atlas of wearable and body-sensed intelligence—from sensing and representation learning to causal reasoning, adaptive interventions and closed-loop health systems.**

[![Explore the Interactive Web Atlas](https://img.shields.io/badge/EXPLORE-INTERACTIVE_WEB_ATLAS-2f7f91?style=for-the-badge)](https://zipengwu365.github.io/awesome-wearable-ai/)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Registry CI](https://github.com/ZipengWu365/awesome-wearable-ai/actions/workflows/validate.yml/badge.svg)](https://github.com/ZipengWu365/awesome-wearable-ai/actions/workflows/validate.yml)
[![Accepted](https://img.shields.io/badge/accepted-396-1f6feb)](generated/statistics.json)
[![Models](https://img.shields.io/badge/models-102-8250df)](data/records/models.yaml)
[![Watchlist](https://img.shields.io/badge/watchlist-45-b7791f)](data/excluded/watchlist.yaml)
[![Version](https://img.shields.io/badge/version-v0.3.0-4c1)](CHANGELOG.md)

**Models · Datasets · Digital Measures · Causal Methods · JITAIs · Closed-loop Systems · Standards**

</div>

Research map: [full-repository interactive timeline](site/research-map.html) · [designer handoff and editable assets](assets/research-map/README.md). Every accepted record and watchlist candidate is included, with an [ID-by-ID coverage ledger](assets/research-map/coverage.json), expandable year groups and complete search results.

> **Scope and evidence rule.** Scientific entries must appear in the explicit venue whitelist: SCI/SCIE journals, explicitly whitelisted top journals, top conferences, or domain-leading archival conferences. Official technical reports from major research organizations are allowed. Canonical datasets, standards and research tools use separate official-resource criteria. Pure preprints, workshop-only papers, unresolved publication claims and borderline venues remain in a visible watchlist and are excluded from headline counts.

## What changed in v0.3.0

The earlier package contained only a small seed registry. This release rebuilds the project around **396 accepted records**, **45 screened watchlist candidates**, and **2169 machine-derived or explicit relations**. Counts are generated from the YAML source files during every build; they are not manually typed marketing figures.

## Registry at a glance

| Record type | Accepted records |
|---|---:|
| Models and representation systems | 102 |
| Datasets, cohorts and benchmarks | 116 |
| Causal, counterfactual and adaptive-policy methods | 61 |
| Digital measures and computational phenotypes | 35 |
| Adaptive interventions and closed-loop systems | 40 |
| Tools, platforms, standards and guidance | 42 |

> The **102 model records are not claimed to be 102 foundation models**. They include 84 records explicitly tagged as foundation-model work, plus leading self-supervised representations, sensor-language systems, cross-dataset models and wearable control interfaces. This distinction prevents count inflation through terminology drift.

### Curation depth

| Evidence depth | Records | Interpretation |
|---|---:|---|
| `evidence_card` | 95 | Contribution, limitation and claim boundary were curated from a primary or canonical source. |
| `metadata_verified` | 225 | Core metadata and scope were checked; full methodological appraisal remains pending. |
| `venue_verified` | 76 | Bibliographic and venue eligibility were screened; treat as an index record, not a completed evidence appraisal. |

### Source-verification status

| Verification status | Records |
|---|---:|
| `official_resource_checked` | 153 |
| `primary_source_checked` | 167 |
| `review_reference_checked` | 76 |

## Navigate by research question

- **Which sensor model should I start from?** Read the [model landscape](docs/MODEL_LANDSCAPE.md) and browse [model-family pages](generated/families/index.md).
- **Which dataset can support external validation or population modelling?** Use the [dataset registry](data/records/datasets.yaml), [coverage report](generated/coverage.md), or searchable site.
- **What can a wearable-derived association legitimately support?** Consult the [Evidence Guide](docs/EVIDENCE_GUIDE.md); association, prediction, causal effect, policy value and clinical utility are separate claim layers.
- **How should counterfactual or personalized intervention questions be formulated?** Use the [counterfactual and intervention map](docs/COUNTERFACTUAL_AND_INTERVENTION_MAP.md).
- **How was this literature located and screened?** See the reproducible [search strategy](docs/SEARCH_STRATEGY.md), [inclusion policy](docs/INCLUSION_POLICY.md) and transparent [watchlist](data/excluded/watchlist.yaml).

## Wearable AI lifecycle

```text
Sensing and acquisition
        ↓
Signal quality, calibration and cross-device harmonisation
        ↓
Representation learning and foundation models
        ↓
Digital measures and computational phenotypes
        ↓
Prediction, monitoring and prognosis
        ↓
Causal identification and counterfactual reasoning
        ↓
Policy learning and adaptive intervention design
        ↓
Closed-loop delivery, clinical utility, safety and governance
```

## Sensor and model landscape

A single `sensor model` category hides major differences in signal physics, annotation, time scale, supervision and clinical use. The registry currently separates eleven model families:

| Family | Count |
|---|---:|
| Motion / IMU models and representations | 12 |
| PPG and optical physiology | 3 |
| ECG and cardiac sensing | 15 |
| EEG, MEG and neural foundation models | 14 |
| EMG and neuromotor interfaces | 3 |
| Sleep and polysomnography | 4 |
| CGM and metabolic sensing | 2 |
| Respiratory and acoustic sensing | 2 |
| Multimodal physiological models | 10 |
| Sensor-language models and agents | 15 |
| General time-series enablers | 22 |

| Resource | Year | Venue/source | Family | Evidence boundary |
|---|---:|---|---|---|
| [A Foundation Model for Continuous Glucose Monitoring Data](https://www.nature.com/articles/s41586-025-09925-9) | 2026 | Nature | `cgm-metabolic-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [A Multimodal Sleep Foundation Model for Disease Prediction](https://www.nature.com/articles/s41591-025-04133-4) | 2026 | Nature Medicine | `sleep-psg-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [A Unified Time-Frequency Foundation Model for Sleep Decoding](https://www.nature.com/articles/s41467-025-67970-4) | 2026 | Nature Communications | `sleep-psg-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Cardiac Health Assessment across Scenarios and Devices Using a Multimodal Foundation Model Pretrained on Data from 1.7 Million Individuals](https://www.nature.com/articles/s42256-026-01180-5) | 2026 | Nature Machine Intelligence | `ecg-cardiac-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [GlucoFM: A Foundation Model for Continuous Glucose Monitoring](https://research.google/blog/glucofm-a-foundation-model-for-continuous-glucose-monitoring/) | 2026 | Google Research | `cgm-metabolic-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [High-Performance Self-Supervised Learning by Joint Training of Flow Matching](https://proceedings.mlr.press/v300/ukita26a.html) | 2026 | AISTATS | `motion-imu-foundation-models` | This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention. |
| [Insulin Resistance Prediction from Wearables and Routine Blood Biomarkers](https://www.nature.com/articles/s41586-026-10179-2) | 2026 | Nature | `multimodal-physiological-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [PhysioJEPA: Joint Embedding Representations of Physiological Signals for Real Time Risk Estimation in the Intensive Care Unit](https://proceedings.mlr.press/v297/fox26a.html) | 2026 | CHIL | `multimodal-physiological-models` | This is representation-learning or predictive evidence. It does not establish that a sensor-derived prediction is a causal treatment effect, clinically useful decision rule, or safe deployed intervention. |
| [TimesFM-3: A Zero-Shot Foundation Model for Multivariate Forecasting](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/) | 2026 | Google Research | `general-time-series-enablers` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Toward Foundation Models for Multivariate Wearable Sensing of Physiological Signals](https://doi.org/10.1145/3803808) | 2026 | Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies | `multimodal-physiological-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Towards a General Intelligence and Interface for Wearable Health Data](https://research.google/blog/sensorfm-towards-a-general-intelligence-and-interface-for-wearable-health-data/) | 2026 | Google Research | `multimodal-physiological-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Transforming Wearable Data into Personal Health Insights Using Large Language Model Agents](https://www.nature.com/articles/s41467-025-67922-y) | 2026 | Nature Communications | `sensor-language-agents` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Wearable Optomyography Enables Continuous Neuroprosthetic Control](https://www.nature.com/articles/s41598-025-32646-y) | 2026 | Scientific Reports | `emg-neuromotor-models` | This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness. |
| [A Criss-Cross Brain Foundation Model for EEG Decoding](https://openreview.net/forum?id=NPNUHgHF2w) | 2025 | ICLR | `eeg-neural-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [A Generic Noninvasive Neuromotor Interface for Human-Computer Interaction](https://www.nature.com/articles/s41586-025-09255-w) | 2025 | Nature | `emg-neuromotor-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [A Hybrid EMG–EEG Interface for Robust Intention Detection and Fatigue-Adaptive Control of an Elbow Rehabilitation Robot](https://www.nature.com/articles/s41598-025-24831-w) | 2025 | Scientific Reports | `emg-neuromotor-models` | This record supports a representation, recognition, sensing or control-system claim under the reported evaluation. It does not by itself establish clinical benefit, causal treatment effect, safety, transportability or regulatory readiness. |
| [An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains](https://doi.org/10.1056/AIoa2401033) | 2025 | NEJM AI | `ecg-cardiac-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |
| [Beyond Sensor Data: Foundation Models of Behavioral Data from Wearables Improve Health Predictions](https://openreview.net/forum?id=DtVVltU1ak) | 2025 | ICML | `motion-imu-foundation-models` | This is representation or predictive-model evidence. It does not by itself establish a causal treatment effect, clinical benefit, safety, or regulatory readiness. |

The README shows only recent representative records. The complete source of truth is [models.yaml](data/records/models.yaml), and every accepted family receives a generated page under [generated/families](generated/families/index.md).

## Adaptive intervention and closed-loop evidence

The intervention registry contains **40 accepted records**, including **14 records explicitly marked as negative, null or materially mixed**. Protocols, proximal-effect analyses, randomized clinical outcomes and deployed closed-loop systems are kept distinct. A protocol is not effectiveness evidence; a model counterfactual is not a causal treatment effect.

| Resource | Year | Venue/source | Family | Evidence boundary |
|---|---:|---|---|---|
| [A Digital Platform with Activity Tracking for Energy Management Support in Long COVID: A Randomised Controlled Trial](https://www.nature.com/articles/s41467-025-64831-y) | 2026 | Nature Communications | `jitai-behavioral-interventions` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [A Randomized Trial of a Digitally Delivered, Home-Based Neuromodulation and Mindfulness Intervention for Pain Management in Older Adults with Knee Osteoarthritis](https://www.nature.com/articles/s41746-026-02577-7) | 2026 | npj Digital Medicine | `closed-loop-and-home-neuromodulation` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [An Umbrella Review of Systematic Reviews of the Impact of Wrist-Worn Wearables on Health Outcomes](https://doi.org/10.1152/physrev.00049.2024) | 2026 | Physiological Reviews | `wearable-feedback-evidence-synthesis` | Evidence synthesis estimates average effects over included studies and does not establish effectiveness for every device, population or intervention design. |
| [A Randomized Controlled Trial of a Digital Lifestyle Intervention Involving Postoperative Patients with Colorectal Cancer](https://www.nature.com/articles/s41746-025-01716-w) | 2025 | npj Digital Medicine | `remote-monitoring-and-clinical-escalation` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [An Adaptive AI-Based Virtual Reality Sports System for Adolescents with Excess Body Weight: A Randomized Controlled Trial](https://www.nature.com/articles/s41591-025-03724-5) | 2025 | Nature Medicine | `adaptive-rehabilitation-and-exercise` | The reported effect is tied to the randomized intervention, comparator, population, follow-up and endpoint; it should not be generalized to other devices or care pathways without new evidence. |
| [Closed-Loop Vagus Nerve Stimulation Aids Recovery from Spinal Cord Injury](https://www.nature.com/articles/s41586-025-09028-5) | 2025 | Nature | `responsive-neurostimulation` | The reported effect is tied to the randomized intervention, comparator, population, follow-up and endpoint; it should not be generalized to other devices or care pathways without new evidence. |
| [Comparative Effectiveness of Remote Perioperative Telemonitoring in Cancer Surgery: A Randomized Trial](https://www.nature.com/articles/s41746-025-01961-z) | 2025 | npj Digital Medicine | `remote-monitoring-and-clinical-escalation` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Effects of Physical Activity-Promoting Wearable Devices on Blood Pressure in Adults: A Systematic Review and Meta-Analysis](https://www.nature.com/articles/s41440-025-02260-6) | 2025 | Hypertension Research | `wearable-feedback-evidence-synthesis` | Evidence synthesis estimates average effects over included studies and does not establish effectiveness for every device, population or intervention design. |
| [Human-Centred Design and Fabrication of a Wearable Multimodal Visual Assistance System](https://www.nature.com/articles/s42256-025-01018-6) | 2025 | Nature Machine Intelligence | `assistive-wearable-systems` | Participant experiments support system feasibility and usability but do not establish population-level clinical benefit. |
| [Human-Machine Co-Adaptation to Automated Insulin Delivery: A Randomised Clinical Trial Using Digital Twin Technology](https://www.nature.com/articles/s41746-025-01679-y) | 2025 | npj Digital Medicine | `automated-insulin-delivery` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Physical Activity and Diet Just-in-Time Adaptive Intervention to Reduce Blood Pressure: A Randomized Controlled Trial](https://www.nature.com/articles/s41746-025-01844-3) | 2025 | npj Digital Medicine | `jitai-behavioral-interventions` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Randomized Controlled Study of a Digital Data-Driven Intervention for Depressive and Generalized Anxiety Symptoms](https://www.nature.com/articles/s41746-025-01511-7) | 2025 | npj Digital Medicine | `jitai-behavioral-interventions` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Telehealth Virtual Reality Intervention Reduces Chronic Pain in a Randomized Crossover Study](https://www.nature.com/articles/s41746-025-01553-x) | 2025 | npj Digital Medicine | `digital-rehabilitation-and-pain` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Utilization of Telemedicine in Conjunction with Wearable Devices for Patients with Chronic Musculoskeletal Pain: A Randomized Controlled Clinical Trial](https://www.nature.com/articles/s41598-024-85056-x) | 2025 | Scientific Reports | `digital-rehabilitation-and-pain` | The reported effect is tied to the randomized intervention, comparator, population, follow-up and endpoint; it should not be generalized to other devices or care pathways without new evidence. |
| [A Randomized Clinical Trial Testing Digital Mindset Intervention for Knee Osteoarthritis Pain and Activity Improvement](https://www.nature.com/articles/s41746-024-01281-8) | 2024 | npj Digital Medicine | `digital-rehabilitation-and-pain` | Randomization supports the specified trial estimand, but it does not validate every algorithmic component, subgroup policy or future deployment configuration. |
| [Efficacy and Safety of Using Auditory-Motor Entrainment to Improve Walking after Stroke: A Multi-Site Randomized Controlled Trial of InTandem](https://www.nature.com/articles/s41467-024-44791-5) | 2024 | Nature Communications | `adaptive-rehabilitation-and-exercise` | The reported effect is tied to the randomized intervention, comparator, population, follow-up and endpoint; it should not be generalized to other devices or care pathways without new evidence. |
| [Overground Gait Training With a Wearable Robot in Children With Cerebral Palsy: A Randomized Clinical Trial](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2821278) | 2024 | JAMA Network Open | `wearable-robotics-and-assistance` | The reported effect is tied to the randomized intervention, comparator, population, follow-up and endpoint; it should not be generalized to other devices or care pathways without new evidence. |
| [Soft Robotic Apparel to Avert Freezing of Gait in Parkinson's Disease](https://www.nature.com/articles/s41591-023-02731-8) | 2024 | Nature Medicine | `wearable-robotics-and-assistance` | Repeated within-person effects are compelling mechanistic evidence for this participant but cannot establish population-level effectiveness. |

## Counterfactual reasoning: four non-equivalent meanings

| Layer | Question | Evidence required |
|---|---|---|
| Predictive counterfactual | What input change flips a model output? | Model-behaviour validation; no treatment-effect claim. |
| Causal counterfactual | What would happen under a different action? | Identification assumptions, randomization, or defensible causal design. |
| Policy counterfactual | What would a different sequential policy achieve? | Online trial or reliable off-policy evaluation with overlap and uncertainty checks. |
| Generative / digital-twin counterfactual | Can an individual trajectory be simulated under intervention? | Calibration, interventional validity, external validation and prospective utility evidence. |

## Machine-readable structure

```text
data/records/          # accepted source-of-truth records
data/excluded/         # transparent watchlist and exclusion reasons
data/venues.yaml       # venue and source eligibility policy
data/concepts.yaml     # controlled vocabularies
data/relations.yaml    # explicit cross-record links
schema/                # JSON Schemas
generated/             # JSON, CSV, statistics, family pages and coverage
site/                  # dependency-free searchable atlas
scripts/               # validation, export, rendering, audit and site generation
```

Build locally:

```bash
python -m pip install -r requirements.txt
make build
make test
make audit
```

## Coverage boundary

This release is intentionally broad but does **not** claim PRISMA-level exhaustive retrieval. It prioritizes source quality and transparent curation depth. Known gaps, unresolved venues and candidate preprints are documented in [COVERAGE_LIMITS.md](docs/COVERAGE_LIMITS.md) and [watchlist.yaml](data/excluded/watchlist.yaml). Venue prestige is an inclusion filter, not evidence of clinical validity.

## Contributing

Use the issue templates or submit a PR. Every scientific proposal must provide a version-of-record URL, venue, year, inclusion basis, concise contribution, limitation and evidence boundary. Watchlist promotion requires resolving the recorded exclusion reason. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation and license

Please cite the original papers, datasets and standards directly. Repository citation metadata are in [CITATION.cff](CITATION.cff). Repository code and text use [LICENSE](LICENSE); linked resources retain their own licenses and access conditions.
