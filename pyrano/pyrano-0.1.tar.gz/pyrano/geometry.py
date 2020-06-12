'''This module contains functions to generate sensor points for Radiance
simulations and to work with EnergyPlus IDF geometry.
Some (most) of the functions here are from the Daypym project:
https://gitlab.tue.nl/bp-tue/daypym'''

import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt
from geomeppy.geom.transformations import align_face, invert_align_face
from geomeppy import IDF, view_geometry
from geomeppy.geom.polygons import (break_polygons, Polygon2D, Polygon3D,
                                    Vector2D, Vector3D)
from geomeppy.view_geometry import (_get_collection, _get_collections,
                                    _get_surfaces, _get_limits)
from io import StringIO
from eppy.iddcurrent import iddcurrent

def IDFsurf_to_poly(surface):
    "Makes a poly from IDF surface"
    # get its vertices
    corstrings = ['_Xcoordinate', '_Ycoordinate', '_Zcoordinate']
    vertnums = list(range(1, int(surface['Number_of_Vertices'])+1, 1))
    surf_verts = []
    for vn in vertnums:
        vert_cords = tuple([surface['Vertex_'+ str(vn) + cs] for cs in corstrings])
        surf_verts.append(vert_cords)
    # make a 3d polygon from vertices
    poly = Polygon3D(surf_verts)
    return poly


def grid_2d(bbox_2d, d, edges):
    """Creates a grid over the bbox with siden divided to n. TODO: n-ratio"""
    a = abs((bbox_2d[0] - bbox_2d[2])[0])
    b = abs((bbox_2d[0] - bbox_2d[2])[1])
    n = d * a * b
    y1 = (-(a/b + 1) + np.sqrt((a/b + 1)**2 - 4*a/b*(1 - a*b*d))) / (2 * a/b)
    y2 = (-(a/b + 1) - np.sqrt((a/b + 1)**2 - 4*a/b*(1 - a*b*d))) / (2 * a/b)
    x1 = y1* a/b
    x2 = y2* a/b
    y = max(y1, y2)
    x = y * a/b
    #print('a={}; b={}; x={}; y={}; n={}'.format(a,b,x,y,n))
    xs = (bbox_2d.vertices_list[0][0], bbox_2d.vertices_list[2][0])
    ys = (bbox_2d.vertices_list[0][1], bbox_2d.vertices_list[2][1])
    xv = np.linspace(xs[0], xs[1], round(x+1, 0))
    yv = np.linspace(ys[0], ys[1], round(y+1, 0)) # this should be a func of the reatio of width height of the bbox
    grid = np.meshgrid(xv, yv)
    if edges == False:
        lr = max(grid[0].max() - grid[0].min(), grid[1].max() - grid[1].min()) # calc the length of the module in the row-direction (longer direction)
        lc = min(grid[0].max() - grid[0].min(), grid[1].max() - grid[1].min()) # calc the length of the module in the column-direction (shorter direction)
        n_row = grid[0].shape[0]
        n_col = grid[0].shape[1]
        dr = (lr/n_row) / 2
        dc = (lc/n_col) / 2
        grid_transp = [grid[0] + dr, grid[1] + dc] # Pushing the grid to the center of the cells. Now we have a row and column of points off the surface of the pv. These are needed to be removed with gridpoints_in_poly_2d func!
        return grid_transp
    elif edges == True:
        return grid
    else:
        raise ValueError('"edges" should be = "True" or "False"')


