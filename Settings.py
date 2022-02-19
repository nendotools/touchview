import bpy
from bpy.types import Context
from bpy.props import BoolProperty, FloatVectorProperty, EnumProperty, FloatProperty, StringProperty
from .lib.items import position_items, pivot_items

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
    pivot_mode: EnumProperty(
            name="Sculpt Pivot Mode",
            items=pivot_items,
            default="SURFACE"
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
                "alpha": 0.5,
                "color_highlight": [0.5,0.5,0.5],
                "alpha_highlight": 0.5
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
    show_pivot_mode: BoolProperty(
        name="Pivot Mode", 
        default=True 
    )
    show_snap_view: BoolProperty(
        name="Snap View", 
        default=True 
    )
    show_n_panel: BoolProperty(
        name="N Panel", 
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
        default="RIGHT"
    )
    gizmo_sets = {
        # ALL includes only the modes in this list
        "ALL": {
            "fullscreen",
            "quadview",
            "snap_view",
            "n_panel",
            "rotation_lock"
        },
        "SCULPT": {
            "pivot_mode",
            "voxel_resize",
            "voxel_remesh"
        },
        "OBJECT":{},
        "EDIT":{},
        "POSE":{},
        "TEXTURE_PAINT":{}
    }
    floating_position: FloatVectorProperty(
        name= "Floating Offset",
        default= (95.00,5.00),
        size=2,
        precision=2,
        step=1,
        soft_min=5,
        soft_max=100
    )

    show_float_menu: BoolProperty(
        name="Enable Floating Menu",
        default=False
    )

    menu_slot_1: StringProperty(
        name="Menu Item",
        default= "object.quadriflow_remesh"
    )

    menu_slot_2: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_3: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_4: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_5: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_6: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_7: StringProperty(
        name="Menu Item",
        default= ""
    )

    menu_slot_8: StringProperty(
        name="Menu Item",
        default= "view3d.move_float_menu"
    )

# set up addon preferences UI
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

        col.separator()
        col.prop(self, "show_float_menu")

        box = col.box()
        box.active = self.show_float_menu
        col = box.column()
        col.prop(self, "floating_position")
        for i in range(7):
            col.prop(self, "menu_slot_"+str(i+1))

    def getGizmoSet(self, mode:str):
        available = list(self.gizmo_sets["ALL"])
        
        if not self.gizmo_sets[mode]: return available
        return available + list(self.gizmo_sets[mode])
        

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100
