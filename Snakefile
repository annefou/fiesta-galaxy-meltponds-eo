# Reproducible melt-pond pipeline.
#
# A hermetic, local mirror of the Galaxy `imgteam` workflow (same algorithm,
# no Galaxy key) so the whole analysis reruns from a clean clone with:
#
#     pixi run snakemake --cores 1
#
# The notebooks/*.py are jupytext "percent" files that also run as plain
# scripts, which is what the rules below execute.

SCENE = "S2_22WEV_20190723"
BANDS = {"B02": "blue", "B03": "green", "B04": "red"}
RAW_TIFS = [f"data/raw/{SCENE}_{b}_{role}.tif" for b, role in BANDS.items()]


rule all:
    input:
        "results/summary.json",
        "results/pond_measurements.csv",
        "figures/melt_ponds_overlay.png",


rule data_download:
    output:
        "data/raw/sources.json",
        *RAW_TIFS,
    shell:
        "python notebooks/01_data_download.py"


rule data_clean:
    input:
        "data/raw/sources.json",
    output:
        "data/processed/ndwi.nc",
    shell:
        "python notebooks/02_data_clean.py"


rule analysis:
    input:
        "data/processed/ndwi.nc",
    output:
        "results/summary.json",
        "results/pond_measurements.csv",
        "results/labels.tif",
    shell:
        "python notebooks/03_analysis.py"


rule figures:
    input:
        "results/labels.tif",
        *RAW_TIFS,
    output:
        "figures/melt_ponds_overlay.png",
        "figures/truecolor.png",
        "figures/ndwi.png",
    shell:
        "python notebooks/04_figures.py"


# Validation against the state of the art. NOT part of `rule all`: it downloads
# the ~79 MB Glen et al. (2024) outlines, so it is run on demand with
#     pixi run snakemake validation --cores 1
# (kept out of the CI smoke run to avoid a large download on every push).
rule validation:
    input:
        "data/processed/ndwi.nc",
        *RAW_TIFS,
    output:
        "results/validation_methods.csv",
        "results/validation_summary.json",
        "figures/validation_groundtruth.png",
    shell:
        "python notebooks/05_validation.py"
