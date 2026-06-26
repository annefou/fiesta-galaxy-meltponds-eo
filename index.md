---
title: Counting Greenland melt ponds with off-the-shelf bioimage tools
---

# Counting Greenland melt ponds with off-the-shelf bioimage tools

**A cross-discipline OSCARS–FIESTA example.** This book takes the *standard*
Galaxy bioimage-analysis workflow — the exact "threshold → label → count →
measure" chain that the
[GTN imaging intro tutorial](https://training.galaxyproject.org/training-material/topics/imaging/tutorials/imaging-introduction/tutorial.html)
uses to count stained cell nuclei — and, **without modifying or adding a single
tool**, applies it to a Sentinel-2 satellite image to map and count
**supraglacial melt ponds** on the Greenland ice sheet.

```{figure} results/overlay.png
:alt: Detected melt-pond contours on a Sentinel-2 true-colour image
:width: 100%

Detected melt ponds (red contours) on the Sentinel-2 true-colour image of the
SW Greenland melt zone. **90 ponds**, **1.46 km²** of melt water, largest lake
**0.64 km²** — produced entirely with deployed Galaxy `imgteam` tools.
```

## The idea in one line

A "segment → count → measure" pipeline is generic raster maths: the
[`imgteam`](https://github.com/BMCV/galaxy-image-analysis) tools a biologist runs
on a microscope image run **unchanged** on a glacier. The only discipline-specific
choice is *which quantity we threshold* — a stain intensity for cells, a water
index for melt ponds.

## What's here

| Page | Contents |
|---|---|
| [Tutorial](tutorial/tutorial.md) | step-by-step walkthrough (cell-nuclei → melt-ponds) |
| [Results](results/results.md) | the 90-pond detection, areas, overlay |
| [Data](data/provenance.md) | Sentinel-2 scene provenance & bands |
| [Workflow](workflows/import.md) | the importable Galaxy `.ga` |

## Run it yourself

- **Public Galaxy history (already run, import as-is):**
  <https://usegalaxy.eu/u/annefou/h/11ac94870d0bb33aee961e7883fc2313>
- **Workflow:** [`workflows/meltpond_mapping_sentinel2.ga`](workflows/meltpond_mapping_sentinel2.ga)
- **Regenerate the input chip from source (no login):** `python scripts/make_chip.py data/`

## The cross-discipline family

Part of a set of OSCARS–FIESTA demonstrations that move a method across
disciplines using Galaxy — see the
[repository README](https://github.com/annefou/fiesta-galaxy-meltponds-eo#how-this-fits-the-fiesta-cross-discipline-family).
This one is the lowest-friction of all: only **plain, deployed tools**, no custom
wrapper, no deep-learning model — same tools, new science.
