import bpy

class CUserProperties(bpy.types.PropertyGroup):
    terrainSize: bpy.props.FloatProperty(name="Size of terrain", default=2) # type: ignore
    numberOfSubdivision: bpy.props.FloatProperty(name="Number of cuts for the grid object", default=10) # type: ignore
    terrainVariety: bpy.props.FloatProperty(name="Terrain Variety", default=1) # type: ignore
    terrainDetail: bpy.props.FloatProperty(name="Terrain Detail", default=5) # type: ignore
    terrainRoughness: bpy.props.FloatProperty(name="Terrain Roughness", default=0.5) # type: ignore
    terrainDistortion: bpy.props.FloatProperty(name="Terrain Distortion", default=0) # type: ignore
    randomSeed: bpy.props.FloatProperty(name="Random seed for terrain generation", default=50) # type: ignore
