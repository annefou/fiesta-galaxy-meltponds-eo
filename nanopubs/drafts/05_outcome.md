# 05 — FORRT Replication Outcome

> The **result**. `Search for a FORRT replication study` = the **Study URI**
> (step 04). Numbers come from `results/summary.json`, `results/validation_summary.json`
> and the public Galaxy history.

## Form fields (`docs/forrt-form-fields.md` § FORRT Replication Outcome)

`Short URI suffix for outcome ID` · `Plain-text label for the outcome` · `Search for a FORRT replication study` (required) · `Repository URL` · `Completion date` · `Validation status` (dropdown) · `Confidence level` (dropdown) · `Describe the overall conclusion` · `Describe the evidence` · `Describe what limits the conclusions` (optional)

---

### Short URI suffix for outcome ID

```
meltpond-offtheshelf-outcome
```

### Plain-text label for the outcome

```
Off-the-shelf bioimage workflow recovers ~88% of mapped Greenland melt-lake area
```

### Search for a FORRT replication study (required)

```
<paste Study URI from PUBLISHED.md step 04 after publishing>
```

### Repository URL

```
https://github.com/annefou/fiesta-galaxy-meltponds-eo
```

### Completion date

```
2026-06-27
```

### Validation status (dropdown)

```
PartiallySupported
```

> **Choice for Anne.** `PartiallySupported` (→ CiTO `qualifies`) is the honest
> default: the cross-discipline transfer works and recovers most mapped lakes
> (recall 0.88), but a single water-index threshold over-detects relative to a
> purpose-built lakes-only inventory (precision 0.58). If you prefer to emphasise
> that the *specific* claim in the AIDA — "recovers ~88 % of mapped lake area" — is
> met outright, `Validated` is also defensible; then the over-count sits purely in
> the limitations field.

### Confidence level (dropdown)

```
HighConfidence
```

> Strong evidence: the same result is produced two independent ways (interactive
> Galaxy run and a hermetic local re-implementation, agreeing to 3 significant
> figures on melt-water area) and is benchmarked against an independent published
> dataset — much stronger than a single un-benchmarked run.

### Describe the overall conclusion about the original claim

```
The off-the-shelf Galaxy bioimage-analysis workflow transfers cross-discipline:
applied without modification to a Sentinel-2 image, the same threshold → label →
count → measure chain that counts cell nuclei detects supraglacial melt water on
the Greenland ice sheet. It recovers about 88 percent of the area of the
independently mapped supraglacial lakes (Glen et al. 2024) for the same location
and melt season, and the total melt-water area is reproducible to three significant
figures between an interactive Galaxy run (90 ponds, 1.46 km²) and a hermetic local
re-implementation (85 ponds, 1.457 km²). The transfer is only partially supported
as a lakes inventory, because a single water-index threshold also flags meltwater
channels and crevasse water that the purpose-built product catalogs separately.
```

### Describe the evidence that supports your conclusion

```
Detection (results/summary.json): Galaxy run = 90 ponds, 1.46 km² melt water,
largest lake 0.64 km²; hermetic local re-implementation = 85 ponds, 1.457 km² —
agreeing to 3 significant figures on area. Benchmark against Glen et al. (2024)
Sentinel-2 lake outlines for tile T22WEV, 2019-07-25 (2 days after our scene),
rasterised to the analysis grid (results/validation_summary.json): precision 0.58,
recall 0.88, F1 0.70, IoU 0.54 versus the mapped lakes. Method comparison on the
same chip (results/validation_methods.csv): IoU = 0.54 (NDWIice > 0.25, this study)
vs 0.44 (Moussavi 2020 threshold, 0.19) vs 0.56 (automatic Otsu). Reproducible
public Galaxy history: https://usegalaxy.eu/published/history?id=11ac94870d0bb33aee961e7883fc2313 .
Archived release: https://doi.org/10.5281/zenodo.20943752 .
```

### Describe what limits the conclusions of the study (optional)

```
A single 10 km × 10 km chip on a single date, not a full ice-sheet or full-season
inventory. The ground-truth outlines are 2 days after our scene, an irreducible
source of disagreement for these ephemeral features. A single NDWIice threshold
does not separate lakes from channels and slush, so it over-detects relative to a
lakes-only inventory (precision 0.58); automatic Otsu matches the published lakes
marginally better than the literature 0.25 cut. The Galaxy image tools discard
georeferencing, so areas are pixel counts converted at 100 m² per pixel. No lake
depth, volume, or drainage dynamics are retrieved. The local count (85) and Galaxy
count (90) differ slightly because of median-filter implementation details, though
the melt-water area agrees to 3 significant figures.
```
