import bpy

class OBJECT_OT_create_terrain(bpy.types.Operator):
    """Creates terrain object based on the parameters"""
    bl_idname = "object.create_terrain"
    bl_label = ""
    def execute(self, context):
        print("Terrain Created")
        return {'FINISHED'}