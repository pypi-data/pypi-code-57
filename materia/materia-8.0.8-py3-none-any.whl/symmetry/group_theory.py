import itertools
import numpy as np
import scipy.linalg


class PointGroup:
    def __init__(self, products):
        self.products = products

    @property
    def labels(self):
        return tuple(set(self.products.values()))

    @property
    def order(self):
        return len(self.labels)

    @property
    def identity(self):
        identity_label = set.intersection(
            *(
                set((l1, l2))
                for (l1, l2), v in self.products.items()
                if l1 == v or l2 == v
            )
        ).pop()
        return GroupElement(label=identity_label, group=self)

    def inverse(self, label):
        inverse_label = next(
            l2 for (l1, l2), v in self.products.items() if l1 == label and v == 0
        )
        return GroupElement(label=inverse_label, group=self)

    def irreps(self):
        return set(
            tuple(np.real_if_close(X.trace()).item() for X in r)
            for r in self.regular_representation().reduce()
        )

    def cayley_table(self):
        lookup = dict(zip(self.labels, np.argsort(self.labels).argsort()))
        ctable = np.empty(
            shape=(self.order, self.order), dtype=int
        )  # FIXME: dtype should be 'S1' for single-character labels, etc.
        for (l1, l2), l3 in self.products.items():
            ctable[lookup[l1], lookup[l2]] = l3

        return ctable

    def regular_representation(self):
        return Representation(map=lambda g: g.regular_representation, group=self)

    def binary_operation(self, label1, label2):
        return self.products[(label1, label2)]

    def get_element(self, label):
        return GroupElement(label=label, group=self)

    @property
    def conjugacy_classes(self):
        return tuple(set(g.conjugacy_class for g in self))

    @property
    def conjugacy_representatives(self):
        return tuple(cls[0] for cls in self.conjugacy_classes)

    def __iter__(self):
        for l in self.labels:
            yield GroupElement(label=l, group=self)

    def __eq__(self, other):
        return hasattr(other, "products") and self.products == other.products

    def __hash__(self):
        return hash(frozenset(self.products.items()))


class GroupElement:
    def __init__(self, label, group):
        self.label = label
        self.group = group

    @property
    def regular_representation(self):
        permutation_dict = {
            l2: l3 for (l1, l2), l3 in self.group.products.items() if l1 == self.label
        }
        return self._permutation_matrix(permutation_dict=permutation_dict)

    @property
    def conjugacy_class(self):
        return tuple(set(g.inverse * self * g for g in self.group))

    def is_conjugate_to(self, other):
        return other in self.conjugacy_class

    @property
    def inverse(self):
        return self.group.inverse(label=self.label)

    def _permutation_matrix(self, permutation_dict):
        n = len(permutation_dict)
        I = np.eye(n, dtype=int)
        return np.hstack(
            [
                I[:, col_ind].reshape(n, -1)
                for _, col_ind in sorted(permutation_dict.items())
            ]
        )

    def __mul__(self, other):
        if (
            hasattr(other, "label")
            and hasattr(other, "group")
            and other.group == self.group
        ):
            return GroupElement(
                label=self.group.binary_operation(
                    label1=self.label, label2=other.label
                ),
                group=self.group,
            )

    def __eq__(self, other):
        return (
            hasattr(other, "label")
            and self.label == other.label
            and hasattr(other, "group")
            and self.group == other.group
        )

    def __hash__(self):
        return hash((self.label, self.group))


