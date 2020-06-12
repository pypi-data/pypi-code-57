"""
This module contains functions related to calculating flux-transfer
coefficients (sometimes called daylight coefficients).
"""
import pandas as pd
import numpy as np
import time
from matplotlib import pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sklearn.svm import SVC
from sklearn import preprocessing
# Pyrano imports
from pyrano.pointcloud import sph2cart
from pyrano.pointcloud import xyz2proj


def divide_sky(m):
    '''Returns a Pandas DataFrame with the lower, upper, left and right limits
    of the sky-segments. The basis is the Reinhart sky division. m parameter
    controls the further discretization of the Reinhart sky division. It works
    the same way as MF in radiance: m=1 gives the Reinhart sky with 145
    sky-patches (the middle of sky segment 1 points to 360 degs (North), sky
    segment 2 is the one next to it in the counter-clockwise direction); m=2
    divides each sky segment to 4 smaller sky segments except for the top one
    and results in 577 sky-patches. m=4 results in 2305 sky-patches etc.
    Segment 0 is the segment of the ground.'''
    rein_bands = np.linspace(0, 90-(84/7/m/2), 7*m, endpoint=False).tolist()
    rein_top = np.linspace(90-(84/7/m/2), 90, 1*m, endpoint=False).tolist()
    el_lims = rein_bands + rein_top + [90]
    n_az_divs = [30*m]*2*m + [24*m]*2*m + [18*m]*m + [12*m]*m + [6*m]*m + [1]
    el_low_lims = []
    el_high_lims = []
    az_left_lims = []
    az_right_lims = []
    for i in list(range(len(n_az_divs))):
        el_low_lim = el_lims[i]
        el_high_lim = el_lims[i+1]
        az_div = n_az_divs[i]
        az_right_lim = np.linspace(0 + 360/az_div/2, 360 + 360/az_div/2,
                                   az_div, endpoint=False)
        az_left_lim = az_right_lim - 360/az_div
        el_low_lims += [el_low_lim] * len(az_right_lim)
        el_high_lims += [el_high_lim] * len(az_right_lim)
        az_left_lims += az_left_lim.tolist()
        az_right_lims += az_right_lim.tolist()
    sky_seg_lims = pd.DataFrame(data={'sky_patch':range(1, len(el_low_lims) + 1),
                                      'elev_low_lims':el_low_lims,
                                      'elev_high_lims':el_high_lims,
                                      'azim_left_lims':az_left_lims,
                                      'azim_right_lims':az_right_lims})
    sky_seg_lims.set_index('sky_patch', inplace=True)
    # fixing negative azimuths
    sky_seg_lims['azim_left_lims'] += (sky_seg_lims['azim_left_lims'] < 0)*360
    sky_seg_lims['azim_right_lims'] += (sky_seg_lims['azim_right_lims'] < 0)*360
    last_seg = sky_seg_lims.index[-1]
    # suspicious fix for the last new
    sky_seg_lims.loc[last_seg, 'elev_high_lims'] = 90
    # setting ground sky segment
    sky_seg_lims.loc[0] = {'elev_low_lims':-180, 'elev_high_lims':0,
                           'azim_left_lims':0, 'azim_right_lims':360}
    sky_seg_lims.sort_index(inplace=True)
    return sky_seg_lims


