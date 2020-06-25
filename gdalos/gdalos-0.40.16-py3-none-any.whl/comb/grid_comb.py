from gdalos import gdalos_trans
from gdalos import GeoRectangle
from pathlib import Path


def crop_map(extent, output_path):
    filename = r'd:\Maps\w84u36\SRTM1_hgt.x[27.97,37.98]_y[27.43,37.59].cog.tif'
    out_filename = Path(output_path) / Path('srtm_grid.tif')
    gdalos_trans(filename, extent=extent, extent_in_4326=False, out_filename=out_filename)
    # talos.ShowMessage(filename)


def calc_extent(center, grid_range, interval, md, frame):
    # i is for x-y;
    # j is for min and max values of the grid
    # k is for the sign (to subtract or to add) the max_range
    minmax = [center[i] + grid_range[j] * interval + k * (md + frame) for i in (0, 1) for j, k in zip((0, -1), (-1, 1))]
    full_extent = GeoRectangle.from_min_max(*minmax)
    return full_extent


def talos_run(md, interval, grid_range, center, oz, tz, output_path):
    import talos
    save_to_file = True
    classname = 'TFieldOfSight'
    talos.DeleteObjects(classname)
    talos.SetScriptWGSGeo(False)

    for i in grid_range:
        for j in grid_range:
            ox = center[0] + i * interval
            oy = center[1] + j * interval
            p = (ox, oy)
            f = talos.CreateObject(classname)
            name = '{}_{}'.format(i, j)
            talos.SetVal(f, 'Name', name)
            talos.SetVal(f, 'Geometry', p)
            talos.SetVal(f, 'Range', md)
            talos.SetVal(f, 'Height', oz)
            talos.SetVal(f, 'TargetHeight', tz)
            talos.Run('FieldOfSight')
            if save_to_file:
                filename = output_path / (name + '.tif')
                # talos.ShowMessage(filename)
                talos.RasterSaveToFile(f, str(filename), False)
    if save_to_file:
        combined = talos.GetObjects('TGlobalFOS')[0]
        filename = output_path / 'combined.tif'
        # talos.ShowMessage(filename)
        talos.RasterSaveToFile(combined, str(filename), False)


def main():
    md = 2000
    interval = md / 2
    j = 1
    grid_range = range(-j, j + 1)
    center = (700_000, 3550_000)
    oz = 10
    tz = 100
    frame = 500
    output_path = Path(r'd:\dev\TaLoS\data\grid_comb')

    full_extent = calc_extent(center, grid_range, interval, md, frame)
    crop_map(full_extent, output_path)
    # return full_extent

    talos_run(md, interval, grid_range, center, oz, tz, output_path)


if __name__ == "__main__":
    main()
