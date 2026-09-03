# Evidence guide

## Evidence depth

The registry exposes how deeply an entry has been checked.

| Level | Meaning | Permitted use |
|---|---|---|
| `venue_verified` | Title, year, venue and source identity were screened. | Discovery and bibliographic mapping. |
| `metadata_verified` | Core design/resource metadata were checked against a primary or canonical source. | Structured comparison with caution. |
| `evidence_card` | Design, contribution, limitation and evidence boundary were reviewed from the primary source at abstract/method-summary level or deeper. | Evidence-aware research planning; still not a full systematic-review risk-of-bias judgment. |

No level means that every numerical result or subgroup analysis has been independently reproduced.

## Five claims that must remain separate

| Claim | Typical question | Minimum evidence |
|---|---|---|
| Association | Are a sensor feature and outcome related? | Correct observational design, confounding assessment and uncertainty. |
| Prediction | Does a model generalize to new people/settings? | Participant-safe splits, external/temporal validation, calibration and clinically relevant metrics. |
| Causal effect | What would happen under another exposure or treatment? | Randomization or explicit identification assumptions with sensitivity analysis. |
| Policy value | Would a different sequential decision policy improve cumulative outcomes? | Online trial or defensible off-policy evaluation with overlap, uncertainty and safety constraints. |
| Clinical utility | Does use of the system improve patient or care outcomes? | Prospective comparative evaluation in the intended workflow, including harms and implementation. |

## Four meanings of counterfactual

### Predictive counterfactual

Changes an input until a model output changes. It explains model behaviour or offers recourse under assumptions. It does not identify the biological effect of making that change in reality.

### Causal counterfactual

Defines potential outcomes under alternative actions or exposures. It requires treatment consistency, exchangeability or randomization, positivity, an explicit time zero and defensible handling of interference and measurement error.

### Policy counterfactual

Compares sequential decision policies. Validity depends on action support/overlap, correct reward and state definitions, delayed effects, burden, non-stationarity and reliable off-policy evaluation.

### Generative or digital-twin counterfactual

Simulates an individual's trajectory under proposed interventions. Distributional fidelity alone is insufficient. The simulator must be calibrated for interventions, tested for temporal consistency, externally validated and shown to support better decisions prospectively.

## Intervention evidence ladder

1. Conceptual framework or algorithm.
2. Retrospective simulation.
3. Protocol.
4. Micro-randomized trial or proximal-effect study.
5. Randomized clinical/behavioural outcome evaluation.
6. External replication or systematic review.
7. Real-world deployment with safety, fairness and monitoring.

The repository records negative and null evidence. A technically sophisticated adaptive system can fail to improve the primary outcome.

## Common wearable-specific threats

- participant leakage through windows;
- repeated measurements treated as independent samples;
- pretraining overlap with benchmark subjects or datasets;
- device, placement and sampling-rate shift;
- algorithm-version drift in consumer APIs;
- non-wear and missing-not-at-random data;
- outcome ascertainment affected by the intervention;
- weak or circular reference labels;
- demographic and skin-tone performance differences;
- clinical threshold selection after test-set inspection;
- proxy improvement without patient benefit;
- short follow-up and engagement decay.