def grid_2d_pvmodule(n_row, n_col, bbox_2d):
    """This makes a rectangular grid over the pv cells. Use the
    gridpoints_in_poly_2d on the list of arrays it returns, because this
    produces some extra points as well, that are needed to be clipped off.
    Define rows and cols as n_row > n_col!"""
    #TODO: Make it unambiguous what happens when n_row = n_col
    a = abs((bbox_2d[0] - bbox_2d[2])[0])
    b = abs((bbox_2d[0] - bbox_2d[2])[1])
    area = a * b
    d = ((n_col*n_row) + (n_row + 1) + (n_col + 1) - 1) / area # calc the point density to have 1 sp over each cell
    test_grid = grid_2d(bbox_2d=bbox_2d, d=d, edges=True) # make a 2D test grid on the x-y plane (daypym) This grid contains the edges as well. Not good yet. We will push this with half cell-size in eac direction.
    lr = max(test_grid[0].max() - test_grid[0].min(), test_grid[1].max() -
             test_grid[1].min()) # calc the length of the module in the row-direction (longer direction)
    lc = min(test_grid[0].max() - test_grid[0].min(), test_grid[1].max() -
             test_grid[1].min()) # calc the length of the module in the column-direction (shorter direction)
    dr = (lr/n_row) / 2
    dc = (lc/n_col) / 2
    test_grid_transp = [test_grid[0] + dr, test_grid[1] + dc] # Pushing the grid to the center of the cells. Now we have a row and column of points off the surface of the pv. These are needed to be removed with gridpoints_in_poly_2d func!
    return test_grid_transp


def point_in_poly(point, poly):
    "True if a 2D point is in or on the edge of a 2D poly."
    # TODO: add dynamic quasi infinite point distance with bounding box clue
    qip1_r = Vector2D(10000, 0) # quasi-infinite point 1 to the right
    qip2_r = Vector2D(10000, 1) # quasi-infinite point 2 to the right
    qip1_l = Vector2D(-10000, 0) # quasi-infinite point 1 to the left
    qip2_l = Vector2D(-10000, 1) # quasi-infinite point 2 to the left
    qip1_u = Vector2D(0, 10000) # quasi-infinite point 1 upwards
    qip2_u = Vector2D(1, 10000) # quasi-infinite point 2 upwards
    qip1_d = Vector2D(0, -10000) # quasi-infinite point 1 downwards
    qip2_d = Vector2D(1, -10000) # quasi-infinite point 2 downwards
    test_poly_r = Polygon2D([point, qip1_r, qip2_r])#.order_points('upperleftcorner') # maybe we wouldn't need this anyway
    test_poly_l = Polygon2D([point, qip1_l, qip2_l])#.order_points('upperleftcorner') # maybe we wouldn't need this anyway
    test_poly_u = Polygon2D([point, qip1_u, qip2_u])
    test_poly_d = Polygon2D([point, qip1_d, qip2_d])
    #poly = poly.order_points('upperleftcorner') # maybe we wouldn't need this anyway
    inter_r = poly.intersect(test_poly_r)
    inter_l = poly.intersect(test_poly_l)
    inter_u = poly.intersect(test_poly_u)
    inter_d = poly.intersect(test_poly_d)
    if len(inter_r) == 0:
        inter_r.append([0])
    if len(inter_l) == 0:
        inter_l.append([0])
    if len(inter_u) == 0:
            inter_u.append([0])
    if len(inter_d) == 0:
            inter_d.append([0])
    no_inter_r = len(inter_r[0])
    no_inter_l = len(inter_l[0])
    no_inter_u = len(inter_u[0])
    no_inter_d = len(inter_d[0])
    return True if no_inter_r == 3 or no_inter_l == 3 or no_inter_u == 3 or no_inter_d == 3 else False # we will see how robust this is # check this again later


def gridpoints_in_poly_2d(grid_2d, poly_2d):
    """Returns a list of points, that are inside a 2d poly. Takes a meshgrid
    (made with grid_2d) and a 2d poly as input"""
    pip = [] # list of points in poly
    for x, y in list(zip(grid_2d[0], grid_2d[1])):
        for cx, cy in list(zip(x, y)):
            test_point = Vector2D(cx, cy)
            if point_in_poly(point=test_point, poly=poly_2d):
                pip.append(test_point)
    return pip


