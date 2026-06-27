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
# # 05 — Validation against the state of the art
#
# Two comparisons:
#
# **A. Method benchmark** (self-contained) — our detection threshold
# (NDWIᵢ𝒸 > 0.25, Williamson et al. 2018) vs the more permissive Moussavi et al.
# (2020) threshold (0.19) and vs automatic Otsu, on the same chip.
#
# **B. Ground-truth validation** — against the independently published
# Sentinel-2 supraglacial-lake outlines of **Glen et al. (2024)**
# ([Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884)) for
# this exact area. Their nearest acquisition is **2019-07-25**, two days after our
# 2019-07-23 scene — close, but melt ponds evolve day to day, so the 2-day gap is
# a genuine source of disagreement and is reported as such.

# %%
import json
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import xarray as xr
from rasterio.features import rasterize
from skimage.filters import median, threshold_otsu

RAW = Path("data/raw")
PROC = Path("data/processed")
RES = Path("results")
FIG = Path("figures")
FIG.mkdir(parents=True, exist_ok=True)
SCENE = "S2_22WEV_20190723"
PX_AREA_M2 = 100.0

# %%
# grid geometry from the red band; smoothed NDWIice (same preprocessing as nb 03)
with rasterio.open(RAW / f"{SCENE}_B04_red.tif") as src:
    transform = src.transform
    H, W = src.height, src.width
    bounds = src.bounds
ndwi = xr.open_dataarray(PROC / "ndwi.nc").values.astype("float32")
ndwi_s = median(ndwi, np.ones((3, 3), dtype=bool))


def metrics(pred, gt):
    pred, gt = pred.astype(bool), gt.astype(bool)
    tp = int((pred & gt).sum()); fp = int((pred & ~gt).sum()); fn = int((~pred & gt).sum())
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else float("nan")
    iou = tp / (tp + fp + fn) if tp + fp + fn else float("nan")
    return dict(precision=round(prec, 3), recall=round(rec, 3), f1=round(f1, 3),
                iou=round(iou, 3), area_km2=round(pred.sum() * PX_AREA_M2 / 1e6, 3))


# %% [markdown]
# ## B. Ground truth — Glen et al. (2024), 2019-07-25 lakes

# %%
GLEN = RAW / "glen"
GLEN.mkdir(parents=True, exist_ok=True)
zpath = GLEN / "Meltwater_Features.zip"
if not zpath.exists():
    import urllib.request
    print("downloading Glen et al. (2024) outlines (~79 MB)...")
    urllib.request.urlretrieve(
        "https://zenodo.org/records/11645884/files/Meltwater_Features.zip?download=1", zpath)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(GLEN)

base = GLEN / "Meltwater_Features" / "2019"


def rasterise(*shp_paths):
    geoms = []
    for p in shp_paths:
        g = gpd.read_file(p).to_crs("EPSG:32622")
        geoms += [geom for geom in g.geometry if geom is not None]
    return rasterize(((g, 1) for g in geoms), out_shape=(H, W),
                     transform=transform, fill=0, dtype="uint8").astype(bool)


# Glen catalogs LAKES (LL = large, SmL = small) separately from SLUSH and RIVERS.
# Our single NDWIice threshold cannot tell them apart, so we score against both:
#   - lakes only          -> the directly-comparable "ponds/lakes" product
#   - all surface water   -> lakes + slush (a fairer target for a water-extent mask)
gt_lakes = rasterise(base / "LL" / "S2_20190725_LL.shp",
                     base / "SmL" / "S2_20190725_SmL.shp")
gt_all = gt_lakes | rasterise(base / "Slush" / "T22WEV_20190725.shp")
gt_mask = gt_lakes  # headline ground truth = lakes
print(f"Glen 2019-07-25 lakes:        {gt_lakes.sum() * PX_AREA_M2 / 1e6:.3f} km²")
print(f"Glen 2019-07-25 lakes+slush:  {gt_all.sum() * PX_AREA_M2 / 1e6:.3f} km²")

# %% [markdown]
# ## A. Method benchmark + scoring each method against the ground truth

# %%
methods = {
    "Williamson 2018 (NDWIice > 0.25) — this study": ndwi_s > 0.25,
    "Moussavi 2020 threshold (NDWIice > 0.19)": ndwi_s > 0.19,
    "Otsu (automatic)": ndwi_s > threshold_otsu(ndwi_s),
}
rows = []
for name, mask in methods.items():
    m = metrics(mask, gt_mask)
    m["method"] = name
    rows.append(m)
table = pd.DataFrame(rows)[["method", "area_km2", "precision", "recall", "f1", "iou"]]
table.to_csv(RES / "validation_methods.csv", index=False)
print(table.to_string(index=False))