def plot_sky_segments(sky_segments, dir_arrows=True, return_ax=False,
                      c_values=None, c_v_lims=None, cmap=None, r=1, alpha=0.2):
    '''Plots the sky-segments in 3D from a Pandas DataFrame made with
    divide_sky function. If return_ax is true then instead of plotting the
    function returns a matplotlib.axes object so further plots can be added to
    it. If dir_arrows is True, arrows for the 4 cardinal directions are added
    to the plot. North arrow is red, east arrow is yellow. c_values = iterable
    to color the sky segments (e.g. with DC values) if = None, the plot uses a
    default color; c_v_lims = tuple or list of 2 values for min and max range
    of coloring with c_values; cmap = matplotlib.cm colormapobject to use for
    coloring the sky segments; r = radius of the 3D sky segment plot; alpha =
    transparency of the colors in the plot.'''
    fig = plt.figure(figsize=(6,6))
    ax = Axes3D(fig, proj_type='persp')
    axlim = r/2 + 0.1*r
    ax.set_xlim(-axlim, axlim)
    ax.set_ylim(-axlim, axlim)
    ax.set_zlim(-axlim, axlim)
    # adding polygons of each sky segment to the plot: the vertices
    # (looking from the inside) start from bottom left and go counter clockwise
    if c_values is not None:
        norm = matplotlib.colors.Normalize(c_v_lims[0], c_v_lims[1])
        colors = [cmap(norm(c_value)) for c_value in c_values]
    else:
        colors = ['orange'] + ['deepskyblue'] * (len(sky_segments) - 1)
    sky_segments['colors'] = colors
    coll3ds = []
    for ss in sky_segments.index[0:-1]:
        elevations = [sky_segments.loc[ss, 'elev_low_lims']]*2
        elevations += [sky_segments.loc[ss, 'elev_high_lims']]*2
        azimuths = [sky_segments.loc[ss, 'azim_left_lims']]
        azimuths += [sky_segments.loc[ss, 'azim_right_lims']]*2
        azimuths += [sky_segments.loc[ss, 'azim_left_lims']]
        ss_coords = sph2cart(az_deg=azimuths, el_deg=elevations, r=r)
        verts = [list(zip(ss_coords['x'], ss_coords['y'], ss_coords['z']))]
        coll3d = Poly3DCollection(verts, alpha=alpha,
                         facecolor=sky_segments.loc[ss, 'colors'],
                         edgecolor='k')
        coll3ds.append(coll3d)
        ax.add_collection3d(coll3d)
        # TODO: implement plotting top sky segment later
    # top sky segment:
    top_segments = sky_segments[sky_segments['elev_high_lims'] ==
                   sky_segments.loc[sky_segments.index[-1], 'elev_low_lims']]
    elevations = top_segments['elev_high_lims']
    azimuths = sky_segments['azim_left_lims']
    ss_coords = sph2cart(az_deg=azimuths, el_deg=elevations, r=r)
    verts = [list(zip(ss_coords['x'], ss_coords['y'], ss_coords['z']))]
    coll3d = Poly3DCollection(verts, alpha=alpha,
                facecolor=sky_segments.loc[sky_segments.index[-1], 'colors'],
                edgecolor='k')
    coll3ds.append(coll3d)
    ax.add_collection3d(coll3d)
    if dir_arrows:
        # add North-South arrows
        arrow_azverts = {'n':[345, 15, 0], 's':[165, 195, 180],
                         'w':[255, 285, 270], 'e':[75, 105, 90]}
        arrow_colors = {'n':'r', 's':'b', 'w':'g', 'e':'yellow'}
        for cd in arrow_azverts.keys():
            arrow = sph2cart(az_deg=arrow_azverts[cd], el_deg=[0, 0, 0],
                             r=[1.125*r, 1.125*r, 1.25*r])
            verts = [list(zip(arrow['x'], arrow['y'], arrow['z']))]
            ax.add_collection3d(Poly3DCollection(verts, alpha=0.5,
                                facecolor=arrow_colors[cd], edgecolor='k'))
    if return_ax:
        return ax
    else:
        plt.show(block=False)


def calc_cr(sp, pointcloud, sky_grid, test_points, sky_segments, c=1, gamma=50,
            weight=2, threshold=0.5, cull_tol=1.5, return_test_points=False,
            verbose=False):
    '''Calculates Cover Ratio of a sensor point for each sky segment based on
    LiDAR point cloud input. sp: sensor_point with 'x' 'y' 'z' coordinates.
    sky_grid: a set of sky-points as training input for the SVm made with the
    uniform_grid_sphr() function. test_points: a set of points where we
    predict the sky shadedness with the SVM made with the
    test_points_for_sky_segments() function. sky_segments: sky segments made
    with the divide_sky() function. c, gamma see here:
    https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
    threshold: threshold value to binarize the SVM prediction (shaded or not
    shaded). cull_tol: angle in degrees used to reduce the density of the
    projected LiDAR points. If return_test_points = True, the test point-wise
    result is returned as well. If verbose = true, information about the
    training and prediction will be printed'''
    # move the pointcloud to view it from the place of the irrad sensorpoint
    pointcloud_sp = pd.DataFrame(data={'x':pointcloud['x'] - sp['x'],
                                       'y':pointcloud['y'] - sp['y'],
                                       'z':pointcloud['z'] - sp['z']})
    # cull and project the pointcloud to a sphere
    start = time.time()
    ptcld_sphr_proj = xyz2proj(xyz=pointcloud_sp,
                      testpoint_height=0, cull_tol=cull_tol,
                      plot_proj=False, save_projplot=False, save_proj=False,
                      proj_name='proj', cyl=False, radius=1)
    azs = list(ptcld_sphr_proj['azimuth'])
    elevs = list(ptcld_sphr_proj['elevation'])
    duration = round(time.time() - start, 2)
    if verbose:
        print(f'Pointcloud culling time = {duration} seconds')
    # preprocess the test grid
    test_grid_sky_segments = []
    for i in test_points.index:
        test_grid_sky_segments.append([test_points.loc[i, 'azim'],
                                       test_points.loc[i, 'elev']])
    test_grid_sky_segments = np.array(test_grid_sky_segments)
    # train the SVM model
    clf, scaler = svm_train(x=azs, y=elevs, skygrid=sky_grid, gamma=gamma, c=c,
                            lidarweight=weight, verbose=verbose)
    # use the SVM model to test the shadedness of the test points
    predicted = svm_predict(clf, scaler, testgrid=test_grid_sky_segments,
                            threshold=threshold, verbose=verbose)
    predicted.rename(columns={'x':'azimuth', 'y':'elevation'}, inplace=True)
    # calculate CR:
    test_points['shaded'] = (1 - predicted['shaded']).to_list()
    sf = pd.Series(index=sky_segments.index)
    for i in sky_segments.index:
        sf[i] = (test_points[test_points['segment'] == i].mean()['shaded'])
    cr = 1 - sf
    if return_test_points:
        return cr, test_points
    else:
        return cr


