import numpy as np

from point_spread_functions import gaussian_func

class VectorMap():
    def __init__(self, px, py, qx, qy, wt=None, gt=None):
        if wt is None:
            wt = [1, 1]
        if gt is None:
            gt = [0.3, 0.3]

        self.num_samples = len(px)
        self._px = np.atleast_1d(px)
        self._py = np.atleast_1d(py)
        self._qx = np.atleast_1d(qx)
        self._qy = np.atleast_1d(qy)
        self._wt = np.atleast_2d(wt) * np.ones((self.num_samples, 2))
        self._gt = np.atleast_2d(gt) * np.ones((self.num_samples, 2))

    def sample_vectors(self):
        return np.array([self._qx - self._px, self._qy - self._py])

    def sample_vector_magnitudes(self):
        return np.linalg.norm(self.sample_vectors(), axis=0)

    def sample_vector_norms(self):
        return self.sample_vectors() / self.sample_vector_magnitudes()

    def velocity_func(self):
        scaling_func = self._scaling_func()
        unscaled_velocity_func = self._unscaled_velocity_func()

        return lambda x: scaling_func(x) * unscaled_velocity_func(x)

    def mapping_func(self):
        return lambda x: x - self.velocity_func()(x)

    def _unscaled_velocity_func(self):
        def v(x):
            wx = weight_func_arr(x)
            return np.sum(wx[None, :, :, :] * pq_norms[:, :, None, None], axis=1) / np.sum(wx, axis=0)

        pq_norms = self.sample_vector_norms()
        weight_func_arr = self._weight_funcs()

        return v

    def _weight_funcs(self):
        def w(x):
            dx = [di(x) for di in d_func_arr]
            out = dx
            for i in range(1, self.num_samples):
                out *= 1 - np.roll(dx, i, axis=0)

            return out

        d_func_arr = self._point_weighting_funcs()

        return w

    def _point_weighting_funcs(self):
        return [gaussian_func(self._wt[i], [self._px[i], self._py[i]]) for i in range(self.num_samples)]

    def _scaling_func(self):
        def g(x):
            gx_arr = np.array([g_func_arr[i](x) for i in range(self.num_samples)])

            return np.max(self.sample_vector_magnitudes()[:, None, None] * gx_arr, axis=0)

        g_func_arr = self._point_scaling_funcs()

        return g

    def _point_scaling_funcs(self):
        return [gaussian_func(self._gt[i], [self._px[i], self._py[i]]) for i in range(self.num_samples)]


def map_image(image, velocity_func):
    x = np.array([image[0], image[1]])
    return np.array([*(x - velocity_func(x)), image[2]])

