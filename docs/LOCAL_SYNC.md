# Local catalogue integration

This merge extends the existing YAML registry; it does not replace it with the independently packaged local v1.2 implementation. Local and repository version numbers are separate histories.

## What was preserved and added

- All 396 existing accepted IDs remain. A hash manifest checks unchanged records and documents the single existing-record correction: UniMTS weights and their official source. SensorLM and UniMTS retain their NeurIPS publication metadata.
- Twelve digital-twin-related publications whose identities were checked on primary publisher/proceedings pages enter the existing accepted schema and venue policy. Their appraisal text comes from the supplied local catalogue with its original source depth retained.
- Eight publications remain in the watchlist because venue eligibility or primary-source retrieval needs resolution. Their thematic profiles remain available when watchlist is enabled.
- All 22 twin profiles and 54 causal profiles are retained. Only profiles linked to accepted/watchlist records are exposed in the portal. Multiple local profiles may describe one remote record; profiles are not independent studies.
- Ninety-one local resource descriptions link to accepted/watchlist records. The remaining 111 resource rows form a review backlog, not 111 verified new studies. Aliases, variants and paper/model duplication require review before promotion.
- The existing HeartSteps diffusion-twin watchlist record is reused, not duplicated. Three other local frontier candidates remain in the import backlog.
- The original author, license, citation and 45 watchlist records are preserved.

## Sources of truth

| Data | Location | Meaning |
|---|---|---|
| Accepted records | `data/records/*.yaml` | Existing schema, IDs and eligibility policy |
| Watchlist | `data/excluded/watchlist.yaml` | Visible but excluded from accepted counts |
| Source-linked detail | `data/profiles/resources.json` | Release/variant-specific imported metadata; not a replacement for canonical publication status |
| Source registry | `data/profiles/sources.json` | Source dates and original appraisal notes |
| Thematic appraisals | `data/profiles/causal.json`, `digital_twin.json` | Independent annotations with mapped IDs |
| Pending imports | `data/imports/local_candidates.json`, `local_watchlist.json` | Retained material awaiting review, excluded from portal counts |
| Migration manifest | `data/imports/migration.json` | Base commit, mappings, preservation hashes and publication checks |

`unknown` is now explicitly allowed alongside booleans for code, weights and data availability. Existing false values are not retrospectively reinterpreted. Never infer a negative from an imported unknown.

Dataset release constraints are evaluated within one profile. For example, NHANES PAX80 and MIMS descriptions are not combined to imply that one product has both sets of attributes. All of Us CDR v8 metadata remains release-specific. Source dates on imports describe their original curation; the merge does not claim a fresh full-text review of every field.

## Explore and contribute

The portal supports sensor/scope/weights filters, twin role/entity/evaluation filters, dataset release filters, shareable queries, per-record source details and CSV/JSON export of all matching results. All original record types and model families remain searchable. Watchlist is excluded by default.

- [Chinese digital-twin reading route](digital_twins_zh.md)
- [Twin evaluation checklist](digital_twin_evaluation.md)
- [Dataset selection guide](datasets.md)
- [Population cohort and release notes](population_cohorts.md)

For a pending candidate, first check aliases, source identity, final publication and venue eligibility. Then add or link a canonical record, move its resource profile out of the pending file, update ID mappings and thematic targets, and run the checks below. An intentional correction of an original record must update the migration manifest with a reason and reviewed expected hash; never silently reset the baseline.

## Build and validate

```bash
python -m pip install -r requirements.txt
python scripts/build_all.py
python -m unittest discover -s tests -v
node --test tests/engine.test.mjs
python scripts/internal_link_check.py
python scripts/release_audit.py
python -m http.server 8000 --directory site
```

Open `http://127.0.0.1:8000`. Generated site files remain in `site/`; there is no second `public/` deployment. The optional Pages workflow runs only on main and when repository variable `ENABLE_PAGES_DEPLOYMENT=true`; configure Pages to use GitHub Actions before enabling it. A bundled workflow does not establish that a public deployment exists.

The independent local discovery/maintenance runtime was not copied over: it writes a different data contract. Review its candidates through the existing registry rather than running two competing acceptance pipelines.
