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
# # 02 — Clean / derive the water index
#
# Computes the ice-adapted normalised-difference water index
#
# $$\mathrm{NDWI_{ice}} = \frac{B_{02} - B_{04}}{B_{02} + B_{04}}$$
#
# (Williamson et al. 2018) from the blue and red bands, and stores it as a
# self-describing **NetCDF** file (`data/processed/ndwi.nc`) — not `.npz` — so it
# keeps its CRS/affine metadata and is reusable across tools (see `DOMAIN.md`).
# This is the exact quantity the Galaxy `image_math` step produces.

# %%
from pathlib import Path

import numpy as np
import rasterio
import xarray as xr

RAW = Path("data/raw")
PROC = Path("data/processed")
PROC.mkdir(parents=True, exist_ok=True)
SCENE = "S2_22WEV_20190723"

# %%
with rasterio.open(RAW / f"{SCENE}_B02_blue.tif") as src:
    blue = src.read(1).astype("float32")
    transform = src.transform
    crs = src.crs
with rasterio.open(RAW / f"{SCENE}_B04_red.tif") as src:
    red = src.read(1).astype("float32")

ndwi = (blue - red) / (blue + red + 1e-6)
print(f"NDWIice range: {ndwi.min():.3f} .. {ndwi.max():.3f}")

# %%
# geographic coordinates of pixel centres (UTM zone 22N, metres)
ny, nx = ndwi.shape
xs = transform.c + transform.a * (np.arange(nx) + 0.5)
ys = transform.f + transform.e * (np.arange(ny) + 0.5)

da = xr.DataArray(
    ndwi, dims=("y", "x"), coords={"y": ys, "x": xs}, name="ndwi_ice",
    attrs={
        "long_name": "ice-adapted normalised-difference water index",
        "formula": "(B02 - B04) / (B02 + B04)",
        "reference": "Williamson et al. 2018, doi:10.5194/tc-12-3045-2018",
        "crs": str(crs), "pixel_size_m": 10.0,
    },
)
ds = da.to_dataset()
ds.attrs["crs"] = str(crs)
ds.to_netcdf(PROC / "ndwi.nc")
print("wrote", PROC / "ndwi.nc")
