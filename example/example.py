import datetime
from nnpycgal.nninterpol import nninterpol
import numpy as np
import matplotlib.pyplot as plt

step = 1
nx, ny = 1000, 1000
nsamples = 100
xo = np.arange(0, nx, step)
yo = np.arange(0, ny, step)
xx, yy = np.meshgrid(xo, yo)

x = np.random.randint(0, nx, nsamples)
y = np.random.randint(0, ny, nsamples)
z = np.random.random(nsamples)

result = np.array(nninterpol(x, y, z, nx, ny))
plt.imshow(result)
plt.scatter(x, y, c=z, edgecolor='k', linewidth=0.5)
plt.savefig('nn.jpg', dpi=120, bbox_inches='tight')

# rm -rf build && pip uninstall nnpycgal -y && python setup.py install && python example/example.py