from django.test import TestCase

from  calcFence import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches #polygon draw

framesList = [[2.93,.99]]
#    [2.80,1.71],[2.81,0.90],[2.81,0.90],
#    [2.81,0.90],[2.60,1.71],[2.81,1.71]
#             ]
frame_length = 2.93  # frame length
frame_height = .99  # frame height
plank_width = 0.088 # perpendicular width of the plank
space_width = 0.015  #perpendicular distance between planks
plank_angle = -45
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

   

fig = plt.figure(figsize=(ff.frame_length, ff.frame_height), dpi=600)
fig.set_size_inches(7,4)

ax = fig.add_subplot(1,1,1)
ax.set_xlabel('[m]', fontsize=6)
ax.set_ylabel('[m]', fontsize=6)

plt.axis(xmin=-.1, xmax=ff.frame_length+ff.plank_width, ymin=-.1, ymax=ff.frame_height+ff.plank_width)
plt.xticks(np.arange(0,ff.frame_length,.25))
plt.title(f'Frame: {ff.frame_length:.3f} x {ff.frame_height:.3f}', size=8)

for plank in ff.planksList:
    if ff.plank_orientation:
        xy=list(tuple(map(tuple,plank.plank)))
    else:
        xy=list(tuple(map(tuple,(abs([ff.frame_length,0]-plank.plank)))))
    ax.add_patch(patches.Polygon(xy, facecolor='green'))

    
if show_frame:    
    xy=[(-1*frame_width, -1*frame_width), (-1*frame_width, 0.0), (ff.frame_length+frame_width, 0), (ff.frame_length+frame_width, -1*frame_width)]
    ax.add_patch(patches.Polygon(xy, facecolor='black'))
    xy=[(-1*frame_width, ff.frame_height), (-1*frame_width, ff.frame_height+frame_width), (ff.frame_length+frame_width, ff.frame_height+frame_width), (ff.frame_length+frame_width, ff.frame_height)]
    ax.add_patch(patches.Polygon(xy, facecolor='black'))
    xy=[(-1*frame_width, 0), (0, 0), (0,ff.frame_height), (-1*frame_width, ff.frame_height)]
    ax.add_patch(patches.Polygon(xy, facecolor='black'))
    xy=[(ff.frame_length, 0), (ff.frame_length+frame_width, 0), (ff.frame_length+frame_width,ff.frame_height), (ff.frame_length, ff.frame_height)]
    ax.add_patch(patches.Polygon(xy, facecolor='black'))
    
plt.show() 