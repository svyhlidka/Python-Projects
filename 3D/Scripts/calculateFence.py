# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:30:53 2020

@author: stvyh
"""

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches #polygon draw
from calcFence import Plank, fenceFrame

framesList = [
    [2.80,1.71],[2.81,0.90],[2.81,0.90],
    [2.81,0.90],[2.60,1.71],[2.81,1.71]
             ]
frame_length = 2.80  # frame length
frame_height = 1.71  # frame height
plank_width = 0.088 # perpendicular width of the plank
space_width = 0.018  #perpendicular distance between planks
plank_angle = 45
reserve_cut = 0.02
show_frame = True
frame_width = 0.04
frame_angle = 45
plank_color = ['green'] #,'brown','blue']
frame_color = 'red'
reserve_cut = 0.02
apply_corr=True

def show_picture(ff):
    fig = plt.figure(figsize=(ff.frame_length, ff.frame_height), dpi=600)
    fig.set_size_inches(7,4)
    labeldegree = '$^\circ$' 
    str=f'[m]\n angle: {ff.plank_angle}{labeldegree}, total planks: {len(ff.planksList)}, total planks length: {ff.total_plank_length} [m]'
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(str, fontsize=8)
    ax.set_ylabel('[m]', fontsize=8)
    plt.xlabel(str)
    plt.axis(xmin=-.1, xmax=ff.frame_length+ff.plank_width, ymin=-.1, ymax=ff.frame_height+ff.plank_width)
    plt.xticks(np.arange(0,ff.frame_length,.2))
    plt.title(f'Frame: {ff.frame_length:.3f} x {ff.frame_height:.3f}', size=8)
    col = 0
    for plank in ff.planksList:
        xy=list(tuple(map(tuple,plank.plank)))
        #xy=list(tuple(map(tuple,plank+[0.05,0.05])))
        ax.add_patch(patches.Polygon(xy, facecolor=ff.plank_color[col]))
        col += 1
        if col > len(ff.plank_color)-1:
            col = 0
        
    if show_frame:    
        for xy in ff.frame:
            ax.add_patch(patches.Polygon(xy, facecolor=ff.frame_color))
    plt.show() 
            
    
ff = fenceFrame(frame_length,
                frame_height,
                frame_angle,
                plank_angle,
                plank_width,
                space_width,
                plank_color,
                show_frame,
                frame_width,
                frame_color,
                reserve_cut,
                apply_corr)


if plank_angle in [0, 90]:
    ff.angle_0_90()
else:
    ff.angle_normal()
    
print('=================================')
print(f'total planks: {len(ff.planksLengths)}')
print(f'total plank length: {ff.total_plank_Length()}')
show_picture(ff)        