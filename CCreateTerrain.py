import bpy
import random

class OBJECT_OT_create_terrain(bpy.types.Operator):
    """Creates terrain object based on the parameters"""
    bl_idname = "object.create_terrain"
    bl_label = ""
    def __init__(self):
        self.terrainObject = None
    def execute(self, context):
        self.createTerrain(context)
        return {'FINISHED'}
    def createTerrain(self, context):
        userSize = context.scene.terrainSize
        userSubdivision = context.scene.numberOfSubdivision
        # userSize = 2
        # userSubdivision = 50
        print(context.scene.terrainSize)
        bpy.ops.mesh.primitive_grid_add(
            x_subdivisions=userSubdivision, 
            y_subdivisions=userSubdivision, 
            enter_editmode=False, 
            align='WORLD', 
            location=(0, 0, 0), 
            scale=(1, 1, 1),
            size=userSize)
        

        selectedObjs = bpy.context.selected_objects
        terrainObject = selectedObjs[0]
        terrainObject.name="Terrain"
        self.terrainObject = terrainObject
        self.createTerrainMaterial(context)

        print("Terrain Created")
        context.scene.terrainGenerated = True

    def createTerrainMaterial(self, context):
        geo_nodes = self.terrainObject.modifiers.new(name="TerrainGenerator", type='NODES')
        node_group = bpy.data.node_groups.new(name="TerrainGeneratorGroup", type='GeometryNodeTree')
        
        geo_nodes.node_group = node_group
        nodes = node_group.nodes
        links = node_group.links

        geometry_input = node_group.interface.new_socket(
            name="Geometry",
            description="",
            in_out='INPUT',
            socket_type='NodeSocketGeometry'
        )
        geometry_output = node_group.interface.new_socket(
            name="Geometry",
            description="",
            in_out='OUTPUT',
            socket_type='NodeSocketGeometry'
        )
        # Create input and output nodes
        group_input = nodes.new(type="NodeGroupInput")
        group_input.location = (-400, 0)


        group_output = nodes.new(type="NodeGroupOutput")
        group_output.location = (400, 0)

        # Add a Noise Texture node
        noise_texture = nodes.new(type="ShaderNodeTexNoise")
        noise_texture.location = (-200, 200)
        noise_texture.noise_dimensions = '4D'

        # Add a Combine XYZ node to offset positions
        combine_xyz = nodes.new(type="ShaderNodeCombineXYZ")
        combine_xyz.location = (0, 200)

        # Add a Set Position node to apply displacement
        set_position = nodes.new(type="GeometryNodeSetPosition")
        set_position.location = (200, 0)

        # Add a Random Value node for randomness
        random_value = nodes.new(type="ShaderNodeValue")
        random_value.location = (-400, 0)

        # Generate a random seed for the noise
        random_seed = random.uniform(0, 100)
        random_value.outputs[0].default_value = random_seed

        # Link nodes
        links.new(group_input.outputs[0], set_position.inputs["Geometry"])
        links.new(noise_texture.outputs["Fac"], combine_xyz.inputs["Z"])
        links.new(combine_xyz.outputs["Vector"], set_position.inputs["Offset"])
        links.new(set_position.outputs["Geometry"], group_output.inputs[0])
        links.new(random_value.outputs[0], noise_texture.inputs["W"])

        # Adjust Noise Texture properties
        noise_texture.inputs["Scale"].default_value = 1.0  # Scale of the terrain features
        noise_texture.inputs["Detail"].default_value = 5.0  # Fine detail in the noise
        noise_texture.inputs["Roughness"].default_value = 0.5
        noise_texture.inputs["Distortion"].default_value = 0.0

        # Apply smooth shading to the object
        bpy.ops.object.shade_smooth()
    def updateTerrainValues(self, context):
        if not context.scene.terrainObject:
            print("Terrain object no longer exists")
            return
        terrainObject = bpy.data.objects.get(context.scene.terrainObject)

        for mod in terrainObject.modifiers:
            if mod.type == 'NODES':
                geoMod = mod

        node_group = geoMod.node_group
        for node in node_group.nodes:
            if node.type == 'TEX_NOISE':
                noiseTexture = node
        
        terrainObject.scale = (context.scene.terrainSize/2,context.scene.terrainSize/2,context.scene.terrainSize/2)
        noiseTexture.inputs["Scale"].default_value = context.scene.terrainVariety
        noiseTexture.inputs["Detail"].default_value = context.scene.terrainDetail
        noiseTexture.inputs["Roughness"].default_value = context.scene.terrainRoughness
        noiseTexture.inputs["Distortion"].default_value = context.scene.terrainDistortion
    def getTerrainObject(self, context):
        sets = []
        objs = context.selectable_objects
        for obj in objs:
            if obj.name == 'Terrain':
                sets.append((obj.name, obj.name, obj.name))
        for set in sets:
            if (bpy.data.objects.find(set[0]))==-1:
                sets.remove(set)
        return sets
    
    bpy.types.Scene.terrainObject = bpy.props.EnumProperty(
         name="terrainObject",
         items=getTerrainObject,
         update=updateTerrainValues
     )
    bpy.types.Scene.terrainSize = bpy.props.IntProperty(
        name="Size of Terrain", 
        default=2,
        min=0,
        update=updateTerrainValues
        )
    bpy.types.Scene.numberOfSubdivision = bpy.props.IntProperty(
        name="Number of cuts for the grid object",
        default=50,
        min=0)
    bpy.types.Scene.terrainVariety = bpy.props.FloatProperty(
        name="Terrain Variety",
        default=1,
        update=updateTerrainValues)
    bpy.types.Scene.terrainDetail = bpy.props.FloatProperty(
        name="Terrain Detail",
        default=5,
        update=updateTerrainValues)
    bpy.types.Scene.terrainRoughness = bpy.props.FloatProperty(
        name="Terrain Roughness",
        default=0.5,
        min=0.0,
        max=1.0,
        update=updateTerrainValues)
    bpy.types.Scene.terrainDistortion = bpy.props.FloatProperty(
        name="Terrain Distortion",
        default=0,
        update=updateTerrainValues)
    bpy.types.Scene.randomSeed = bpy.props.FloatProperty(
        name="Random seed for Terrain Generation",
        default=50)
    bpy.types.Scene.terrainGenerated = bpy.props.BoolProperty(
        name="Check if terrain was generated",
        default=False
    )