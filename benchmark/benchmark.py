import time
from nnpycgal.nninterpol import nninterpol
import numpy as np
import ngl
import matplotlib.pyplot as plt

# nsamples_list = [10, 100, 250, 500, 1000]
# nsamples_times_cgal = []
# nsamples_times_ngl = []
# for nsamples in nsamples_list:
#     nx, ny = 1000, 1000
#     xo = np.arange(0, nx)
#     yo = np.arange(0, ny)
#     xx, yy = np.meshgrid(xo, yo)

#     x = np.random.randint(0, nx, nsamples)
#     y = np.random.randint(0, ny, nsamples)
#     z = np.random.random(nsamples)

#     t0 = time.time()
#     nn_cgal = np.array(nninterpol(x, y, z, nx, ny))
#     nsamples_times_cgal.append(time.time() - t0)

#     t0 = time.time()
#     nn_ngl = ngl.natgrid(x, y, z, xo, yo)
#     nsamples_times_ngl.append(time.time() - t0)

# fig, ax = plt.subplots(1, 1)
# ax.plot(nsamples_list, nsamples_times_cgal, 'bx-', label='CGAL')
# ax.plot(nsamples_list, nsamples_times_ngl, 'rx-', label='NGL')
# ax.set_xlabel('Number of samples')
# ax.set_ylabel('Time in seconds')
# ax.legend()
# plt.savefig('benchmark.jpg', bbox_inches='tight')


gridsize_list = [500, 1000, 1500, 2000]
gridsize_times_cgal = []
gridsize_times_ngl = []
for gridsize in gridsize_list:
    nsamples = 500
    nx, ny = gridsize, gridsize
    xo = np.arange(0, nx)
    yo = np.arange(0, ny)
    xx, yy = np.meshgrid(xo, yo)

    x = np.random.randint(0, nx, nsamples)
    y = np.random.randint(0, ny, nsamples)
    z = np.random.random(nsamples)

    t0 = time.time()
    nn_cgal = np.array(nninterpol(x, y, z, nx, ny))
    gridsize_times_cgal.append(time.time() - t0)

    t0 = time.time()
    nn_ngl = ngl.natgrid(x, y, z, xo, yo)
    gridsize_times_ngl.append(time.time() - t0)

fig, ax = plt.subplots(1, 1)
ax.plot(gridsize_list, gridsize_times_cgal, 'bx-', label='CGAL')
ax.plot(gridsize_list, gridsize_times_ngl, 'rx-', label='NGL')
ax.set_xlabel('Gridsize n x n pixels')
ax.set_ylabel('Time in seconds')
ax.legend()
plt.savefig('benchmark2.jpg', bbox_inches='tight')
