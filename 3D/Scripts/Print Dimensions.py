# import the necessary modules we need
# in our case, blender's python API and python's os module
import bpy, os

# get the current selection
selection = bpy.context.selected_objects

# initialize a blank result variable
result = ""

# iterate through the selected objects
for sel in selection:
    # get the current object's dimensions
    dims = sel.dimensions
    # write the selected object's name and dimensions to a string
    result += "%s - %.03fm x %.03fm x %.03fm\n" % (sel.name, dims.x, dims.y, dims.z)

# get path to render output (usually /tmp\)
tempFolder = os.path.abspath (bpy.context.scene.render.filepath)
# make a filename
filename = os.path.join (tempFolder, "newfile.txt")
# confirm path exists
os.makedirs(os.path.dirname(filename), exist_ok=True)
# open a file to write to
file = open(filename, "w")
# write the data to file
file.write(result)
# close the file
file.close()
