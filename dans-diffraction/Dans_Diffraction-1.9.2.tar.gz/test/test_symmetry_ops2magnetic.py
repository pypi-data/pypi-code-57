"""
Test better implementation of symmetry_ops2magnetic
9/6/2020

Results:
"""

import time
import re
import numpy as np
import Dans_Diffraction as dif
fg = dif.fg


"""---------------------------------- From funcitons_crystallography.py ---------------------------------------------"""


def gen_sym_mat(sym_ops):
    """
     Generate transformation matrix from symmetry operation
     Currently very ugly but it seems to work
     Tested in Test/test_gen_sym_mat - found to be fast and reliable.
     sym_mat = gen_sym_mat(['x,y,z','y,-x,z+1/2'])
     sym_mat[0] = [[ 1.,  0.,  0.,  0.],
                   [ 0.,  1.,  0.,  0.],
                   [ 0.,  0.,  1.,  0.],
                   [ 0.,  0.,  0.,  1.]])
     sym_mat[1] = [[ 0. ,  1. ,  0. ,  0. ],
                   [-1. ,  0. ,  0. ,  0. ],
                   [ 0. ,  0. ,  1. ,  0.5],
                   [ 0.,   0.,   0.,   1.]]
    """

    if type(sym_ops) is str:
        sym_ops = [sym_ops]

    sym_mat = []
    for sym in sym_ops:
        sym = sym.lower()
        sym = sym.strip('\"\'')
        sym = sym.replace('/', './')  # float division
        ops = sym.split(',')
        mat = np.zeros((4, 4))
        mat[3, 3] = 1

        for n in range(3):
            op = ops[n]
            if 'x' in op: mat[n, 0] = 1
            if '-x' in op: mat[n, 0] = -1
            if 'y' in op: mat[n, 1] = 1
            if '-y' in op: mat[n, 1] = -1
            if 'z' in op: mat[n, 2] = 1
            if '-z' in op: mat[n, 2] = -1

            # remove these parts
            op = op.replace('-x', '').replace('x', '')
            op = op.replace('-y', '').replace('y', '')
            op = op.replace('-z', '').replace('z', '')
            op = op.replace('+', '')

            if len(op.strip()) > 0:
                mat[n, 3] = eval(op)
        sym_mat += [mat]
    return sym_mat


def sym_op_det(sym_ops):
    """
    Return the determinant of a symmetry operation
    :param sym_op: str e.g. 'x,-y,z+1/2' or 'y, x+y, -z, -1' or list of str ['x,y,z',...]
    :return: float |det| or list of floats
    """
    mat = gen_sym_mat(sym_ops)
    if len(mat) == 1:
        return np.linalg.det(mat[0][:3, :3])
    return [np.linalg.det(m[:3, :3]) for m in mat]


def invert_sym(sym_op):
    """
    Invert the sign of the given symmetry operation
    Usage:
      new_op = invert_sym(sym_op)
      sym_op = str symmetry operation e.g. 'x,y,z'
      new_op = inverted symmetry
    E.G.
      new_op = invert_sym('x,y,z')
      >> new_op = '-x,-y,-z'
    """
    sym_op = sym_op.lower()
    new_op = sym_op.replace('x', '-x').replace('y', '-y').replace('z', '-z').replace('--', '+').replace('+-', '-')
    return new_op


def sym_op_time(sym_op):
    """
    Return the time symmetry of a symmetry operation
    :param sym_op: str e.g. 'x,-y,z+1/2' or 'y, x+y, -z, -1'
    :return: +/-1
    """
    ops = sym_op.split(',')
    if len(ops) < 4:
        return 1
    return eval(ops[3])


