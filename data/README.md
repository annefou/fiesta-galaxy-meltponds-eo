# Input data — Sentinel-2 melt-pond demo chip

These are small clips of a single, public Sentinel-2 scene, provided so the
Galaxy workflow can be run end-to-end without any data download or login.

## Source scene

| | |
|---|---|
| Product | `S2A_22WEV_20190723_0_L2A` (Sentinel-2A, Level-2A surface reflectance) |
| Tile | T22WEV (MGRS) |
| Acquired | 2019-07-23, ~15:14 UTC |
| Cloud cover | 2.6 % (scene-level) |
| Region | SW Greenland ice-sheet melt zone — Russell–Leverett / Isunnguata Sermia margin, near Kangerlussuaq |
| CRS | EPSG:32622 (UTM zone 22N) |
| Resolution | 10 m → **100 m² per pixel** (1 px = 1×10⁻⁴ km²) |
| Access | AWS Open Data, free, no login: <https://registry.opendata.aws/sentinel-2-l2a-cogs/> |
| STAC item | `sentinel-2-l2a` / `S2A_22WEV_20190723_0_L2A` (Element84 Earth Search v1) |

## Files

| File | Band | Description |
|---|---|---|
| `S2_22WEV_20190723_B02_blue.tif`  | B02 (blue, 490 nm) | single-band GeoTIFF, uint16, 1000×1000 px |
| `S2_22WEV_20190723_B04_red.tif`   | B04 (red, 665 nm)  | single-band GeoTIFF, uint16, 1000×1000 px |
| `S2_22WEV_20190723_truecolor.png` | B04/B03/B02 | true-colour preview (display only) |

The window is a **1000×1000 px (10 km × 10 km)** subset (full-resolution columns
9760–10760, rows 6930–7930) over the bare-ice ablation zone, where supraglacial
melt ponds form. It is regenerated exactly by [`../scripts/make_chip.py`](../scripts/make_chip.py).

## Why these two bands

Supraglacial melt water is detected with the **ice-adapted normalised-difference
water index**

```
NDWIice = (B02 − B04) / (B02 + B04)
```

(Williamson et al. 2018; Moussavi et al. 2020; Glen et al. 2025). Melt ponds are
bright in blue and dark in red, so they have high NDWIice; bare ice and snow are
near zero. A threshold of **NDWIice > 0.25** separates water from ice. The Galaxy
workflow computes this index from the two bands, thresholds it, then labels,
counts and measures the resulting ponds.

## Licence

Contains modified Copernicus Sentinel data 2019, processed by ESA, made available
on AWS Open Data. Sentinel data are free and open under the
[Copernicus data licence](https://sentinels.copernicus.eu/web/sentinel/terms-conditions).

## Validation reference (not redistributed here)

Independent supraglacial-lake outlines for this exact area and melt season are
published by Glen et al. (2025), *The Cryosphere* —
[Zenodo 10.5281/zenodo.11645884](https://doi.org/10.5281/zenodo.11645884) (vector
shapefiles), companion to <https://tc.copernicus.org/articles/19/1047/2025/>.
