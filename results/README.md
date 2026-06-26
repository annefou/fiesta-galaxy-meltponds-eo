# Results

Outputs of the workflow run on the demo chip
([public Galaxy history](https://usegalaxy.eu/u/annefou/h/11ac94870d0bb33aee961e7883fc2313)).

| File | Produced by | Contents |
|---|---|---|
| `pond_count.tabular` | `count_objects` | number of detected ponds (**90**) |
| `pond_features.tabular` | `2d_feature_extraction` | one row per pond: `label`, `area` (px), `mean_intensity` (mean NDWIᵢ𝒸), `centroid_x`, `centroid_y` |
| `overlay.png` | `overlay_images` | detected pond contours (red) on the Sentinel-2 true-colour image |
| `summary.json` | post-processing | aggregate statistics (below) |

## Summary

- **Ponds detected:** 90 (57 larger than 500 m² / 5 px)
- **Total melt-water area:** 1.46 km²
- **Largest lake:** 0.64 km² (6363 px)
- **Median pond:** ~900 m²
- **Pixel size:** 10 m → 100 m² per pixel (multiply `area` column by 100 for m²)

## Notes

`count_objects` counts every connected component, so a handful of single-pixel
specks are included in the 90. Areas in `pond_features.tabular` are in **pixels**;
the Galaxy image tools drop georeferencing, so convert with the known 100 m²/px.
For an independent check, compare with the published Sentinel-2 lake outlines of
Glen et al. (2025) for this area and melt season
([Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884)).
