"""Distance from structurally complex reef.

Thresholds the multiscale roughness layer at 2.5 degrees to define complex reef, runs a
Euclidean distance transform, and samples the result at each grazing photograph.
Written to outputs/grazing_distance_to_reef.csv; a copy of that file is in data/ and is
what R/analyses.Rmd reads (Fig. 8b).
"""
import csv
import os
import numpy as np
import rasterio
from scipy import ndimage
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
GIS = os.path.join(DATA, 'gis')
OUT = os.path.join(HERE, '..', 'outputs')
os.makedirs(OUT, exist_ok=True)

THRESH = 2.5  # degrees, as used to classify complex reef in the manuscript

src = rasterio.open(os.path.join(GIS, 'Multiscale-roughness.tif'))
rough = src.read(1).astype('float32')
nod = src.nodata if src.nodata is not None else -32767
valid = (rough > nod + 1) & np.isfinite(rough)
print("raster %dx%d, %.1f m px, valid %d px (%.1f%%)" % (src.width, src.height, src.res[0], valid.sum(), 100*valid.mean()))

complex_reef = valid & (rough > THRESH)
print("complex reef (> %.1f deg): %d px = %.2f ha" % (THRESH, complex_reef.sum(), complex_reef.sum()*src.res[0]*src.res[1]/1e4))

# Euclidean distance to nearest complex-reef pixel, in metres
dist = ndimage.distance_transform_edt(~complex_reef, sampling=(src.res[1], src.res[0])).astype('float32')
dist[~valid] = np.nan
print("distance surface: median %.1f m, max %.1f m" % (np.nanmedian(dist), np.nanmax(dist)))

prof = src.profile
prof.update(dtype='float32', count=1, nodata=np.nan, compress='lzw')
with rasterio.open(os.path.join(OUT, 'distance_to_complex_reef.tif'), 'w', **prof) as dst:
    dst.write(dist, 1)

# ---- sample at the grazing photographs ----
tr = Transformer.from_crs('EPSG:4326', 'EPSG:2039', always_xy=True)
rows_out = []
for fn, sample, hcol in [('2025_04_19_Algae_transect.csv', 1, 'height_cm'),
                         ('2025_04_29_Algae_transect.csv', 2, 'algae_height')]:
    rows = list(csv.DictReader(open(os.path.join(DATA, fn))))
    n_ok = 0
    for r in rows:
        try:
            lon, lat = float(r['longitude']), float(r['latitude'])
        except (TypeError, ValueError):
            continue
        x, y = tr.transform(lon, lat)
        row, col = src.index(x, y)
        if not (0 <= row < src.height and 0 <= col < src.width):
            continue
        d = float(dist[row, col]); rr = float(rough[row, col])
        rows_out.append(dict(sample=sample, filename=r.get('filename', ''),
                             timestamp=r.get('timestamp', ''), longitude=lon, latitude=lat,
                             itm_x=round(x, 2), itm_y=round(y, 2),
                             dist_complex_reef=None if np.isnan(d) else round(d, 2),
                             roughness_1m=None if np.isnan(rr) else round(rr, 3)))
        n_ok += 1
    print("%s -> %d photographs located" % (fn, n_ok))

with open(os.path.join(OUT, 'grazing_distance_to_reef.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows_out[0].keys())); w.writeheader(); w.writerows(rows_out)

d1 = [r['dist_complex_reef'] for r in rows_out if r['sample'] == 1 and r['dist_complex_reef'] is not None]
d2 = [r['dist_complex_reef'] for r in rows_out if r['sample'] == 2 and r['dist_complex_reef'] is not None]
for lab, d in [('19 Apr', d1), ('29 Apr', d2)]:
    print("  %s: n=%d  distance %.1f - %.1f m (median %.1f)" % (lab, len(d), min(d), max(d), np.median(d)))
