# Counterfactual, intervention and closed-loop map

## From observation to action

```text
observational sensor stream
        ↓
measurement model
        ↓
prediction or risk score
        ↓
causal estimand and identification
        ↓
choice of action or policy
        ↓
intervention delivery
        ↓
proximal and clinical outcomes
        ↓
safety, burden, adaptation and monitoring
```

Every arrow can fail. A highly predictive biomarker may be non-actionable; a valid causal effect may not define the best sequential policy; a good policy in simulation may fail under burden, non-adherence or distribution shift.

## Method layers represented in the registry

- target-trial emulation, g-methods and marginal structural models;
- heterogeneous treatment effects and individual treatment-effect estimation;
- longitudinal counterfactual neural models;
- causal discovery, invariance and transportability;
- counterfactual explanations and recourse;
- micro-randomized trials and SMART designs;
- contextual bandits, dynamic treatment regimes and reinforcement learning;
- off-policy evaluation;
- missingness, calibration, sensor bias, fairness and privacy.

## Intervention families represented

- wearable feedback and behaviour change;
- JITAI and adaptive messaging;
- remote monitoring and clinical escalation;
- digital screening;
- automated insulin delivery;
- responsive and adaptive neurostimulation;
- closed-loop sleep stimulation;
- adaptive rehabilitation, wearable robotics and prosthetic control;
- assistive sensory systems;
- pain and mental-health digital care.

## Interpretation rules

- Protocols show planned design, not effectiveness.
- Micro-randomized trials often estimate proximal effects, not long-term clinical outcomes.
- Randomized detection studies may improve case finding without proving improved patient outcomes.
- Closed-loop implant studies can provide mechanistic and randomized evidence but may involve small, highly selected populations.
- Simulator or digital-twin fidelity is a prerequisite for policy testing, not proof that the recommended policy is beneficial.
- Null results remain central evidence because they identify failures of engagement, timing, burden, implementation or treatment mechanism.
