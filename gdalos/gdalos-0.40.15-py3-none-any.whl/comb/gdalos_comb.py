import os
import glob
import gdal
import tempfile
from pathlib import Path
from gdalos import gdal_helper, get_extent, GeoRectangle
from comb.gdal_calc1 import Calc, AlphaList
from gdal_color_helper import make_color_table


def do_comb(filenames, outfile, color_table):
    kwargs = dict()
    calc = None
    for filename, alpha in zip(filenames, AlphaList):
        kwargs[alpha] = filename
        alpha1 = '{}*({}>3)'.format(1, alpha)
        # alpha1 = alpha
        if calc is None:
            calc = alpha1
        else:
            calc = '{}+{}'.format(calc, alpha1)
        # break
    Calc(calc, color_table=color_table, outfile=str(outfile), **kwargs)
    # Calc("A+B", A="input1.tif", B="input2.tif", outfile="result.tif")


def combine(dirpath, outpath, color_table):
    extents = []
    filenames = []
    dss = []
    union_extent = None
    intersect_extent = None
    for filename in glob.glob(str(dirpath)):
        # print(filename)
        ds = gdal_helper.open_ds(filename)
        org_points_extent, _ = get_extent.get_points_extent_from_ds(ds)
        extent = GeoRectangle.from_points(org_points_extent)

        filenames.append(filename)
        dss.append(ds)
        extents.append(extent)
        if union_extent is None:
            union_extent = extent
            intersect_extent = extent
        else:
            intersect_extent = intersect_extent.intersect(extent)
            union_extent = union_extent.union(extent)

    vrt_filenames = build_vrts(filenames, dss, union_extent, '_u.vrt')
    outfile = tempfile.mktemp(suffix='_union_combine.tif', dir=str(outpath))
    # outfile = outpath / suffix
    do_comb(vrt_filenames, outfile, color_table)

    vrt_filenames = build_vrts(filenames, dss, intersect_extent, '_i.vrt')
    outfile = tempfile.mktemp(suffix='_intersect_combine.tif', dir=str(outpath))
    # outfile = outpath / suffix
    do_comb(vrt_filenames, outfile, color_table)
    return filenames, extents


def build_vrts(filenames, dss, extent: GeoRectangle, suffix):
    vrt_filenames = []
    for filename, ds in zip(filenames, dss):
        options = gdal.BuildVRTOptions(outputBounds=(extent.min_x, extent.min_y, extent.max_x, extent.max_y),
                                       hideNodata=True,
                                       separate=False)
        out_vrt = filename + suffix
        vrt_filenames.append(out_vrt)
        out_ds = gdal.BuildVRT(out_vrt, ds, options=options)
        if out_ds is None:
            return None
        del out_ds
    return vrt_filenames


if __name__ == '__main__':
    color_filename = r'd:\dev\TaLoS\data\grid_comb\comb_color_file.txt'
    color_table = make_color_table(color_filename)

    # path = Path(r'd:\dev\TaLoS\data\6comb\1')
    path = Path(r'd:\dev\TaLoS\data\grid_comb')
    outpath = path / 'comb'
    pattern = Path('*.tif')
    os.makedirs(str(outpath), exist_ok=True)
    dirpath = path / pattern
    filenames, extents = combine(dirpath, outpath, color_table)

    print(filenames)
    print(extents)
