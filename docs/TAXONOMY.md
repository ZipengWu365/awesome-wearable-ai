# Taxonomy

The atlas uses a lifecycle axis, a record-type axis and orthogonal metadata. This avoids forcing a resource into a single branch when it spans several signals, tasks or evidence stages.

## Lifecycle

1. sensing and acquisition;
2. quality control, calibration and harmonisation;
3. representation and foundation models;
4. digital measures and computational phenotypes;
5. prediction, monitoring and prognosis;
6. causal identification and counterfactual reasoning;
7. policy learning and adaptive intervention design;
8. clinical evaluation and closed-loop deployment;
9. safety, fairness, regulation and post-deployment monitoring.

## Primary record types

- `model`: a learned representation, predictor, generator, language interface or decision model;
- `dataset`: a cohort, benchmark or canonical data resource;
- `method`: causal, counterfactual, trial-design, policy-learning, missingness or evaluation methodology;
- `measure`: a sensor-derived digital measure or computational phenotype with health/behavioural interpretation;
- `intervention`: a system that changes information, behaviour, treatment, stimulation or physical assistance;
- `infrastructure`: software, data platforms, standards, reporting guidance and regulation.

## Orthogonal metadata

Each record can be indexed by modality, body location, population, clinical domain, study design, evidence stage, causal status, openness, venue tier and scope ring.

## Evidence taxonomy

See `docs/EVIDENCE_GUIDE.md`. The repository explicitly separates association, prediction, causal effect, policy value and clinical utility.
