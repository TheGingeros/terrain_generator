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