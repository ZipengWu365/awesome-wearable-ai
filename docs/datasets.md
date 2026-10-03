> Imported from the local v1.2 research notes. Historical local counts and paths describe that source package. Current accepted/watchlist placement and ID mapping are documented in [the migration guide](LOCAL_SYNC.md); profile data live in [data/profiles](../data/profiles/).

# Dataset selection guide

The canonical unit is a release or well-defined data product, not necessarily an independent participant cohort. All key attributes are in `data/datasets.json`; CSVs are generated views. Read `release_id` and `sample_scope` before interpreting `n_participants`.

## Common traps
A subject is not a recording, window, episode or cohort member with any data. Raw counts are not raw acceleration. A device's hardware sampling rate is not necessarily the released signal's rate. Mixed sensors can have different rates and locations. Camera labels do not imply that camera images are downloadable. Health outcomes at cohort level do not imply complete linkage for every wearable participant.

For CAPTURE-24, the record separates released participants, total recording time and annotated time. For WESAD it keeps wrist and chest channels and their different rates. NHANES stores the older hip activity-count product separately from later raw wrist acceleration. These choices follow [CAPTURE-24](https://www.nature.com/articles/s41597-024-03960-3), [WESAD](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection) and the [NHANES 2011–2012 raw-waveform documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAX80_G.htm).

## A reproducible selection procedure
Write the target deployment: modality, device location, target population and output label. Filter source-supported properties. Read official access terms and download the exact release. Retain subject/time/device identifiers, signal units and label provenance. Define a split before windowing. Record excluded people and missingness rather than advertising the source cohort's maximum number as your sample size.

The hub does not download controlled data, generate credentials or certify licenses. HAPT/UCI HAR, NHANES raw/derived products and cohort substudies may overlap. Their row counts must not be added into independent-person totals.
