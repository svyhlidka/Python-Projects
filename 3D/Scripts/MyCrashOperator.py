import bpy
from math import radians
from bpy.props import *

class MyCrashOperator(bpy.types.Operator):
    
    bl_idname  = "object.my_crash_operator"
    bl_label   = "Crash Operator"
    bl_options = {'REGISTER', 'UNDO'} 

    #create properties
    noise_scale: FloatProperty(
       name = "Noise Scale",
       description = "The scale of the noise",
       default = 1.0,
       min = 0.0,
       max = 2.0
    )
    
    def execute(self, context):     


        #create cube
        bpy.ops.mesh.primitive_cube_add()

        # so  - for selected object


        so = bpy.context.active_object

        #move object
        so.location[0] = 3

        #rotation X
        degrees = 45
        #rad = degrees * pi / 180
        so.rotation_euler[0] += radians(45)

        #create a modifier
        #so.modifiers.new("My Modifier", 'SUBSURF')
        #so.modifiers["My Modifier"].levels = 3

        # or better
        mod_subsurf = so.modifiers.new("My Modifier", 'SUBSURF')
        mod_subsurf.levels = 3
        #mod_subsurf.render_levels = 3
        # etc


        #shading 

        bpy.ops.object.shade_smooth()

        # or more convoluted way
        #mesh = so.data
        #for face in mesh.polygons:
        #    face.use_smooth = True

        #create displacement modifier  for texture
        # https://docs.blender.org/api/current/bpy.types.Modifier.html
        mod_displace = so.modifiers.new("My Displacement", 'DISPLACE')

        #create texture
        # https://docs.blender.org/api/current/bpy.types.Texture.html
        new_tex = bpy.data.textures.new("My Texture", 'DISTORTED_NOISE')

        #change the texture settings
        #new_tex.noise_scale = 0.23
        new_tex.noise_scale = self.noise_scale

        #assign the texture to displacement modifier

        mod_displace.texture = new_tex

        #materials

        new_mat = bpy.data.materials.new(name = "My Material")
        so.data.materials.append(new_mat)

        #going to use nodes
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes  # just a shortcut

        material_output = nodes.get("Material Output")

        #creating emisive shader
        node_emission = nodes.new(type='ShaderNodeEmission')


        node_emission.inputs[0].default_value = (0.0, 0.3, 1.0, 1)  #"Cyan"  Base Color
        node_emission.inputs[1].default_value = 500.0 #strength

        #having two nodes material_output and node_emission
        #need to be connected 
        #left side inputs (list[0,1,...])  right side outputs
        # Base Color 0, SubSurface 1, ...

        links = new_mat.node_tree.links
        new_link = links.new(node_emission.outputs[0], material_output.inputs[0])     

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MyCrashOperator)


def unregister():
    bpy.utils.unregister_class(MyCrashOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.my_crash_operator()
