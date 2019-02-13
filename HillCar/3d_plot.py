import os
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

filename = 'values.npy'

if os.path.exists(filename):
#https://medium.com/@sebastiannorena/3d-plotting-in-python-b0dc1c2e5e38
    Zvals = np.load(filename)
    fig = plt.figure()
    Xvals = []
    Yvals = []
    
    for i in range(50):
        Xvals.append(-1.2 + i*1.7/50)
    for j in range(50):
        Yvals.append(-0.07 + j*0.14/50)
    Xm, Ym = np.meshgrid(Xvals, Yvals)
            
    ax = mplot3d.Axes3D(plt.gcf())
    ax.plot_surface(Xm, Ym, Zvals)
    ax.set_xlabel('position')
    ax.set_ylabel('velocity')
    ax.set_zlabel('-height')