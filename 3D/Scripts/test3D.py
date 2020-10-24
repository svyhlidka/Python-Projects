# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:40:38 2020

@author: stvyh
"""

#import bpy
from  calcFence import *

import numpy as np


framesList = [[2.93,.99]]
#    [2.80,1.71],[2.81,0.90],[2.81,0.90],
#    [2.81,0.90],[2.60,1.71],[2.81,1.71]
#             ]
frame_length = 2.93  # frame length
frame_height = .99  # frame height
plank_width = 0.088 # perpendicular width of the plank
space_width = 0.015  #perpendicular distance between planks
plank_angle = 45
reserve_cut = 0.02
show_frame = True#
frame_width = 0.04
frame_angle = 90  # frame angle not implemented yet
plank_colors = ['black','green','brown']
frame_color = 'black'



ff = fenceFrame(
      frame_length,
      frame_height,
      45.0, # frame_angle,
      plank_angle,
      plank_width,
      space_width,
      plank_colors,
      show_frame,
      frame_width,
      frame_color,
       reserve_cut
      )  

if int(ff.plank_angle) in [0, 90]:
    ff.angle_0_90()
else:
    ff.angle_normal()

planks = []      # this is what createMesh expects!!!!!!!!!!!!!!!!

x=0.
y=.0
   
for p in ff.planksList:
    planks.append(np.round(p.plank+[x,y],3).tolist())
    
print(planks) # this is what createMesh expects!!!!!!!!!!!!!!!!