def pos_in_module(n_row, n_col, test_grid_transp):
    """Returns a tuple of the local column and row and column (ri, ci) indexes
    within the PV module"""
    mod_pos = []
    if test_grid_transp[0].shape != (n_row+1, n_col+1):
        for c in range(n_col):
            mod_pos.append([(r, c) for r in range(n_row)])
    else:
        for r in range(n_row):
            mod_pos.append([(r, c) for c in range(n_col)])
    ri = []
    for row in mod_pos:
        ri = ri + [col[0] for col in row]
    ci = []
    for row in mod_pos:
        ci = ci + [col[1] for col in row]
    return ri, ci


def create_sensor_points(surf_name, points_in_poly_2d, row_index, col_index,
                         original_poly, sp_offset=0.01, sp_pos_round=3):
    """Returns a dict {'surf_name':surface name, 'sensor_points':list of sensor
    points, 'ri':row_index, 'ci':col_index, 'sp_ori':list of normal vectors}.
     sesor points are translated with sp_offset from the original plane. Takes
     points_in_poly_2d (made with gridpoints_in_poly_2d function) and the
     original poly as input. We can round the coords of the sps. Make sure,
     that the rounding has more digits, than the smallest distances and the
     offset. Default is 1 cm offset and 1 mm rounding."""
    # make a 3D polygon from these points and rotate them back
    sensor_points_poly_trans = Polygon3D(points_in_poly_2d)
    sensor_points_poly = invert_align_face(original=original_poly,
                                           poly2=sensor_points_poly_trans)
    normal_vectors = np.array([original_poly.normal_vector[0],
                              original_poly.normal_vector[1],
                              original_poly.normal_vector[2]])
    transl_vect = normal_vectors * sp_offset
    sensor_points = [list(np.add(tuple([round(sp[i], sp_pos_round) for i in range(len(sp))]), transl_vect)) for sp in sensor_points_poly.vertices_list] # sorry
    sensor_points_surf = {'surf_name':surf_name,
                          'surf_coords':original_poly.vertices_list,
                          'sensor_points':sensor_points,
                          'ri':row_index,
                          'ci':col_index,
                          'sp_ori':list(normal_vectors)} # make a dict for the sensor points with name points and vectors, later export this to DS file
    return sensor_points_surf


def xyz_coords_from_sps(sps):
    """Takes sps dict as input. Extracts x, y, z coords from an sps dict made
    with the create_sensor_points() or the pointgrid_over_surface() function"""
    x, y, z = ([] for i in list(range(3)))
    for p in sps:
        x += [c[0] for c in p['sensor_points']]
        y += [c[1] for c in p['sensor_points']]
        z += [c[2] for c in p['sensor_points']]
    return pd.DataFrame(data={'x':x, 'y':y, 'z':z})


