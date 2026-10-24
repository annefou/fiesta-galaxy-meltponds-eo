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

This `.ga` reproduces the public, tool-by-tool run above (tool versions pinned:
`image_math 2.3.5`, `2d_simple_filter 1.16.3`, `2d_auto_threshold 0.25.2`,
`binary2labelimage 0.7.3`, `count_objects 0.0.5-2`, `2d_feature_extraction 0.25.2`,
`overlay_images 0.0.6`; parameters NDWIᵢ𝒸 = (blue − red)/(blue + red), median size 3,
manual threshold 0.25).

The version released in v0.1.0 was extracted from that history with Galaxy's
"Extract workflow", which left five steps unconnected (the tools use nested input
names such as `setup|input`), so it could not run end to end. On 2026-10-24 the
connections were rebuilt from the job records of the history, and the workflow was
run as an invocation on usegalaxy.eu on the v0.1.0 input chips. It reproduces the
published result: 90 ponds, 1.458 km² of melt water, largest pond 0.636 km².

- Workflow run (public history): <https://usegalaxy.eu/histories/view?id=11ac94870d0bb33a1cca8076136fbff5>
- Invocation: `b44716558a0e0379` (exported as a Workflow Run RO-Crate)

The unchanged Galaxy Training Network workflow of *Introduction to image analysis*
was also run as an invocation on the melt-pond water-index image used by the
tutorial's Earth-observation path ([10.5281/zenodo.20960690](https://doi.org/10.5281/zenodo.20960690)):
13 ponds, as in the tutorial. Public history:
<https://usegalaxy.eu/histories/view?id=11ac94870d0bb33a80e622e5b528f7fb>
(invocation `8649820f3b4fe496`).
