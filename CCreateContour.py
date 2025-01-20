import bpy

def getobjs(self, context):
    sets = []
    objs = context.selectable_objects

    #Go through objects in scene, if its mesh, store it
    for obj in objs:
        if obj.type == 'MESH':
            sets.append((obj.name, obj.name, obj.name))

    #Go through our created list of meshes. If the object no longer exists, we delete it from our list
    for set in sets:
        if (bpy.data.objects.find(set[0]))==-1:
            sets.remove(set)
    return sets
def obj_update(self, context):
    pass

bpy.types.Scene.selectable_meshes = bpy.props.EnumProperty(
    items=getobjs, 
    update=obj_update, 
    name="All Available Meshes")

bpy.types.Scene.custom_mesh = bpy.props.BoolProperty(
    name="custom_mesh")

class OBJECT_OT_create_contour_lines(bpy.types.Operator):
    """Creates countour lines from selected object"""
    bl_idname = "object.create_contour_lines"
    bl_label = ""

    def execute(self, context):
        if not context.selected_objects or len(context.selected_objects) > 1:
            self.report({"WARNING"}, "Select one object!")
            return {'CANCELLED'}

        self.createContour(context)
        return {'FINISHED'}

    def createContour(self, context):
        pass