class Representation:
    def __init__(self, map, group):
        self.__call__ = map
        self.group = group

    def __iter__(self):
        for g in self.group:
            yield self.__call__(g)

    @property
    def dimension(self):
        try:
            (shape,) = tuple(set(rho.shape for rho in self))
        except ValueError:  # thrown from tuple unpacking into a single variable
            raise ValueError("Representation matrices have different shapes.")

        try:
            (dimension,) = tuple(set(shape))
        except ValueError:  # thrown from tuple unpacking into a single variable
            raise ValueError("Representation matrices are not square.")

        return dimension

    def reduce(self):
        # algorithm based on: http://sheaves.github.io/Group-Ring-Regular-Representation/
        H = self._commuting_matrix()
        _, P = np.linalg.eigh(H)
        blockified_reps = tuple(
            self._transform_rep(rho=rho, P=P) for rho in self
        )  # (self.representations[g] for g in list(self.representations.keys())[0].group.conjugacy_representatives))
        for reduced_reps in self.extract_blocks(*blockified_reps):
            map = lambda g: dict(zip((gp.label for gp in self.group), reduced_reps))[
                g.label
            ]
            rep = Representation(map=map, group=self.group)
            if rep.is_irreducible:
                yield rep
            else:
                yield from rep.reduce()

    @property
    def is_irreducible(self):
        return np.allclose(self._commuting_matrix(), np.eye(self.dimension))

    def _commuting_matrix(self):
        H_function_generator = (
            self.H_function(H=H) for H in self._hermitian_matrix_basis()
        )

        try:
            return next(
                (H for H in H_function_generator if not self._is_scalar_matrix(H=H))
            )
        except StopIteration:  # all H matrices are scalar matrices (so this is an irrep)
            return np.eye(self.dimension)

    def H_function(self, H):
        return sum(rho.T.conj() @ H @ rho for rho in self) / self.group.order

    def _hermitian_matrix_basis(self):
        for r, s in itertools.product(range(self.dimension), range(self.dimension)):
            E = np.zeros(shape=(self.dimension, self.dimension)).astype(np.complex)
            E[r, s] = 1j if r < s else 1
            yield E + E.T.conj() - np.diag(E.diagonal())

    def _is_scalar_matrix(self, H):
        return np.allclose(H, H[0, 0] * np.eye(self.dimension))

    def _transform_rep(self, rho, P):
        X = P.T.conj() @ rho @ P
        r = np.copy(X.real)
        i = np.copy(X.imag)
        r[np.isclose(r, 0)] = 0
        i[np.isclose(i, 0)] = 0
        return r + 1j * i

    def extract_blocks(self, *arrays):
        prev = -1
        (max_block_size,) = tuple(set(arrays[0].shape))
        for i in range(max_block_size - 1):
            if all(array[i + 1][i] == 0 and array[i][i + 1] == 0 for array in arrays):
                yield [array[prev + 1 : i + 1, prev + 1 : i + 1] for array in arrays]
                prev = i
        yield [array[prev + 1 : len(array), prev + 1 : len(array)] for array in arrays]

    # def _blockify(self, *matrices,first_time=True):
    #
    #     try:
    #         #FIXME: use np.ndim!!!
    #         (shape,) = tuple(set(A.shape for A in matrices))
    #     except ValueError:
    #         raise ValueError('Matrices must have same shapes.')
    #
    #     try:
    #         (dimension,) = tuple(set(shape))
    #     except ValueError:
    #         raise ValueError('Matrices must be square.')
    #
    #     Ts = (self.T_matrix(A=A) for A in matrices)
    #     null_vecs = scipy.linalg.null_space(sum(T.T@T for T in Ts)).T
    #     num_null_vecs,_ = null_vecs.shape
    #
    #     coeffs = np.random.uniform(low=1,high=2,size=num_null_vecs)
    #     coeffs /= np.linalg.norm(coeffs)
    #
    #     u = np.dot(coeffs,null_vecs)
    #     U = u.reshape(dimension,dimension)
    #
    #     X = U + U.T
    #     _,P = np.linalg.eigh(X)
    #
    #     blocked_matrices = [P.T@A@P for A in matrices]
    #     for B in blocked_matrices:
    #         B[np.isclose(B,0)] = 0
    #     if first_time:
    #         for list_of_mats in self.extract_blocks(*blocked_matrices):
    #             print(self._blockify(*list_of_mats,first_time=False))
    #     return blocked_matrices
    #
    # def T_matrix(self, A):
    #     try:
    #         (dimension,) = tuple(set(A.shape))
    #     except ValueError:
    #         raise ValueError('Cannot construct T-matrix for non-square matrix.')
    #
    #     if dimension == 1:
    #         return np.zeros(shape=(1,1))
    #     elif dimension == 2:
    #         a,b,c,d = np.ravel(A)
    #         return np.array([[0,-c,b,0],[-b,a-d,0,b],[c,0,d-a,-c],[0,a,-b,0]])
    #     elif dimension == 3:
    #         a,b,c,d,e,f,g,h,i = np.ravel(A)
    #         return np.array([[0,-d,-g,b,0,0,c,0,0],[-b,a-e,-h,0,b,0,0,c,0],
    #                          [-c,-f,a-i,0,0,b,0,0,c],[d,0,0,e-a,-d,-g,f,0,0],
    #                          [0,d,0,-b,0,-h,0,f,0],[0,0,d,-c,-f,e-i,0,0,f],
    #                          [g,0,0,h,0,0,i-a,-d,-g],[0,g,0,0,h,0,-b,i-e,-h],
    #                          [0,0,g,0,0,h,-c,-f,0]])
    #     else:
    #         raise ValueError('Cannot construct T-matrix for matrix with dimension greater than 3.')


class C1(PointGroup):
    def __init__(self):
        self.products = {(0, 0): 0}


class Cs(PointGroup):
    def __init__(self):
        self.products = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}


class Ci(PointGroup):
    def __init__(self):
        self.products = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}


class C2(PointGroup):
    def __init__(self):
        self.products = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}


class C2(PointGroup):
    def __init__(self):
        self.products = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (0, 2): 2,
            (2, 0): 2,
            (1, 1): 2,
            (1, 2): 0,
            (2, 1): 0,
            (2, 2): 1,
        }
