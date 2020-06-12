import torch.nn
from typing import Tuple, Union, Optional
import operator
import functools
import geoopt.utils
from geoopt.manifolds import Manifold


__all__ = ["ProductManifold"]


def _shape2size(shape: Tuple[int]):
    return functools.reduce(operator.mul, shape, 1)


def _calculate_target_batch_dim(*dims: int):
    return max(dims) - 1


class ProductManifold(Manifold):
    """
    Product Manifold.

    Examples
    --------
    A Torus

    >>> import geoopt
    >>> sphere = geoopt.Sphere()
    >>> torus = ProductManifold((sphere, 2), (sphere, 2))
    """

    ndim = 1

    def __init__(
        self, *manifolds_with_shape: Tuple[Manifold, Union[Tuple[int, ...], int]]
    ):
        if len(manifolds_with_shape) < 1:
            raise ValueError(
                "There should be at least one manifold in a product manifold"
            )
        super().__init__()
        self.shapes = []
        self.slices = []
        name_parts = []
        manifolds = []
        dtype = None
        device = None
        pos0 = 0
        for i, (manifold, shape) in enumerate(manifolds_with_shape):
            # check shape consistency
            shape = geoopt.utils.size2shape(shape)
            ok, reason = manifold._check_shape(shape, str("{}'th shape".format(i)))
            if not ok:
                raise ValueError(reason)
            # check device consistency
            if manifold.device is not None and device is not None:
                if device != manifold.device:
                    raise ValueError("Not all manifold share the same device")
            elif device is None:
                device = manifold.device
            # check dtype consistency
            if manifold.dtype is not None and dtype is not None:
                if dtype != manifold.dtype:
                    raise ValueError("Not all manifold share the same dtype")
            elif dtype is None:
                dtype = manifold.dtype

            name_parts.append(manifold.name)
            manifolds.append(manifold)
            self.shapes.append(shape)
            pos1 = pos0 + _shape2size(shape)
            self.slices.append(slice(pos0, pos1))
            pos0 = pos1
        self.name = "x".join(["({})".format(name) for name in name_parts])
        self.n_elements = pos0
        self.n_manifolds = len(manifolds)
        self.manifolds = torch.nn.ModuleList(manifolds)

    @property
    def reversible(self) -> bool:
        return all(m.reversible for m in self.manifolds)

    def take_submanifold_value(
        self, x: torch.Tensor, i: int, reshape=True
    ) -> torch.Tensor:
        """
        Take i'th slice of the ambient tensor and possibly reshape.

        Parameters
        ----------
        x : tensor
            Ambient tensor
        i : int
            submanifold index
        reshape : bool
            reshape the slice?

        Returns
        -------
        torch.Tensor
        """
        slc = self.slices[i]
        part = x.narrow(-1, slc.start, slc.stop - slc.start)
        if reshape:
            part = part.reshape((*part.shape[:-1], *self.shapes[i]))
        return part

    def _check_shape(self, shape: Tuple[int], name: str) -> Tuple[bool, Optional[str]]:
        ok = shape[-1] == self.n_elements
        if not ok:
            return (
                ok,
                "The last dimension should be equal to {}, but got {}".format(
                    self.n_elements, shape[-1]
                ),
            )
        return ok, None

    def _check_point_on_manifold(
        self, x: torch.Tensor, *, atol=1e-5, rtol=1e-5
    ) -> Tuple[bool, Optional[str]]:
        ok, reason = True, None
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            ok, reason = manifold.check_point_on_manifold(
                point, atol=atol, rtol=rtol, explain=True
            )
            if not ok:
                break
        return ok, reason

    def _check_vector_on_tangent(
        self, x, u, *, atol=1e-5, rtol=1e-5
    ) -> Tuple[bool, Optional[str]]:
        ok, reason = True, None
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            tangent = self.take_submanifold_value(u, i)
            ok, reason = manifold.check_vector_on_tangent(
                point, tangent, atol=atol, rtol=rtol, explain=True
            )
            if not ok:
                break
        return ok, reason

    def inner(
        self, x: torch.Tensor, u: torch.Tensor, v=None, *, keepdim=False
    ) -> torch.Tensor:
        if v is not None:
            target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim(), v.dim())
        else:
            target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim())
        products = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            u_vec = self.take_submanifold_value(u, i)
            if v is not None:
                v_vec = self.take_submanifold_value(v, i)
            else:
                v_vec = None
            inner = manifold.inner(point, u_vec, v_vec, keepdim=True)
            inner = inner.view(*inner.shape[:target_batch_dim], -1).sum(-1)
            products.append(inner)
        result = sum(products)
        if keepdim:
            result = torch.unsqueeze(result, -1)
        return result

    def component_inner(self, x: torch.Tensor, u: torch.Tensor, v=None) -> torch.Tensor:
        products = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            u_vec = self.take_submanifold_value(u, i)
            target_shape = geoopt.utils.broadcast_shapes(point.shape, u_vec.shape)
            if v is not None:
                v_vec = self.take_submanifold_value(v, i)
            else:
                v_vec = None
            inner = manifold.component_inner(point, u_vec, v_vec)
            inner = inner.expand(target_shape)
            products.append(inner)
        result = self.pack_point(*products)
        return result

    def projx(self, x: torch.Tensor) -> torch.Tensor:
        projected = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            proj = manifold.projx(point)
            proj = proj.view(*x.shape[: len(x.shape) - 1], -1)
            projected.append(proj)
        return torch.cat(projected, -1)

    def proju(self, x: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim())
        projected = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            tangent = self.take_submanifold_value(u, i)
            proj = manifold.proju(point, tangent)
            proj = proj.reshape((*proj.shape[:target_batch_dim], -1))
            projected.append(proj)
        return torch.cat(projected, -1)

    def expmap(self, x: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim())
        mapped_tensors = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            tangent = self.take_submanifold_value(u, i)
            mapped = manifold.expmap(point, tangent)
            mapped = mapped.reshape((*mapped.shape[:target_batch_dim], -1))
            mapped_tensors.append(mapped)
        return torch.cat(mapped_tensors, -1)

    def retr(self, x: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim())
        mapped_tensors = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            tangent = self.take_submanifold_value(u, i)
            mapped = manifold.retr(point, tangent)
            mapped = mapped.reshape((*mapped.shape[:target_batch_dim], -1))
            mapped_tensors.append(mapped)
        return torch.cat(mapped_tensors, -1)

    def transp(self, x: torch.Tensor, y: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), y.dim(), v.dim())
        transported_tensors = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            point1 = self.take_submanifold_value(y, i)
            tangent = self.take_submanifold_value(v, i)
            transported = manifold.transp(point, point1, tangent)
            transported = transported.reshape(
                (*transported.shape[:target_batch_dim], -1)
            )
            transported_tensors.append(transported)
        return torch.cat(transported_tensors, -1)

    def logmap(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), y.dim())
        logmapped_tensors = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            point1 = self.take_submanifold_value(y, i)
            logmapped = manifold.logmap(point, point1)
            logmapped = logmapped.reshape((*logmapped.shape[:target_batch_dim], -1))
            logmapped_tensors.append(logmapped)
        return torch.cat(logmapped_tensors, -1)

    def transp_follow_retr(
        self, x: torch.Tensor, u: torch.Tensor, v: torch.Tensor
    ) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim(), v.dim())
        results = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            direction = self.take_submanifold_value(u, i)
            vector = self.take_submanifold_value(v, i)
            transported = manifold.transp_follow_retr(point, direction, vector)
            transported = transported.reshape(
                (*transported.shape[:target_batch_dim], -1)
            )
            results.append(transported)
        return torch.cat(results, -1)

    def transp_follow_expmap(
        self, x: torch.Tensor, u: torch.Tensor, v: torch.Tensor
    ) -> torch.Tensor:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim(), v.dim())
        results = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            direction = self.take_submanifold_value(u, i)
            vector = self.take_submanifold_value(v, i)
            transported = manifold.transp_follow_expmap(point, direction, vector)
            transported = transported.reshape(
                (*transported.shape[:target_batch_dim], -1)
            )
            results.append(transported)
        return torch.cat(results, -1)

    def expmap_transp(
        self, x: torch.Tensor, u: torch.Tensor, v: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim(), v.dim())
        results = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            direction = self.take_submanifold_value(u, i)
            vector = self.take_submanifold_value(v, i)
            new_point, transported = manifold.expmap_transp(point, direction, vector)
            transported = transported.reshape(
                (*transported.shape[:target_batch_dim], -1)
            )
            new_point = new_point.reshape((*new_point.shape[:target_batch_dim], -1))
            results.append((new_point, transported))
        points, vectors = zip(*results)
        return torch.cat(points, -1), torch.cat(vectors, -1)

    def retr_transp(self, x: torch.Tensor, u: torch.Tensor, v: torch.Tensor):
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim(), v.dim())
        results = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            direction = self.take_submanifold_value(u, i)
            vector = self.take_submanifold_value(v, i)
            new_point, transported = manifold.retr_transp(point, direction, vector)
            transported = transported.reshape(
                (*transported.shape[:target_batch_dim], -1)
            )
            new_point = new_point.reshape((*new_point.shape[:target_batch_dim], -1))
            results.append((new_point, transported))
        points, vectors = zip(*results)
        return torch.cat(points, -1), torch.cat(vectors, -1)

    def dist2(self, x: torch.Tensor, y: torch.Tensor, *, keepdim=False):
        target_batch_dim = _calculate_target_batch_dim(x.dim(), y.dim())
        mini_dists2 = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            point1 = self.take_submanifold_value(y, i)
            mini_dist2 = manifold.dist2(point, point1, keepdim=True)
            mini_dist2 = mini_dist2.reshape(
                (*mini_dist2.shape[:target_batch_dim], -1)
            ).sum(-1)
            mini_dists2.append(mini_dist2)
        result = sum(mini_dists2)
        if keepdim:
            result = torch.unsqueeze(result, -1)
        return result

    def dist(self, x, y, *, keepdim=False):
        return self.dist2(x, y, keepdim=keepdim).clamp_min_(1e-15) ** 0.5

    def egrad2rgrad(self, x: torch.Tensor, u: torch.Tensor):
        target_batch_dim = _calculate_target_batch_dim(x.dim(), u.dim())
        transformed_tensors = []
        for i, manifold in enumerate(self.manifolds):
            point = self.take_submanifold_value(x, i)
            grad = self.take_submanifold_value(u, i)
            transformed = manifold.egrad2rgrad(point, grad)
            transformed = transformed.reshape(
                (*transformed.shape[:target_batch_dim], -1)
            )
            transformed_tensors.append(transformed)
        return torch.cat(transformed_tensors, -1)

    def unpack_tensor(self, tensor: torch.Tensor) -> Tuple[torch.Tensor]:
        parts = []
        for i in range(self.n_manifolds):
            part = self.take_submanifold_value(tensor, i)
            parts.append(part)
        return tuple(parts)

    def pack_point(self, *tensors: torch.Tensor) -> torch.Tensor:
        if len(tensors) != len(self.manifolds):
            raise ValueError(
                "{} tensors expected, got {}".format(len(self.manifolds), len(tensors))
            )
        flattened = []
        for i in range(self.n_manifolds):
            part = tensors[i]
            shape = self.shapes[i]
            if len(shape) > 0:
                if part.shape[-len(shape) :] != shape:
                    raise ValueError(
                        "last shape dimension does not seem to be valid. {} required, but got {}".format(
                            part.shape[-len(shape) :], shape
                        )
                    )
                new_shape = (*part.shape[: -len(shape)], -1)
            else:
                new_shape = (*part.shape, -1)
            flattened.append(part.reshape(new_shape))
        return torch.cat(flattened, -1)

    @classmethod
    def from_point(cls, *parts: "geoopt.ManifoldTensor", batch_dims=0):
        """
        Construct Product manifold from given points.

        Parameters
        ----------
        parts : tuple[geoopt.ManifoldTensor]
            Manifold tensors to construct Product manifold from
        batch_dims : int
            number of first dims to treat as batch dims and not include in the Product manifold

        Returns
        -------
        ProductManifold
        """
        batch_shape = None
        init = []
        for tens in parts:
            manifold = tens.manifold
            if batch_shape is None:
                batch_shape = tens.shape[:batch_dims]
            elif not batch_shape == tens.shape[:batch_dims]:
                raise ValueError("Not all parts have same batch shape")
            init.append((manifold, tens.shape[batch_dims:]))
        return cls(*init)

    def random_combined(
        self, *size, dtype=None, device=None
    ) -> "geoopt.ManifoldTensor":
        shape = geoopt.utils.size2shape(*size)
        self._assert_check_shape(shape, "x")
        batch_shape = shape[:-1]
        points = []
        for manifold, shape in zip(self.manifolds, self.shapes):
            points.append(
                manifold.random(batch_shape + shape, dtype=dtype, device=device)
            )
        tensor = self.pack_point(*points)
        return geoopt.ManifoldTensor(tensor, manifold=self)

    random = random_combined

    def origin(
        self, *size, dtype=None, device=None, seed=42
    ) -> "geoopt.ManifoldTensor":
        shape = geoopt.utils.size2shape(*size)
        self._assert_check_shape(shape, "x")
        batch_shape = shape[:-1]
        points = []
        for manifold, shape in zip(self.manifolds, self.shapes):
            points.append(
                manifold.origin(
                    batch_shape + shape, dtype=dtype, device=device, seed=seed
                )
            )
        tensor = self.pack_point(*points)
        return geoopt.ManifoldTensor(tensor, manifold=self)
