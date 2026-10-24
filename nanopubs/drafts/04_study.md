# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
meltpond-offtheshelf-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

Human-readable title.

```
Cross-discipline reuse of a Galaxy cell-counting workflow to map Greenland supraglacial melt ponds
```

<!-- field: type -->
### Choose the study type (dropdown, required)

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
Whether the generic segment-count-measure behaviour of the Galaxy imgteam image-analysis workflow — threshold an image into a binary mask, label connected components as objects, and count and measure them — holds when the input is Sentinel-2 optical imagery of supraglacial meltwater rather than a fluorescence micrograph of cell nuclei, and how closely the resulting detection matches an independent, purpose-built lake-mapping product. In scope: detection agreement (precision/recall/F1/IoU) against the published lakes, pond count, and total melt-water area, for one Sentinel-2 chip on one date. Out of scope: a full ice-sheet or full-season lake inventory; lake-versus-channel-versus-slush classification; lake depth/volume retrieval; and drainage-event detection.
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
Two Sentinel-2 Level-2A bands (B02 blue, B04 red) of the melt-zone chip were read directly from the AWS Open Data Cloud-Optimized GeoTIFF archive. The ice-adapted normalised-difference water index NDWIice = (B02 − B04) / (B02 + B04) was computed, median-filtered to suppress single-pixel speckle, thresholded at the established 0.25 cut (Williamson et al. 2018) to a binary water mask, labelled into objects by connected-component analysis, and each object counted and measured (area, mean index). The pipeline was run two ways: interactively on usegalaxy.eu with the deployed imgteam tools (image_math → 2d_simple_filter → 2d_auto_threshold → binary2labelimage → count_objects + 2d_feature_extraction + overlay_images, captured as an importable Galaxy workflow and a public history), and as a hermetic, credential-free local re-implementation (scikit-image, driven by Snakemake) for CI reproducibility. The detection was then benchmarked against the independently published Glen et al. (2024) Sentinel-2 lake outlines for the same area (nearest acquisition 2019-07-25), rasterised to the analysis grid, scoring precision, recall, F1 and intersection-over-union; and against two alternative thresholds on the same imagery (automatic Otsu; the Moussavi et al. 2020 value of 0.19).
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
Relative to the original Galaxy "Introduction to Image Analysis" tutorial (gxy.io/GTN:T00181), only the input domain and the meaning of the threshold changed: fluorescence-microscopy nuclei images were replaced by Sentinel-2 satellite bands, and the stain-intensity threshold was replaced by a water-index threshold (NDWIice > 0.25). One band-math step (image_math) was added to compute the water index from the two input bands; the threshold → label → count → measure tool chain and the tools themselves are unchanged. The Galaxy image tools discard georeferencing, so object areas are reported in pixels and converted at the known 100 m² per pixel.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- supraglacial lake (Q2420381)
- Greenland ice sheet (Q1542432)
- Sentinel-2 (Q4302480)
- image segmentation (Q56933)
- meltwater (Q360925)

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

Provide labels.

- glaciology (Q52120)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
