import bpy

from .CCreateTerrain import OBJECT_OT_create_terrain
from .CCreateContour import *

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
        bt_createTerrain = box.operator(
            "object.create_terrain",
            text="Create Terrain"
        )
        if not context.scene.terrainObject:
            pass
        else:
            box = layout.box()
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

class OBJECT_PT_ContourLinesGenerator_UI(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ContourLinesGenerator_UI"
    bl_label = "Contour Lines Generator" #Name when tab is open
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Terrain Generator" #Name of the category in 3d view
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = OBJECT_PT_TerrainGenerator_UI.bl_idname
    bl_order = 0

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self,context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(
            context.scene,
            "custom_mesh",
            text="Use Custom Object"
        )
        if(context.scene.custom_mesh):
            if context.scene.custom_mesh:
                row.prop(
                    context.scene, 
                    "selectable_meshes", 
                    text="Terrain Object")
            else:
                row.label(
                    text="No Mesh in Scene. Create one."
                )
        else:
            row.label(text="Selected object will be used")

        bt_createContour = box.operator(
            "object.add_plane_cuts",
            text="Add plane cuts"
        )
            

            