# type: ignore
import json
from os import path

from bpy.props import (BoolProperty, CollectionProperty, EnumProperty,
                       FloatProperty, FloatVectorProperty, IntProperty,
                       StringProperty)
from bpy.types import AddonPreferences, Context, PropertyGroup

from .lib.constants import (double_click_items, edit_modes, gizmo_sets,
                            menu_defaults, menu_orientation_items,
                            menu_style_items, pivot_items, position_items)


##
# Action Menu Settings
##
class MenuModeGroup(PropertyGroup):
    mode: StringProperty(name="mode", default="OBJECT")
    menu_slot_1: StringProperty(name="Menu Item", default="")
    menu_slot_2: StringProperty(name="Menu Item", default="")
    menu_slot_3: StringProperty(name="Menu Item", default="")
    menu_slot_4: StringProperty(name="Menu Item", default="")
    menu_slot_5: StringProperty(name="Menu Item", default="")
    menu_slot_6: StringProperty(name="Menu Item", default="")
    menu_slot_7: StringProperty(name="Menu Item", default="")
    menu_slot_8: StringProperty(name="Menu Item", default="")

    def to_dict(self):
        return {
            "mode": self.mode,
            "menu_slot_1": self.menu_slot_1,
            "menu_slot_2": self.menu_slot_2,
            "menu_slot_3": self.menu_slot_3,
            "menu_slot_4": self.menu_slot_4,
            "menu_slot_5": self.menu_slot_5,
            "menu_slot_6": self.menu_slot_6,
            "menu_slot_7": self.menu_slot_7,
            "menu_slot_8": self.menu_slot_8,
        }

    def from_dict(self, data: dict):
        self.mode = data.get("mode", "OBJECT")
        self.menu_slot_1 = data.get("menu_slot_1", "")
        self.menu_slot_2 = data.get("menu_slot_2", "")
        self.menu_slot_3 = data.get("menu_slot_3", "")
        self.menu_slot_4 = data.get("menu_slot_4", "")
        self.menu_slot_5 = data.get("menu_slot_5", "")
        self.menu_slot_6 = data.get("menu_slot_6", "")
        self.menu_slot_7 = data.get("menu_slot_7", "")
        self.menu_slot_8 = data.get("menu_slot_8", "")


