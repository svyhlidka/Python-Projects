# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 22:57:30 2020

@author: stvyh
"""

import numpy as np

def createFrameMesh(a, c, lx, ly, lz, xyz): 
    """
       a,c frame cross section
       a - x coord
       c - z coord
       lx frame length in x ..
       xyz - zero position ARRAY! np.array([x,y,z])
       returns 
    """
    verts = []
    edges = []
    faces = []
    v = [0,0,0,0]

   
    v[0] = np.array([
        [0,0,0], [a,0,c], 
        [a,c,c], [0,c,0]
        ])
    v[0] += xyz        
    v[1] = np.array([
        [lx-a,0,c], [lx,0,0],
        [lx,c,0], [lx-a,c,c]
        ]) 
    v[1] += xyz 
    v[2] = np.array([
        [lx-a,0,lz-c], [lx,0,lz],
        [lx,c,lz], [lx-a,c,lz-c]
        ]) 
    v[2] += xyz 

    v[3] = np.array([
        [0,0,lz], [a,0,lz-c], 
        [a,c,lz-c], [0,c,lz]
        ])
    v[3] += xyz        
    
    edges = [
        [0,1], [1,2], [2,3], [3,0], 
        [4,5], [5,6], [6,7], [7,4],
        [8,9], [9,10], [10,11], [11,8],
        [12,13], [13,14], [14,15], [15,12],
        [0,5], [1,4], [2,7], [3,6],
        [4,8], [5,9], [6,10], [7,11],
        [8,13], [9,12], [11,14], [10,15],
        [12,0], [13,1], [15,3], [14,2]
        ]
    
    #faces = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
    
    verts=[list(iitem) for item in v for iitem in item]
    
    faces = [
        [0,5,4,1], [0,5,6,3], [1,4,7,2], [6,7,2,3],
        [4,8,9,5], [5,6,10,9], [6,10,11,7], [4,7,11,8],
        [8,9,12,13], [11,10,15,14], [9,10,15,12], [8,11,14,13],
        [0,1,13,12], [2,14,15,3], [1,2,14,13], [0,3,15,12]
         ]
    
    #faces = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
    
    verts=[list(iitem) for item in v for iitem in item]
    
    return verts, edges, faces

def createFrameLShapeMesh(a, b, c, lx, ly, lz, xyz): 
    """
       a thickness
       c vertical width  - z
       b horizontal width - y
       lx frame length in x ..
       xyz - zero position ARRAY! np.array([x,y,z])
       returns 
    """
    verts = []
    edges = []
    faces = []
    createFrameMesh(a, b, lx, ly, lz, xyz)    
    verts=[list(iitem) for item in v for iitem in item]
    
    return verts, edges, faces
    
v, e , f  = createFrameMesh(4, 5, 200, 0, 100, [100,100,100])


    
    frame_mat = bpy.data.materials.new(name = "Frame Material")
    vert, edg , fac  = createFrameMesh(frame_width_x, frame_width_y, frame_length, 0, frame_height, np.array(xyz))
    nameF = f'Frame Nr.{f}'
    meshF = bpy.data.meshes.new(nameF) 
    meshF.from_pydata(vert, edg , fac)  
    objF  = bpy.data.objects.new(nameF, meshF)
    bpy.context.collection.objects.link(objF)
    bpy.context.view_layer.objects.active = objF
    so = bpy.context.active_object
    so.data.materials.append(frame_mat)
    bpy.context.object.active_material.diffuse_color = frame_color #change color
     