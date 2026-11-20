import json
from os import path

import bpy
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)
from bpy.types import AddonPreferences, PropertyGroup, UILayout

from .addon import addon_path, package
from .constants import (
    double_click_items,
    edit_modes,
    gizmo_sets,
    menu_defaults,
    menu_orientation_items,
    menu_style_items,
    pivot_items,
    position_items,
)
from .log import log

_NON_SERIALIZED = frozenset({"rna_type", "bl_idname"})


def _serialized_properties(prefs):
    for prop in prefs.bl_rna.properties:
        if prop.identifier in _NON_SERIALIZED:
            continue
        if prop.type == "COLLECTION" or not prop.is_readonly:
            yield prop


def _serialize(prefs):
    data = {}
    for prop in _serialized_properties(prefs):
        name = prop.identifier
        value = getattr(prefs, name)
        if prop.type == "COLLECTION":
            data[name] = [item.to_dict() for item in value]
        elif getattr(prop, "array_length", 0) > 1:
            data[name] = list(value)
        else:
            data[name] = value
    return data


def _deserialize(prefs, data: dict):
    for prop in _serialized_properties(prefs):
        name = prop.identifier
        if prop.type == "COLLECTION":
            collection = getattr(prefs, name)
            while collection:
                collection.remove(0)
            for item in data.get(name, ()):
                collection.add().from_dict(item)
            continue
        default = list(prop.default_array) if getattr(prop, "array_length", 0) > 1 else prop.default
        setattr(prefs, name, data.get(name, default))


def _config_path() -> str:
    return path.join(addon_path(), "preferences.json")


def draw_header_toggle(header, context):
    prefs = context.preferences.addons[package].preferences
    layout = header.layout
    layout.separator()
    layout.prop(prefs, "is_enabled", toggle=True)


def update_header_toggle_position(context):
    prefs = context.preferences.addons[package].preferences
    for header in (bpy.types.NODE_HT_header, bpy.types.IMAGE_HT_header):
        header.remove(draw_header_toggle)
        if prefs.header_toggle_position == "LEFT":
            header.prepend(draw_header_toggle)
        else:
            header.append(draw_header_toggle)


# preference changes made outside the viewport don't redraw gizmos on their own
def redraw_viewports(_, context):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()


class TOUCHVIEW_PG_menu_mode(PropertyGroup):
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
        return _serialize(self)

    def from_dict(self, data: dict):
        _deserialize(self, data)


