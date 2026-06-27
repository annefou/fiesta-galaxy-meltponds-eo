#!/usr/bin/env python3
"""Build the communications figure for this study (`figures/linkedin_crossdiscipline.png`).

This is deliberately part of the repository, not a hand-made graphic: the figure
that goes on social media is generated from the same data and code as the science,
so the claim "the cell-counting workflow counts melt ponds" is reproducible end to
end — including the picture used to communicate it. Transparency extends to comms.

It composes:
  * the "input contract" — the metadata an image-analysis workflow needs about its
    input to give a relevant result, and how it transposes microscopy -> Sentinel-2;
  * the reused tutorial's own cell-nuclei data (downloaded from Zenodo), counted;
  * our Greenland melt-pond detection (from the local pipeline outputs).

Prerequisites: run the pipeline first so the melt-pond inputs/outputs exist —
    pixi run snakemake --cores 1
Then:
    pixi run python scripts/make_linkedin_figure.py
"""
import glob
import os
import urllib.request
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import tifffile
from skimage.filters import threshold_otsu
from skimage.measure import find_contours, label
from skimage.morphology import remove_small_objects

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw"
FIG = REPO / "figures"
SCENE = "S2_22WEV_20190723"
TEAL, ORANGE, BLUE, INK = "#009E73", "#E69F00", "#0072B2", "#1d1d1f"

# The reused tutorial's own data (DAPI HeLa nuclei) — the same siRNA-screen course
# images the Galaxy "Introduction to Image Analysis" tutorial (gxy.io/GTN:T00181) uses.
HELA_ZIP_URL = "https://zenodo.org/api/records/3362976/files/B2.zip/content"


def stretch(a, lo=1, hi=99):
    p1, p2 = np.percentile(a, [lo, hi])
    return np.clip((a - p1) / (p2 - p1 + 1e-6), 0, 1)


def get_nuclei_image():
    hela_dir = RAW / "hela"
    hela_dir.mkdir(parents=True, exist_ok=True)
    tifs = sorted(glob.glob(str(hela_dir / "*dapi.tif")))
    if not tifs:
        zpath = hela_dir / "B2.zip"
        if not zpath.exists():
            print("downloading reused-tutorial nuclei images (Zenodo 3362976)...")
            urllib.request.urlretrieve(HELA_ZIP_URL, zpath)
        with zipfile.ZipFile(zpath) as z:
            z.extractall(hela_dir)
        tifs = sorted(glob.glob(str(hela_dir / "*dapi.tif")))
    return tifs[0]