def calc_empty_flux_transf_coeff(sky_segments, sp_az=0, sp_el=90):
    '''Calculates the Flux transfer coefficients* of the sky and ground
    segments from a Pandas DataFrame made with the divide_sky function. These
    are the flux transfer coeffs for an empty scene, without any obstruction
    for a sensor point looking at the azimuth = sp_az and elevation = sp_el
    (in degrees) direction.
    * dE for each sky segment in equation 1 in Tregenza, P.R., 2015. Daylight
    coefficients. https://doi.org/10.1177/096032718301500201'''
    # sky segment limits
    el_low = np.radians(sky_segments['elev_low_lims'])
    el_high = np.radians(sky_segments['elev_high_lims'])
    az_left = np.radians(sky_segments['azim_left_lims'])
    c_360 = sky_segments['azim_right_lims'] <= sky_segments['azim_left_lims']
    az_right_c = sky_segments['azim_right_lims'] + c_360*360
    az_right = np.radians(az_right_c)
    # calculating DC for each sky segment
    t = np.radians(90 - sp_el) # sensor surface tilt in radians
    z = np.radians(sp_az + 180) # sensor surface azimuth in radians # WHY THE +180??
    #separate calcs for horizontal and non-horizontal dc
    if t == 0:
        dc = -0.25*(np.cos(2*el_high) - np.cos(2*el_low))*(az_right - az_left)
    else:
        dc = -0.25*((np.sin(t)*np.sin(z-az_left)*((np.sin(2*el_high) + 2*el_high) - (np.sin(2*el_low) + 2*el_low)) - np.cos(t)*az_left*(np.cos(2*el_high) - np.cos(2*el_low)))
                 - (np.sin(t)*np.sin(z-az_right)*((np.sin(2*el_high) + 2*el_high) - (np.sin(2*el_low) + 2*el_low)) - np.cos(t)*az_right*(np.cos(2*el_high) - np.cos(2*el_low))))
    dc_clip = dc.clip(0)
    dc_clip[0] = -0.5*np.pi*(np.cos(t)-1)
    return dc_clip


def calc_segment_area(sky_segments):
    '''Calculates the segment areas of the sky and ground segments from a
    Pandas DataFrame made with the divide_sky function '''
    # sky segment limits
    el_low = np.radians(sky_segments['elev_low_lims'])
    el_high = np.radians(sky_segments['elev_high_lims'])
    az_left = np.radians(sky_segments['azim_left_lims'])
    c_360 = sky_segments['azim_right_lims'] <= sky_segments['azim_left_lims']
    az_right_c = sky_segments['azim_right_lims'] + c_360*360
    az_right = np.radians(az_right_c)
    # calculating SA for each sky segment
    sa = -(az_left - az_right) * (np.sin(el_high) - np.sin(el_low))
    sa[0] = np.pi*2 # ground segment is always 2 PI
    return sa


def calc_refl_flux_transf_coeff(e_cos, cr, sky_segments, albedo):
    '''Calculates the "reflected flux transfer coefficients" for each sky
    segment. The reflected flux transfer coefficientsare re-distributed in an
    area-weighted way to the sky and ground segments'''
    e_0 = e_cos.mul((1 - cr), axis=0)
    segment_areas = calc_segment_area(sky_segments)
    delta_e = (e_cos - e_0).sum() * (1 - albedo)
    e_ref = (delta_e/segment_areas.sum()) * segment_areas * (1 - cr)
    return e_ref


