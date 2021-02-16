# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:48:01 2020

@author: stvyh
"""
#https://brushingupscience.com/2019/08/01/elaborate-matplotlib-animations/
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from IPython.display import HTML

Nframes = 400
t = np.linspace(0, 2*np.pi, Nframes, endpoint=False)
zz=np.linspace(0, 0, Nframes, endpoint=False)
yy = np.sin(t)*np.exp(-1j*2*np.pi*t)

x = yy.real
y = yy.imag

fig, ax1 = plt.subplots(figsize=(6, 6))
#ax1 = plt.subplot(111) #, projection='polar')

ax1.set_ylim([-1, 1])
ax1.set_xlim([-1, 1])
#ax1.grid(True)

curve1, = ax1.plot(x[:0],y[:0])
def init():
    return curve1,

def animate(i):
    print(i)
    #curve1.set_data(np.angle(yy[i:]),np.absolute(yy[i:]))
    curve1.set_data(x[:i],y[:i])
    return curve1,

anim = animation.FuncAnimation(fig, func=animate, init_func=init, interval=50, frames=400, blit=True)
#plt.show()
# for jupyter notebook
#HTML(anim.to_html5_video())
#plt.savefig("mygraph.png")
writer = animation.writers['ffmpeg'](fps=5)

anim.save('demo.mp4', writer=writer)