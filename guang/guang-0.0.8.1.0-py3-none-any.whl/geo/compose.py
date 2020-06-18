import matplotlib.pyplot as plt
import numpy as np

colors = plt.cycler(
    color=['red', 'blue', '#9988DD', '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('axes', prop_cycle=colors)


def circle_points(R=10, N=20):
    theta = np.linspace(0, np.pi * 2, N)
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return x, y


def connect(*vertex):
    """connect vertex[0]、vertex[1]、vertex[2] ..."""
    x, y = [], []
    for idx, point in enumerate(vertex):
        x.append(point[0])
        y.append(point[1])
        if len(x) == 2:
            plt.plot(x, y)
            x.pop(0)
            y.pop(0)


def drawCircles(R=10, N=25):
    X, Y = circle_points(R, N)
    plt.figure(figsize=(10, 10))
    for idx, (x, y) in enumerate(zip(X, Y)):
        tX, tY = np.delete(X, idx), np.delete(Y, idx)
        for tx, ty in zip(tX, tY):
            connect([x, y], [tx, ty])
    plt.axis("equal")
    plt.show()


def quadrate(edge_length=10, centre=[0, 0]):
    vertex1 = [centre[0] - edge_length / 2, centre[1] + edge_length / 2]
    vertex2 = [centre[0] + edge_length / 2, centre[1] + edge_length / 2]
    vertex3 = [centre[0] + edge_length / 2, centre[1] - edge_length / 2]
    vertex4 = [centre[0] - edge_length / 2, centre[1] - edge_length / 2]
    return vertex1, vertex2, vertex3, vertex4


def line_eq(point1, point2):
    """get line equation (2D)
    return:
        1. the map of x, i.e. f(x)
        2. the coefficient a, b, c of  ax + by = c 
    """
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    if x1 == x2:
        #         return (1e16, np.inf), (np.inf, x1, y1, y2)
        x1 += 1e-15

    k = (y2 - y1) / (x2 - x1)
    f = lambda x: k * (x - x1) + y1
    b = k * x1 + y1

    A = k
    B = -1
    C = k * x1 - y1
    return (k, b), (A, B, C)


def kb2abc(k, b):
    A = k
    B = -1
    C = -b
    return A, B, C


def rot_mat(theta):
    mat = np.array([[np.cos(theta), np.sin(theta)],
                    [-np.sin(theta), np.cos(theta)]])
    return mat


def k_rot(theta, k):
    A = k
    B = -1
    theta = theta * np.pi / 180
    res = rot_mat(theta) @ np.array([[A, B]]).T
    a = np.float(res[[0]])
    b = np.float(res[[1]])
    k = -a / b
    return k


def solve_eq(eq1, eq2):

    A = np.array([[eq1[0], eq1[1]], [eq2[0], eq2[1]]])
    b = np.array([eq1[2], eq2[2]]).T
    res = np.linalg.solve(A, b)
    return res


def slove_b(k, x, y):
    b = y - k * x
    return b


def special_(N=180, theta=3):
    plt.figure(figsize=(10, 10))
    v1, v2, v3, v4 = quadrate()
    connect(v1, v2, v3, v4, v1)
    (k0, b0), (A0, B0, C0) = line_eq(v1, v2)
    v = [v1, v2, v3, v4, v1]
    p0 = v[0]
    for idx in range(N):
        p1 = v[idx + 1]
        p2 = v[idx + 2]
        (k1, b1), coeff = line_eq(p1, p2)
        rot_k0 = k_rot(theta, k0)
        b = slove_b(rot_k0, *p0)
        point = solve_eq(kb2abc(rot_k0, b), coeff)
        connect(p0, point)
        p0 = point
        v.append(point)
        k0, b0 = k1, b1
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    drawCircles()
    special_(N=2000, theta=1)
