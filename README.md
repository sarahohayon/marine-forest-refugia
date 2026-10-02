# Low-complexity reefs as refugia for Mediterranean marine forests

Data and code for:

> Ohayon, S., et al. Low-Complexity Reefs Act as Refugia for Mediterranean Marine Forests under Intense Herbivory by Invasive Rabbitfish. *Marine Environmental Research* (in revision).

The code reproduces every statistical result and every data figure in the paper
(Figs 5, 7, 8 and 10), plus the GIS distance metrics used in Fig. 8b and Table S1.

## Repository layout

```
data/                    input data (CSV) and GIS rasters (data/gis)
R/analyses.Rmd           all statistical models and Figs 5, 7, 8, 10
python/01_distance_to_complex_reef.py   distance of each photographed plant to complex reef (input to Fig. 8b)
python/02_patch_grazing_distance.py     site-1 grazing distance, edge-wide and patch-level (Results 3.2, Table S1)
figures/                 figures as produced by R/analyses.Rmd
```

## Figures

| Figure | Content | Produced by |
|---|---|---|
| 1 | Field photographs, grazing halos | photographs, not code |
| 2 | Study-area map | QGIS 3.40.5 |
| 3 | Substrate roughness and UVC design | QGIS (roughness raster in `data/gis`) |
| 4 | Grazing-status photographs | photographs |
| 5 | Macroalgal cover vs distance from complex reef (2010) | `R/analyses.Rmd`, chunk `figure 5` |
| 6 | Seascape configuration at the two sites | QGIS; distances from `python/02_patch_grazing_distance.py` |
| 7 | Fish community and macroalgal height vs visual complexity; rabbitfish share of biomass | `R/analyses.Rmd`, chunk `figure 7` (fish drawings in panel e added by hand) |
| 8 | Macroalgal height vs roughness; grazing status vs distance | `R/analyses.Rmd`, chunks `figure 8a/8b/8`; distances from `python/01_...` |
| 9 | Translocation photographs | photographs |
| 10 | Fish functional-group MaxN, translocation vs control | `R/analyses.Rmd`, chunks `maxn by guild`, `figure 10` |

## How to run

R (from the `R/` folder):

```r
rmarkdown::render("analyses.Rmd")   # writes analyses.html and the figures to ../figures
```

Python (from the `python/` folder):

```bash
python 01_distance_to_complex_reef.py   # writes ../outputs/grazing_distance_to_reef.csv
python 02_patch_grazing_distance.py
```

`data/grazing_distance_to_reef.csv` is the output of script 01 and is what the R analysis
reads, so the R part runs without the Python step.

## Software

Tested with R 4.3.3 (mgcv 1.9.1, tidyverse 2.0.0, ggplot2 3.4.4, ggpubr 0.6.0,
patchwork 1.2.0, rmarkdown 2.25) and Python 3.11 (numpy 2.4, scipy 1.17, rasterio 1.4,
pyproj 3.7). GIS layers were prepared in QGIS 3.40.5; the multiscale roughness layer was
computed with WhiteboxTools MultiscaleRoughness (radii 1–10 cells, 0.5–5 m; maximum
across scales). All spatial data are in EPSG:2039 (Israel 1993 / Israeli TM Grid).

## Data files

| File | Description |
|---|---|
| `bat_galim_fish_2024_2025_analysis.csv` | Underwater visual census, fish records (one row per species × size class × transect); artificial-substrate sites removed |
| `bat_galim_algae_2024_2025_analysis.csv` | Habitat points per UVC transect: visual complexity and macroalgal height |
| `fish_algae_data.csv` | Transect-level summary used in the models: biomass, abundance, richness, mean visual complexity, mean macroalgal height, depth, site, season |
| `species_a_b.csv` | Length–weight coefficients (a, b) per species, from FishBase |
| `2025_04_19_Algae_transect.csv`, `2025_04_29_Algae_transect.csv` | Photographed plants along the two grazing transects: species, height, grazing status, coordinates |
| `2025_04_29_complexity_layer.csv` | Substrate roughness sampled under each plant of the 29 April transect |
| `grazing_distance_to_reef.csv` | Distance of each photographed plant to the nearest complex-reef pixel (output of python/01) |
| `seascape_experiments_data.csv` | Translocation experiment stations: date, treatment, camera, rabbitfish MaxN |
| `MaxN_seascape_experiments.csv` | MaxN per species per video in the translocation experiments |
| `shikmona_achziv_2010.csv` | 2010 surveys at Carmel Head (Shikmona) and Achziv: mean percent cover ± SE of turf and canopy along distance from the reef edge |
| `gis/Multiscale-roughness.tif` | Multiscale substrate roughness (degrees), 1 m |
| `gis/site1_algae_mask.tif`, `gis/site1_distance_to_complex_reef.tif` | Site 1 algal-patch mask and distance-to-complex-reef surface, 0.5 m |

## License

Code: MIT. Data: CC BY 4.0.