def main():
    if not (RAW / f"{SCENE}_B04_red.tif").exists() or not (REPO / "results" / "labels.tif").exists():
        raise SystemExit("Run the pipeline first: pixi run snakemake --cores 1")

    nuc = stretch(tifffile.imread(get_nuclei_image()).astype(float), 2, 99.5)
    nlbl = label(remove_small_objects(label(nuc > threshold_otsu(nuc)), 25) > 0)
    n_nuclei = int(nlbl.max())

    bands = {}
    for band, role in (("B02", "blue"), ("B03", "green"), ("B04", "red")):
        with rasterio.open(RAW / f"{SCENE}_{band}_{role}.tif") as src:
            bands[band] = src.read(1).astype(float)
    tci = np.dstack([stretch(bands["B04"]), stretch(bands["B03"]), stretch(bands["B02"])])
    plbl = tifffile.imread(REPO / "results" / "labels.tif")
    n_ponds = int(plbl.max())

    fig = plt.figure(figsize=(12.5, 12.5))
    fig.patch.set_facecolor("white")
    fig.text(0.045, 0.965, "A workflow crosses disciplines when its", fontsize=24, fontweight="bold", color=INK, va="top")
    fig.text(0.045, 0.925, "input contract is FAIR.", fontsize=24, fontweight="bold", color=TEAL, va="top")
    fig.text(0.045, 0.892, "OSCARS–FIESTA · cross-discipline FAIR image analysis with the Galaxy Project",
             fontsize=13.5, color="#666", va="top")

    fig.text(0.045, 0.825, "THE INPUT CONTRACT", fontsize=14.5, fontweight="bold", color=INK, va="top")
    fig.text(0.045, 0.800, "what the workflow must be told about the image\nto return a meaningful result — the metadata that transposes:",
             fontsize=11.5, color="#666", va="top", linespacing=1.4)

    axT = fig.add_axes([0.045, 0.305, 0.52, 0.45]); axT.axis("off"); axT.set_xlim(0, 100); axT.set_ylim(0, 100)
    axT.add_patch(plt.Rectangle((0, 0), 100, 100, facecolor="#f5f5f7", edgecolor="#ddd"))
    rows = [
        ("one quantity per pixel\n(an “index”)", "DAPI fluorescence", "NDWIⁱᶜᵉ = (blue−red)/(blue+red)"),
        ("targets are peaks\nof that index", "nuclei brighter\nthan background", "ponds have a\nhigh water index"),
        ("a separating\nthreshold", "Otsu (automatic)", "0.25 (Williamson 2018)"),
        ("a pixel size\n(counts → area)", "micrometres / pixel", "10 m / pixel → km²"),
    ]
    axT.text(2, 95, "the workflow needs…", fontsize=10.5, fontweight="bold", color="#444", va="top")
    axT.add_patch(plt.Rectangle((39, 92), 2.4, 3.2, facecolor=TEAL, edgecolor="none"))
    axT.text(43, 95, "microscopy", fontsize=10.5, fontweight="bold", color="#117a5e", va="top")
    axT.add_patch(plt.Rectangle((69, 92), 2.4, 3.2, facecolor=ORANGE, edgecolor="none"))
    axT.text(73, 95, "Sentinel-2", fontsize=10.5, fontweight="bold", color="#b06b00", va="top")
    y = 84
    for need, micro, eo in rows:
        axT.text(2, y, need, fontsize=10, color=INK, va="top", linespacing=1.25)
        axT.text(40, y, micro, fontsize=9.5, color="#333", va="top", linespacing=1.25)
        axT.text(70, y, eo, fontsize=9.5, color="#333", va="top", linespacing=1.25)
        y -= 20.5
        if y > 5:
            axT.plot([2, 98], [y + 8.5, y + 8.5], color="#e2e2e4", lw=1)

    fig.text(0.045, 0.268,
             "Same tools, unchanged. Only the index and the threshold are domain-specific —\n"
             "describe them precisely, and the cell-counting workflow counts melt ponds.",
             fontsize=11, color="#444", va="top", linespacing=1.45, style="italic")
    fig.text(0.045, 0.215,
             "Publishing a workflow isn't enough.\n"
             "You unlock its potential only by replicating\n"
             "it in a new discipline — that triggers reuse.",
             fontsize=12.5, color=BLUE, va="top", linespacing=1.5, fontweight="bold")

    axN = fig.add_axes([0.60, 0.60, 0.17, 0.17]); axN.imshow(nuc, cmap="gray")
    for rid in range(1, n_nuclei + 1):
        for c in find_contours(nlbl == rid, 0.5):
            axN.plot(c[:, 1], c[:, 0], color=TEAL, lw=0.5)
    axN.set_xticks([]); axN.set_yticks([])
    axN.set_title(f"{n_nuclei} cell nuclei", fontsize=11, color="#117a5e", fontweight="bold")
    fig.text(0.685, 0.585, "the reused tutorial's own data\ngxy.io/GTN:T00181", ha="center",
             fontsize=8.8, color="#888", va="top", linespacing=1.3)

    axH = fig.add_axes([0.60, 0.165, 0.355, 0.355]); axH.imshow(tci)
    for rid in range(1, n_ponds + 1):
        for c in find_contours(plbl == rid, 0.5):
            axH.plot(c[:, 1], c[:, 0], color=ORANGE, lw=0.8)
    axH.set_xticks([]); axH.set_yticks([])
    axH.set_title(f"{n_ponds} Greenland melt ponds", fontsize=13.5, color="#b06b00", fontweight="bold", pad=6)
    fig.text(0.7775, 0.150, "Sentinel-2, 2019  ·  validated against published lakes:\nrecovers ~88% of independently-mapped lake area",
             ha="center", fontsize=9.8, color="#666", va="top", linespacing=1.35)

    fig.text(0.5, 0.105,
             "We didn't just reuse the Galaxy training — we replicated it for ourselves, and recorded that\n"
             "reuse as a CiTO nanopublication chain (credits the tutorial, the tools and the method).",
             ha="center", fontsize=11.5, color=INK, va="top", linespacing=1.45, fontweight="bold")
    for i, logo in enumerate(["oscars.png", "fiesta.png", "galaxy.png"]):
        axl = fig.add_axes([0.345 + i * 0.115, 0.018, 0.092, 0.05])
        axl.imshow(mpimg.imread(REPO / "figures" / "logos" / logo)); axl.axis("off")

    out = FIG / "linkedin_crossdiscipline.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
    print(f"nuclei: {n_nuclei}  ponds: {n_ponds}  ->  {out}")


if __name__ == "__main__":
    main()
