import functools
import numpy as np
import numba

# Backup tqdm wrapper

def notqdm(x, *args, **kwargs):
    return x

# === Functions for handling 3D projection math ===

@numba.jit(nopython=True)
def proj3d_make(w, h, ex, ey, origin, target, dclip, pclip, mindist = -1000000.0, cz = 0, d = 1, f = None):
    # Build transform from x, y, z into [-1, 1]**2, d space
    
    print('Making transform')
    print(origin)
    print(target)

    ed = target - origin;
    ed /= np.linalg.norm(ed);
    
    print(ed)

    A = np.stack((ex, ey, ed), axis = 1);
    A = np.linalg.inv(A);
    
    print(A)

    b = np.dot(A, -origin);
    #c = np.asarray([0., 0., cz]);
    c = cz * ed
    d = d - np.dot(origin, c)
    
    print(b)
    print(c)
    #d = 1.;
    
    clip_abc = dclip;
    clip_d = -np.dot(dclip, pclip);

    return (w, h, A, b, c, d, clip_abc, clip_d, mindist);

@numba.jit(nopython=True)
def proj3d_apply(proj, x):
    w, h, A, b, c, d, clip_abc, clip_d, mindist = proj;
    
    tmp = (A @ x + b) / (np.dot(x, c) + d);
        
    # Rescale from [-1, 1] to [0, w] resp. [0, h]
    tmp[0] = 0.5 * w * (1 + tmp[0]);
    tmp[1] = 0.5 * h * (1 + tmp[1]);

    return tmp;

@numba.jit(nopython=True)
def proj3d_apply_unscaled(proj, x):
    w, h, A, b, c, d, clip_abc, clip_d, mindist = proj;
    
    unscaled = A @ x + b
        
    return unscaled

@numba.jit(nopython=True)
def tdot(x, y):
    return np.asarray([
        [x[0] * y[0], x[0] * y[1], x[0] * y[2]],
        [x[1] * y[0], x[1] * y[1], x[1] * y[2]],
        [x[2] * y[0], x[2] * y[1], x[2] * y[2]]
    ]);
    
@numba.jit(nopython=True)
def proj3d_deriv(proj, x):
    w, h, A, b, c, d, clip_abc, clip_d, mindist = proj;
    
    hc = np.dot(c, x) + d;
    y = np.dot(A, x) + b;

    result = A / hc - tdot(y, c) / (hc**2);

    result[0] *= 0.5 * w;
    result[1] *= 0.5 * h;

    return result;

@numba.jit(nopython=True)
def proj3d_clip(proj, p):
    w, h, A, b, c, d, clip_abc, clip_d, mindist = proj;
    
    if np.dot(p, clip_abc) + clip_d > 0:
        return True;
    
    return False;
    
# === Functions for rasterization ===

@numba.jit(nopython=True)
def cross(x1, x2):
    return np.asarray([
        x1[1] * x2[2] - x1[2] * x2[1],
        x1[2] * x2[0] - x1[0] * x2[2],
        x1[0] * x2[1] - x1[1] * x2[0]
    ]);
    
