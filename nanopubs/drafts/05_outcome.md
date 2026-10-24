# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
meltpond-offtheshelf-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Off-the-shelf bioimage workflow recovers ~88% of mapped Greenland melt-lake area
```

<!-- field: study -->
### Choose study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: repo -->
### Repository URL (text input, required)

Use the Zenodo **version DOI** URL for the release the results came from — not a
bare branch URL, and not the concept DOI.

> **Why not the bare repo URL.** `https://github.com/ORG/REPO` names a *moving
> branch*. This Outcome asserts "this code produced this number", in a signed,
> immutable record. A branch URL means that assertion points at whatever `main`
> happens to be years from now — code that may never have produced the number
> above. A concept DOI has the same flaw: it resolves to the latest version.
> The version DOI pins the exact release. `docs/chain-decision-tree.md` § Anchor
> ranks the options: SWHID > Zenodo DOI > repo URL > Wayback.
>
> Both DOIs and the SWHID are in `CITATION.cff` under `identifiers:`, recorded
> automatically at release by `.github/workflows/release-identifiers.yml`. Take
> the one described as *"Version DOI"*.

```
https://doi.org/10.5281/zenodo.20943837
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-06-27
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)


This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [x] partially supported
- [ ] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

_Vocabulary not yet captured._

```

```

- [x] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [ ] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
The off-the-shelf Galaxy bioimage-analysis workflow transfers cross-discipline: applied without modification to a Sentinel-2 image, the same threshold → label → count → measure chain that counts cell nuclei detects supraglacial melt water on the Greenland ice sheet. It recovers about 88 percent of the area of the independently mapped supraglacial lakes (Glen et al. 2024) for the same location and melt season, and the total melt-water area is reproducible to three significant figures between an interactive Galaxy run (90 ponds, 1.46 km²) and a hermetic local re-implementation (85 ponds, 1.457 km²). The transfer is only partially supported as a lakes inventory, because a single water-index threshold also flags meltwater channels and crevasse water that the purpose-built product catalogs separately.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Detection: Galaxy run (public history below) = 90 ponds, 1.46 km² melt water, largest lake 0.64 km²; hermetic local re-implementation (results/summary.json) = 85 ponds, 1.457 km² — agreeing to 3 significant figures on area. Benchmark against Glen et al. (2024) Sentinel-2 lake outlines for tile T22WEV, 2019-07-25 (2 days after our scene), rasterised to the analysis grid (results/validation_summary.json): precision 0.58, recall 0.88, F1 0.70, IoU 0.54 versus the mapped lakes. Method comparison on the same chip (results/validation_methods.csv): IoU = 0.54 (NDWIice > 0.25, this study) vs 0.44 (Moussavi 2020 threshold, 0.19) vs 0.56 (automatic Otsu). Reproducible public Galaxy history: https://usegalaxy.eu/published/history?id=11ac94870d0bb33aee961e7883fc2313 . Archived release: https://doi.org/10.5281/zenodo.20943837 .
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
A single 10 km × 10 km chip on a single date, not a full ice-sheet or full-season inventory. The ground-truth outlines are 2 days after our scene, an irreducible source of disagreement for these ephemeral features. A single NDWIice threshold does not separate lakes from channels and slush, so it over-detects relative to a lakes-only inventory (precision 0.58); automatic Otsu matches the published lakes marginally better than the literature 0.25 cut. The Galaxy image tools discard georeferencing, so areas are pixel counts converted at 100 m² per pixel. No lake depth, volume, or drainage dynamics are retrieved. The local count (85) and Galaxy count (90) differ slightly because of median-filter implementation details, though the melt-water area agrees to 3 significant figures.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
