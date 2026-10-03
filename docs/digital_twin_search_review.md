> Imported from the local v1.2 research notes. Historical local counts and paths describe that source package. Current accepted/watchlist placement and ID mapping are documented in [the migration guide](LOCAL_SYNC.md); profile data live in [data/profiles](../data/profiles/).

# Digital-twin search and source-review log

Snapshot: 2026-09-28. Targeted incremental update to v1.1.0; not a systematic or exhaustive review.

## Search families

- Wearable / human digital twin + sensors, personalization, online updating, state estimation.
- Cardiovascular digital twin + Windkessel, bioimpedance, coronary hemodynamics.
- Wearable digital twin + gait, musculoskeletal modeling, bone stress, rehabilitation.
- Digital twin + CGM, ReplayBG, insulin, exercise support, trial replay, randomized trial.
- Digital twin + hydration, respiratory signals, bladder bioimpedance, synthetic data.
- Mobile-health / HeartSteps + digital twin, subpopulation simulator, JITAI.

Primary publisher/proceedings pages and PubMed/PMC were used for inclusion. Secondary pages only supplied discovery leads. Search ranking was not used as evidence of methodological quality.

## Review depth

| Scope | Profiles |
| --- | --- |
| abstract_and_open_reviews | 1 |
| abstract_metadata | 4 |
| primary_sections | 13 |
| prior_version_annotation | 4 |

Scope includes 18 new publication profiles and 4 preserved-v1.1 connections. The hydration-paper author list, some code availability and exact refresh intervals remain unknown because they were not captured in the checked source. No clinical data or paywalled article text is redistributed.

## Included publications

| ID | Source | Review scope |
| --- | --- | --- |
| paper-dt-body-roadmap | [A roadmap for the development of human body digital twins](https://www.nature.com/articles/s44287-024-00025-w) | abstract_metadata |
| paper-dt-health-scoping | [Digital twins for health: a scoping review](https://www.nature.com/articles/s41746-024-01073-0) | primary_sections |
| paper-dt-wearables-review | [Digital Twins for Healthcare Using Wearables](https://pmc.ncbi.nlm.nih.gov/articles/PMC11200512/) | primary_sections |
| paper-dt-nmsk-framework | [A Digital Twin Framework for Precision Neuromusculoskeletal Health Care: Extension Upon Industrial Standards](https://doi.org/10.1123/jab.2023-0114) | primary_sections |
| paper-dt-lhmf | [Establishing the longitudinal hemodynamic mapping framework for wearable-driven coronary digital twins](https://www.nature.com/articles/s41746-024-01216-3) | primary_sections |
| paper-dt-wpinn | [Cardiovascular digital twins using a Windkessel physics informed neural network](https://www.nature.com/articles/s41746-026-02610-9) | primary_sections |
| paper-dt-gait-lab | [A wearable gait lab powered by sensor-driven digital twins for quantitative biomechanical analysis post-stroke](https://www.cambridge.org/core/journals/wearable-technologies/article/wearable-gait-lab-powered-by-sensordriven-digital-twins-for-quantitative-biomechanical-analysis-poststroke/05C0872598A6602725105FA6EFE3C2EE) | primary_sections |
| paper-dt-bone-stress | [Integrating personalized shape prediction, biomechanical modeling, and wearables for bone stress prediction in runners](https://www.nature.com/articles/s41746-025-01677-0) | primary_sections |
| paper-dt-bladder-electrodes | [Digital twin driven electrode optimization for wearable bladder monitoring via bioimpedance](https://pmc.ncbi.nlm.nih.gov/articles/PMC11782588/) | primary_sections |
| paper-dt-replaybg | [ReplayBG: A Digital Twin-Based Methodology to Identify a Personalized Model From Type 1 Diabetes Data and Simulate Glucose Concentrations to Assess Alternative Therapies](https://pubmed.ncbi.nlm.nih.gov/37368794/) | abstract_metadata |
| paper-dt-uva-replay-validation | [Validation of the UVA Simulation Replay Methodology Using Clinical Data: Reproducing a Randomized Clinical Trial](https://journals.sagepub.com/doi/10.1089/dia.2023.0595) | abstract_metadata |
| paper-dt-exercise-dss | [Design and In Silico Evaluation of an Exercise Decision Support System Using Digital Twin Models](https://journals.sagepub.com/doi/10.1177/19322968231223217) | primary_sections |
| paper-dt-studia | [A digital twin-enhanced decision support system improves time-in-range in type 1 diabetes: a randomized clinical trial](https://www.nature.com/articles/s41598-025-23165-x) | primary_sections |
| paper-dt-replaybg-web | [ReplayBG-Web: A Novel Web Interface to Ease the Creation and Use of Digital Twins for Type 1 Diabetes](https://journals.sagepub.com/doi/10.1177/19322968261481540) | abstract_metadata |
| paper-dt-nurse-pdt | [Human-in-the-loop AI predictive digital twin to extend virtual precision diabetes care between visits](https://www.nature.com/articles/s44401-026-00118-8) | primary_sections |
| paper-dt-synthetic-sharing | [Medical data sharing and synthetic clinical data generation – maximizing biomedical resource utilization and minimizing participant re-identification risks](https://www.nature.com/articles/s41746-025-01935-1) | primary_sections |
| paper-dt-hydration | [Multi-modal human digital twin for hydration](https://www.sciencedirect.com/science/article/pii/S2666518226000185) | primary_sections |
| paper-dt-lung | [Digital Twin of the Lung from Wearable Biosignals for Real-Time Respiratory Monitoring](https://papers.miccai.org/miccai-2026/0280-Paper5574.html) | abstract_and_open_reviews |

## Deliberate boundaries

- The existing AID digital-twin study remains one canonical paper. ReplayBG and ReplayBG-Web are distinct publications in a shared lineage, not two independent clinical trials.
- Synthetic data analogues are separately tagged and do not inflate an implemented-personal-twin count.
- Framework papers remain framework evidence; broad non-wearable healthcare branches were not imported wholesale.
- Commercial marketing pages without a verified primary study are not accepted as evidence of performance or clinical benefit.
- Planned trials, source-code availability claims and prospective deployments were not promoted to completed validation.
- JITAI-Twins (arXiv:2607.21403) remains a separate preprint candidate. The official arXiv page does not supply a verified archival venue in this pass.

## Known limits

This pass did not reproduce model code, acquire patient data, perform a formal risk-of-bias assessment, adjudicate every statistical claim or systematically test all external links. Direct source-page fetches sometimes failed; publisher-indexed text was used where available and the relevant source note specifies the examined content. An unreachable page does not imply a nonexistent paper.

## Follow-up curation contract

Prioritize missing primary metadata, direct same-person modality linkage, update cadence, uncertainty treatment, held-out evaluation and action support. Correct unclear claims through a sourced migration; do not silently change historical profiles. Automated discovery produces candidates only.
