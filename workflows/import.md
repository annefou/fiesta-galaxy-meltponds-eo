# Workflow

`meltpond_mapping_sentinel2.ga` — the Galaxy workflow that maps and counts
supraglacial melt ponds from two Sentinel-2 bands.

**Inputs (3):** B02 (blue) TIFF, B04 (red) TIFF, true-colour PNG (for the overlay).
**Steps (7 tools):** `image_math` (NDWIᵢ𝒸) → `2d_simple_filter` (median) →
`2d_auto_threshold` (manual 0.25) → `binary2labelimage` (cca) → `count_objects`
+ `2d_feature_extraction` + `overlay_images`.

All tools are deployed on [usegalaxy.eu](https://usegalaxy.eu); no installation
needed.

## Import and run

1. usegalaxy.eu → **Workflow → Import** → upload
   `meltpond_mapping_sentinel2.ga` (or paste its URL).
2. Upload the three files from [`../data/`](../data) to a history (datatypes
   `tiff`, `tiff`, `png`).
3. Run the workflow, mapping the three inputs.

Or just open the public, already-run copy and import from there:
<https://usegalaxy.eu/published/history?id=11ac94870d0bb33aee961e7883fc2313>

## Provenance

This `.ga` was extracted directly from the public history above, so it reproduces
that exact run (tool versions pinned: `image_math 2.3.5`, `2d_simple_filter
1.16.3`, `2d_auto_threshold 0.25.2`, `binary2labelimage 0.7.3`, `count_objects
0.0.5-2`, `2d_feature_extraction 0.25.2`, `overlay_images 0.0.6`).