def calc_refl_flux_transf_coeff_os(dc_0, dc_cos, dc_sf, sky_segments, albedo):
    '''EXPERIMENTL FUNCTION: Calculates the "reflected DC" for each sky
    segment. The reflected DC of each sky segment is distrubuted
    to the sky segments on the opposite half of the sky hemisphere and the
    ground in an area-weighted way'''
    segment_areas = calc_segment_area(sky_segments)
    segment_midpoints = pd.Series(index=sky_segments.index)
    for i in sky_segments.index:
        az_ll = sky_segments.loc[i, 'azim_left_lims']
        az_rl = sky_segments.loc[i, 'azim_right_lims']
        if np.abs(az_ll - az_rl) > 180:
            segment_midpoints[i] = (az_ll + (az_rl+360)) / 2
        else:
            segment_midpoints[i] = (az_ll + az_rl) / 2
    # collecting "opposite segments"for ech segment
    opposite_segments = []
    for i in sky_segments.index:
        cp = segment_midpoints[i]
        cp_ll = cp - 90
        cp_rl = cp + 90
        if cp_ll < 0:
            cp_ll += 360
        if cp_rl > 360:
            cp_rl -= 360
        os = []
        for sm, ii in list(zip(segment_midpoints, segment_midpoints.index)):
            if (cp >= 90 and cp <= 270):
                if ((sm < cp_ll) | (sm > cp_rl)):
                    os.append(ii)
            else:
                if ((sm < cp_ll) & (sm > cp_rl)):
                    os.append(ii)
        opposite_segments.append(os)
    # top and ground segment has all other segments as opposite
    opposite_segments[-1] = list(sky_segments.index[:-1])
    opposite_segments[0] = list(sky_segments.index[1:])
    opposite_segments = pd.Series(index=sky_segments.index, data=opposite_segments)
    # distributing the reflected dc over the opposite segments in an
    # area-weighted way
    delta_dc = (dc_cos - dc_0) * (1 - albedo)
    dc_refs = pd.Series(index=sky_segments.index, data=[float(0)]*len(sky_segments))
    segment_areas[0] = segment_areas[0] / 2 # should we halve the ground segmetn area?
    for i in sky_segments.index:
        osa = segment_areas[opposite_segments[i]].sum()
        dc_ref = delta_dc[i] / osa
        for j in opposite_segments[i]:
            dc_refs[j] = dc_refs[j] + dc_ref * segment_areas[j] * dc_sf[j]
    return dc_refs


def test_points_for_sky_segments(sky_segments, s):
    '''Generate test points for the sky segments. s = further division of sky
    segments with test points'''
    # TODO: test and doublecheck this and divide_sky if it works the same way
    # as sky division with MF in Radiance
    elevs = []
    azims = []
    segs = []
    for segment in sky_segments.index:
        el = sky_segments.loc[segment, 'elev_low_lims']
        eh = sky_segments.loc[segment, 'elev_high_lims']
        al = sky_segments.loc[segment, 'azim_left_lims']
        ar = sky_segments.loc[segment, 'azim_right_lims']
        de = (eh - el)/s
        da = (ar - al)/s
        if da < 0:
            ar += 360
            da = (ar - al)/s
            aps = np.linspace(al + da/2, ar + da/2, s, endpoint=False)
            aps -= 360
        elif da == 0:
            ar += 360
            da = (ar - al)/s
            aps = np.linspace(al + da/2, ar + da/2, s, endpoint=False)
        else:
            aps = np.linspace(al + da/2, ar + da/2, s, endpoint=False)
        eps = np.linspace(el + de/2, eh + de/2, s, endpoint=False)

        for e in eps:
            for a in aps:
                elevs.append(e)
                azims.append(a)
                segs.append(segment)
    test_points = pd.DataFrame(data={'azim':azims, 'elev':elevs,
                                     'segment':segs})
    return test_points


def read_pts_file(sps_file):
    'Reading the sps file to a dataframe'
    pts = pd.read_csv(sps_file, sep=' ', names=['x', 'y', 'z', 'vx', 'vy',
                                                'vz'])
    return pts