def translate_to_ds_pts(surf_sensor_points, p_name, grid_method, fname=None):
    """Translates and saves the sensorpoints as a .pts file.
    Inputs: grid_method: use grid_method = "pv_module" for saving sensor point
    metadata to simulate irradiance for PVMismatch simulations.
    Use grid_method = "point_density" for saving metadata for general
    irradiance simulation purposes.
    Also saves a csv or json with additional info useful for postprocessing.
    If fname != the sps will be saved to the given location not the default pts
    folder"""
    x, y, z, vx, vy, vz, surf_name, ri, ci = ([] for i in list(range(9)))
    for surf in surf_sensor_points:
        for i in list(range(len(surf['sensor_points']))):
            x.append(surf['sensor_points'][i][0])
            y.append(surf['sensor_points'][i][1])
            z.append(surf['sensor_points'][i][2])
            vx.append(surf['sp_ori'][0])
            vy.append(surf['sp_ori'][1])
            vz.append(surf['sp_ori'][2])
            surf_name.append(surf['surf_name'])
            if grid_method == 'pv_module':
                ri.append(surf['ri'][i])
                ci.append(surf['ci'][i])
                spdf = pd.DataFrame(data={'x':x, 'y':y, 'z':z, 'vx':vx,
                                          'vy':vy, 'vz':vz, 'ri':ri, 'ci':ci,
                                          'surf_name':surf_name})
            elif grid_method == 'point_density':
                spdf = pd.DataFrame(data={'x':x, 'y':y, 'z':z, 'vx':vx,
                                          'vy':vy, 'vz':vz,
                                          'surf_name':surf_name})
            else:
                raise ValueError('"grid_method" should be = "pv_module" or "point_density"')
    spdf.index.name = 'sp_index'
    if fname == None:
        savepath = r'pts/'
        save_fname = p_name
    else:
        savepath = r''
        save_fname = fname
    ptsfile = open(r'{}{}.pts'.format(savepath, save_fname), 'w')
    for p in spdf.index:
        ptsfile.write(str(spdf['x'][p]) +' '+ str(spdf['y'][p]) +' '+
                      str(spdf['z'][p]) +' '+ str(spdf['vx'][p]) +' '+
                      str(spdf['vy'][p]) +' '+ str(spdf['vz'][p]) + '\n')
    ptsfile.close()
    # saving metadatata of sensor points in csv or json format
    spdf.to_csv(r'{}{}.csv'.format(savepath, save_fname))
    for s in surf_sensor_points:
        spi = spdf[spdf['surf_name']==s['surf_name']].index.tolist()
        s.update({'sp_index':[int(i) for i in spi]})
    with open(r'{}{}.json'.format(savepath, save_fname), 'w') as fp:
        json.dump(surf_sensor_points, fp, indent=4)
    return


def view_idf_to_ax(fname=None, idf_txt=None, test=False):
    """This is originally from https://github.com/jamiebull1/geomeppy/blob/master/geomeppy/view_geometry.py
    This just returns an ax instead of viewing it on order to  plot it together
    with the sensorpoints"""
    # type: (Optional[str], Optional[str], Optional[bool]) -> None
    if fname and idf_txt:
        raise ValueError("Pass either fname or idf_txt, not both.")
    # set the IDD for the version of EnergyPlus
    iddfhandle = StringIO(iddcurrent.iddtxt)
    if IDF.getiddname() is None:
        IDF.setiddname(iddfhandle)
    if fname:
        # import the IDF
        idf = IDF(fname)
    elif idf_txt:
        idf = IDF()
        idf.initreadtxt(idf_txt)
    # create the figure and add the surfaces
    ax = plt.axes(projection="3d")
    collections = _get_collections(idf, opacity=0.5)
    for c in collections:
        ax.add_collection3d(c)
    # calculate and set the axis limits
    limits = _get_limits(idf=idf)
    ax.set_xlim(limits["x"])
    ax.set_ylim(limits["y"])
    ax.set_zlim(limits["z"])
    return ax


def view_idf_and_sps(p_name, idf_name, sps, savefig=False, return_ax=False):
    """To view the e+ IDF and the DS sensorpoints together. Utilizing modified
    version of Geomeppy view_idf function:
    https://github.com/jamiebull1/geomeppy/"""
    # TODO implement auto save fig: Save_fig False: no saving, True: save it to /geo
    surfcoords = []
    polys = []
    for surf in sps:
        polys.append(Polygon3D(surf['surf_coords']))
        for sp in surf['sensor_points']:
            surfcoords.append((sp[0], sp[1], sp[2]))
    xs = [c[0] for c in surfcoords]
    ys = [c[1] for c in surfcoords]
    zs = [c[2] for c in surfcoords]
    ax2 = view_idf_to_ax(fname=idf_name, idf_txt=None, test=False)
    ax2.scatter(xs, ys, zs, marker='o', s=2, c='k')
    if savefig:
        try:
            plt.savefig('geo/{}.png'.format(p_name))
        except:
            plt.savefig('{}.png'.format(p_name))
    if return_ax:
        return ax2
    else:
        plt.show(block=False)


