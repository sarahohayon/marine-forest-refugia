"""Patch-level grazing distance at site 1 (Results 3.2, Table S1).

Distance from each algal edge pixel to the nearest complex-reef pixel is summarised two
ways: across all ~30,000 edge pixels (edge-wide mean), and averaged within each discrete
algal patch with a bootstrap confidence interval across patches (patch-level mean).
"""
import os
import numpy as np, rasterio
GIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'gis')
from scipy import ndimage

rng = np.random.default_rng(42)

def patch_stats(dist_path, mask_path=None, label=""):
    d = rasterio.open(dist_path); dist = d.read(1).astype('float32')
    nod = d.nodata
    valid = np.isfinite(dist) if nod is None else (dist != nod) & np.isfinite(dist)
    if mask_path:
        m = rasterio.open(mask_path); algae = m.read(1) > 0
    else:
        algae = valid & (dist > 0)
    lab, n = ndimage.label(algae)
    # edge pixels of each patch = algae pixels touching a non-algae pixel
    er = ndimage.binary_erosion(algae, structure=np.ones((3, 3)))
    edge = algae & ~er
    means, sizes = [], []
    for pid in range(1, n + 1):
        sel = (lab == pid) & edge & valid
        if sel.sum() == 0: continue
        v = dist[sel]
        means.append(float(v.mean())); sizes.append(int(sel.sum()))
    means = np.array(means); sizes = np.array(sizes)
    allpix = dist[algae & edge & valid]
    print("\n=== %s ===" % label)
    print("  patches: %d | edge pixels: %d" % (len(means), sizes.sum()))
    print("  PIXEL-level  : mean %.2f m, SD %.2f, SE %.3f  (n = %d pixels)" %
          (allpix.mean(), allpix.std(ddof=1), allpix.std(ddof=1)/np.sqrt(len(allpix)), len(allpix)))
    print("  PATCH-level  : mean %.2f m, SD %.2f, SE %.2f   (n = %d patches)" %
          (means.mean(), means.std(ddof=1), means.std(ddof=1)/np.sqrt(len(means)), len(means)))
    # weighted by patch size, and a non-parametric bootstrap over patches
    w = sizes / sizes.sum()
    wmean = float((means * w).sum())
    boot = np.array([np.mean(rng.choice(means, size=len(means), replace=True)) for _ in range(5000)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print("  patch-size-weighted mean: %.2f m" % wmean)
    print("  bootstrap over patches  : 95%% CI %.2f - %.2f m" % (lo, hi))
    print("  --> SE inflates %.0fx when patches rather than pixels are the unit" %
          ((means.std(ddof=1)/np.sqrt(len(means))) / (allpix.std(ddof=1)/np.sqrt(len(allpix)))))
    return means

patch_stats(os.path.join(GIS, 'site1_distance_to_complex_reef.tif'), os.path.join(GIS, 'site1_algae_mask.tif'),
            "Site 1 - algal patches (manuscript: 32.3 m edge-wide; 20.5 m patch mean)")
