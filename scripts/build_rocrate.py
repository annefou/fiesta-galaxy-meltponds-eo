"""Build the RO-Crate 1.2 "study crate" of this repository for deposit in ROHub (ROH-ON).

One crate per study repository: the Galaxy workflow (definition), the inputs and
results, the archived release, the community FAIR Implementation Profile it conforms
to, and the signed FORRT nanopublication chain that states what was claimed, how it
was tested and how it held. Small files are included; large or third-party data are
referenced by their identifiers.

The executions are not re-described here: each Galaxy workflow invocation is exported
by Galaxy as a Workflow Run RO-Crate (RO-Crate 1.1, Workflow Run Crate 0.5), deposited
with its own DOI, and referenced from this crate as a nested crate (--subcrate). The
study crate itself follows RO-Crate 1.2 and the community FAIR Implementation Profile.

    python scripts/build_rocrate.py -o ro-crate.zip \
        --subcrate "https://doi.org/...|Workflow run: GTN workflow, unchanged|https://usegalaxy.eu/histories/view?id=..."
"""

import argparse
import re
import shutil
from pathlib import Path

from rocrate.model.contextentity import ContextEntity
from rocrate.rocrate import ROCrate

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/annefou/fiesta-galaxy-meltponds-eo"
VERSION_DOI = "https://doi.org/10.5281/zenodo.20943837"
CONCEPT_DOI = "https://doi.org/10.5281/zenodo.20943752"
ZIP_URL = ("https://zenodo.org/records/20943837/files/annefou/"
           "fiesta-galaxy-meltponds-eo-v0.1.0.zip")
SWHID = ("swh:1:rev:d1a052a8432e0c82d99d1f601fac543d13655cd9;"
         "origin=https://github.com/annefou/fiesta-galaxy-meltponds-eo")
EO_FIP = "https://w3id.org/np/RAQXwdUrfZ40k2MdeDv9fokzyh35UKuN3w17G2yO4Wm8A"
GTN_TUTORIAL = "https://gxy.io/GTN:T00181"
GALAXY_HISTORY = "https://usegalaxy.eu/published/history?id=11ac94870d0bb33aee961e7883fc2313"
WFRUN = "https://w3id.org/ro/wfrun/workflow/0.5"
ANNE = "https://orcid.org/0000-0002-1784-2920"
BBOX = (-48.7719, 66.8852, -48.5347, 66.9782)  # lon/lat of the 10 km x 10 km chip

STEP_TYPES = {
    "01": "PICO research question", "02": "AIDA sentence", "03": "FORRT claim",
    "04": "FORRT replication study", "05": "FORRT replication outcome", "06": "CiTO citation",
}


