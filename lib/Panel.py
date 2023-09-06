# type: ignore
# NOTE: generally, we don't want to ignore all type-enforcement in a file,
# but the current implementation of the AnyType[T] used as input for prop()
# doesn't get enforced as the native: any[T]
import bpy
from bpy.types import Context, Menu, Panel, VIEW3D_PT_gizmo_display

from .utils import get_settings


class VIEW3D_PT_NendoPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NENDO"


class VIEW3D_PT_NendoViewport(VIEW3D_PT_NendoPanel, Panel):
    bl_idname = "VIEW3D_PT_NendoViewport"
    bl_label = "Touchview Settings"

    def draw(self, _: Context):
        pass


class VIEW3D_PT_ControlZones(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Control Zones"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, _: Context):
        settings = get_settings()

        col = self.layout.column()
        col.label(text="Input Mode")
        box = col.box()
        if settings.input_mode == 'full':
            box.label(
                text="pen, mouse, and touch input",
                icon="CON_CAMERASOLVER"
            )
        if settings.input_mode == 'pen':
            box.label(text="pen-only input", icon="STYLUS_PRESSURE")
        if settings.input_mode == 'touch':
            box.label(text="mouse/touch only input", icon="VIEW_PAN")
        r = box.row()
        r.prop(settings, "input_mode", expand=True)
        box.prop(settings, 'lazy_mode', toggle=1)
        box.prop(settings, "is_enabled", toggle=1)

        col.prop(settings, "swap_panrotate")
        col.prop(settings, "isVisible", text="Show Overlay")
        col.prop(settings, "use_multiple_colors")
        col.prop(settings, "overlay_main_color", text="Main Color")
        if settings.use_multiple_colors:
            col.prop(settings,
                     "overlay_secondary_color",
                     text="Secondary Color")
        col.prop(settings, "width")
        col.prop(settings, "radius")
        col.separator()


class VIEW3D_PT_RightClick_Menu(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Right Click Actions"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, _: Context):
        settings = get_settings()
        group = self.layout.column()
        r = group.split(factor=0.3, align=True)
        r.label(text="Input Source")
        r = r.row()
        r.prop(settings, "right_click_source", expand=True)

        r = group.split(factor=0.3, align=True)
        r.label(text="Click Action")
        c = r.column()
        c.prop(settings, "right_click_mode", expand=True)


class VIEW3D_PT_DoubleClick_Menu(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Double Click Actions"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, _: Context):
        settings = get_settings()
        group = self.layout.column()
        r = group.split(factor=0.3, align=True)
        group.separator()
        group.prop(settings, "enable_double_click", toggle=1)
        r = group.split(factor=0.3, align=True)
        r.label(text="Click Action")
        c = r.column()
        c.prop(settings, "double_click_mode", expand=True)


class VIEW3D_PT_GizmoBar(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Gizmo Bar"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, _: Context):
        settings = get_settings()
        group = self.layout.column()
        group.label(text="Menu Style")
        r = group.row()
        r.prop(settings, "menu_style", expand=True)
        if settings.menu_style == 'fixed.bar':
            group.prop_menu_enum(settings, "gizmo_position")
        group.prop(settings, "menu_spacing", slider=True)
        if settings.menu_style == 'float.radial':
            group.prop(settings, "gizmo_padding", slider=True)
        group.prop(settings, "gizmo_scale", slider=True)


class VIEW3D_PT_ToolSettings(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Tool Options"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, _: Context):
        settings = get_settings()
        group = self.layout.column()
        group.prop(settings, "subdivision_limit", slider=True)


class VIEW3D_PT_ViewportOptions(VIEW3D_PT_NendoPanel, Panel):
    bl_label = "Viewport Options"
    bl_parent_id = "VIEW3D_PT_NendoViewport"

    def draw(self, context: Context):
        settings = get_settings()
        view = context.space_data
        space = context.area.spaces.active
        group = self.layout.column()
        group.prop(settings, "show_float_menu", toggle=1)
        group.operator("view3d.tools_region_flip", text="Flip Tools")
        if len(space.region_quadviews) > 0:
            group.operator("screen.region_quadview", text="Disable Quadview")
        else:
            group.operator("screen.region_quadview", text="Enable Quadview")
            group.prop(space, "lock_cursor", text="Lock to Cursor")
            group.prop(view.region_3d, "lock_rotation", text="Lock Rotation")
        context.area.tag_redraw()


class PIE_MT_Floating_Menu(Menu):
    """ Open a custom menu """
    bl_idname = "PIE_MT_Floating_Menu"
    bl_label = "Floating Menu"
    bl_description = "Customized Floating Menu"

    def draw(self, context: Context):
        settings = get_settings()
        menu = settings.getMenuSettings(context.mode)

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
        except:
            return False
        return True


# UI panel to append Gizmo menu
class VIEW3D_PT_Gizmo_Panel(bpy.types.Panel):
    bl_label = "Gizmo display control"
    bl_idname = "VIEW3D_PT_Gizmo_Panel"
    bl_parent_id = "VIEW3D_PT_gizmo_display"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Gizmos"
    bl_ui_units_x = 16

    def draw(self, context: Context):
        layout = self.layout

        col = layout.column()
        col.label(text="Touch Gizmos")
        settings = get_settings()
        available_gizmos = settings.getGizmoSet(context.object.mode)

        col = col.column(align=True)
        col.active = context.space_data.show_gizmo
        col.prop(settings, "show_menu")
        col = col.column()
        col.active = settings.show_menu
        for toggle in available_gizmos:
            col.prop(settings, 'show_' + toggle)


__classes__ = (PIE_MT_Floating_Menu, VIEW3D_PT_NendoViewport,
               VIEW3D_PT_ControlZones, VIEW3D_PT_ViewportOptions,
               VIEW3D_PT_RightClick_Menu, VIEW3D_PT_DoubleClick_Menu,
               VIEW3D_PT_GizmoBar, VIEW3D_PT_ToolSettings,
               VIEW3D_PT_Gizmo_Panel)


def register():
    from bpy.utils import register_class
    for cls in __classes__:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(__classes__):
        unregister_class(cls)