@numba.jit(nopython=True)
def rasterize_triangle(proj, dbuf, detbuf, p1, p2, p3, ptol = 0.5, dtol = 1e-3):
    projpoints = np.stack((proj3d_apply(proj, p1), proj3d_apply(proj, p2), proj3d_apply(proj, p3)), axis = 0);
    #print('Projected points: {}'.format(projpoints));
    
    xmin = np.min(projpoints[:,0]) - ptol;
    xmax = np.max(projpoints[:,0]) + ptol;
    ymin = np.min(projpoints[:,1]) - ptol;
    ymax = np.max(projpoints[:,1]) + ptol;
    
    xmin = max(xmin, 0);
    ymin = max(ymin, 0);
    
    xmax = min(xmax, dbuf.shape[0] - 1);
    ymax = min(ymax, dbuf.shape[1] - 1);
    
    xmin = int(np.floor(xmin));
    xmax = int(np.ceil(xmax));
    ymin = int(np.floor(ymin));
    ymax = int(np.ceil(ymax));
    
    if xmax < xmin or ymax < ymin:
        return;
    
    # Matrix that maps from triangle- into 3D space
    mat = np.stack(((p2 - p1), (p3 - p1)), axis = 1);
    realspace_det = np.linalg.norm(cross(p2 - p1, p3 - p1));
    
    tribuf_shape = (xmax + 1 - xmin, ymax + 1 - ymin)
    tri_dbuf   = np.zeros(tribuf_shape)
    tri_dbuf[:] =np.inf
    tri_detbuf = np.zeros(tribuf_shape)
    
    # Check if triangle partially clips behind the camera
    if proj3d_apply_unscaled(proj, p1)[2] < proj[-1]:
        return
    
    if proj3d_apply_unscaled(proj, p2)[2] < proj[-1]:
        return
    
    if proj3d_apply_unscaled(proj, p3)[2] < proj[-1]:
        return
        
    
    for x in numba.prange(xmin, xmax + 1):
        for y in numba.prange(ymin, ymax + 1):
            # Reconstruct the pixel position on the triangle (in triangle coordinates)
            # using Newton's method
            p = np.asarray([0.3, 0.3]);
            target = np.asarray([x, y])
            
            p0 = p

            for iter in range(0, 10):
                p3d = p1 + p[0] * (p2 - p1) + p[1] * (p3 - p1);
                p2d = proj3d_apply(proj, p3d);

                deriv = proj3d_deriv(proj, p3d)[:2, :];
                deriv = np.dot(deriv, mat);

                if np.abs(np.linalg.det(deriv)) < 1e-10:
                    #w, h, A, b, c, d, clip_abc, clip_d, mindist = proj;
                    #print('Reconstruction breakdown')
                    #print(p0)
                    #print(p)
                    #print(p3d)
                    #print(p2d)
                    #print(target)
                    #print(deriv)
                    #hc = np.dot(c, p3d) + d;
                    #y2 = np.dot(A, p3d) + b;
                    #print(hc)
                    #print(y2)
                    #print(A / hc)
                    #print(tdot(y2, c) / (hc**2))
                    #
                    #raise(ValueError('Numerical breakdown'))
                    break;

                deriv_inv = np.linalg.inv(deriv);
                delta = np.dot(deriv_inv, target - p2d[0:2]);

                p += delta;

                if(np.linalg.norm(delta) < 1e-3):
                    break;
                
                if p[0] < -9:
                    p[0] = 0
                if p[1] < -9:
                    p[1] = 0
                
                if p[0] + p[1] > 10:
                    scale = 1 / (p[0] + p[1])
                    p[0] *= scale
                    p[1] *= scale

            # If the position of the reconstructed pixel on the triangle is inaccurate,
            # skip it
            if np.linalg.norm(p2d[0:2] - target) > 0.1:
                continue;

            # If the pixel is outside the triangle, see if we can get a close point inside
            if p[0] < 0 or p[1] < 0 or p[0] + p[1] > 1:                        
                # Check how far we have to move the pixel to get it back into the triangle
                dup = p[0] + p[1];

                if dup > 1:
                    p[0] -= 0.5 * (dup - 1);
                    p[1] -= 0.5 * (dup - 1);

                # Project point into triangle
                p[0] = max(p[0], 0.0);
                p[1] = max(p[1], 0.0);

                p[0] = min(p[0], 1.0);
                p[1] = min(p[1], 1.0);

                if not(p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= 1 + 1e-5):
                    #print(p);
                    assert False;

                p3d = p1 + p[0] * (p2 - p1) + p[1] * (p3 - p1);
                p2d_new = proj3d_apply(proj, p3d);

                if np.linalg.norm(p2d_new[0:2] - p2d[0:2]) > ptol:
                    #print('Discarded');
                    continue;

                p2d = p2d_new;

            if p2d[2] < proj[-1]:
                #print('Point discarded due to being too close to camera')
                continue;

            #if p3d[2] > 0:
            #    continue;
            if proj3d_clip(proj, p3d):
                continue;

            pixel_det = abs(np.linalg.det(deriv));
            detratio = pixel_det / realspace_det;
            
            tri_dbuf[x-xmin, y-ymin] = proj3d_apply_unscaled(proj, p3d)[2]
            tri_detbuf[x-xmin, y-ymin] = detratio

    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            d = tri_dbuf[x-xmin, y-ymin]
            detratio = tri_detbuf[x-xmin, y-ymin]
            
            if d > dbuf[x, y]:
                if d < dbuf[x, y] + dtol:
                    detbuf[x, y] = max(detbuf[x, y], detratio);

                continue;
            else:
                if d > dbuf[x, y] - dtol:
                    detbuf[x, y] = max(detbuf[x, y], detratio);
                else:
                    detbuf[x, y] = detratio;

            dbuf[x,y] = d;

