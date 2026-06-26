#!/usr/bin/env python3
"""Reproducibly clip the Sentinel-2 melt-pond demo chip used in this repository.

It reads two Cloud-Optimized GeoTIFF bands (B02 blue, B04 red) of the public
Sentinel-2 L2A scene S2A_22WEV_20190723_0_L2A directly from the free AWS Open
Data archive (no login), extracts a 1000x1000 px (10 km x 10 km) window over the
supraglacial melt zone of the SW Greenland ice sheet (Russell-Leverett /
Isunnguata Sermia margin), and writes the two single-band GeoTIFFs plus a
true-colour preview PNG.

Scene .... S2A_22WEV_20190723_0_L2A (tile T22WEV, 2019-07-23, 2.6% cloud)
CRS ...... EPSG:32622 (UTM zone 22N), 10 m pixels -> 100 m^2 / pixel
Window ... full-res cols 9760:10760, rows 6930:7930

Requirements: rasterio, numpy, imageio
    python make_chip.py [output_dir]
"""
import os
import sys
import numpy as np
import rasterio
from rasterio.windows import Window
import imageio.v3 as iio

os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")

BASE = ("https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/"
        "22/W/EV/2019/7/S2A_22WEV_20190723_0_L2A")
SCENE = "S2_22WEV_20190723"
C0, R0, SZ = 9760, 6930, 1000  # melt-zone window (full-resolution pixels)


def stretch(a, lo=2, hi=98):
    p1, p2 = np.percentile(a, [lo, hi])
    return np.clip((a - p1) / (p2 - p1 + 1e-6), 0, 1)


def main(out="."):
    os.makedirs(out, exist_ok=True)
    win = Window(C0, R0, SZ, SZ)
    chips = {}
    for band in ("B02", "B03", "B04"):
        with rasterio.open(f"{BASE}/{band}.tif") as src:
            arr = src.read(1, window=win)
            prof = src.profile.copy()
            prof.update(height=SZ, width=SZ, transform=src.window_transform(win),
                        driver="GTiff", compress="deflate")
            chips[band] = arr
            if band in ("B02", "B04"):
                label = {"B02": "blue", "B04": "red"}[band]
                path = os.path.join(out, f"{SCENE}_{band}_{label}.tif")
                with rasterio.open(path, "w", **prof) as dst:
                    dst.write(arr, 1)
                print(f"wrote {path}  ({arr.shape}, {arr.dtype})")
    tci = np.dstack([stretch(chips["B04"].astype("f4")),
                     stretch(chips["B03"].astype("f4")),
                     stretch(chips["B02"].astype("f4"))])
    png = os.path.join(out, f"{SCENE}_truecolor.png")
    iio.imwrite(png, (tci * 255).astype(np.uint8))
    print(f"wrote {png}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
