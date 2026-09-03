# Contributing

Contributions are welcome from model authors, dataset and cohort teams, trialists, causal-method researchers, standards groups and tool maintainers.

## Eligible submissions

- wearable, biosignal and sensor foundation models;
- population cohorts, waveform datasets and benchmarks;
- digital measures and validated computational phenotypes;
- causal, counterfactual, trial-design and adaptive-policy methods;
- wearable-enabled interventions and closed-loop systems;
- canonical tools, standards and regulator guidance;
- corrections, exclusions and evidence upgrades.

## Scientific publication rule

Core scientific papers must have an eligible version of record in `data/venues.yaml`. Pure preprints and workshop-only papers belong in `data/excluded/watchlist.yaml`. Major-lab official technical reports and canonical infrastructure use separate inclusion bases. Read `docs/INCLUSION_POLICY.md` before proposing a record.

## Required content

Every accepted record must include:

- stable unique ID;
- exact title, year, venue and primary URL;
- record type and family;
- modalities, scope and lifecycle stage;
- study design, evidence stage and causal status;
- concise contribution and practical importance;
- at least one limitation;
- an evidence boundary stating what the source cannot establish;
- verification status, evidence depth and check date.

Do not infer participant counts, sampling rates, open-weight status, clinical effectiveness or regulatory status.

## Workflow

```bash
python -m pip install -r requirements.txt
make build
make test
make audit
```

Commit source YAML and generated artifacts together. A pull request should state the evidence used and whether it adds a bibliographic record, metadata-verified record or evidence card.

## Curation style

- Prefer version-of-record and official URLs.
- Remove promotional adjectives.
- Preserve negative and null results.
- Distinguish raw waveforms from vendor-derived summaries.
- Use participant-safe language about generalization.
- Do not call predictive input perturbations causal counterfactuals.
- Do not call protocols or simulations evidence of clinical effectiveness.
