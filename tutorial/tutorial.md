# Counting Greenland melt ponds with off-the-shelf bioimage tools

> A cross-discipline image-analysis tutorial. We take the **standard Galaxy
> bioimage-analysis workflow** — the one the
> [GTN "Introduction to Image Analysis"](https://training.galaxyproject.org/training-material/topics/imaging/tutorials/imaging-introduction/tutorial.html)
> tutorial uses to count stained cell nuclei — and, *without changing a single
> tool*, point it at a Sentinel-2 satellite image to map and count **supraglacial
> melt ponds** on the Greenland ice sheet.

## Why this works

A "segment → label → count → measure" pipeline is generic raster maths. It does
not care whether the bright/dark blobs are cell nuclei, galaxies, or melt ponds.
The same [`imgteam`](https://github.com/BMCV/galaxy-image-analysis) tools that
biologists use on a microscope image work, unchanged, on a 10 m-resolution
satellite image. The only discipline-specific part is **which number we
threshold**: for cells it is a stain intensity; for melt ponds it is a water
index.

## What you will do

1. Load two Sentinel-2 bands (blue, red) of the SW Greenland melt zone.
2. Compute the ice water index **NDWIᵢ𝒸 = (blue − red) / (blue + red)** with
   **Image arithmetics**.
3. Smooth it, then **threshold** it at the literature value 0.25 to get a water
   mask.
4. Turn the mask into labelled objects, **count** them, and **measure** each
   pond's area and mean water index.
5. Overlay the detected pond outlines on the true-colour image.

Everything runs on [usegalaxy.eu](https://usegalaxy.eu) with deployed tools — no
installation, no new wrappers.

## Input data

From this repository's [`data/`](../data) folder (or
[Zenodo](#)):

| File | Sentinel-2 band |
|---|---|
| `S2_22WEV_20190723_B02_blue.tif` | B02 blue (490 nm) |
| `S2_22WEV_20190723_B04_red.tif`  | B04 red (665 nm) |
| `S2_22WEV_20190723_truecolor.png` | true-colour preview |

A 10 km × 10 km clip of scene `S2A_22WEV_20190723_0_L2A` (2019-07-23, 2.6 %
cloud) over the Russell–Leverett ice margin. 10 m pixels → **100 m² per pixel**.
See [`data/provenance.md`](../data/provenance.md) for full provenance.

```{figure} images/truecolor.png
:alt: Sentinel-2 true-colour image of the Greenland melt zone
:width: 100%

The input: a true-colour view of the bare-ice ablation zone, dotted with cyan
supraglacial melt ponds and lakes (and a dark crevasse field, lower right). This
is what the workflow will find and count.
```

> ### Tip — upload
> Upload the two `.tif` files and the `.png` to a new Galaxy history. Make sure
> the two bands are detected as datatype **`tiff`** and the preview as **`png`**.

## Step 1 — Water index with Image arithmetics

**Tool:** `Image arithmetics` (`imgteam/image_math`)

- **Expression:** `(1.0*blue - red) / (1.0*blue + red + 0.000001)`
- **Data type of the produced TIFF image:** `float32`
- **Input images:**
  - image = `..._B02_blue.tif`, variable name = `blue`
  - image = `..._B04_red.tif`, variable name = `red`

This produces a single-band floating-point image: high (≈ 0.3–0.9) on melt water,
near zero on ice and snow. The `1.0*` promotes the 16-bit integers to float so the
difference can go negative; the `+ 0.000001` avoids divide-by-zero.

## Step 2 — Smooth (remove single-pixel speckle)

**Tool:** `Filter 2-D image` (`imgteam/2d_simple_filter`)

- **target:** 2D
- **input:** the NDWIᵢ𝒸 image from Step 1
- **filter type:** `median`, **size:** 3

A 3×3 median filter removes isolated noisy pixels without blurring pond edges.

## Step 3 — Threshold to a water mask

**Tool:** `Threshold image` (`imgteam/2d_auto_threshold`)

- **input:** the smoothed NDWIᵢ𝒸 image
- **thresholding method:** `manual`, **threshold value:** `0.25`

0.25 is the established NDWIᵢ𝒸 cut for supraglacial water (Williamson et al. 2018).

> ### Comment — automatic thresholding
> Choose `otsu` instead of `manual` to let Galaxy pick the threshold from the
> image histogram. On this scene Otsu chooses ≈ 0.32 and finds fewer, only the
> most certain, ponds — a useful sensitivity check.

## Step 4 — Label the ponds

**Tool:** `Convert binary image to label map` (`imgteam/binary2labelimage`)

- **method:** connected component analysis (`cca`)
- **input:** the water mask

Each separate blob of water pixels becomes one numbered object.

## Step 5 — Count

**Tool:** `Count objects in label map` (`imgteam/count_objects`)

- **input:** the label map from Step 4

Output is a one-line table with the number of detected ponds.

## Step 6 — Measure each pond

**Tool:** `Extract image features` (`imgteam/2d_feature_extraction`)

- **label map:** the label map from Step 4
- **mode:** with intensities, **intensity image:** the NDWIᵢ𝒸 image from Step 1
- **features:** `label`, `area`, `mean_intensity`, `centroid`

You get one row per pond: its pixel area (× 100 m² = area on the ground) and its
mean water index (a rough depth proxy — deeper ponds are bluer).

## Step 7 — Overlay the result

**Tool:** `Overlay images` (`imgteam/overlay_images`)

- **method:** segmentation contour (`seg_contour`)
- **image 1:** the true-colour preview, **image 2:** the label map
- **contour colour:** red, **thickness:** 2

This draws the detected pond outlines on the satellite image so you can check the
detection by eye.

## Results

On the demo chip the workflow detects **90 melt ponds and lakes** (Step 5)
covering **1.46 km²** of melt water (Step 6: sum of areas × 100 m²), with the
largest lake **0.64 km²** and a median pond of ≈ 900 m². 57 of the 90 are larger
than 500 m².

![Detected pond contours on Sentinel-2 true colour](images/overlay.png)

A fully-run, public copy of this analysis is here — import it or just look at every
intermediate dataset:
<https://usegalaxy.eu/u/annefou/h/11ac94870d0bb33aee961e7883fc2313>

> ### Comment — is 90 right?
> `count_objects` counts every connected blob, including a few single-pixel
> specks the median filter missed. For a cleaner count, add
> `Filter label map by rules` (`imgteam/2d_filter_segmentation_by_features`) to
> drop objects below ~5 px, or raise the threshold. Independent Sentinel-2 lake
> outlines for this area and season (Glen et al. 2025) provide a real check.

## What changed vs. the cell-counting tutorial?

| | Cell nuclei (GTN intro) | Melt ponds (this tutorial) |
|---|---|---|
| Image | fluorescence microscope | Sentinel-2 satellite |
| "Brightness" used | DAPI stain intensity | NDWIᵢ𝒸 water index |
| Threshold | Otsu on the stain | 0.25 on the water index |
| Tools | `imgteam` threshold → label → count | **identical** |
| Object = | a cell | a melt pond |
| Measurement | nuclei per field | melt-water area (km²) |

Only the **input data** and the **meaning of the threshold** changed. The
analysis tools are exactly the same — that is the whole point.

## Citation & licence

See the repository [README](../README.md) and `CITATION.cff`. Contains modified
Copernicus Sentinel data 2019.
