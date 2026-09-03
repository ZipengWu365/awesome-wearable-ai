# Frontier map: beyond HAR and foundation models

This map separates established directions, active but unsettled areas, and longer-horizon research bets. Inclusion is not an endorsement of clinical readiness.

## A. Intervention and adaptive health systems

### Just-in-time adaptive interventions

Wearable state estimates trigger context-sensitive behavioral support. Key methods include micro-randomized trials, contextual bandits, reinforcement learning, burden-aware policies and delayed-effect modeling. Core failure modes are habituation, treatment burden, non-stationarity, missing context and unsafe exploration.

### Closed-loop therapeutics

Examples include automated insulin delivery, responsive neurostimulation, closed-loop rehabilitation, stimulation for sleep or movement, and physiologically controlled drug or device delivery. Evaluation must cover control stability, latency, fail-safe behavior, human override and clinically meaningful outcomes.

### Remote monitoring linked to action

Monitoring systems become clinically relevant only when abnormal signals lead to a defined response pathway. Registry cards therefore distinguish passive monitoring from triage, clinician escalation, medication adjustment, rehabilitation and emergency response.

## B. Causal and counterfactual wearable AI

### Time-varying causal inference

Wearable exposures, symptoms, treatment and context evolve together. Relevant approaches include marginal structural models, g-methods, dynamic treatment regimes, target-trial emulation and sensitivity analysis for unmeasured confounding.

### Individual and heterogeneous effects

Estimating who benefits from which intervention is more demanding than predicting risk. Useful metadata include treatment variation, positivity, outcome horizon, effect modifiers, uncertainty and whether evaluation is randomized, observational or simulated.

### Counterfactual explanations

Actionable perturbations to a model input can improve interpretability, but changing a recorded activity pattern in silico does not prove that prescribing that change will improve health. The registry treats predictive counterfactuals and interventional counterfactuals as separate subtypes.

### Causal representation learning

This remains an emerging area. Claims of invariant, disentangled or causally sufficient wearable representations require explicit assumptions and out-of-distribution or interventional tests.

## C. Longitudinal models, world models and digital twins

Promising directions include continuous latent health-state models, multimodal trajectory models, generative simulators, patient-specific state-space models, physiological world models and decision-aware digital twins. Major unresolved issues include identifiability, calibration over long horizons, intervention validity, uncertainty propagation and external validation.

## D. Wearable-native multimodal agents

Potential systems integrate sensors, EHR, medication, conversation, environment and user goals. High-value research questions include when an agent should query the user, which sensor to activate, when to escalate to a clinician, how to preserve privacy, and how to prevent unsupported health advice.

## E. Active, efficient and on-device sensing

The frontier includes adaptive sampling, sensor selection, energy-aware inference, event-triggered acquisition, continual personalization, federated learning, split computation, quantization and hardware-software co-design. Accuracy must be evaluated together with battery, thermal load, latency and missingness induced by the sensing policy.

## F. Generative and synthetic wearable data

Use cases include pretraining, rare-event augmentation, privacy-preserving sharing, simulator-based policy evaluation and device-domain translation. Evaluation should test downstream utility, structural fidelity, diversity, privacy leakage, memorization, causal consistency and transfer to real cohorts.

## G. Cross-device and cross-population generalization

Device placement, sampling rate, sensor range, firmware, wear behavior and population mix can all shift the data-generating process. Harmonisation and domain adaptation should be evaluated under leave-device-out, leave-site-out, prospective and external-cohort protocols where feasible.

## H. Clinical evidence, safety and regulation

Important gaps include prospective impact studies, workflow integration, alarm fatigue, human factors, fairness, disability accessibility, post-deployment drift, incident reporting and evidence standards for adaptive software.

## Research maturity labels

| Label | Meaning |
|---|---|
| Established | Repeated empirical support and recognizable evaluation practice |
| Emerging | Multiple active studies, but methods or conclusions remain unsettled |
| Exploratory | Early demonstrations with limited external or clinical validation |
| Speculative | Coherent research direction without strong direct evidence yet |
