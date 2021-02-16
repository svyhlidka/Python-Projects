# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:36:11 2020

@author: stvyh
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
%matplotlib inline
# Use matplotlib ggplot stylesheet if available
try:
    plt.style.use('ggplot')
except OSError:
    pass

# Set which type of animation will be plotted. One of:
# quiver, 3d_contour, polar, scatter, fill
animation_type = 'polar'

Nframes = 120

fig = plt.figure(figsize=(3, 3))
ax = fig.add_subplot(111, projection='polar')
ax.set_ylim([-2, 2])
ax.set(yticks=np.r_[-1:3])

# Create two similar curves
r = np.linspace(0, 2*np.pi, 100)
t = np.linspace(0, 2*np.pi, Nframes, endpoint=False)

# theta1 and theta2 have size (Nr, Nframes) where
# Nr is the number of elements making up each curve
theta1 = (np.sin(r)[None, :]*np.cos(2*t)[:, None] +
          np.cos(2*r)[None, :]*np.cos(5*t)[:, None])
theta2 = (np.sin(1*r)[None, :]*np.cos(t)[:, None] +
          np.cos(2*r)[None, :]*np.cos(3*t)[:, None])

# Plot the 0th curves
curve1 = ax.plot(r, theta1[0, :])[0]
curve2 = ax.plot(r, theta2[0, :])[0]

def animate(i):
    # Updating lines on a polar plot is no different
    # to updating lines on a regular plot
    curve1.set_ydata(theta1[i, :])
    curve2.set_ydata(theta2[i, :])
    
anim = FuncAnimation(
    fig, animate, interval=500, frames=Nframes, repeat=True)
#fig.show()
# anim.save(animation_type + '.gif', writer='imagemagick')