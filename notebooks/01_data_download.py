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
# # 01 — Data download
#
# Fetches the two Sentinel-2 bands used by the melt-pond pipeline directly from
# the free **AWS Open Data** Cloud-Optimized GeoTIFF archive (no login). Only a
# 1000×1000 px (10 km × 10 km) window over the SW Greenland melt zone is read,
# so each band is a few MB. A record of the source is written to
# `data/raw/sources.json`.
#
# Scene: `S2A_22WEV_20190723_0_L2A` (tile T22WEV, 2019-07-23, 2.6 % cloud),
# EPSG:32622, 10 m pixels → 100 m² per pixel.

# %%
import json
import os
from pathlib import Path

import rasterio
from rasterio.windows import Window

os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")

BASE = (
    "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/"
    "22/W/EV/2019/7/S2A_22WEV_20190723_0_L2A"
)
SCENE = "S2_22WEV_20190723"
C0, R0, SZ = 9760, 6930, 1000  # melt-zone window (full-resolution pixels)
BANDS = {"B02": "blue", "B03": "green", "B04": "red"}  # B03 is for the true-colour figure only

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

# %%
window = Window(C0, R0, SZ, SZ)
written = []
for band, role in BANDS.items():
    with rasterio.open(f"{BASE}/{band}.tif") as src:
        arr = src.read(1, window=window)
        profile = src.profile.copy()
        profile.update(
            height=SZ, width=SZ, transform=src.window_transform(window),
            driver="GTiff", compress="deflate",
        )
        out = RAW / f"{SCENE}_{band}_{role}.tif"
        with rasterio.open(out, "w", **profile) as dst:
            dst.write(arr, 1)
        print(f"wrote {out}  shape={arr.shape} dtype={arr.dtype}")
        written.append(out.name)

# %%
sources = {
    "scene": "S2A_22WEV_20190723_0_L2A",
    "tile": "T22WEV",
    "acquired": "2019-07-23",
    "cloud_cover_pct": 2.6,
    "crs": "EPSG:32622",
    "pixel_size_m": 10,
    "area_per_pixel_m2": 100,
    "window_px": {"col_off": C0, "row_off": R0, "size": SZ},
    "archive": "https://registry.opendata.aws/sentinel-2-l2a-cogs/",
    "cog_base_url": BASE,
    "bands": BANDS,
    "files": written,
    "licence": "Contains modified Copernicus Sentinel data 2019, processed by ESA.",
}
with open(RAW / "sources.json", "w") as fd:
    json.dump(sources, fd, indent=2)
print("wrote", RAW / "sources.json")