def chain_uris() -> dict[str, str]:
    """Step number -> nanopub URI, from the ledger."""
    out = {}
    for line in (ROOT / "nanopubs" / "PUBLISHED.md").read_text().splitlines():
        m = re.match(r"\|\s*(0[1-6])\s*\|[^|]*\|\s*(https://w3id\.org/\S+?)\s*\|", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def ref(crate: ROCrate, uri: str, props: dict) -> ContextEntity:
    return crate.add(ContextEntity(crate, uri, properties=props))


def add_metadata(crate: ROCrate) -> None:
    root = crate.root_dataset
    anne = ref(crate, ANNE, {"@type": "Person", "name": "Anne Fouilloux",
                             "affiliation": {"@id": "https://ror.org/02a8eka68"}})
    ref(crate, "https://ror.org/02a8eka68", {"@type": "Organization", "name": "LifeWatch ERIC"})
    oscars = ref(crate, "https://cordis.europa.eu/project/id/101129751", {
        "@type": "Grant", "name": "OSCARS", "identifier": "101129751",
        "funder": {"@id": "https://ror.org/00k4n6c32"}})
    ref(crate, "https://ror.org/00k4n6c32", {"@type": "Organization", "name": "European Commission"})
    lic = ref(crate, "https://spdx.org/licenses/MIT", {"@type": "CreativeWork", "name": "MIT License"})
    fip = ref(crate, EO_FIP, {
        "@type": ["CreativeWork", "Profile"], "version": "1.0.2",
        "name": "FAIR Implementation Profile: Earth Observation (OSCARS-FIESTA), v1.0.2",
        "description": "The FAIR Enabling Resources the Earth-observation community of "
                       "OSCARS-FIESTA agreed to use, published as nanopublications with the FIP Wizard."})
    place = ref(crate, "#study-area", {
        "@type": "Place", "name": "SW Greenland ice-sheet ablation zone (Russell-Leverett / Isunnguata Sermia)",
        "geo": {"@id": "#study-area-box"}})
    ref(crate, "#study-area-box", {
        "@type": "GeoShape", "box": f"{BBOX[1]} {BBOX[0]} {BBOX[3]} {BBOX[2]}"})

    root["name"] = "Off-the-shelf Galaxy bioimage workflow maps supraglacial melt ponds on Sentinel-2 (OSCARS-FIESTA)"
    root["description"] = (
        "Cross-discipline reuse: the Galaxy Training Network 'Introduction to image analysis' workflow "
        "(threshold, label, count, measure), built to count cell nuclei, applied unchanged to a Sentinel-2 "
        "chip of the Greenland ice sheet to detect and measure supraglacial melt ponds, and benchmarked "
        "against independent lake outlines (Glen et al.). The data are GeoTIFF/TIFF where the Earth-"
        "observation FIP declares NetCDF: the bioimaging workflow only accepts image formats, a deviation "
        "caused by the cross-domain reuse itself.")
    root["author"] = anne
    root["publisher"] = {"@id": "https://ror.org/02a8eka68"}
    root["license"] = lic
    root["datePublished"] = "2026-06-27"
    root["keywords"] = ["supraglacial lake", "Greenland ice sheet", "Sentinel-2", "image segmentation",
                        "meltwater", "Galaxy", "cross-discipline reuse", "FORRT", "OSCARS-FIESTA"]
    root["funding"] = oscars
    root["contentLocation"] = place
    root["identifier"] = VERSION_DOI
    root["sameAs"] = {"@id": CONCEPT_DOI}
    root["codeRepository"] = REPO
    root["isBasedOn"] = [{"@id": GTN_TUTORIAL}, {"@id": SWHID}]
    root["conformsTo"] = fip

    ref(crate, GTN_TUTORIAL, {"@type": "CreativeWork",
                              "name": "Introduction to Image Analysis using Galaxy (Galaxy Training Network)"})
    ref(crate, SWHID, {"@type": "CreativeWork", "name": "Source code of release v0.1.0 (Software Heritage)",
                       "codeRepository": REPO, "version": "0.1.0"})
    ref(crate, GALAXY_HISTORY, {"@type": "CreativeWork", "name": "Public Galaxy history of the run (usegalaxy.eu)"})

    # the signed FORRT chain: what was claimed, how it was tested, how it held
    chain = []
    for step, uri in sorted(chain_uris().items()):
        chain.append(ref(crate, uri, {"@type": "CreativeWork", "additionalType": "Nanopublication",
                                      "name": f"{STEP_TYPES[step]} (FORRT chain step {step})",
                                      "encodingFormat": "application/trig"}))
    root["subjectOf"] = chain + [{"@id": GALAXY_HISTORY}]

    # references the study cites (from the CiTO step)
    cites = {
        "https://doi.org/10.5194/tc-12-3045-2018": ("ScholarlyArticle", "Williamson et al. 2018, NDWI-ice method for supraglacial lakes"),
        "https://doi.org/10.7717/peerj.453": ("ScholarlyArticle", "scikit-image: image processing in Python"),
        "https://doi.org/10.5281/zenodo.11645884": ("Dataset", "Glen et al., supraglacial meltwater feature outlines (validation reference)"),
    }
    root["citation"] = [ref(crate, u, {"@type": t, "name": n}) for u, (t, n) in cites.items()]
    root.append_to("hasPart", crate.get("https://doi.org/10.5281/zenodo.11645884"))


def add_files(crate: ROCrate) -> None:
    galaxy = ref(crate, "https://w3id.org/workflowhub/workflow-ro-crate#galaxy", {
        "@type": "ComputerLanguage", "name": "Galaxy", "version": "26.1", "identifier": {"@id": "https://galaxyproject.org/"},
        "url": {"@id": "https://galaxyproject.org/"}})
    wf = crate.add_file(ROOT / "workflows" / "meltpond_mapping_sentinel2.ga",
                        dest_path="workflows/meltpond_mapping_sentinel2.ga", properties={
                            "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
                            "name": "Supraglacial melt-pond mapping (Sentinel-2, cross-discipline imaging)",
                            "programmingLanguage": galaxy, "encodingFormat": "application/json",
                            "isBasedOn": {"@id": GTN_TUTORIAL}})
    crate.root_dataset["mainEntity"] = wf
    scene = ref(crate, "https://registry.opendata.aws/sentinel-2-l2a-cogs/", {
        "@type": "Dataset", "name": "Sentinel-2 L2A scene S2A_22WEV_20190723 (AWS Open Data)",
        "license": {"@id": "https://sentinels.copernicus.eu/web/sentinel/terms-conditions"}})
    ref(crate, "https://sentinels.copernicus.eu/web/sentinel/terms-conditions",
        {"@type": "CreativeWork", "name": "Copernicus Sentinel data terms"})
    # inputs by reference: the chips are in the archived release, the scene at its source
    archive = ref(crate, ZIP_URL, {
        "@type": "File", "name": "Release v0.1.0 archive (Zenodo): code, input chips, results, figures",
        "encodingFormat": "application/zip", "contentSize": "11804894",
        "isPartOf": {"@id": VERSION_DOI}, "license": {"@id": "https://spdx.org/licenses/MIT"}})
    ref(crate, VERSION_DOI, {"@type": "CreativeWork", "name": "fiesta-galaxy-meltponds-eo v0.1.0 (Zenodo version DOI)",
                             "distribution": {"@id": ZIP_URL}})
    for f, desc in [("data/S2_22WEV_20190723_B02_blue.tif", "Sentinel-2 B02 (blue), 10 km x 10 km chip"),
                    ("data/S2_22WEV_20190723_B04_red.tif", "Sentinel-2 B04 (red), 10 km x 10 km chip")]:
        chip = ref(crate, f"{ZIP_URL}#{f}", {"@type": "File", "name": desc, "encodingFormat": "image/tiff",
                                             "isPartOf": archive, "isBasedOn": scene,
                                             "contentLocation": {"@id": "#study-area"}})
        crate.root_dataset.append_to("hasPart", chip)
    crate.root_dataset.append_to("hasPart", archive)
    crate.root_dataset.append_to("hasPart", scene)
    results = {
        "results/summary.json": "Pond count, total and largest melt-water area (local run)",
        "results/validation_summary.json": "Detection versus Glen et al. lake outlines: precision, recall, F1, IoU",
        "results/validation_methods.csv": "Threshold comparison: Williamson 0.25, Moussavi 0.19, Otsu",
        "figures/main_result.png": "Detection versus ground truth, and threshold benchmark",
    }
    fmt = {".json": "application/json", ".csv": "text/csv", ".png": "image/png", ".md": "text/markdown"}
    for f, desc in results.items():
        crate.add_file(ROOT / f, dest_path=f, properties={"name": desc, "encodingFormat": fmt[Path(f).suffix]})


def add_subcrates(crate: ROCrate, specs: list[str]) -> None:
    """Each spec: DOI|name|public history URL. Referenced (not embedded) nested crates."""
    wfrun = ref(crate, WFRUN, {"@type": ["CreativeWork", "Profile"], "name": "Workflow Run Crate", "version": "0.5"})
    ref(crate, "https://w3id.org/ro/crate/1.1", {"@type": ["CreativeWork", "Profile"], "name": "RO-Crate", "version": "1.1"})
    for spec in specs:
        doi, name, history = (spec.split("|") + ["", ""])[:3]
        sub = ref(crate, doi, {"@type": "Dataset", "name": name,
                               "conformsTo": [{"@id": "https://w3id.org/ro/crate/1.1"}, wfrun],
                               "description": "Workflow Run RO-Crate exported by Galaxy from the workflow invocation.",
                               "encodingFormat": "application/zip"})
        if history:
            sub["subjectOf"] = ref(crate, history, {"@type": "CreativeWork", "name": f"Public Galaxy history: {name}"})
        crate.root_dataset.append_to("hasPart", sub)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--out", default="ro-crate.zip")
    ap.add_argument("--subcrate", action="append", default=[], help="DOI|name|public history URL")
    ap.add_argument("--dir", default=None, help="also write the unzipped crate to this directory")
    args = ap.parse_args()
    crate = ROCrate(version="1.2")
    add_files(crate)
    add_metadata(crate)
    add_subcrates(crate, args.subcrate)
    if args.dir:
        shutil.rmtree(args.dir, ignore_errors=True)
        crate.write(args.dir)
    crate.write_zip(args.out)
    print(f"wrote {args.out}" + (f" and {args.dir}/" if args.dir else ""))


if __name__ == "__main__":
    main()
