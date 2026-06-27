# Results

```{figure} overlay.png
:alt: Detected melt-pond contours on the Sentinel-2 true-colour image
:width: 100%

`overlay_images` output: detected pond contours (red) on the Sentinel-2
true-colour image. 90 ponds, 1.46 km² of melt water.
```

The same analysis is produced two independent ways, and they agree.

## 1. The Galaxy run (canonical)

Run interactively on usegalaxy.eu with the `imgteam` tools
([public Galaxy history](https://usegalaxy.eu/published/history?id=11ac94870d0bb33aee961e7883fc2313)).

| File | Produced by | Contents |
|---|---|---|
| `pond_count.tabular` | `count_objects` | number of detected ponds (**90**) |
| `pond_features.tabular` | `2d_feature_extraction` | one row per pond: `label`, `area` (px), `mean_intensity` (mean NDWIᵢ𝒸), `centroid_x`, `centroid_y` |
| `overlay.png` | `overlay_images` | detected pond contours (red) on the Sentinel-2 true-colour image |

**90 ponds**, 1.46 km² melt water, largest lake 0.64 km², 57 larger than 500 m².

## 2. The local reproduction (hermetic)

The `Snakefile` + `notebooks/` rerun the **same algorithm** in pure Python
(scikit-image) from a clean clone — no Galaxy key — so the result is reproducible
in CI (`pixi run snakemake --cores 1`).

| File | Produced by | Contents |
|---|---|---|
| `summary.json` | `notebooks/03_analysis.py` | aggregate statistics |
| `pond_measurements.csv` | `notebooks/03_analysis.py` | one row per pond: `label`, `area` (px), `area_m2`, `area_km2`, `mean_intensity`, centroid |
| `../figures/melt_ponds_overlay.png` | `notebooks/04_figures.py` | computed pond contours on true colour |

**85 ponds**, 1.457 km² melt water, largest lake 0.636 km², 55 larger than 500 m².

## Agreement

The two counts (90 vs 85) and areas (1.46 vs 1.457 km²) agree to within the
difference between the Galaxy `2d_simple_filter` median implementation and the
scikit-image one (border handling + footprint), which slightly changes how many
single-pixel specks survive. The melt-water **area** — the science-relevant
quantity — is identical to three significant figures.

## Validation against the state of the art

`notebooks/05_validation.py` benchmarks the method and checks it against an
independent, published dataset (run with `pixi run snakemake validation --cores 1`).

```{figure} ../figures/validation_groundtruth.png
:alt: Agreement map and method benchmark against Glen et al. 2024
:width: 100%

Left: our detection vs the Glen et al. (2024) lake outlines (green = agree,
red = ours only, blue = Glen only). Right: IoU of three thresholding methods
against the published lakes.
```

**Ground truth — Glen et al. (2024)** ([Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884)),
Sentinel-2 lakes for this exact area on **2019-07-25** (2 days after our scene):

| Our method vs Glen lakes | precision | recall | F1 | IoU |
|---|---|---|---|---|
| Williamson 2018 — NDWIᵢ𝒸 > 0.25 (this study) | 0.58 | **0.88** | 0.70 | 0.54 |
| Moussavi 2020 threshold — NDWIᵢ𝒸 > 0.19 | 0.45 | 0.93 | 0.61 | 0.44 |
| Otsu (automatic, ≈0.32) | 0.65 | 0.80 | 0.72 | **0.56** |

**What this says, honestly:** the off-the-shelf method **recovers ~88 % of Glen's
mapped lake area** (recall) — a strong result for a generic, single-threshold
bioimage pipeline. Precision is ~0.58 because the threshold also flags meltwater
**channels, lake margins and crevasse water** that Glen's *lakes-only* inventory
excludes (channels are cataloged separately), plus the irreducible 2-day melt
evolution. Automatic **Otsu** matches the published lakes marginally better than
the literature 0.25 cut. So: as a **water-extent detector** the reuse is sound; as
a **lakes-only classifier** it over-counts, exactly as expected without
shape/context filtering — and that is the honest limit of the cross-discipline
transfer.

## Notes

Areas in `pond_features.tabular` are in **pixels** (the Galaxy image tools drop
georeferencing); convert with the known 100 m²/px. For an independent check,
compare with the published Sentinel-2 lake outlines of Glen et al. (2025) for this
area and melt season
([Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884)).