# %%
summary = {
    "ground_truth": "Glen et al. (2024), Sentinel-2, 2019-07-25",
    "ground_truth_doi": "10.5281/zenodo.11645884",
    "temporal_gap_days": 2,
    "this_study_area_km2": round(float((ndwi_s > 0.25).sum() * PX_AREA_M2 / 1e6), 3),
    "glen_lakes_area_km2": round(float(gt_lakes.sum() * PX_AREA_M2 / 1e6), 3),
    "glen_lakes_plus_slush_area_km2": round(float(gt_all.sum() * PX_AREA_M2 / 1e6), 3),
    "this_study_vs_lakes": metrics(ndwi_s > 0.25, gt_lakes),
    "this_study_vs_all_water": metrics(ndwi_s > 0.25, gt_all),
    "note": (
        "Recall ~0.88: the off-the-shelf method recovers ~88% of Glen's mapped "
        "lake area. Precision ~0.58: it also flags ~40% more water — meltwater "
        "channels and lake margins that Glen's lakes-only inventory excludes "
        "(channels are cataloged separately as 'Rivers'; slush adds negligible "
        "area here), compounded by the 2-day acquisition gap. As a total-water "
        "detector the result is broadly consistent with the published lakes; as a "
        "lakes-only classifier a single threshold with no shape/context filtering "
        "over-counts, exactly as expected."
    ),
}
with open(RES / "validation_summary.json", "w") as fd:
    json.dump(summary, fd, indent=2)
print(json.dumps(summary, indent=2))

# %% [markdown]
# ## Validation figure — our detection vs the published outlines

# %%
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def stretch(a, lo=2, hi=98):
    p1, p2 = np.percentile(a, [lo, hi]); return np.clip((a - p1) / (p2 - p1 + 1e-6), 0, 1)


bands = {}
for b, role in (("B02", "blue"), ("B03", "green"), ("B04", "red")):
    with rasterio.open(RAW / f"{SCENE}_{b}_{role}.tif") as src:
        bands[b] = src.read(1).astype("float32")
tci = np.dstack([stretch(bands["B04"]), stretch(bands["B03"]), stretch(bands["B02"])])
# washed-out greyscale backdrop: keeps the satellite texture as faint context but
# lets the (near-opaque) agreement colours stand out instead of blending into the ice
_lum = 0.2126 * tci[..., 0] + 0.7152 * tci[..., 1] + 0.0722 * tci[..., 2]
backdrop = np.dstack([_lum, _lum, _lum]) * 0.5 + 0.4  # pale grey, range ~0.4–0.9

# Okabe-Ito colour-blind-safe palette (distinguishable for all common colour
# vision deficiencies) — replaces the red/green agreement colours.
OI_AGREE = (0.0, 0.620, 0.451)   # #009E73 bluish green — agreement (TP)
OI_OURS = (0.902, 0.624, 0.0)    # #E69F00 orange — ours only (FP)
OI_GLEN = (0.0, 0.447, 0.698)    # #0072B2 blue — Glen only (FN)

pred = ndwi_s > 0.25
agree = np.zeros((H, W, 4), dtype=float)
agree[pred & gt_mask] = (*OI_AGREE, 0.95)      # TP
agree[pred & ~gt_mask] = (*OI_OURS, 0.95)      # FP (ours only)
agree[~pred & gt_mask] = (*OI_GLEN, 0.95)      # FN (Glen only)

fig, ax = plt.subplots(1, 2, figsize=(15, 7.5))
ax[0].imshow(backdrop); ax[0].imshow(agree)
ax[0].set_title("This study vs Glen et al. 2024 lakes\n"
                f"green=agree  orange=ours only  blue=Glen only  (IoU={summary['this_study_vs_lakes']['iou']})")
ax[1].bar(range(len(table)), table["iou"], color=[OI_GLEN, OI_OURS, OI_AGREE])
ax[1].set_xticks(range(len(table)))
ax[1].set_xticklabels(["Williamson\n0.25 (ours)", "Moussavi\n0.19", "Otsu"], fontsize=9)
ax[1].set_ylabel("IoU vs Glen et al. ground truth"); ax[1].set_ylim(0, 1)
ax[1].set_title("Method benchmark")
for a in (ax[0],):
    a.set_xticks([]); a.set_yticks([])
fig.legend(handles=[Patch(color=OI_AGREE, label="agreement (TP)"),
                    Patch(color=OI_OURS, label="ours only (FP)"),
                    Patch(color=OI_GLEN, label="Glen only (FN)")],
           loc="lower center", ncol=3)
fig.savefig(FIG / "validation_groundtruth.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print("wrote", FIG / "validation_groundtruth.png")
