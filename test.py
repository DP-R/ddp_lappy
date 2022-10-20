import numpy as np
import numpy.random as random
a=np.random.uniform([10,10])
print(a)
import scipy.io as sio
sio.savemat('a.mat',{'a':a})