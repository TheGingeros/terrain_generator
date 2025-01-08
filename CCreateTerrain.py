import bpy
import random

class OBJECT_OT_create_terrain(bpy.types.Operator):
    """Creates terrain object based on the parameters"""
    bl_idname = "object.create_terrain"
    bl_label = ""
    def execute(self, context):
        self.createTerrain(context)
        return {'FINISHED'}
    
    def createTerrain(self, context):
        userSize = 10
        userSubdivision = 50
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
        self.createTerrainMaterial(context, terrainObject)
        # terrainMaterial = self.createTerrainMaterial(context, terrainObject)
        # terrainObject.data.materials.append(terrainMaterial)

        print("Terrain Created")

    def createTerrainMaterialUsingModifier(self, context, grid):

        # Add a Subdivision Surface modifier for more geometry
        bpy.ops.object.modifier_add(type='SUBSURF')
        subsurf_mod = grid.modifiers[-1]
        subsurf_mod.levels = 4  # Viewport subdivisions
        subsurf_mod.render_levels = 6  # Render subdivisions

        # Add a Displace modifier for terrain shaping
        bpy.ops.object.modifier_add(type='DISPLACE')
        displace_mod = grid.modifiers[-1]
        displace_mod.name = "TerrainDisplacement"

        # Create a new texture for the displacement modifier
        disp_texture = bpy.data.textures.new(name="TerrainHeightMap", type='CLOUDS')
        disp_texture.noise_scale = 2.0  # Adjust noise scale for terrain detail
        disp_texture.noise_depth = 4  # Increase detail in the noise

        # Assign the texture to the displacement modifier
        displace_mod.texture = disp_texture
        displace_mod.texture_coords = 'GLOBAL'

        # Apply smooth shading to the object
        bpy.ops.object.shade_smooth()

    def createTerrainMaterial(self, context, grid):
        geo_nodes = grid.modifiers.new(name="TerrainGenerator", type='NODES')
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

        # Link input to output (pass-through)
        #links.new(group_input.outputs[0], group_output.inputs[0])

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

        # Apply smooth shading to the object
        bpy.ops.object.shade_smooth()