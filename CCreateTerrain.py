import bpy

class OBJECT_OT_create_terrain(bpy.types.Operator):
    """Creates terrain object based on the parameters"""
    bl_idname = "object.create_terrain"
    bl_label = ""
    def execute(self, context):
        self.createTerrain(context)
        return {'FINISHED'}
    
    def createTerrain(self, context):
        userSize = 20
        userSubdivision = 5
        bpy.ops.mesh.primitive_plane_add(size=userSize, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
        print("Terrain Created")