import bpy
import mathutils
import math

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

class OBJECT_OT_add_plane_cuts(bpy.types.Operator):
    """Adds plane cuts to the current selected terrain object"""
    bl_idname = "object.add_plane_cuts"
    bl_label = ""

    def execute(self, context):
        if not context.selected_objects or len(context.selected_objects) > 1:
            self.report({"WARNING"}, "Select one object!")
            return {'CANCELLED'}
        
        self.addPlaneCuts(context)
        return {'FINISHED'}

    def addPlaneCuts(self, context):
        # Create Copy of the terrain for possible reuse and hide it
        if context.scene.custom_mesh:
            print(context.scene.selectable_meshes)
            terrainObject = obj = bpy.data.objects.get(context.scene.selectable_meshes)
        else:
            for obj in context.selected_objects:
                terrainObject = obj
        
        terrainObjectDuplicate = terrainObject.copy()
        terrainObjectDuplicate.name = "Contour Lines"
        original_collection = terrainObject.users_collection[0]
        original_collection.objects.link(terrainObjectDuplicate)
        terrainObject.hide_set(True)

        # Add Plane at the same origin at the lowest point of the terrain
        plane = self.createPlane(context, terrainObjectDuplicate)
        
        # Add Boolean modifier to the terrain object
        bool_modifier = terrainObjectDuplicate.modifiers.new(name="Boolean", type='BOOLEAN')
        bool_modifier.operation = 'INTERSECT'  # Set the operation to Intersect
        bool_modifier.use_self = False  # Don't use the terrain itself
        #bool_modifier.use_flip_normals = False  # Don't flip the normals
        bool_modifier.solver = 'FAST'
        # Set the right source
        bool_modifier.object = plane

    def createPlane(self, context, terrain):
        world_matrix = terrain.matrix_world
        world_vertices = [world_matrix @ vert.co for vert in terrain.data.vertices]
        # Find the lowest z value
        min_z = min(v.z for v in world_vertices)
        max_z = max(v.z for v in world_vertices)

        # Calculate the terrain's bounding box (in world coordinates)
        min_x = min(v.x for v in world_vertices)
        max_x = max(v.x for v in world_vertices)
        min_y = min(v.y for v in world_vertices)
        max_y = max(v.y for v in world_vertices)

        # Calculate width and length of the terrain
        width = max_x - min_x
        length = max_y - min_y

        # Create a new plane with the same width and length as the terrain
        bpy.ops.mesh.primitive_plane_add(size=2)  # Default plane size is 2, we will scale it later
        plane = bpy.context.object  # The newly created plane
        plane.name = "Terrain Cutter"
        # Scale the plane to match the terrain's size
        plane.scale = (width / 2, length / 2, 1)

        plane.location = mathutils.Vector((terrain.location.x, terrain.location.y, min_z))

        # Add Array modifier to the plane
        array_modifier = plane.modifiers.new(name="Array", type='ARRAY')

        # Set the array modifier's properties
        array_modifier.fit_type = 'FIXED_COUNT'  # Use fixed count
        array_modifier.use_relative_offset = False  # Use constant offset
        array_modifier.use_constant_offset = True  # Use constant offset

       # Calculate the required number of planes
        z_offset = 0.02  # Offset for each plane in Z direction
        distance = max_z - min_z
        num_planes = math.ceil(distance / z_offset)  # Round up to ensure we reach or exceed the max_z

        array_modifier.count = num_planes  # Set the number of planes to cover the distance
        array_modifier.constant_offset_displace = mathutils.Vector((0, 0, z_offset))  # Set Z offset to 0.02

        return plane