def sym_mat2str(sym_mat, time=None):
    """
    Generate symmetry operation string from matrix
    :param sym_mat: array [3x3] or [4x4]
    :param time: +/-1 or None
    :return: str 'x,y,z(,1)'
    """
    sym_mat = np.asarray(sym_mat)

    rot = sym_mat[:3, :3]
    if sym_mat.shape[1] == 4:
        trans = sym_mat[:, 3]
    else:
        trans = np.zeros(3)

    denominators = range(2, 8)
    out = []
    for n in range(3):
        # Convert rotational part
        xyz = '%1.3gx+%1.3gy+%1.3gz' % (rot[n][0], rot[n][1], rot[n][2])
        xyz = re.sub('[+-]?0[xyz]', '', xyz).replace('1', '').replace('+-', '-').strip('+')

        # Convert translational part
        if abs(trans[n]) < 0.01:
            add = ''
        else:
            chk = [(d * trans[n]) % 1 < 0.01 for d in denominators]
            if any(chk):
                denom = denominators[chk.index(True)]
                add = '+%1.0f/%1.0f' % (denom*trans[n], denom)
            else:
                add = '+%1.4g' % trans[n]
            add = add.replace('+-', '+')
        #print(n, rot[n], trans[n], xyz, add)
        out += [xyz + add]
    if time is not None:
        out += ['%+1.3g' % time]
    return ','.join(out)


"""------------------------------------------------------------------------------------------------------------------"""


def symmetry_ops2magnetic(operations):
    """
    Convert list of string symmetry operations to magnetic symmetry operations
    i.e. remove translations

    Magnetic symmetry
        µ' = TPMµ
    T = Time operators x,y,z,(+1)
    P = Parity operator (determinant of M)
    M = Symmetry operator without translations
    See Vesta_Manual.pdf Section 9.1.1 "Creation and editing of a vector"
    """
    # convert string to list
    if type(operations) is str:
        operations = [operations]
    # Use RegEx to find translations
    mag_op = []
    for op in operations:
        translations = re.findall('[\+\-]?\d/\d[\+\-]?', op)
        op = fg.multi_replace(op, translations, '')
        # also remove +/-1
        translations = re.findall('[\+\-]?\d+?[\+\-]?', op)
        op = fg.multi_replace(op, translations, '')
        mag_op += [op]
    return mag_op


def symmetry_ops2magnetic2(operations):
    """
    Convert list of string symmetry operations to magnetic symmetry operations
    i.e. remove translations

    Magnetic symmetry
        µ' = TPMµ
    T = Time operators x,y,z,(+1)
    P = Parity operator (determinant of M)
    M = Symmetry operator without translations
    See Vesta_Manual.pdf Section 9.1.1 "Creation and editing of a vector"
    """
    # Convert operations to matrices
    mat_ops = gen_sym_mat(operations)
    str_ops = []
    for n, mat in enumerate(mat_ops):
        # Get time operation
        t = sym_op_time(operations[n])

        # Only use rotational part
        m = mat[:3, :3]

        # Get parity
        p = np.linalg.det(m)

        # Generate string
        mag_str = sym_mat2str(t * p * m)
        mag_str = mag_str.replace('x', 'mx').replace('y', 'my').replace('z', 'mz')
        str_ops += [mag_str]
    return str_ops

sgs = dif.fc.spacegroups()
msgs = dif.fc.spacegroups_magnetic()
mmm = '12.59' # '167.106'
ops = msgs[mmm]['positions general']
magops = msgs[mmm]['positions magnetic']

