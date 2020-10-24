class FenceProject(bpy.types.Operator):
    
    bl_idname  = "object.fence_project"
    bl_label   = "Fence Project"
    bl_options = {'REGISTER', 'UNDO'} 


    def createMesh(self, plank, z, xyz):
        """
           plank - array to be append
           z - z-coordinate
           xyz - zero position
           returns 
        """
        verts = []
        edges = []
        faces = []
        
        pl = []     #removing duplicates vertices (possible numbers 3, 4, 5)
        for item in plank:
            if item not in pl:
                pl.append(item)
                
        j = len(pl) 
     
        for i in range(j):
            verts.append([ pl[i][0], xyz[2], pl[i][1]]) #swapping y to z
        for i in range(j):
            verts.append([ pl[i][0], xyz[2]+z, pl[i][1]]) #swapping y to z
        
        if j == 5:
            edges = [[0,1], [1,2], [2,3], [3,4], [4,0], [5,6], [6,7], [7,8], [8,9],[9,5],[0,5],[1,6],[2,7],[3,8],[4,9]]
        elif j == 4:
            edges = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
        else:
            edges = [[0,1], [1,2], [2,0], [3,4], [4,5], [5,3], [0,3], [1,4], [2,5]]


        if j == 5:
            faces = [
                [0,1,2,3,4],[5,6,7,8,9],  
                [0,1,6,5],[1,2,7,6],[2,3,8,7],[3,4,9,8],[4,0,5,9]
            ]
        elif j == 4:
            faces = [
                [0,1,2,3],[4,5,6,7],
                [0,1,5,4],[1,2,6,5],[2,3,7,6] ,[3,0,4,7]
            ]
        else:
            faces = [[0,1,2], [3,4,5], [0,1,4,3], [1,2,5,4], [0,2,5,3]]
            
        return verts, edges, faces
    
    def execute(self, context): 

#verts, edges, faces = createMesh(planks[0],plank_thickness, xyz) 
#i=20
#verts, edges, faces = createMesh(planks[i],plank_thickness, xyz) 
#name = f'The Plank Nr.{i}'
#mesh = bpy.data.meshes.new(name) 
#mesh.from_pydata(verts, edges, faces)    
#obj  = bpy.data.objects.new(name, mesh)
#bpy.context.collection.objects.link(obj)
#bpy.context.view_layer.objects.active = obj

#mod_skin = obj.modifiers.new('Skin','SKIN')
        last_frame_length = 0.0
        last_frame_height = 0.0
        f = 0
        for frame in framesList:
            f += 1
            frame_length = frame[0]
            frame_height = frame[1]
            xyz[0] += last_frame_length
            last_frame_length = frame[3] + frame_length
            last_frame_height = frame_height

            planks = calculateFrame(
                          frame_length,
                          frame_height,
                          frame_angle,
                          frame[2],
                          plank_width,
                          space_width,
                          plank_colors,
                          show_frame,
                          frame_width,
                          frame_color,
                          reserve_cut,
                          xyz 
                    ) 
                     
            i=1
            for plank in planks:
                verts, edges, faces = self.createMesh(plank,plank_thickness, xyz) 
                name = f'Fr:{f} Plank Nr.{i}'
                mesh = bpy.data.meshes.new(name) 
                mesh.from_pydata(verts, edges, faces)    
                obj  = bpy.data.objects.new(name, mesh)
                bpy.context.collection.objects.link(obj)
                bpy.context.view_layer.objects.active = obj
                if i==1:
                    new_mat = bpy.data.materials.new(name = "Plank Material")
                so = bpy.context.active_object
                so.data.materials.append(new_mat)
                bpy.context.object.active_material.diffuse_color = plank_colors[0] #change color
                i += 1
        return {'FINISHED'}
