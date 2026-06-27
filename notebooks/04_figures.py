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
# # 04 — Figures
#
# Renders the publication figures from the pipeline outputs:
#
# - `figures/truecolor.png` — the Sentinel-2 input (B04/B03/B02)
# - `figures/ndwi.png` — the water index
# - `figures/melt_ponds_overlay.png` — detected pond outlines on the true colour

# %%
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import tifffile
import xarray as xr
from skimage.measure import find_contours

RAW = Path("data/raw")
PROC = Path("data/processed")
RES = Path("results")
FIG = Path("figures")
FIG.mkdir(parents=True, exist_ok=True)
SCENE = "S2_22WEV_20190723"


def stretch(a, lo=2, hi=98):
    p1, p2 = np.percentile(a, [lo, hi])
    return np.clip((a - p1) / (p2 - p1 + 1e-6), 0, 1)


# %%
bands = {}
for b in ("B02", "B03", "B04"):
    role = {"B02": "blue", "B03": "green", "B04": "red"}[b]
    with rasterio.open(RAW / f"{SCENE}_{b}_{role}.tif") as src:
        bands[b] = src.read(1).astype("float32")
tci = np.dstack([stretch(bands["B04"]), stretch(bands["B03"]), stretch(bands["B02"])])
ndwi = xr.open_dataarray(PROC / "ndwi.nc").values
labels = tifffile.imread(RES / "labels.tif")

# %%
plt.imsave(FIG / "truecolor.png", tci)
plt.imsave(FIG / "ndwi.png", stretch(ndwi, 1, 99), cmap="viridis")
print("wrote truecolor.png, ndwi.png")

# %%
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(tci)
for region_id in range(1, int(labels.max()) + 1):
    for contour in find_contours(labels == region_id, 0.5):
        ax.plot(contour[:, 1], contour[:, 0], color="red", linewidth=0.8)
ax.set_title(f"{int(labels.max())} supraglacial melt ponds — NDWIice > 0.25")
ax.set_xticks([]); ax.set_yticks([])
fig.savefig(FIG / "melt_ponds_overlay.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print("wrote melt_ponds_overlay.png")
