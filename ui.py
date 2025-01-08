import bpy

from .CCreateTerrain import OBJECT_OT_create_terrain

class OBJECT_PT_TerrainGenerator_UI(bpy.types.Panel):
    bl_idname = "OBJECT_PT_TerrainGenerator_UI"
    bl_label = "Terrain Generator" #Name when tab is open
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Terrain Generator" #Name of the category in 3d view
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self,context):
        layout = self.layout

        row = layout.row()
        bt_createTerrain = row.operator(
            "object.create_terrain",
            text="Create Terrain"
        )
        if not context.scene.terrainGenerated:
            pass
        else:
            box = layout.box()
            box.label(
                text="Terrain Properties:"
            )
            row = box.row()
            row.prop(
                context.scene,
                "terrainSize"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "numberOfSubdivision"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "terrainVariety"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "terrainDetail"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "terrainRoughness"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "terrainDistortion"   
            )
            row = box.row()
            row.prop(
                context.scene,
                "randomSeed"   
            )
        