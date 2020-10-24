# when done, addon must be installed
# Edit->Preferences->Addons->Install->navigate to this file on disk
# ->select it-> Install Add-on -> click check box Add Mesh



bl_info = {
    "name": "Object Adder",
    "author": "rosomak",
    "version": "(1.0)",
    "blender": "(2.80.0)",
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy

class TestPanel(bpy.types.Panel):
    bl_label       = "Test Panel"
    bl_idname      = "PT_TestPanel"  # PT test Panel
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "My First Addon"  # like "Tool" after pressing n
    bl_options     = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()  # like add a new space
        row.label(text= "Sample Text", icon='CUBE' )
        # now adding operation - cube
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon='CUBE')
        #now adding another operation - sphere
        row = layout.row()
        #how to find the new object name: shift A
        row.operator("mesh.primitive_uv_sphere_add", icon='SPHERE')
        row = layout.row()
        row.operator("object.text_add", icon='SPHERE')
        row = layout.row()
        row.operator("object.text_add", icon = 'FILE_FONT', text="Font Button")
    
        
class PanelA(bpy.types.Panel):
    bl_label       = "Panel A"
    bl_idname      = "PT_PanelA"  # PT test Panel
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "My First Addon"  # like "Tool" after pressing n
    bl_parent_id   = "PT_TestPanel" # to create a sub panel of main panel
    bl_options     = {"DEFAULT_CLOSED"}

            
    def draw(self, context):
        layout = self.layout
        obj = context.object # to shorten text below
        
        row = layout.row()  # like add a new space
        row.label(text= "Select an option to scale your object ", icon='FONT_DATA' )
        row = layout.row()
        row.operator("transform.resize")
        row = layout.row()
      #  row.prop(context.object,"scale") # shows details
      # version in one row
      # ----------------------------
        #row.prop(obj,"scale")  # short version of above
      # ----------------------------
  
      # version in column in a separate row:
      # ----------------------------
        col = layout.column()
        col.prop(obj,"scale")
      # ----------------------------
        
class PanelB(bpy.types.Panel):
    bl_label       = "Specials"
    bl_idname      = "PT_PanelB"  # PT test Panel
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "My First Addon"  # like "Tool" after pressing n
    bl_parent_id   = "PT_TestPanel"
    bl_options     = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()  # like add a new space
        row.label(text= "Select a special option", icon="COLOR_BLUE" )
        row = layout.row()
        row.operator("object.shade_smooth", icon="MOD_SMOOTH", text="Set Smooth Shading")
        row.operator("object.subdivision_set")
        row = layout.row()
        row.operator("object.modifier_add")
        

        


# new class  must be registered

def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(PanelA)
    bpy.utils.register_class(PanelB)
    
def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(PanelB)

if __name__ == "__main__":

    register()