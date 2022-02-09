import bpy
from bpy.types import Context
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from . items import position_items

class OverlaySettings(bpy.types.PropertyGroup):
    def updateSubscribers(self, context:Context):
        try:
            len(self.subscribers)
        except:
            return
        for subscriber in self.subscribers:
            subscriber()

    subscribers: list
    width: FloatProperty(
        name="Width", 
        default=40.0, 
        min=10.0, 
        max=100,
        update=updateSubscribers
    )
    radius: FloatProperty(
        name="Radius", 
        default=35.0, 
        min=10.0, 
        max=100.0,
        update=updateSubscribers
    )
    isVisible: BoolProperty(
        name="Show Overlay", 
        default=False, 
        update=updateSubscribers
    )
    gizmo_colors = {
            "disabled": {
                "color": [0.0,0.0,0.0],
                "color_highlight": [0.0,0.0,0.0],
                "alpha": 0.3,
                "alpha_highlight": 0.3
        },
            "active": {
                "color": [0.0,0.0,0.0],
                "color_highlight": [0.8,0.8,0.8],
                "alpha": 0.3,
                "alpha_highlight": 0.3
        }
    }
    show_fullscreen: BoolProperty(
        name="Show Quadview", 
        default=True 
    )
    show_quadview: BoolProperty(
        name="Show Quadview", 
        default=True 
    )
    show_snap_view: BoolProperty(
        name="Show Snap View", 
        default=True 
    )
    show_rotation_lock: BoolProperty(
        name="Show Rotation Lock", 
        default=True 
    )
    show_voxel_resize: BoolProperty(
        name="Show Voxel Resize", 
        default=True 
    )
    show_voxel_remesh: BoolProperty(
        name="Show Voxel Remesh", 
        default=True 
    )
    gizmo_position: EnumProperty(
        items=position_items,
        name="Gizmo Position",
        default="BOTTOM"
    )
    gizmo_sets = {
        # ALL includes only the modes in this list
        "ALL": {
            "fullscreen",
            "quadview",
            "snap_view",
            "center_on_cursor",
            "rotation_lock"
        },
        "SCULPT": {
            "voxel_resize",
            "voxel_remesh"
        },
        "OBJECT":{},
        "EDIT":{},
        "POSE":{},
        "TEXTURE_PAINT":{}
    }

    def subscribe(self, function):
        try:
            len(self.subscribers)
        except:
            self.subscribers = []
        self.subscribers.append(function)

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100
