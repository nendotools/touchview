# type: ignore
import bpy
from bpy.types import Panel, Menu, UILayout

from ..utils.blender import preferences


class TouchView:
    bl_label = "Touchview Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Touchview"


class TOUCHVIEW_PT_view_3d_panel(TouchView, Panel):
    # bl_label = "Touchview Settings"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False

        box = layout.box()
        box.label(
            text=UILayout.enum_item_description(prefs, "input_mode", prefs.input_mode),
            icon_value=UILayout.enum_item_icon(prefs, "input_mode", prefs.input_mode),
        )

        row = box.row()
        row.prop(prefs, "input_mode", expand=True)

        col = box.column(align=True)
        col.use_property_split = True
        col.prop(prefs, "lazy_mode")
        if prefs.input_mode == "FULL":
            col.prop(prefs, "enable_floating_toggle")


class TOUCHVIEW_PT_ControlZones(TouchView, Panel):
    bl_label = "Control Zones"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw_header(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False

        layout.prop(prefs, "is_enabled", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False

        prefs = preferences()

        layout.active = prefs.is_enabled

        row = layout.row()
        row.prop(prefs, "header_toggle_position", expand=True)

        layout.use_property_split = True

        col = layout.column(align=True)
        col.prop(prefs, "isVisible", text="Show Overlay")
        col.prop(prefs, "swap_panrotate")
        col.prop(prefs, "use_multiple_colors")

        col = layout.column()
        col.prop(prefs, "overlay_main_color", text="Main Color")
        if prefs.use_multiple_colors:
            col.prop(prefs, "overlay_secondary_color", text="Secondary Color")
        col.prop(prefs, "width", slider=True)
        col.prop(prefs, "radius", slider=True)


class TOUCHVIEW_PT_gizmo_bar(TouchView, Panel):
    bl_label = "Gizmo"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        col = layout.column()
        col.prop(prefs, "menu_style", expand=True)

        if prefs.menu_style == "fixed.bar":
            col.prop(prefs, "gizmo_position")
        elif prefs.menu_style == "float.radial":
            col.prop(prefs, "menu_spacing", slider=True)

        col.prop(prefs, "gizmo_scale", slider=True)
        col.prop(prefs, "gizmo_padding", slider=True)


class TOUCHVIEW_PT_right_click(TouchView, Panel):
    bl_label = "Right Click Actions"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        col = layout.column()
        col.prop(prefs, "right_click_source", text="Source", expand=True)
        col.prop(prefs, "right_click_mode", text="Mode", expand=True)


class TOUCHVIEW_PT_double_click(TouchView, Panel):
    bl_label = "Double Click Actions"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        col = layout.column()
        col.prop(prefs, "enable_double_click")
        col.prop(prefs, "double_click_mode", text="Mode", expand=True)


class TOUCHVIEW_PT_tool_settings(TouchView, Panel):
    bl_label = "Tool Options"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        layout.prop(prefs, "subdivision_limit", slider=True)


class TOUCHVIEW_PT_viewport_options(TouchView, Panel):
    bl_label = "Viewport Options"
    bl_parent_id = "TOUCHVIEW_PT_view_3d_panel"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        view = context.space_data
        space = context.area.spaces.active

        col = layout.column()
        col.operator("view3d.tools_region_flip", text="Flip Tools")
        if len(space.region_quadviews) > 0:
            col.operator("screen.region_quadview", text="Disable Quadview")
        else:
            col.operator("screen.region_quadview", text="Enable Quadview")

        col = layout.column(align=True)
        col.prop(prefs, "show_float_menu")
        if not len(space.region_quadviews) > 0:
            col.prop(space, "lock_cursor", text="Lock to Cursor")
            col.prop(view.region_3d, "lock_rotation", text="Lock Rotation")


class TOUCHVIEW_PT_image_editor_panel(TouchView, Panel):
    bl_space_type = "IMAGE_EDITOR"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False

        box = layout.box()
        box.label(
            text=UILayout.enum_item_description(prefs, "input_mode", prefs.input_mode),
            icon_value=UILayout.enum_item_icon(prefs, "input_mode", prefs.input_mode),
        )

        row = box.row()
        row.prop(prefs, "input_mode", expand=True)

        col = box.column(align=True)
        col.use_property_split = True
        col.prop(prefs, "is_enabled")
        subcol = col.column(align=True)
        subcol.active = prefs.is_enabled
        subcol.prop(prefs, "header_toggle_position", expand=True)


class TOUCHVIEW_PT_node_editor_panel(TouchView, Panel):
    bl_space_type = "NODE_EDITOR"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        layout.use_property_decorate = False

        box = layout.box()
        box.label(
            text=UILayout.enum_item_description(prefs, "input_mode", prefs.input_mode),
            icon_value=UILayout.enum_item_icon(prefs, "input_mode", prefs.input_mode),
        )

        row = box.row()
        row.prop(prefs, "input_mode", expand=True)

        col = box.column(align=True)
        col.use_property_split = True
        col.prop(prefs, "is_enabled")
        subcol = col.column(align=True)
        subcol.active = prefs.is_enabled
        subcol.prop(prefs, "header_toggle_position", expand=True)


# UI panel to append Gizmo menu
class TOUCHVIEW_PT_gizmo_display(Panel):
    bl_label = "Touchview Gizmos"
    bl_parent_id = "VIEW3D_PT_gizmo_display"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"

    def draw(self, context):
        prefs = preferences()

        layout = self.layout
        col = layout.column()
        available_gizmos = prefs.getGizmoSet(context.object.mode)

        col = col.column(align=True)
        col.active = context.space_data.show_gizmo
        col.prop(prefs, "show_menu")
        col = col.column()
        col.active = prefs.show_menu
        for toggle in available_gizmos:
            col.prop(prefs, "show_" + toggle)


class TOUCHVIEW_MT_floating(Menu):
    """Open a custom menu"""

    bl_label = "Floating Menu"
    bl_description = "Customized Floating Menu"

    def draw(self, context):
        prefs = preferences()
        menu = prefs.getMenuSettings(context.mode)

        layout = self.layout
        pie = layout.menu_pie()
        for i in range(8):
            op = getattr(menu, "menu_slot_" + str(i + 1))
            if op == "":
                continue
            elif "_MT_" in op:
                pie.menu(op)
                continue
            elif self.__operator_exists(op):
                pie.operator(op)

    def __operator_exists(self, idname):
        try:
            names = idname.split(".")
            a = bpy.ops
            for prop in names:
                a = getattr(a, prop)
            a.__repr__()
        except Exception as _:
            return False
        return True


classes = (
    TOUCHVIEW_PT_view_3d_panel,
    TOUCHVIEW_PT_ControlZones,
    TOUCHVIEW_PT_gizmo_bar,
    TOUCHVIEW_PT_right_click,
    TOUCHVIEW_PT_double_click,
    TOUCHVIEW_PT_tool_settings,
    TOUCHVIEW_PT_viewport_options,
    TOUCHVIEW_PT_image_editor_panel,
    TOUCHVIEW_PT_node_editor_panel,
    TOUCHVIEW_PT_gizmo_display,
    TOUCHVIEW_MT_floating,
)


register, unregister = bpy.utils.register_classes_factory(classes)