class TOUCHVIEW_AP_preferences(AddonPreferences):
    bl_idname = package

    is_enabled: BoolProperty(
        name="Enable Controls",
        default=True,
    )

    header_toggle_position: EnumProperty(
        items=[
            ("LEFT", "Left", "Toggle position on the left"),
            ("RIGHT", "Right", "Toggle position on the right"),
        ],
        name="Header Toggle Position",
        default="RIGHT",
        update=lambda _, context: update_header_toggle_position(context),
    )

    lazy_mode: BoolProperty(
        name="Lazy Mode",
        default=False,
        description="always control camera when not touching selected object",
    )

    toggle_position: FloatVectorProperty(
        name="Toggle Position",
        soft_min=0,
        soft_max=100,
        size=2,
        default=(0, 0),
    )

    toggle_color: FloatVectorProperty(
        name="Toggle Button Color",
        default=(0.1, 0.1, 0.2, 0.5),
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
    )

    show_overlay: BoolProperty(
        name="Show Overlay",
        default=False,
    )

    input_mode: EnumProperty(
        name="Input Mode",
        items=[
            ("FULL", "Full", "Mouse/Touch and Pen input", "CON_CAMERASOLVER", 0),
            ("PEN", "Pen", "Pen input only", "STYLUS_PRESSURE", 1),
            ("TOUCH", "Touch", "Mouse/Touch input only", "VIEW_PAN", 2),
        ],
        default="FULL",
        update=redraw_viewports,
    )

    enable_floating_toggle: BoolProperty(
        name="Floating Toggle",
        description=(
            "Show a floating button in the viewport (bottom-left by default, drag to move) "
            "that turns touch controls on/off. Always shown in Pen and Touch input modes"
        ),
        default=False,
        update=redraw_viewports,
    )

    enable_double_click: BoolProperty(
        name="Double Click",
        default=True,
    )

    enable_right_click: BoolProperty(
        name="Enable Right Click",
        default=True,
    )

    right_click_mode: EnumProperty(
        name="Right Click Mode",
        items=double_click_items,
        default="wm.window_fullscreen_toggle",
    )

    right_click_source: EnumProperty(
        name="Right Click Source",
        items=[
            ("MOUSE", "Mouse", "Mouse/Touch right click"),
            ("PEN", "Pen", "Pen right click"),
            ("NONE", "None", "Disabled"),
        ],
        default="MOUSE",
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

    use_multiple_colors: BoolProperty(
        name="Multicolor Overlay",
        default=False,
    )

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

    show_menu: BoolProperty(
        name="Toggle Menu Display",
        default=True,
    )

    show_gizmos: BoolProperty(
        name="Toggle Gizmos on Menu",
        default=True,
    )

    menu_style: EnumProperty(
        name="Menu Style",
        items=menu_style_items,
        default="float.radial",
        update=redraw_viewports,
    )

    gizmo_position: EnumProperty(
        name="Gizmo Position",
        items=position_items,
        default="RIGHT",
        update=redraw_viewports,
    )

    menu_orientation: EnumProperty(
        name="Menu Orientation",
        items=menu_orientation_items,
        default="HORIZONTAL",
    )

    menu_spacing: FloatProperty(
        name="Menu Scale",
        min=1,
        max=2,
        default=1,
    )

    gizmo_scale: FloatProperty(
        name="Gizmo Scale",
        min=1,
        max=2,
        default=1,
    )

    gizmo_padding: FloatProperty(
        name="Gizmo Padding",
        subtype="PIXEL",
        min=0,
        soft_max=24,
        default=4,
    )

    menu_position: FloatVectorProperty(
        name="Menu Position",
        soft_min=0,
        soft_max=100,
        size=2,
        default=(100, 0),
    )

    show_undoredo: BoolProperty(
        name="Undo/Redo",
        default=True,
    )

    show_is_enabled: BoolProperty(
        name="Toggle Touch",
        default=True,
    )

    show_control_gizmo: BoolProperty(
        name="Toggle Control Gizmo",
        default=True,
    )

    show_show_fullscreen: BoolProperty(
        name="Fullscreen",
        default=True,
    )

    show_region_quadviews: BoolProperty(
        name="Quadview",
        default=True,
    )

    show_pivot_mode: BoolProperty(
        name="Pivot Mode",
        default=True,
    )

    show_snap_view: BoolProperty(
        name="Snap View",
        default=True,
    )

    show_n_panel: BoolProperty(
        name="N Panel",
        default=True,
    )

    show_lock_rotation: BoolProperty(
        name="Rotation Lock",
        default=True,
    )

    show_multires: BoolProperty(
        name="Multires",
        default=True,
    )

    show_voxel_remesh: BoolProperty(
        name="Voxel Remesh",
        default=True,
    )
    show_brush_dynamics: BoolProperty(
        name="Brush Dynamics",
        default=True,
    )

    subdivision_limit: IntProperty(
        name="Subdivision Limit",
        default=4,
        min=1,
        max=7,
    )

    pivot_mode: EnumProperty(
        name="Sculpt Pivot Mode",
        items=pivot_items,
        default="SURFACE",
    )

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

    show_float_menu: BoolProperty(
        name="Floating Menu",
        default=False,
    )

    floating_position: FloatVectorProperty(
        name="Floating Offset",
        soft_min=0,
        soft_max=100,
        size=2,
        default=(100, 0),
    )

    double_click_mode: EnumProperty(
        name="Double Click Mode",
        items=double_click_items,
        default="wm.window_fullscreen_toggle",
    )

    menu_sets: CollectionProperty(
        type=TOUCHVIEW_PG_menu_mode,
        options={"LIBRARY_EDITABLE"},
    )

    active_menu: EnumProperty(
        name="Mode Settings",
        items=edit_modes,
    )

    gizmo_tabs: EnumProperty(
        name="Gizmo Tabs",
        items=[
            ("GIZMO", "Gizmo", "", 0),
            ("ACTIONS", "Action", "", 1),
        ],
        default="GIZMO",
    )

    def to_dict(self):
        return _serialize(self)

    def from_dict(self, data: dict):
        _deserialize(self, data)
        if "show_overlay" not in data and "is_visible" in data:
            self.show_overlay = data["is_visible"]

    def load(self):
        filename = _config_path()
        if not path.exists(filename):
            return

        try:
            with open(filename, "r") as file:
                self.from_dict(json.load(file))
        except Exception as error:
            log(f"could not load preferences: {error}", "WARNING")
            return

    def save(self):
        filename = _config_path()
        try:
            with open(filename, "w") as file:
                json.dump(self.to_dict(), file)
        except (OSError, TypeError):
            # a failed write must not abort add-on teardown
            return

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False

        self._draw_input_mode(layout)
        self._draw_control_zones(layout)
        self._draw_gizmo_options(layout)

    def _draw_input_mode(self, layout):
        box = layout.box()
        box.label(text="Input Mode")
        box.use_property_split = True

        row = box.row()
        row.prop(
            self, "input_mode", text=UILayout.enum_item_description(self, "input_mode", self.input_mode), expand=True
        )
        col = box.column(align=True)
        col.prop(self, "lazy_mode")
        if self.input_mode == "FULL":
            col.prop(self, "enable_floating_toggle")

    def _draw_control_zones(self, layout):
        box = layout.box()
        box.prop(self, "is_enabled", text="Control Zones")

        col = box.column()
        col.use_property_split = True
        col.active = self.is_enabled

        row = col.row()
        row.prop(self, "header_toggle_position", expand=True)
        col = col.column(align=True)
        col.prop(self, "show_overlay", text="Show Overlay")
        col.prop(self, "swap_panrotate")
        col.prop(self, "use_multiple_colors")
        col = col.column()
        col.prop(self, "overlay_main_color", text="Main Color")
        if self.use_multiple_colors:
            col.prop(self, "overlay_secondary_color", text="Secondary Color")
        col.prop(self, "width", slider=True)
        col.prop(self, "radius", slider=True)

    def _draw_gizmo_options(self, layout):
        box = layout.box()
        col = box.row(align=True)
        col.prop(self, "gizmo_tabs", expand=True)
        box.use_property_split = True
        content = box.column()

        if self.gizmo_tabs == "GIZMO":
            self._draw_gizmo_settings(box, content)
        else:
            self._draw_action_settings(content)

    def _draw_gizmo_settings(self, box, col):
        row = col.row()
        row.prop(self, "menu_style", expand=True)

        if self.menu_style == "fixed.bar":
            col.prop(self, "gizmo_position")
        elif self.menu_style == "float.radial":
            col.prop(self, "menu_spacing", slider=True)

        col.prop(self, "gizmo_scale", slider=True)
        col.prop(self, "gizmo_padding", slider=True)

        column = box.column()
        right_click = column.box()
        right_click.label(text="Right Click Actions")
        col = right_click.column()
        row = col.row()
        row.prop(self, "right_click_source", text="Source", expand=True)
        col.prop(self, "right_click_mode", text="Mode", expand=True)

        double_click = box.box()
        double_click.label(text="Double Click Actions")
        col = double_click.column()
        col.prop(self, "enable_double_click")
        col.prop(self, "double_click_mode", text="Mode", expand=True)

        tools = box.column()
        tools.label(text="Tool Settings")
        tools.prop(self, "subdivision_limit", slider=True)

    def _draw_action_settings(self, col):
        if not self.show_float_menu:
            col.operator("touchview.toggle_floating_menu", text="Show Action Menu")
            return
        col.operator("touchview.toggle_floating_menu", text="Hide Action Menu", depress=True)
        box = col.box()
        box.active = self.show_float_menu
        col = box.column()
        col.prop(self, "active_menu")
        menu_settings = self.get_menu_settings(self.active_menu)
        for index in range(8):
            col.prop(menu_settings, f"menu_slot_{index + 1}")

    def get_menu_settings(self, mode: str):
        for menu in self.menu_sets:
            if menu.mode == mode:
                return menu
        menu = self.menu_sets.add()
        menu.mode = mode
        for index, operator in enumerate(menu_defaults.get(mode, ())):
            setattr(menu, f"menu_slot_{index + 1}", operator)
        return menu

    def get_gizmo_set(self, mode: str | int):
        available = list(gizmo_sets["ALL"])
        if mode in gizmo_sets:
            available.extend(gizmo_sets[mode])
        return available

    def get_width(self):
        return self.width / 100

    def get_radius(self):
        return self.radius / 100


classes = (
    TOUCHVIEW_PG_menu_mode,
    TOUCHVIEW_AP_preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon = bpy.context.preferences.addons[package]
    addon.preferences.load()
    update_header_toggle_position(bpy.context)


def unregister():
    addon = bpy.context.preferences.addons.get(package)
    if addon is not None:
        try:
            addon.preferences.save()
        except Exception:
            pass

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    for header in (bpy.types.NODE_HT_header, bpy.types.IMAGE_HT_header):
        try:
            header.remove(draw_header_toggle)
        except (ValueError, RuntimeError):
            pass
