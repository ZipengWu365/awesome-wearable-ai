> Imported from the local v1.2 research notes. Historical local counts and paths describe that source package. Current accepted/watchlist placement and ID mapping are documented in [the migration guide](LOCAL_SYNC.md); profile data live in [data/profiles](../data/profiles/).

# Population wearable cohorts: release-aware comparisons

## UK Biobank
The indexed original accelerometry study reports the analyzable sample for that study, not the entire UK Biobank population or today's maximum accessible sample. Linkage availability must be checked for the current approved data product and analysis intersection. [Original accelerometry study](https://doi.org/10.1371/journal.pone.0169649).

## NHANES
Keep survey cycle, body location, instrument, released signal product and publication date separate. The 2003–2004 `PAXRAW_C` file contains minute-level activity counts despite “RAW” in its name. The 2011–2012 `PAX80_G` product provides raw 80 Hz wrist accelerometry; `PAXMIN_G` is a different derived minute-level product. Do not add raw and derived release rows into independent participants. [PAXRAW_C](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2003/DataFiles/PAXRAW_C.htm), [PAX80_G](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAX80_G.htm), [PAXMIN_G](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm).

## All of Us
The indexed v8 Fitbit resource reports 59,018 participants in its specified release. A pooled multi-year span is not each person's wear duration. Heart-rate/steps/sleep products are not raw PPG or accelerometry. The waveform flags, release identifier and sample scope make this explicit. [Resource paper](https://www.nature.com/articles/s41591-026-04352-3), [official usage resources](https://support.researchallofus.org/hc/en-us/articles/20281023493908-Resources-for-Using-Fitbit-Data).

## Choosing a cohort
Write down sensor modality and intended phenotype first. Then check who has valid wear, labels, covariates, consent/access and follow-up. Report the resulting intersection, not the sum of marginal availability counts. For a survey analysis, obtain the cycle-specific design and weighting documentation; this hub does not supply a statistical analysis plan or infer weights from wearable rows.

## Coverage gaps
The first release does not comprehensively catalogue MESA, HUNT, Rotterdam, Whitehall or all disease-specific cohorts. Some appear as training sources in model records but not as independently verified dataset releases. These are enrichment priorities, not permission to guess participant numbers.
