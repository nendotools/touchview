import bpy
from bpy.types import Context, PropertyGroup
from bpy.props import BoolProperty, CollectionProperty, FloatVectorProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from .lib.items import position_items, pivot_items, edit_modes, menu_defaults 

class MenuModeGroup(PropertyGroup):
    mode: StringProperty(name="mode", default="OBJECT")
    menu_slot_1: StringProperty(
        name="Menu Item",
        default= ""
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

    menu_slot_8 = "view3d.move_float_menu"


class OverlaySettings(bpy.types.AddonPreferences):
    bl_idname = __package__

    is_enabled: BoolProperty(
        name="Enable Controls", 
        default=True, 
    )
    include_mmb: BoolProperty(
        name="Include MIDDLEMOUSE",
        default=False,
    )
    swap_panrotate: BoolProperty(
        name="Swap Pan/Rotate",
        default=False, 
    )
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
    overlay_main_color: FloatVectorProperty(
        name="Overlay Main Color",
        default=(1.0, 1.0, 1.0, 0.01),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        size=4,
    )
    use_multiple_colors: BoolProperty(
        name="Multicolor Overlay", 
        default=False, 
    )
    overlay_secondary_color: FloatVectorProperty(
        name="Overlay Secondary Color",
        default=(1.0, 1.0, 1.0, 0.01),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        size=4,
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
        },
            "error": {
                "color": [0.3,0.0,0.0],
                "alpha": 0.15,
                "color_highlight": [1.0,0.2,0.2],
                "alpha_highlight": 0.5
        },
            "warn": {
                "color": [0.35,0.3,0.14],
                "alpha": 0.15,
                "color_highlight": [0.8,0.7,0.3],
                "alpha_highlight": 0.3
        }
    }
    show_undoredo: BoolProperty(
        name="Undo/Redo",
        default=True 
    )
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
    show_multires: BoolProperty(
        name="Multires", 
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
    subdivision_limit: IntProperty(
        name="Subdivision Limit",
        default=4,
        min=1,
        max=7
    )
    gizmo_sets = {
        # ALL includes only the modes in this list
        "ALL": {
            "undoredo",
            "fullscreen",
            "quadview",
            "snap_view",
            "n_panel",
            "rotation_lock"
        },
        "SCULPT": {
            "pivot_mode",
            "voxel_remesh",
            "multires"
        },
        "OBJECT":{
            "multires"
        },
        "EDIT_MESH":{},
        "POSE":{},
        "PAINT_TEXTURE":{},
        "PAINT_VERTEX":{},
        "PAINT_WEIGHT":{}
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

    active_menu: EnumProperty(name="Mode Settings", items=edit_modes)
    menu_sets: CollectionProperty(type=MenuModeGroup)

# set up addon preferences UI
    def draw(self, context:Context):
        row = self.layout.row()
        col = row.column()
        col.label(text="Control Zones")
        if self.is_enabled:
            col.operator("view3d.toggle_touch", text="Touch Enabled", depress=True)
        else:
            col.operator("view3d.toggle_touch", text="Touch Disabled")
        col.prop(self, "include_mmb")
        col.prop(self, "swap_panrotate")
        col.prop(self, "isVisible", text="Show Overlay")
        col.prop(self, "use_multiple_colors")
        col.prop(self, "overlay_main_color", text="Main Color")
        if self.use_multiple_colors:
            col.prop(self, "overlay_secondary_color", text="Secondary Color")
        col.prop(self, "width")
        col.prop(self, "radius")
        
        col = row.column()
        col.label(text="Viewport Options")
        col.prop_menu_enum(self, "gizmo_position")
        col.prop(self, "subdivision_limit")
        col.separator()

        if not self.show_float_menu:
            col.operator("view3d.toggle_floating_menu", text="Show Floating Menu")
        else:
            col.operator("view3d.toggle_floating_menu", text="Hide Floating Menu", depress=True)
            box = col.box()
            box.active = self.show_float_menu
            col = box.column()
            col.prop(self, "floating_position")
            col.prop(self, "active_menu")
            mList = self.getMenuSettings(self.active_menu)
            for i in range(7):
                col.prop(mList, "menu_slot_"+str(i+1))

    def getMenuSettings(self, mode:str):
        m = None
        for opts in self.menu_sets:
            if opts.mode == mode:
                m = opts
        if m == None:
            m = self.menu_sets.add()
            m.mode = mode
            ops = menu_defaults[mode]
            for i, o in enumerate(ops):
                setattr(m, "menu_slot_"+str(i+1), o)
        return m

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