class OverlaySettings(AddonPreferences):
    bl_idname = __package__

    ##
    # Viewport Control Options
    ##
    is_enabled: BoolProperty(name="Enable Controls", default=True)
    lazy_mode: BoolProperty(
        name="Lazy Mode",
        default=False,
        description="always control camera when not touching selected object",
    )
    toggle_position: FloatVectorProperty(
        name="Toggle Position", subtype="XYZ", default=(0.5, 0.5, 0.0)
    )
    toggle_color: FloatVectorProperty(
        name="Toggle Button Color",
        default=(0.1, 0.1, 0.2, 0.5),
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
    )

    isVisible: BoolProperty(name="Show Overlay", default=False)

    input_mode: EnumProperty(
        items=[
            ("full", "full", "mouse/touch and pen input"),
            ("pen", "pen", "pen input only"),
            ("touch", "touch", "mouse/touch input only"),
        ],
        name="Input Mode",
        default="full",
    )
    enable_floating_toggle: BoolProperty(
        name="Enable Floating Toggle",
        description="Allows using floating toggle on mixed input mode",
        default=False,
    )

    enable_double_click: BoolProperty(name="Enable Double Click", default=True)
    double_click_mode: EnumProperty(
        items=double_click_items,
        name="Double Click Mode",
        default="screen.screen_full_area",
    )

    enable_right_click: BoolProperty(name="Enable Right Click", default=True)
    right_click_mode: EnumProperty(
        items=double_click_items,
        name="Right Click Mode",
        default="wm.window_fullscreen_toggle",
    )
    right_click_source: EnumProperty(
        items=[
            ("none", "none", "disabled"),
            ("mouse", "mouse", "mouse/touch right click"),
            ("pen", "pen", "pen right click"),
        ],
        name="Right Click Source",
        default="mouse",
    )

    swap_panrotate: BoolProperty(name="Swap Pan/Rotate", default=False)

    width: FloatProperty(name="Width", default=40.0, min=10.0, max=100)
    radius: FloatProperty(name="Radius", default=35.0, min=10.0, max=100.0)

    use_multiple_colors: BoolProperty(name="Multicolor Overlay", default=False)
    overlay_main_color: FloatVectorProperty(
        name="Overlay Main Color",
        default=(1.0, 1.0, 1.0, 0.01),
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
    )
    overlay_secondary_color: FloatVectorProperty(
        name="Overlay Secondary Color",
        default=(1.0, 1.0, 1.0, 0.01),
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
    )

    ##
    # Gizmo Options
    ##
    show_menu: BoolProperty(name="Toggle Menu Display", default=True)
    show_gizmos: BoolProperty(name="Toggle Gizmos on Menu", default=True)
    menu_style: EnumProperty(
        name="Menu Style", default="float.radial", items=menu_style_items
    )
    menu_orientation: EnumProperty(
        name="Menu Orientation", default="HORIZONTAL", items=menu_orientation_items
    )
    menu_spacing: FloatProperty(
        name="Menu Size", default=20.0, precision=2, step=1, min=0.0, max=200.0
    )
    gizmo_padding: FloatProperty(
        name="Gizmo Padding", default=10, precision=1, step=1, min=1, max=200
    )
    gizmo_scale: FloatProperty(
        name="Gizmo Scale", default=4.0, precision=2, step=1, min=1, max=10.0
    )
    menu_position: FloatVectorProperty(
        name="Menu Position",
        default=(95.00, 5.00),
        size=2,
        precision=2,
        step=1,
        soft_min=5,
        soft_max=100,
    )

    show_undoredo: BoolProperty(name="Undo/Redo", default=True)
    show_is_enabled: BoolProperty(name="Toggle Touch", default=True)
    show_control_gizmo: BoolProperty(name="Toggle Control Gizmo", default=True)
    show_show_fullscreen: BoolProperty(name="Fullscreen", default=True)
    show_region_quadviews: BoolProperty(name="Quadview", default=True)
    show_pivot_mode: BoolProperty(name="Pivot Mode", default=True)
    show_snap_view: BoolProperty(name="Snap View", default=True)
    show_n_panel: BoolProperty(name="N Panel", default=True)
    show_lock_rotation: BoolProperty(name="Rotation Lock", default=True)
    show_multires: BoolProperty(name="Multires", default=True)
    show_voxel_remesh: BoolProperty(name="Voxel Remesh", default=True)
    show_brush_dynamics: BoolProperty(name="Brush Dynamics", default=True)
    show_direction: BoolProperty(name="Brush Direction", default=True)
    gizmo_position: EnumProperty(
        items=position_items, name="Gizmo Position", default="RIGHT"
    )
    subdivision_limit: IntProperty(name="Subdivision Limit", default=4, min=1, max=7)
    pivot_mode: EnumProperty(
        name="Sculpt Pivot Mode", items=pivot_items, default="SURFACE"
    )

    ##
    # Topology Control
    ##
    topology_mode: EnumProperty(
        name="Topology Mode",
        items=[
            ("MANUAL", "manual", "user-defined vertex density"),
            ("RELATIVE", "relative", "relative mesh vertex density steps"),
            (
                "RELATIVE-EXP",
                "exponential",
                "relative mesh vertex density steps with scaling",
            ),
        ],
        default="MANUAL",
    )

    ##
    # Action Menu Options
    ##
    show_float_menu: BoolProperty(name="Enable Floating Menu", default=False)
    floating_position: FloatVectorProperty(
        name="Floating Offset",
        default=(95.00, 5.00),
        size=2,
        precision=2,
        step=1,
        soft_min=5,
        soft_max=100,
    )

    double_click_mode: EnumProperty(
        items=double_click_items,
        name="Double Click Mode",
        default="wm.window_fullscreen_toggle",
    )
    menu_sets: CollectionProperty(type=MenuModeGroup, options={"LIBRARY_EDITABLE"})

    ##
    # UI Panel Controls
    ##
    active_menu: EnumProperty(name="Mode Settings", items=edit_modes)
    gizmo_tabs: EnumProperty(
        name="Gizmo Tabs",
        items=[("MENU", "Gizmo Menu", "", 0), ("ACTIONS", "Action Menu", "", 1)],
        default="MENU",
    )

    def to_dict(self):
        return {
            "is_enabled": self.is_enabled,
            "lazy_mode": self.lazy_mode,
            "enable_floating_toggle": self.enable_floating_toggle,
            "toggle_position": list(self.toggle_position),
            "toggle_color": list(self.toggle_color),
            "is_visible": self.isVisible,
            "input_mode": self.input_mode,
            "enable_double_click": self.enable_double_click,
            "double_click_mode": self.double_click_mode,
            "enable_right_click": self.enable_right_click,
            "right_click_mode": self.right_click_mode,
            "right_click_source": self.right_click_source,
            "swap_panrotate": self.swap_panrotate,
            "width": self.width,
            "radius": self.radius,
            "use_multiple_colors": self.use_multiple_colors,
            "overlay_main_color": list(self.overlay_main_color),
            "overlay_secondary_color": list(self.overlay_secondary_color),
            "show_menu": self.show_menu,
            "show_gizmos": self.show_gizmos,
            "menu_style": self.menu_style,
            "menu_orientation": self.menu_orientation,
            "menu_spacing": self.menu_spacing,
            "gizmo_padding": self.gizmo_padding,
            "gizmo_scale": self.gizmo_scale,
            "menu_position": list(self.menu_position),
            "show_undoredo": self.show_undoredo,
            "show_is_enabled": self.show_is_enabled,
            "show_control_gizmo": self.show_control_gizmo,
            "show_show_fullscreen": self.show_show_fullscreen,
            "show_region_quadviews": self.show_region_quadviews,
            "show_pivot_mode": self.show_pivot_mode,
            "show_snap_view": self.show_snap_view,
            "show_n_panel": self.show_n_panel,
            "show_lock_rotation": self.show_lock_rotation,
            "show_multires": self.show_multires,
            "show_voxel_remesh": self.show_voxel_remesh,
            "show_brush_dynamics": self.show_brush_dynamics,
            "gizmo_position": self.gizmo_position,
            "subdivision_limit": self.subdivision_limit,
            "pivot_mode": self.pivot_mode,
            "topology_mode": self.topology_mode,
            "show_float_menu": self.show_float_menu,
            "floating_position": list(self.floating_position),
            "double_click_mode": self.double_click_mode,
            "active_menu": self.active_menu,
            "gizmo_tabs": self.gizmo_tabs,
            "menu_sets": [m.to_dict() for m in self.menu_sets],
        }

    def from_dict(self, data: dict):
        self.is_enabled = data.get("is_enabled", True)
        self.lazy_mode = data.get("lazy_mode", False)
        self.enable_floating_toggle = data.get("enable_floating_toggle", False)
        self.toggle_position = data.get("toggle_position", (0.5, 0.5, 0.0))
        self.toggle_color = data.get("toggle_color", (0.1, 0.1, 0.2, 0.5))
        self.isVisible = data.get("is_visible", False)
        self.input_mode = data.get("input_mode", "full")
        self.enable_double_click = data.get("enable_double_click", True)
        self.double_click_mode = data.get(
            "double_click_mode", "screen.screen_full_area"
        )
        self.enable_right_click = data.get("enable_right_click", True)
        self.right_click_mode = data.get(
            "right_click_mode", "wm.window_fullscreen_toggle"
        )
        self.right_click_source = data.get("right_click_source", "mouse")
        self.swap_panrotate = data.get("swap_panrotate", False)
        self.width = data.get("width", 40.0)
        self.radius = data.get("radius", 35.0)
        self.use_multiple_colors = data.get("use_multiple_colors", False)
        self.overlay_main_color = data.get("overlay_main_color", (1.0, 1.0, 1.0, 0.01))
        self.overlay_secondary_color = data.get(
            "overlay_secondary_color", (1.0, 1.0, 1.0, 0.01)
        )
        self.show_menu = data.get("show_menu", True)
        self.show_gizmos = data.get("show_gizmos", True)
        self.menu_style = data.get("menu_style", "float.radial")
        self.menu_orientation = data.get("menu_orientation", "HORIZONTAL")
        self.menu_spacing = data.get("menu_spacing", 20.0)
        self.gizmo_padding = data.get("gizmo_padding", 10)
        self.gizmo_scale = data.get("gizmo_scale", 4.0)
        self.menu_position = data.get("menu_position", (95.00, 5.00))
        self.show_undoredo = data.get("show_undoredo", True)
        self.show_is_enabled = data.get("show_is_enabled", True)
        self.show_control_gizmo = data.get("show_control_gizmo", True)
        self.show_show_fullscreen = data.get("show_show_fullscreen", True)
        self.show_region_quadviews = data.get("show_region_quadviews", True)
        self.show_pivot_mode = data.get("show_pivot_mode", True)
        self.show_snap_view = data.get("show_snap_view", True)
        self.show_n_panel = data.get("show_n_panel", True)
        self.show_lock_rotation = data.get("show_lock_rotation", True)
        self.show_multires = data.get("show_multires", True)
        self.show_voxel_remesh = data.get("show_voxel_remesh", True)
        self.show_brush_dynamics = data.get("show_brush_dynamics", True)
        self.gizmo_position = data.get("gizmo_position", "RIGHT")
        self.subdivision_limit = data.get("subdivision_limit", 4)
        self.pivot_mode = data.get("pivot_mode", "SURFACE")
        self.topology_mode = data.get("topology_mode", "MANUAL")
        self.show_float_menu = data.get("show_float_menu", False)
        self.floating_position = data.get("floating_position", (95.00, 5.00))
        self.double_click_mode = data.get(
            "double_click_mode", "wm.window_fullscreen_toggle"
        )
        self.active_menu = data.get("active_menu", "VIEW3D")
        self.gizmo_tabs = data.get("gizmo_tabs", "MENU")
        self.menu_sets = [
            MenuModeGroup().from_dict(m) for m in data.get("menu_sets", [])
        ]

    def load(self):
        filename = path.abspath(path.dirname(__file__) + "/settings.json")
        if not path.exists(filename):
            return None

        data = {}
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.from_dict(data)
        except:
            return None

    def save(self):
        filename = path.abspath(path.dirname(__file__) + "/settings.json")
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)

    # set up addon preferences UI
    def draw(self, _: Context):
        # Input Mode
        col = self.layout.column()
        col.label(text="Input Mode")
        col = col.box()
        if self.input_mode == "full":
            col.label(text="pen, mouse, touch input", icon="CON_CAMERASOLVER")
        if self.input_mode == "pen":
            col.label(text="pen-only input", icon="STYLUS_PRESSURE")
        if self.input_mode == "touch":
            col.label(text="mouse/touch only input", icon="VIEW_PAN")
        tabs = col.column_flow(columns=3, align=True)
        tabs.prop_tabs_enum(self, "input_mode")
        col.prop(self, "lazy_mode", toggle=1)
        if self.input_mode == "full":
            col.prop(self, "enable_floating_toggle", toggle=1)

        # main settings
        row = self.layout.split(factor=0.4)
        ##
        # Viewport Settings
        ##
        col = row.column()
        col.label(text="Control Zones")
        col.label(text="Input Mode")
        col.prop(self, "is_enabled", toggle=1)
        col.prop(self, "swap_panrotate")
        col.prop(self, "isVisible", text="Show Overlay")
        col.prop(self, "use_multiple_colors")
        col.prop(self, "overlay_main_color", text="Main Color")
        if self.use_multiple_colors:
            col.prop(self, "overlay_secondary_color", text="Secondary Color")
        col.prop(self, "width", slider=True)
        col.prop(self, "radius", slider=True)

        ##
        # Gizmo Settings
        ##
        col = row.column()
        col.label(text="Gizmo Options")
        tabs = col.column_flow(columns=3, align=True)
        tabs.prop_tabs_enum(self, "gizmo_tabs")

        main = col.box()
        if self.gizmo_tabs == "MENU":
            main.label(text="Gizmo Menu Style")
            tabs = main.column_flow(columns=2, align=True)
            tabs.prop_tabs_enum(self, "menu_style")

            if self.menu_style == "fixed.bar":
                main.prop_menu_enum(self, "gizmo_position")
            main.prop(self, "menu_spacing", slider=True)
            if self.menu_style == "float.radial":
                main.prop(self, "gizmo_padding", slider=True)
            main.prop(self, "gizmo_scale", slider=True)

            main.separator()
            main.label(text="Input Options")
            wrapper = main.box()
            wrapper.label(text="Right Click Actions")
            r = wrapper.split(factor=0.3, align=True)
            r.label(text="Input Source")
            r = r.row()
            r.prop(self, "right_click_source", expand=True)

            r = wrapper.split(factor=0.3, align=True)
            r.label(text="Click Action")
            c = r.column()
            c.prop(self, "right_click_mode", expand=True)
            main.separator()
            wrapper = main.box()
            wrapper.label(text="Double Click Actions")
            wrapper.prop(self, "enable_double_click", toggle=1)
            r = wrapper.split(factor=0.3, align=True)
            r.label(text="Click Action")
            c = r.column()
            c.prop(self, "double_click_mode", expand=True)

            main.separator()
            main.label(text="Tool Settings")
            main.prop(self, "subdivision_limit", slider=True)

        if self.gizmo_tabs == "ACTIONS":
            if not self.show_float_menu:
                main.operator("view3d.toggle_floating_menu", text="Show Action Menu")
            else:
                main.operator(
                    "view3d.toggle_floating_menu", text="Hide Action Menu", depress=True
                )
                box = main.box()
                box.active = self.show_float_menu
                main = box.column()
                main.prop(self, "active_menu")
                mList = self.getMenuSettings(self.active_menu)
                for i in range(7):
                    main.prop(mList, "menu_slot_" + str(i + 1))

    ##
    # Data Accessors
    ##
    def getMenuSettings(self, mode: str):
        m = None
        for opts in self.menu_sets:
            if opts.mode == mode:
                m = opts
        if m is None:
            m = self.menu_sets.add()
            m.mode = mode
            ops = menu_defaults[mode]
            for i, o in enumerate(ops):
                setattr(m, "menu_slot_" + str(i + 1), o)
        return m

    def getGizmoSet(self, mode: str | int):
        available = list(gizmo_sets["ALL"])

        if mode not in list(gizmo_sets):
            return available
        return available + list(gizmo_sets[mode])

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100
