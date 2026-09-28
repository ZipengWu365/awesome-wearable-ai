> Imported from the local v1.2 research notes. Historical local counts and paths describe that source package. Current accepted/watchlist placement and ID mapping are documented in [the migration guide](LOCAL_SYNC.md); profile data live in [data/profiles](../data/profiles/).

# Digital-twin evaluation: a proposed protocol checklist

This is a repository-maintainer design proposal, not a validated benchmark, a reproduced algorithm or clinical guidance. Study-specific evidence is linked in the evidence map.

## Define the claim before selecting a metric

| Claim | Suggested evaluation | Failure to rule out |
| --- | --- | --- |
| Same-person binding | Participant/session linkage audit; multiple devices kept together | Anatomy and signals from different people, identity drift |
| Measurement-to-state mapping | Reference measurement agreement with uncertainty | Motion artifact, nonwear, firmware effects, label mismatch |
| Personalization | Population-only versus matched-budget personal and group-conditioned models | More data or tuning masquerading as personal adaptation |
| Dynamic updating | Static versus updated model on strictly later data | Retraining on future outcomes, mistaken state versus parameter updates |
| Latent parameters | Synthetic parameter recovery plus applicable physiological references | Nonidentifiability; multiple parameter sets fitting the same measurements |
| Factual forecast | Chronological multi-horizon error, calibration and missing-data stress tests | Teacher-forced performance substituted for free-running stability |
| Alternative-action simulation | Known simulated truth, supported action changes and trial-data replay | Predictor input edits mistaken for identified treatment effects |
| Decision value | Appropriate prospective or randomized evaluation of the complete policy | Accurate trajectories with no net benefit, unsafe actions or excess burden |
| Transportability | Separate device, population, site and time-period evaluation | Calling interpolation within a single personal record generalization |

## Minimum data contract

Preserve pseudonymous participant ID, session and device ID, event time and receipt time, source units, observation masks, quality flags, action eligibility, intended and actual action, delivery and adherence, contextual variables, outcome timestamps, model version and update trigger. Store no direct patient identifiers in this public catalogue.

An event's arrival time can differ from its measurement time. A proposed strict protocol feeds only information actually available at a decision point. The immutable evaluation split must precede windowing, adaptation and tuning. Randomized action probabilities, when present, should be retained for policy evaluation.

## Time scales are separate properties

Acquisition frequency, state-estimation cadence, parameter-retraining interval, decision interval and outcome horizon should be recorded separately. Do not fill all five with a device's nominal sampling frequency. For this literature pass, cadence is recorded in source-bound prose; unreported intervals remain unappraised.

## Ablation plan

Compare population prediction, personal/group-conditioned prediction, measurement-updated state estimation and action-conditioned simulation using matched histories and compute. Evaluate the controller separately from the simulator. Compare recommendations actually delivered with recommendations generated but vetoed or ignored. These are proposed comparisons; no new experiment results are supplied by this release.

## Examples motivating separate evidence tracks

[UVA replay validation](https://journals.sagepub.com/doi/10.1089/dia.2023.0595) illustrates why equivalence must be checked outcome by outcome; its time-below-range result did not establish equivalence. [WPINN](https://www.nature.com/articles/s41746-026-02610-9) separates human signal prediction from simulated parameter-recovery checks. [STUDIA](https://www.nature.com/articles/s41598-025-23165-x) supplies evidence for a short-term support-system intervention, not every internal component. These are different kinds of validation.

## Stopping and reporting rules

Preregister intended use, success criteria, safety limits and uncertainty treatment before evaluating an intervention. For a research simulator, report where action support is absent and decline to interpret those scenarios causally. Publish failed horizons, unavailable modalities and subgroup uncertainty. Separate model selection, held-out reporting and later exploratory analyses. Clinical deployment requires its own qualified clinical, ethical and regulatory review; this repository does not authorize it.
