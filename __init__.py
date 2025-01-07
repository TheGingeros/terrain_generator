bl_info ={
    "name": "Terrain Generator",
    "author": "Gingeros",
    "description": "Addon for generating custom terrain",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Tool"
}
from .ui import *
import bpy
import inspect #Module for extracting class objects from other project's files

classes = inspect.getmembers(ui, inspect.isclass)
UI_Classes = classes[::-1]

def register():
    for class_type in UI_Classes:
        bpy.utils.register_class(class_type[1])

def unregister():
    for class_type in UI_Classes:
        bpy.utils.unregister_class(class_type[1])

if __name__ == "__main__":
    register()