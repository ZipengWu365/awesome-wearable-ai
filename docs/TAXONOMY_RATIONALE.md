# Taxonomy and architecture rationale

## Core decision

Awesome Wearable AI uses a **lifecycle backbone plus orthogonal facets**. A single nested tree is inadequate because the same resource can be, for example, an accelerometer model, a sleep phenotype system, a causal method, an older-adult study, and an on-device deployment at the same time.

## Lifecycle backbone

```text
Sensing and acquisition
        ↓
Signal quality, calibration and harmonisation
        ↓
Representation learning and foundation models
        ↓
Digital measures and computational phenotypes
        ↓
Detection, forecasting, prognosis and monitoring
        ↓
Causal identification and counterfactual reasoning
        ↓
Decision, policy learning and adaptive treatment
        ↓
Interventions and closed-loop systems
        ↓
Clinical utility, safety, fairness and deployment
```

Datasets, cohorts, benchmarks, tools, devices, standards, and governance resources support several stages and therefore remain independent entity classes.

## Entity classes

1. **Models** — learned representations, foundation models, multimodal models, generative models, forecasting and risk models.
2. **Datasets and cohorts** — raw signals, derived measures, labels, EHR linkage, longitudinal outcomes, intervention data.
3. **Devices and platforms** — research-grade and consumer wearables, acquisition stacks, edge hardware, APIs.
4. **Digital measures** — algorithms or validated measures for activity, sleep, physiology, behavior, symptoms, function and disease state.
5. **Benchmarks** — fixed tasks, splits, protocols, leaderboards and challenge datasets.
6. **Tools and infrastructure** — preprocessing, calibration, harmonisation, annotation, deployment, privacy and MLOps.
7. **Methods and study designs** — causal inference, target-trial emulation, MRTs, N-of-1 trials, policy learning, counterfactual explanation, missing-data methods and evaluation designs.
8. **Interventions and closed-loop systems** — actions that alter behavior, therapy, stimulation, rehabilitation or device control.
9. **Frontiers** — technically plausible and research-active directions whose evidence may still be early.
10. **Standards, governance and regulation** — interoperability, reporting, privacy, software-as-a-medical-device and clinical evidence guidance.

## Orthogonal facets

Every card may be tagged by:

- sensing modality;
- body location and form factor;
- population and care setting;
- clinical or behavioral domain;
- task and temporal horizon;
- study design;
- intervention/action channel;
- deployment location: cloud, phone, watch, edge device or clinical system;
- evidence level and validation stage;
- openness of data, code, weights and protocol;
- privacy model and regulatory status;
- maturity: established, emerging, exploratory or speculative.

## Evidence semantics

The registry distinguishes several concepts that are often conflated:

- **Association**: a wearable variable is statistically related to an outcome.
- **Prediction**: a model forecasts or discriminates an outcome under a stated validation protocol.
- **Causal effect**: an intervention contrast is identified under explicit assumptions or randomisation.
- **Counterfactual explanation**: a model-level change that would alter a prediction; this does not by itself establish a real-world treatment effect.
- **Policy value**: expected outcome under a decision policy, requiring valid online evaluation or defensible off-policy assumptions.
- **Clinical utility**: evidence that using the system changes decisions or outcomes, beyond predictive performance.

## Why methods and interventions are separate

A micro-randomized trial is a design for estimating proximal treatment effects. A notification, exercise recommendation, insulin dose, stimulation pulse, or exoskeleton command is an intervention. Mixing these categories obscures both the action and the evidence used to evaluate it.

## Inclusion boundary

The scope is intentionally broad, but entries must have a substantive connection to wearable or body-worn sensing, actuation, computation, or intervention. Generic time-series, general medical AI, and generic LLM resources are included only when they materially enable wearable research or deployment.
