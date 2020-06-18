import numpy as np
from numba.experimental import jitclass
from numba import njit # import the decorator
from numba import prange # import the prange
from numba import int32, double, boolean # import the types

spec = [
    ("N", int32),
    ("XMIN", double),
    ("XMAX", double),
    ("DT", double),
    ("DX", double),
    ('is_there_source', boolean),
    ('lock_left', boolean),
    ('lock_right', boolean),
    ('A', double[:]),
    ('B', double[:]),
    ('C', double[:]),
    ('D', double[:]),
    ('a_left', double[:]),
    ('a_right', double[:]),
    ('b_left', double[:]),
    ('b_right', double[:]),
    ('c_left', double[:]),
    ('c_right', double[:]),
    ('f', double[:]),
    ('c_prime', double[:]),
    ('f_prime', double[:]),
    ('temp', double[:]),
    ('x', double[:]),
    ('x0', double[:]),
    ('source', double[:]),
    ('left_extreme', double),
    ('right_extreme', double),
    ('executed_iterations', int32),
]

@jitclass(spec)
class crank_nicolson(object):
    def __init__(self, N, XMIN, XMAX, DT, X0, A, B, C, D):
        self.N = N
        self.XMIN = XMIN
        self.XMAX = XMAX
        self.DT = DT
        self.f = X0
        self.x = X0
        self.x0 = X0

        self.is_there_source = False
        self.lock_left = False
        self.lock_right = False

        assert(X0.size == N)
        assert(A.size == 0 or A.size == N * 2)
        assert(B.size == 0 or B.size == N)
        assert(C.size == 0 or C.size == N)
        assert(D.size == 0 or D.size == N + 2)

        if A.size == 0:
            self.A = np.zeros(N * 2, dtype=double)
        else:
            self.A = A

        if B.size == 0:
            self.B = np.zeros(N, dtype=double)
        else:
            self.B = B

        if C.size == 0:
            self.C = np.zeros(N, dtype=double)
        else:
            self.C = C

        if D.size == 0:
            self.D = np.zeros(N + 2, dtype=double)
        else:
            self.D = D

        self.DX = (XMAX - XMIN) / (N + 1)
        self.executed_iterations = 0

        self.a_left = np.empty(self.N, dtype=double)
        self.b_left = np.empty(self.N, dtype=double)
        self.c_left = np.empty(self.N, dtype=double)
        self.a_right = np.empty(self.N, dtype=double)
        self.b_right = np.empty(self.N, dtype=double)
        self.c_right = np.empty(self.N, dtype=double)
        
        self.c_prime = np.empty(self.N, dtype=double)
        self.temp = np.empty(self.N, dtype=double)

        self.left_extreme = 0.0
        self.right_extreme = 0.0

        self.f_prime = np.empty(self.N, dtype=double)

        self.source = np.empty(self.N, dtype=double)
        
        self.make_left_hand_matrix()
        self.make_right_hand_matrix()
        self.make_c_prime()

    def make_left_hand_matrix(self):
        for i in prange(self.N):
            self.a_left[i] = (
                + self.B[i] / (4 * self.DX)
                - self.A[i * 2] / (2 * self.DX * self.DX)
                - self.D[i] / (2 * self.DX * self.DX)
            )
            self.c_left[i] = (
                - self.B[i] / (4 * self.DX)
                - self.A[i * 2 + 1] / (2 * self.DX * self.DX)
                - self.D[i + 2] / (2 * self.DX * self.DX)
            )
            self.b_left[i] = (
                + 1 / self.DT
                - self.C[i] / 2
                + self.A[i * 2 + 1] / (2 * self.DX * self.DX)
                + self.A[i * 2] / (2 * self.DX * self.DX)
                + self.D[i + 1] / (self.DX * self.DX)
            )

    def make_right_hand_matrix(self):
        for i in prange(self.N):
            self.a_right[i] = (
                - self.B[i] / (4 * self.DX)
                + self.A[i * 2] / (2 * self.DX * self.DX)
                + self.D[i] / (2 * self.DX * self.DX)
            )
            self.c_right[i] = (
                + self.B[i] / (4 * self.DX)
                + self.A[i * 2 + 1] / (2 * self.DX * self.DX)
                + self.D[i + 2] / (2 * self.DX * self.DX)
            )
            self.b_right[i] = (
                + 1 / self.DT
                + self.C[i] / 2
                - self.A[i * 2 + 1] / (2 * self.DX * self.DX)
                - self.A[i * 2] / (2 * self.DX * self.DX)
                - self.D[i + 1] / (self.DX * self.DX)
            )

    def make_c_prime(self):
        self.c_prime[0] = self.c_left[0] / self.b_left[0]
        for i in range(1, self.N - 1):
            self.c_prime[i] = self.c_left[i] / (self.b_left[i] - self.a_left[i] * self.c_prime[i - 1])

    def dot_product_tridiagonal(self):
        self.temp[0] = (
            + self.b_right[0] * self.f[0]
            + self.c_right[0] * self.f[1]
        )
        self.temp[self.N - 1] = (
            + self.a_right[self.N - 1] * self.f[self.N - 2]
            + self.b_right[self.N - 1] * self.f[self.N - 1]
        )

        for i in prange(1, self.N - 1):
            self.temp[i] = (
                + self.a_right[i] * self.f[i - 1]
                + self.b_right[i] * self.f[i]
                + self.c_right[i] * self.f[i + 1]
            )
        
        if self.lock_left:
            self.temp[0] += self.left_extreme * (self.a_right[0] - self.a_left[0])

        if self.lock_right:
            self.temp[self.N - 1] += self.right_extreme * (self.c_right[self.N - 1] - self.c_left[self.N - 1])

        self.f = self.temp.copy()

    def tridiagonal_solver(self):
        self.f_prime[0] = self.f[0] / self.b_left[0]
        for i in prange(1, self.N):
            self.f_prime[i] = (
                (self.f[i] - self.a_left[i] * self.f_prime[i - 1])
                / (self.b_left[i] - self.a_left[i] * self.c_prime[i - 1])
            )
        
        self.x[self.N - 1] = self.f_prime[self.N - 1]
        
        for i in range(self.N - 2, -1, -1):
            self.x[i] = self.f_prime[i] - self.c_prime[i] * self.x[i + 1]

    def apply_source(self):
        for i in prange(self.N):
            if self.source[i] >= 0.0:
                self.x[i] = self.source[i]

    # PUBLIC METHODS

    def reset(self):
        self.x = self.x0
        self.executed_iterations = 0

    def iterate(self, n_iterations):
        for i in range(n_iterations):
            self.executed_iterations += 1
            self.f, self.x = self.x, self.f
            self.dot_product_tridiagonal()
            self.tridiagonal_solver()
            if self.is_there_source:
                self.apply_source()

    # SETTERS

    def set_executed_iterations(self, value):
        self.executed_iterations = value

    def set_x_values(self, new_x):
        self.x = new_x

    def set_source(self, source):
        self.is_there_source = True
        self.soruce = source

    def remove_source(self):
        self.is_there_source = False

    def set_lock_left(self):
        self.lock_left = True
        self.left_extreme = self.x[0]

    def set_lock_right(self):
        self.lock_right = True
        self.right_extreme = self.x[-1]

    def unlock_left(self,):
        self.lock_left = False

    def unlock_right(self):
        self.lock_right = False
