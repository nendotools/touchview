bl_info = {
    "name": "Touch Viewport",
    "description": "Creates active touch zones over View 2D and 3D areas",
    "author": "NENDO, Karan @b3dhub",
    "blender": (4, 2, 0),
    "version": (4, 3, 0),
    "category": "3D View",
    "location": "View3D > Sidebar(N-Panel) > Touch View",
    "warning": "",
    "doc_url": "https://github.com/nendotools/touchview",
    "tracker_url": "https://github.com/nendotools/touchview/issues",
}


import bpy

from . import source


def register():
    source.register()


def unregister():
    source.unregister()