@numba.jit(nopython=True)
def rasterize_polygon(proj, dbuf, detbuf, poly, ptol = 0.5, dtol = 1e-3):
    if poly.shape[0] < 3:
        return;
    
    p0 = poly[0];
    
    for i in range(2, poly.shape[0]):
        p1 = poly[i-1];
        p2 = poly[i];
        
        rasterize_triangle(proj, dbuf, detbuf, p0, p1, p2, ptol, dtol);

#@numba.jit(forceobj=True)
def rasterize_polygons(proj, dbuf, detbuf, polies, ptol = 0.5, dtol = 1e-3):
    for poly in polies:
        rasterize_polygon(proj, dbuf, detbuf, poly, ptol, dtol);

# Transformation functions    
def transform_polygon(proj, poly):    
    if proj3d_clip(proj, poly[0]):
        return np.zeros([0, 2]);
        
    h = proj[1]
    
    def process(x):
        return np.asarray([x[0], h - x[1]]);
    
    return [
        process(proj3d_apply(proj, p)[:2]) for p in poly
    ];

def transform_polygons(proj, polies):
    return [transform_polygon(proj, p) for p in polies];
    
@numba.jit(nopython=True)
def put_point(proj, p, dbuf, pbuf, dtol = 1e-3):
    p2d = proj3d_apply(proj, p);
    
    x = int(round(p2d[0]));
    y = int(round(p2d[1]));
    
    if proj3d_clip(proj, p):
        return;
    
    if x < 0 or y < 0 or x >= dbuf.shape[0] or y >= dbuf.shape[1]:
        return;
    
    if p2d[2] > dbuf[x, y] + dtol:
        return;
    
    if p2d[2] < dbuf[x, y] - dtol:
        return;
    
    pbuf[x, y] += 1;

@numba.jit(nopython=True)
def put_points(proj, ps, dbuf, pbuf, dtol = 1e-3):
    for i in range(0, ps.shape[1]):
        put_point(proj, ps[:,i], dbuf, pbuf, dtol = dtol);

class HFCamera:
    def __init__(self, w, h, phi, theta, htilt, r_target, z_target, d_cam, p_clip, d_clip, zoom, cz, d, meshes, tqdm = notqdm):
        e_r = np.asarray([np.cos(phi), np.sin(phi), 0.0], dtype=np.float64)
        e_phi = np.asarray([-np.sin(phi), np.cos(phi), 0.0], dtype=np.float64)
        e_z   = np.asarray([0, 0, 1], dtype=np.float64)

        e_x = w/h * (np.cos(htilt) * e_phi - np.sin(htilt) * e_r)
        e_y = (-e_r * np.cos(htilt) - e_phi * np.sin(htilt)) * np.cos(theta) + e_z * np.sin(theta)

        e_x /= zoom
        e_y /= zoom

        if theta < 0:
            e_x = -e_x
            e_y = -e_y
        
        target = e_r * r_target + e_z * z_target
        p_cam = target + d_cam * (np.cos(theta) * e_z + np.sin(theta) * (np.cos(htilt) * e_r + np.sin(htilt) * e_phi))
        
        self._proj = proj3d_make(
            w,
            h,
            e_x,
            e_y,
            p_cam,
            target,
            d_clip,
            p_clip,
            cz = cz,
            d = d,
            mindist = 0
        )
        
        self.transformed_meshes = {
            id : transform_polygons(self._proj, tqdm(mesh, desc = 'Transforming ' + str(id), leave = False))
            for id, mesh in tqdm(meshes.items(), desc = 'Transforming meshes')
        }
        
        self.dbuf = np.ones([w, h]) * np.inf
        self.detbuf = np.zeros([w, h])
        
        for id, mesh in tqdm(meshes.items(), 'Rasterizing parts'):            
            rasterize_polygons(
                self._proj, self.dbuf, self.detbuf,
                tqdm(mesh, 'Rasterizing ' + str(id), leave = False),
                dtol = 0.003,
                ptol = 1
            )
    
    def xyz_to_screen(self, xyz):
        return proj3d_apply(self._proj, xyz)
    
    def render(self, points, dtol = 1e-3):
        buffer = np.zeros(self.dbuf.shape)
        
        put_points(self._proj, np.reshape(points, [3, -1]), self.dbuf, buffer, dtol)
        
        n_tot = np.sum(buffer)
        buffer *= self.detbuf
        return buffer, n_tot