# General positions R-3'c' #167.106
"""
ops = [
    'x,  y,  z, +1',
    '-y,  x-y,  z, +1',
    '-x+y,  -x,  z, +1',
    'x-y,  -y,  -z+1/2, +1',
    'y,  x,  -z+1/2, +1',
    '-x,  -x+y,  -z+1/2, +1',
    '-x,  -y,  -z, -1',
    'y,  -x+y,  -z, -1',
    'x-y,  x,  -z, -1',
    '-x+y,  y,  z+1/2, -1',
    '-y,  -x,  z+1/2, -1',
    'x,  x-y,  z+1/2, -1',
    'x+2/3,  y+1/3,  z+1/3, +1',
    '-y+2/3,  x-y+1/3,  z+1/3, +1',
    '-x+y+2/3,  -x+1/3,  z+1/3, +1',
    'x-y+2/3,  -y+1/3,  -z+5/6, +1',
    'y+2/3,  x+1/3,  -z+5/6, +1',
    '-x+2/3,  -x+y+1/3,  -z+5/6, +1',
    '-x+2/3,  -y+1/3,  -z+1/3, -1',
    'y+2/3,  -x+y+1/3,  -z+1/3, -1',
    'x-y+2/3,  x+1/3,  -z+1/3, -1',
    '-x+y+2/3,  y+1/3,  z+5/6, -1',
    '-y+2/3,  -x+1/3,  z+5/6, -1',
    'x+2/3,  x-y+1/3,  z+5/6, -1',
    'x+1/3,  y+2/3,  z+2/3, +1',
    '-y+1/3,  x-y+2/3,  z+2/3, +1',
    '-x+y+1/3,  -x+2/3,  z+2/3, +1',
    'x-y+1/3,  -y+2/3,  -z+1/6, +1',
    'y+1/3,  x+2/3,  -z+1/6, +1',
    '-x+1/3,  -x+y+2/3,  -z+1/6, +1',
    '-x+1/3,  -y+2/3,  -z+2/3, -1',
    'y+1/3,  -x+y+2/3,  -z+2/3, -1',
    'x-y+1/3,  x+2/3,  -z+2/3, -1',
    '-x+y+1/3,  y+2/3,  z+1/6, -1',
    '-y+1/3,  -x+2/3,  z+1/6, -1',
    'x+1/3,  x-y+2/3,  z+1/6, -1'
]
#ops = [
#    'x,  y,  z,  +1',
#    '-x,  -y,  -z,  +1'
#]
"""

mats = gen_sym_mat(ops)

for n, m in enumerate(mats):
    t = sym_op_time(ops[n])
    #print(ops[n], '\t\t\t', sym_mat2str(m, t), '\t', ops[n]==sym_mat2str(m, t))
    print('%30s\t\t%30s\t\t%s' % (ops[n], sym_mat2str(m, t), (ops[n][:-3]==sym_mat2str(m, t)[:-4]) * (ops[n][-2:]==sym_mat2str(m, t)[-2:])))
print('\n\n')

mag_ops1 = symmetry_ops2magnetic(ops)
mag_ops2 = symmetry_ops2magnetic2(ops)

print(msgs[mmm]['space group number'], msgs[mmm]['space group name'], msgs[mmm]['type name'], msgs[mmm]['setting'])
for n in range(len(ops)):
    m2 = re.sub(r',\s+', ',', magops[n])
    print('%2d %30s %30s %30s|%s|%-30s' % (n, ops[n], mag_ops1[n], mag_ops2[n], mag_ops2[n]==m2, magops[n]))


print('\nLooping all magnetic spacegroups:')
diff_count = 0
tested = 0
for nsg in range(230):
    sg = sgs[str(nsg+1)]
    for nmsg in sg['magnetic space groups']:
        if nmsg.count('.') > 1: continue
        msg = msgs[nmsg]
        if ' II ' in msg['type name']: continue  # ignore grey groups
        ops = msg['positions general']
        magops = msg['positions magnetic']
        tested += len(ops)
        mag_ops = symmetry_ops2magnetic2(ops)
        ncount = np.sum([m1 != re.sub(r',\s+', ',', m2) for m1, m2 in zip(mag_ops, magops)])
        diff_count += ncount
        if ncount > 0:
            difstr = ',  '.join(['%s/=%s' % (m2, re.sub(r',\s+', ',', m1)) for m1, m2 in zip(magops, mag_ops) if m2 != re.sub(r',\s+', ',', m1)])
            print('%12s %24s %2d / %2d  %s' % (nmsg, msg['type name'], ncount, len(ops), difstr))

print('Differences: %d / %d' % (diff_count, tested))