import numpy as np
from scipy import ndimage

class Fluid():
    iter = 4

    def __init__(self, size, dt, diff, visc):
        self.size = size
        self.smaller_size = min(self.size)
        self.larger_size = max(self.size)
        self.dt = dt
        self.diff = diff
        self.visc = visc

        self.v = np.zeros((self.size[0], self.size[1], 2), dtype = 'float')
        self.v_old = np.zeros_like(self.v)
        self.d = np.zeros((self.size[0], self.size[1]), dtype = 'float')
        self.d_old = np.zeros_like(self.d)

    def step(self):
        self.diffuse_vector_field()
        # project 1?
        self.v[:,:,0] = self.project(self.v_old, self.v[:,:,0], self.v[:,:,1])
        self.advect_vector_field()
        # project 2?
        self.v_old[:,:,0] = self.project(self.v, self.v_old[:,:,0], self.v_old[:,:,1])

        self.diffuse_dye()
        self.advect_dye()


    def diffuse_vector_field(self):
        k = self.dt*self.visc*(self.size[0] - 2)*(self.size[1] - 2)
        # x component
        self.v_old[:,:,0] = Fluid.lin_solve(1, self.v_old[:,:,0], self.v[:,:,0], k/(1+4*k))
        # y component
        self.v_old[:,:,1] = Fluid.lin_solve(2, self.v_old[:,:,1], self.v[:,:,1], k/(1+4*k))

    def advect_vector_field(self):
        # x component
        self.v[:,:,0] = self.advect(1, self.v[:,:,0], self.v_old[:,:,0], self.v_old)
        # y component
        self.v[:,:,1] = self.advect(2, self.v[:,:,1], self.v_old[:,:,1], self.v_old)

    def diffuse_dye(self):
        k = self.dt*self.diff*(self.size[0] - 2)*(self.size[1] - 2)
        self.d_old = Fluid.lin_solve(0, self.d_old, self.d, k/(1+4*k))

    def advect_dye(self):
        self.d = self.advect(0, self.d, self.d_old, self.v)

    @staticmethod
    def lin_solve(b, x, x0, k):
        kernel1 = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
        ], dtype = 'float')*k
        kernel2 = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
        ], dtype = 'float')
        full_kernel = np.dstack((kernel2, kernel1))

        stack = np.dstack((x, x0))

        for k in range(Fluid.iter):
            ndimage.convolve(stack, full_kernel, output = stack, mode = 'wrap')
            stack[:,:,1] = x0
            Fluid.set_bound(b, stack[:,:,0])

        return stack[:,:,0]

    @staticmethod
    def set_bound(b, arr):
        if b is 2:
            arr[:, 0] = -arr[:, 1]
            arr[:, -1] = -arr[:, -2]
        else:
            arr[:, 0] = arr[:, 1]
            arr[:, -1] = arr[:, -2]

        if b is 1:
            arr[0, :] = -arr[1, :]
            arr[-1, :] = -arr[-2, :]
        else:
            arr[0, :] = arr[1, :]
            arr[-1, :] = arr[-2, :]

        arr[0, 0] = (arr[1, 0] + arr[0, 1])/2.0
        arr[0, -1] = (arr[1, -1] + arr[0, -2])/2.0
        arr[-1, 0] = (arr[-2, 0] + arr[-1, 1])/2.0
        arr[-1, -1] = (arr[-2, -1] + arr[-1, -2])/2.0

    def advect(self, b, d, d0, velocities):
        dtx = self.dt*(self.smaller_size - 2)# using smaller_size makes it look better
        dty = self.dt*(self.smaller_size - 2)# using smaller_size makes it look better

        indices = np.indices((self.size[0], self.size[1]))
        x = indices[0] - dtx*velocities[:, :, 0]
        y = indices[1] - dty*velocities[:, :, 1]

        x.clip(0.5, self.size[0] + 0.5, out = x)# MUST be size[0]
        y.clip(0.5, self.size[1] + 0.5, out = y)# MUST be size[1]

        i0 = np.floor(x)
        j0 = np.floor(y)
        i1 = i0 + 1.0
        j1 = j0 + 1.0

        s1 = x - i0
        t1 = y - j0
        s0 = 1.0 - s1
        t0 = 1.0 - t1

        i0 = i0.astype('int32', copy = False)
        i1 = i1.astype('int32', copy = False)
        j0 = j0.astype('int32', copy = False)
        j1 = j1.astype('int32', copy = False)

        i0.clip(0, self.size[0] - 1, out = i0)# MUST be size[0]
        i1.clip(0, self.size[0] - 1, out = i1)# MUST be size[0]
        j0.clip(0, self.size[1] - 1, out = j0)# MUST be size[1]
        j1.clip(0, self.size[1] - 1, out = j1)# MUST be size[1]

        d[indices[0], indices[1]] = s0*(t0*d0[i0, j0] + t1*d0[i0, j1]) + s1*(t0*d0[i1, j0] + t1*d0[i1, j1])

        Fluid.set_bound(b, d);
        return d

    def project(self, velocities, p, div):
        kernel1 = np.array([
        [0, -1, 0],
        [0, 0, 0],
        [0, 1, 0]
        ], dtype = 'float')
        kernel2 = np.array([
        [0, 0, 0],
        [-1, 0, 1],
        [0, 0, 0]
        ], dtype = 'float')
        full_kernel = np.dstack((kernel2, kernel1))

        div = ndimage.convolve(velocities, full_kernel*0.5/self.larger_size, mode = 'wrap')[:,:,0]# MUST be larger_size
        p[:,:] = 0

        Fluid.set_bound(0, div)
        Fluid.set_bound(0, p)
        p = Fluid.lin_solve(0, p, div, 1.0/8.0)# should be 4, but 8 works better

        velocities[:,:,0] += ndimage.convolve(p, kernel1*0.5*self.smaller_size, mode = 'wrap')# using smaller_size makes it look better
        velocities[:,:,1] += ndimage.convolve(p, kernel2*0.5*self.smaller_size, mode = 'wrap')# using smaller_size makes it look better

        Fluid.set_bound(1, velocities[:,:,0])
        Fluid.set_bound(2, velocities[:,:,1])

        return p
