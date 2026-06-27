# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 03 — Analysis: detect, count and measure the melt ponds
#
# A **hermetic, local mirror** of the Galaxy `imgteam` workflow — same algorithm,
# no Galaxy key required — so the result is reproducible in CI:
#
# 1. 3×3 **median** filter (denoise)  → `2d_simple_filter`
# 2. **threshold** NDWIᵢ𝒸 > 0.25       → `2d_auto_threshold` (manual, Williamson 2018)
# 3. **label** connected components    → `binary2labelimage` (cca, 8-connected)
# 4. **count** + **measure** per pond  → `count_objects` + `2d_feature_extraction`
#
# Outputs the per-pond table (`results/pond_measurements.csv`), a label raster
# (`results/labels.tif`) and an aggregate summary (`results/summary.json`).

# %%
import json
from pathlib import Path

import numpy as np
import tifffile
import xarray as xr
from skimage.filters import median
from skimage.measure import label, regionprops_table

PROC = Path("data/processed")
RES = Path("results")
RES.mkdir(parents=True, exist_ok=True)
PX_AREA_M2 = 100.0  # 10 m pixels
THRESHOLD = 0.25

# %%
ndwi = xr.open_dataarray(PROC / "ndwi.nc").values.astype("float32")
ndwi_s = median(ndwi, np.ones((3, 3), dtype=bool))   # step 1 — 3x3 median
mask = ndwi_s > THRESHOLD                  # step 2 — water mask
labels = label(mask, connectivity=2)       # step 3 — 8-connected CCA
n_ponds = int(labels.max())
print(f"detected {n_ponds} melt ponds (NDWIice > {THRESHOLD})")

# %%
# step 4 — per-pond features (area in pixels, mean water index, centroid)
props = regionprops_table(
    labels, intensity_image=ndwi,
    properties=["label", "area", "mean_intensity", "centroid"],
)
import pandas as pd

df = pd.DataFrame(props).rename(
    columns={"centroid-0": "centroid_row", "centroid-1": "centroid_col"}
)
df["area_m2"] = df["area"] * PX_AREA_M2
df["area_km2"] = df["area_m2"] / 1e6
df = df.sort_values("area", ascending=False).reset_index(drop=True)
df.to_csv(RES / "pond_measurements.csv", index=False)
tifffile.imwrite(RES / "labels.tif", labels.astype("uint16"))

# %%
total_water_km2 = float(df["area_km2"].sum())
summary = {
    "n_ponds": n_ponds,
    "n_ponds_ge_500m2": int((df["area_m2"] >= 500).sum()),
    "total_water_km2": round(total_water_km2, 3),
    "largest_pond_km2": round(float(df["area_km2"].max()), 3),
    "median_pond_m2": round(float(df["area_m2"].median()), 1),
    "threshold_ndwi_ice": THRESHOLD,
    "pixel_area_m2": PX_AREA_M2,
}
with open(RES / "summary.json", "w") as fd:
    json.dump(summary, fd, indent=2)
print(json.dumps(summary, indent=2))