# Default views
@functools.lru_cache(maxsize = None)
def components_db():
    import osa
    
    return osa.Client('http://esb.ipp-hgw.mpg.de:8280/services/ComponentsDBProxy?wsdl')

@functools.lru_cache(maxsize=20)
def get_part(part_id):
    data = components_db().service.getComponentData(part_id)

    vertices = np.asarray([data[0].nodes.x1, data[0].nodes.x2, data[0].nodes.x3]).transpose()
    my_polygons = [
        np.asarray([
            vertices[i - 1] for i in element.vertices
        ])
        for element in data[0].elements
    ]
    
    return my_polygons

@functools.lru_cache(maxsize=20)
def default_view(view, scale = 1, tqdm = notqdm):
    cz = 0
    d = 1
    
    w = 1000
    h = 400

    if view == 'divertor':
        phi = np.radians(5);
        theta = np.radians(60);
        r_origin = 5.5;
        z_origin = -0.4;
        htilt = 0.0

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 1;

    if view == 'divertor_pretty':
        phi = np.radians(5);
        theta = np.radians(75);
        r_origin = 5.5;
        z_origin = -0.4;
        htilt = -np.radians(110.0)

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 0.7;

        w = 600
        h = 800

    if view == 'lbaffles':
        phi = np.radians(5);
        theta = np.radians(75);
        r_origin = 5.3;
        z_origin = -0.4;
        htilt = -np.radians(90)

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 0.8;

        w = 500
        h = 500

    if view == 'cbaffleso':
        phi = np.radians(5);
        theta = np.radians(55);
        r_origin = 5.5;
        z_origin = -0.4;
        htilt = -np.radians(0)

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 1.0;

    if view == 'cbafflesi':
        phi = np.radians(5);
        theta = np.radians(-10);
        r_origin = 5.5;
        z_origin = -0.4;
        htilt = -np.radians(0)

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 1.0;

    if view == 'rbaffles':
        phi = np.radians(5);
        theta = np.radians(60);
        r_origin = 5.5;
        z_origin = -0.4;
        htilt = np.radians(80)

        theta_clip = np.radians(0);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 1;

    elif view == 'uport':
        phi = np.radians(36);
        theta = np.radians(-90);
        r_origin = 5.5;
        z_origin = 0.0;
        htilt = 0.0

        theta_clip = np.radians(-90);
        r_clip = 5.8;
        z_clip = 0.0;
        zoom = 3;
    
    w = int(w * scale)
    h = int(h * scale)

    e_r = np.asarray([np.cos(phi), np.sin(phi), 0.0], dtype=np.float64);
    e_z = np.asarray([0, 0, 1], dtype=np.float64);

    p_clip = r_clip * e_r + z_clip * e_z;
    d_clip = np.cos(theta_clip) * e_z + np.sin(theta_clip) * e_r;

    if view == 'uport':
        useids = [330, 331, 335, 336, 340, 341]

    if view == 'divertor':
        useids = [165]

    if 'baffles' in view:
        useids = [320]

    if view == 'divertor_pretty':
        useids = [165, 320]
    
    meshes = {
        part_id : get_part(part_id)
        for part_id in tqdm(useids, 'Getting meshes for ' + view, leave = False)
    }
    
    d_cam = 10
    
    camera = HFCamera(
        w, h,
        phi, theta, htilt,
        r_origin, z_origin, d_cam,
        p_clip, d_clip,
        zoom, cz, d,
        meshes,
        tqdm = tqdm
    )
    
    return camera