def write_dc_file(dc, dc_file_name, ncomp=3):
    '''Writes dc file made with pyrano. If append=True it adds a new DC line to
    an existing file'''
    # TODO: this is just a quick prototype. Make this more general later.
    ncols = dc.shape[0]
    if(len(dc.shape)) == 1:
        nrows = 1
    else:
        nrows = dc.shape[1]
    with open(dc_file_name , 'w', newline='\n') as f:
        f.write('#Pyrano\n')
        f.write('#\n')
        f.write('#\n')
        f.write('#\n')
        f.write('#\n')
        f.write('#\n')
        f.write('NCOMP={}\n'.format(str(ncomp)))
        f.write('NROWS={}\n'.format(str(nrows)))
        f.write('NCOLS={}\n'.format(str(ncols)))
        f.write('FORMAT=ascii\n')
        f.write('\n')
        if(len(dc.shape)) == 1:
            dcstr = ''
            for dc_i in dc:
                dcstr += str(dc_i) + '\t' + str(dc_i) + '\t' + str(dc_i) + '\t'
            f.write(dcstr + '\n')
        else:
            for c in dc.columns:
                dcstr = ''
                for dc_i in dc[c]:
                    dcstr += str(dc_i) + '\t' + str(dc_i) + '\t' + str(dc_i) + '\t'
                f.write(dcstr + '\n')


def uniform_grid_sphr(az_res=15, zen_res=10):
    """Create a grid uniformly in the testspace (azimuth=0-360, elevation=0-90)"""
    elevs = np.linspace(0, 90, zen_res, endpoint=False)
    azs = []
    for elev in elevs:
        elev_rad = np.radians(elev)
        azs.append(list(np.linspace(0, 360, az_res*np.cos(elev_rad), endpoint=False)))
    uniformgrid = []
    for n_row, elev in enumerate(elevs):
        uniformgrid += [[az, elev] for az in azs[n_row]]
    return np.array(uniformgrid)


def svm_train(x=[], y=[], skygrid=[], gamma=5, c=20, lidarweight=1, verbose=False):
    """x = x-values of LiDAR points. y = y-values of LiDAR points
    skygrid = a list of x's and y's where there is sky. Can be generated
    using uniform_grid or grid_reader
    gamma = gamma parameter as documented here: https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html (default = 5)
    lidarweight = how many times heavier the LiDAR points should 'weigh'
    compared to the skygrid (default = 1)"""
    # start time of training
    start = time.time()
    # create one DataFrame with the x and y values of the LiDAR points
    lidar = pd.DataFrame({'lidar_x':x, 'lidar_y':y})
    # put the lidar and skygrid DataFrame into one list
    X = np.concatenate((lidar, skygrid))
    # make a list the length of both the LiDAR and skygrid with 1's and 0's, where 1 = LiDAR and 0 = skygrid
    y = [1] * len(lidar) + [0] * len(skygrid)
    # create the SVM RBF function
    clf = SVC(C=c, cache_size=2048, class_weight='balanced', coef0=0.0,
              decision_function_shape=None, degree=3, gamma=gamma, kernel='rbf',
              max_iter=-1, probability=False, random_state=None, shrinking=False,
              tol=0.001, verbose=verbose)
    # scale the X data with the preprocessing scaler
    scaler = preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    # add desired weight to the LiDAR points
    sample_weight = [lidarweight] * len(lidar) + [1] * len(skygrid)
    # fit the data with desired weights
    clf.fit(X_scaled, y, sample_weight=sample_weight)
    # end the prediction timer and print the time
    duration = round(time.time() - start, 2)
    if verbose:
        print(f'Training time = {duration} seconds')
    return (clf, scaler)


def svm_predict(clf, scaler, testgrid=[], threshold=0.5, verbose=False):
    """clf = SVM model, scaler = scaler used to make the SVM model. Both are
    outputs from svm_train. testgrid = a list of x's and y's where we want
    to test if it's shaded or not. Can be generated using uniform_grid """
    # start time of prediction
    start = time.time()
    # scale the testgrid with the same scaler. Testgrid is aka Xtest
    Xtest_scaled = scaler.transform(testgrid)
    # predict if the points are shaded or not
    ytest = clf.decision_function(Xtest_scaled)
    # binarize the points with a certain threshold between 0 and 1, where 1 is shaded and 0 is not shaded
    ytest[ytest >= threshold] = 1
    ytest[ytest < threshold] = 0
    # create DataFrame with x and y of the points and whether the point is shaded
    try:
        # if the testgrid is a pandas DataFrame
        predicted_values = pd.DataFrame({'x':testgrid['x'], 'y':testgrid['y'],
                                        'shaded':ytest})
    except:
        # if the testgrid is a numpy array
        predicted_values = pd.DataFrame({'x':testgrid[:,0], 'y':testgrid[:,1],
                                        'shaded':ytest})
    # end the prediction timer and print the time
    duration = round(time.time() - start, 2)
    if verbose:
        print(f'Prediction time = {duration} seconds')
    # return the predicted values and the ax from the figure to use in future functions
    return predicted_values
