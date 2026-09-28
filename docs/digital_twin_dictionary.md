> Imported from the local v1.2 research notes. Historical local counts and paths describe that source package. Current accepted/watchlist placement and ID mapping are documented in [the migration guide](LOCAL_SYNC.md); profile data live in [data/profiles](../data/profiles/).

# Digital-twin overlay contract

The canonical resource ID is the join key. New profiles do not create another paper or modify a prior causal profile. The JSON Schema is generated from `wearable_ai/digital_twins.py`.

## Role and entity

`theme_role` distinguishes `reported_twin`, `conceptual_framework`, `method_enabler` and `synthetic_data_analogue`. “Reported” preserves the source framing and does not mean an independently certified digital twin. `entity` records organ, person, subpopulation, synthetic cohort or concept. A personal twin may model a limited state slice, not the whole person.

## Functional and causal connections

`layers` and `functions` reuse the v1.1 vocabularies. Website thematic filters combine both overlays while each original annotation remains separately inspectable. `causal_status` is a curator-assessed interpretation limit. A randomized support bundle may have treatment-effect evidence without separately identifying its internal simulator, controller or message effects.

## Dynamics and decisions

`personalization` records personal fitting versus group conditioning or external-stream/anatomy composition. `update_mode` records a computational update mechanism, not a maturity score. `simulation_kind` distinguishes factual reconstruction, mechanistic what-if, predictor input scenarios and synthetic data. `execution` records whether anything beyond simulation was delivered.

`state_variables`, `action_space`, `data_linkage`, `time_scope`, `model_mechanism` and `validation_scope` describe what was examined. A mentioned action may be simulated or proposed; read it together with `execution`.

## Verification scope

`review_scope=primary_sections` means the specified primary HTML sections were checked. `abstract_metadata` is limited to the source abstract and bibliographic fields. `abstract_and_open_reviews` also uses the official publication's public review discussion; it does not claim full-paper review. `prior_version_annotation` reuses an existing v1.1 card without new full-paper appraisal. Source notes state the exact scope.

`source_ids` references canonical source records. `reviewed_on` is a source-review date, not an experimental validation date. `classification_origin=curator_assessment` prevents a catalogue label being mistaken for the authors' own terminology.

## Watchlist and counts

`data/imports/local_watchlist.json` contains unresolved archival publication candidates separately from `data/papers.json`. Discovery deduplicates both causal and twin watchlists without accepting them. A later archival version must be merged by identity, not silently counted twice.

The original 184 resource objects, original source objects and three causal overlay files are checked against `config/parent_v1_1_baseline.json`. This frozen baseline is for release auditing; deliberate future corrections must carry an explicit migration record rather than silently editing historical evidence.

## Export paths

The combined API includes `digital_twin_atlas`. Dedicated API files include digital-twin profiles, taxonomy, watchlist and statistics. Browser filtered JSON and CSV include nested profile content and flattened filter fields. Canonical per-resource exports remain unjoined. The complete evidence matrix is generated from the same profiles.
