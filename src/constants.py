import bpy
from bpy.types import Context
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from . items import position_items

class OverlaySettings(bpy.types.AddonPreferences):
    bl_idname = __package__

    width: FloatProperty(
        name="Width", 
        default=40.0, 
        min=10.0, 
        max=100,
    )
    radius: FloatProperty(
        name="Radius", 
        default=35.0, 
        min=10.0, 
        max=100.0,
    )
    isVisible: BoolProperty(
        name="Show Overlay", 
        default=False, 
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
        name="Fullscreen", 
        default=True 
    )
    show_quadview: BoolProperty(
        name="Quadview", 
        default=True 
    )
    show_snap_view: BoolProperty(
        name="Snap View", 
        default=True 
    )
    show_rotation_lock: BoolProperty(
        name="Rotation Lock", 
        default=True 
    )
    show_voxel_resize: BoolProperty(
        name="Voxel Resize", 
        default=True 
    )
    show_voxel_remesh: BoolProperty(
        name="Voxel Remesh", 
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

    def draw(self, context:Context):
        row = self.layout.row()
        col = row.column()
        col.label(text="Control Zones")
        col.prop(self, "width")
        col.prop(self, "radius")
        col.prop(self, "isVisible", text="Show Overlay")
        
        col = row.column()
        col.label(text="Viewport Options")
        col.prop_menu_enum(self, "gizmo_position")

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100
