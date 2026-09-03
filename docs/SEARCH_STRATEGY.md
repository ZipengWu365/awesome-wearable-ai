# Search and screening strategy

## Objective

Build a broad, evidence-aware map of wearable AI while enforcing a strict core-publication policy. This is a structured scoping search, not a PRISMA systematic review.

## Source families screened

1. Official proceedings and journal pages for ICLR, ICML, NeurIPS, AAAI, KDD, UbiComp/IMWUT, ISWC, CHIL, MIDL, ISBI and related whitelisted venues.
2. Nature Portfolio, NEJM/NEJM AI, JAMA, BMJ, Lancet-family and other SCI/SCIE journals listed in `data/venues.yaml`.
3. Official Google Research, Apple Machine Learning Research and other major-lab technical reports.
4. Canonical repositories and portals for datasets, cohorts, standards, regulators and research software.
5. Field-specific review/reference lists used only to discover candidates; scientific promotion still requires an eligible publication identity.

## Concept blocks

### Sensor and foundation models

- wearable, sensor, biosignal and physiological foundation model;
- IMU, accelerometer, motion, ECG, PPG, EEG, MEG, EMG, EOG, PSG, CGM, respiratory audio, radar and multimodal sensing;
- sensor-language, biosignal-language, wearable agent and on-device model;
- cross-device, cross-position, cross-dataset and missing-modality generalization.

### Measurement and prediction

- digital biomarker, digital measure, computational phenotype;
- activity, sleep, circadian rhythm, arrhythmia, metabolic health, neurological disease, mental health, aging, frailty, infection and recovery;
- external validation, prospective study, calibration and clinical utility.

### Causal, counterfactual and policy methods

- target trial, marginal structural model, g-formula, heterogeneous treatment effect;
- longitudinal counterfactual, causal representation, causal discovery and transportability;
- dynamic treatment regime, SMART, micro-randomized trial, JITAI, contextual bandit, reinforcement learning and off-policy evaluation;
- digital twin, world model, intervention simulator and policy counterfactual.

### Intervention and closed-loop systems

- wearable feedback, adaptive messaging, remote monitoring and clinical escalation;
- automated insulin delivery, responsive neurostimulation, adaptive DBS, closed-loop sleep stimulation;
- wearable robotics, prostheses, rehabilitation, exergaming and assistive systems.

## Screening rules

- Deduplicate preprint and version-of-record variants.
- Verify the venue against `data/venues.yaml`.
- Assign one primary record type and cross-link related entities.
- Preserve null and negative trial results.
- Use conservative claims when only abstract-level material was checked.
- Move unresolved candidates to the watchlist rather than guessing.

## Current stopping rule

The release stops when each major lifecycle stage and sensor family has a non-trivial core set, all accepted records pass schema/venue checks, and unresolved candidates are visible. It does not stop because a target count has been reached.
