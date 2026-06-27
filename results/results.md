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

## Notes

Areas in `pond_features.tabular` are in **pixels** (the Galaxy image tools drop
georeferencing); convert with the known 100 m²/px. For an independent check,
compare with the published Sentinel-2 lake outlines of Glen et al. (2025) for this
area and melt season
([Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884)).