def write_manual_sp(pts_file, x, y, z, vx, vy, vz, append=False):
    '''Writes a pts sensor point file. x, y, z are the coordinates of the point
    and vx, vy, vz are the coordinates of the direction vector of the point.
    If append = True, a point will be added to teh pts file in a new line, else
    the pts file is overriden.'''
    if append:
        with open(pts_file, 'a' , newline='\n') as f:
            f.write('{} {} {} {} {} {}\n'.format(x, y, z, vx, vy, vz))
    else:
        with open(pts_file, 'w' , newline='\n') as f:
            f.write('{} {} {} {} {} {}\n'.format(x, y, z, vx, vy, vz))


def pointgrid_over_surface(surface, d=5, edges=True, sp_offset=0.01):
    """Wrapper function for create_sensor_points(). Inputs:
    surface: IDF urface (via geomeppy), d: desired point density sps/m2
    edges: bool to decide if we want poits on the edge of the surface,
    sp_offset: offset of sensorpoints from the surface in m. Returns a dict:
    {'surf_name':surface name, 'sensor_points':list of sensor points,
    'ri':row_index, 'ci':col_index, 'sp_ori':list of normal vectors}."""
    # make poly from idf (daypym)
    poly = IDFsurf_to_poly(surface=surface)
    # translate poly to the x-y plane (geomeppy)
    poly_trans = align_face(poly).order_points('upperleftcorner')
    # make the poly 2D (geomeppy)
    poly_trans_2d = poly_trans.project_to_2D()
    # make a 2d bbox of the translated surface on the xy pane (geomeppy)
    poly_trans_bbox_2d = poly_trans.bounding_box.project_to_2D()
    # make a 2D test grid on the x-y plane (daypym)
    test_grid = grid_2d(bbox_2d=poly_trans_bbox_2d, d=d, edges=edges)
    # makes a list of points, that are inside the 2D poly (daypym)
    pip = gridpoints_in_poly_2d(grid_2d=test_grid, poly_2d=poly_trans_2d)
    # sensor point data dict (daypym)
    sp = create_sensor_points(surf_name=surface['Name'], points_in_poly_2d=pip,
    row_index=[0], col_index=[0], original_poly=poly, sp_offset=sp_offset,
    sp_pos_round=3)
    return sp


def pointgrid_over_pvmodule(surface, n_row=10, n_col=6, sp_offset=0.01):
    """Wrapper function to create sensot points over each cell of a pv module.
    Inputs: surface: IDF urface (via geomeppy), n_row: number of cell-rows in
    the PV module n_col: number of cell-columns in the PV module
    sp_offset: offset of sensorpoints from the surface in m. Returns a dict:
    {'surf_name':surface name, 'sensor_points':list of sensor points,
    'ri':row_index, 'ci':col_index, 'sp_ori':list of normal vectors}."""
    # make poly from idf (daypym)
    poly = IDFsurf_to_poly(surface=surface)
    # translate poly to the x-y plane (geomeppy)
    poly_trans = align_face(poly).order_points('upperleftcorner')
    # make the poly 2D (geomeppy)
    poly_trans_2d = poly_trans.project_to_2D()
    # make a 2d bbox of the translated surface on the xy pane (geomeppy)
    poly_trans_bbox_2d = poly_trans.bounding_box.project_to_2D()
    # make a 2D test grid on the x-y plane (daypym)
    test_grid = grid_2d_pvmodule(n_row=n_row, n_col=n_col,
                                 bbox_2d=poly_trans_bbox_2d)
    # makes a list of points, that are inside the 2D poly (daypym)
    pip = gridpoints_in_poly_2d(grid_2d=test_grid, poly_2d=poly_trans_2d)
    # row and column index information
    ri, ci = pos_in_module(n_row=n_row, n_col=n_col, test_grid_transp=test_grid)
    # sensor point data dict (daypym)
    sp = create_sensor_points(surf_name=surface['Name'], points_in_poly_2d=pip,
    row_index=ri, col_index=ci, original_poly=poly, sp_offset=sp_offset,
    sp_pos_round=3)
    return sp
