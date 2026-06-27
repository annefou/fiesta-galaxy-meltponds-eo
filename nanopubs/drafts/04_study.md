# 04 — FORRT Replication Study

> The study **design** (scope + method + deviations), not the results.
> `Search for a FORRT claim` = the **Claim URI** (step 03).

## Form fields (`docs/forrt-form-fields.md` § FORRT Replication Study)

`Short URI suffix for study ID` · `Label/name of replication study` · `Study type` (dropdown: Reproduction / Replication / both) · `Search for a FORRT claim` (required) · `Describe what part of the claim is reproduced/replicated` (scope) · `Describe how the claim is reproduced/replicated` (method) · `Describe any deviations from original methodology` (optional) · `Search keywords (Wikidata)` (optional) · `Search discipline (Wikidata)` (optional)

---

### Short URI suffix for study ID

```
meltpond-offtheshelf-study
```

### Label/name of replication study

```
Cross-discipline reuse of a Galaxy cell-counting workflow to map Greenland supraglacial melt ponds
```

### Study type (dropdown)

```
Replication Study
```

> Same tools/method as the original GTN tutorial, but the **conditions** change
> (Sentinel-2 satellite imagery of melt ponds instead of fluorescence microscopy of
> cell nuclei). Same method, new data domain → Replication Study (not Reproduction).

### Search for a FORRT claim (required)

```
<paste Claim URI from PUBLISHED.md step 03 after publishing>
```

### Describe what part of the claim is reproduced/replicated (scope — NOT method, NOT results)

```
Whether the generic segment-count-measure behaviour of the Galaxy imgteam
image-analysis workflow — threshold an image into a binary mask, label connected
components as objects, and count and measure them — holds when the input is
Sentinel-2 optical imagery of supraglacial meltwater rather than a fluorescence
micrograph of cell nuclei, and how closely the resulting detection matches an
independent, purpose-built lake-mapping product. In scope: detection agreement
(precision/recall/F1/IoU) against the published lakes, pond count, and total
melt-water area, for one Sentinel-2 chip on one date. Out of scope: a full
ice-sheet or full-season lake inventory; lake-versus-channel-versus-slush
classification; lake depth/volume retrieval; and drainage-event detection.
```

### Describe how the claim is reproduced/replicated (method prose — NOT result numbers)

```
Two Sentinel-2 Level-2A bands (B02 blue, B04 red) of the melt-zone chip were read
directly from the AWS Open Data Cloud-Optimized GeoTIFF archive. The ice-adapted
normalised-difference water index NDWIice = (B02 − B04) / (B02 + B04) was computed,
median-filtered to suppress single-pixel speckle, thresholded at the established
0.25 cut (Williamson et al. 2018) to a binary water mask, labelled into objects by
connected-component analysis, and each object counted and measured (area, mean
index). The pipeline was run two ways: interactively on usegalaxy.eu with the
deployed imgteam tools (image_math → 2d_simple_filter → 2d_auto_threshold →
binary2labelimage → count_objects + 2d_feature_extraction + overlay_images,
captured as an importable Galaxy workflow and a public history), and as a hermetic,
credential-free local re-implementation (scikit-image, driven by Snakemake) for CI
reproducibility. The detection was then benchmarked against the independently
published Glen et al. (2024) Sentinel-2 lake outlines for the same area (nearest
acquisition 2019-07-25), rasterised to the analysis grid, scoring precision,
recall, F1 and intersection-over-union; and against two alternative thresholds on
the same imagery (automatic Otsu; the Moussavi et al. 2020 value of 0.19).
```

### Describe any deviations from original methodology (optional)

```
Relative to the original Galaxy "Introduction to Image Analysis" tutorial
(gxy.io/GTN:T00181), only the input domain and the meaning of the threshold
changed: fluorescence-microscopy nuclei images were replaced by Sentinel-2
satellite bands, and the stain-intensity threshold was replaced by a water-index
threshold (NDWIice > 0.25). One band-math step (image_math) was added to compute
the water index from the two input bands; the threshold → label → count → measure
tool chain and the tools themselves are unchanged. The Galaxy image tools discard
georeferencing, so object areas are reported in pixels and converted at the known
100 m² per pixel.
```

### Search keywords (Wikidata — labels, not QIDs; optional)

```
supraglacial lake; Greenland ice sheet; Sentinel-2; image segmentation; meltwater
```

> ✅ **Verified against the Wikidata API (2026-06-27)** — type the label, then pick
> the exact concept item below (each label's lower search hits are articles /
> patents / companies — *do not* pick those):
>
> | Label | Pick this item | Its Wikidata description |
> |---|---|---|
> | supraglacial lake | **Q2420381** | pond of liquid water on the top of a glacier |
> | Greenland ice sheet | **Q1542432** | glacier in Greenland |
> | Sentinel-2 | **Q4302480** | model of Earth observation satellite |
> | image segmentation | **Q56933** | division of an image into sets of pixels for further processing |
> | meltwater | **Q360925** | water released by the melting of snow or ice |
>
> Traps to avoid: "supraglacial lake" also returns *articles*; "meltwater" also
> returns *Meltwater Group* (a company); "image segmentation" also returns a
> *thesis* and a *patent*.

### Search discipline (Wikidata — optional)

```
glaciology; remote sensing
```

> ✅ **Verified:** glaciology = **Q52120** (*study of glaciers*); remote sensing =
> **Q199687** (*acquisition of information about an object without physical
> contact*). Avoid the lower hits: a *documentary film* and an *article* for
> glaciology; the *journals* "Remote Sensing" / "Remote Sensing of Environment".
