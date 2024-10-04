import bpy
from bpy.types import Operator

import math

from ..utils.blender import preferences
from ..utils.constants import CANCEL, FINISHED, pivot_items


class TOUCHVIEW_OT_flip_tools(Operator):
    """Relocate Tools panel between left and right"""

    bl_label = "Tools Region Swap"
    bl_idname = "view3d.tools_region_flip"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D" and context.region.type == "WINDOW"

    def execute(self, context):
        override = context.copy()
        override["area"] = context.area
        override["region"] = context.region
        for r in context.area.regions:
            if r.type == "TOOLS":
                override["region"] = r
        with context.temp_override(region=override["region"]):  # type: ignore
            bpy.ops.screen.region_flip()
        return FINISHED


class TOUCHVIEW_OT_next_pivot_mode(Operator):
    """Step through Pivot modes"""

    bl_label = "Use next Pivot mode"
    bl_idname = "view3d.step_pivot_mode"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D" and context.region.type == "WINDOW"

    def execute(self, context):
        prefs = preferences()
        count = 0
        for enum, _, _ in pivot_items:
            if enum == prefs.pivot_mode:
                count += 1
                if count == len(pivot_items):
                    count = 0
                pivot = pivot_items[count][0]
                bpy.ops.sculpt.set_pivot_position(mode=pivot)
                prefs.pivot_mode = pivot
                context.area.tag_redraw()
                return FINISHED
            count += 1
        return FINISHED


class TOUCHVIEW_OT_toggle_touch_controls(Operator):
    """Toggle Touch Controls"""

    bl_label = "Toggle Touch Controls"
    bl_idname = "touchview.toggle_touch"

    def execute(self, context):
        prefs = preferences()
        prefs.is_enabled = not prefs.is_enabled
        context.area.tag_redraw()
        return FINISHED


class TOUCHVIEW_OT_toggle_npanel(Operator):
    """Toggle Settings Panel"""

    bl_label = "Display prefs Panel"
    bl_idname = "touchview.toggle_n_panel"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D" and context.region.type == "WINDOW"

    def execute(self, context):
        if not isinstance(context.space_data, bpy.types.SpaceView3D):
            return CANCEL
        context.space_data.show_region_ui ^= True
        return FINISHED


class TOUCHVIEW_OT_toggle_floating_menu(Operator):
    """Toggle Floating Menu"""

    bl_label = "Toggle Floating Menu"
    bl_idname = "view3d.toggle_floating_menu"

    def execute(self, context):
        prefs = preferences()
        prefs.show_float_menu = not prefs.show_float_menu
        return FINISHED


class TOUCHVIEW_OT_viewport_recenter(Operator):
    """Recenter Viewport and Cursor on Selected Object"""

    bl_label = "Recenter Viewport and Cursor on Selected"
    bl_idname = "touchview.viewport_recenter"

    def execute(self, context):
        current = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = "ACTIVE_ELEMENT"
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.view_center_cursor()
        bpy.ops.view3d.view_selected()
        context.scene.tool_settings.transform_pivot_point = current
        return FINISHED


class TOUCHVIEW_OT_viewport_lock(Operator):
    """Toggle Viewport Rotation"""

    bl_label = "Viewport rotation lock toggle"
    bl_idname = "touchview.viewport_lock"

    region_ids = []

    def execute(self, context):
        if not isinstance(context.area.spaces.active, bpy.types.SpaceView3D):
            return CANCEL
        if len(context.area.spaces.active.region_quadviews) == 0:
            context.region_data.lock_rotation ^= True
            return FINISHED

        for region in context.area.spaces.active.region_quadviews:
            self.region_ids.append((region.as_pointer(), region.lock_rotation))

        start_change = False
        regions = dict(self.region_ids)
        for i in range(3, -1, -1):
            region_data = context.area.spaces.active.region_quadviews[i]
            if context.region_data.as_pointer() == region_data.as_pointer():
                start_change = True
                context.region_data.lock_rotation ^= True
                continue

            if start_change:
                region_data.lock_rotation = regions[region_data.as_pointer()]
        self.region_ids = []
        return FINISHED


class TOUCHVIEW_OT_brush_resize(Operator):
    """Brush Resize"""

    bl_label = "Brush Size Adjust"
    bl_idname = "touchview.brush_resize"

    def invoke(self, context, event):
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y
        self.execute(context)
        return FINISHED

    # activate radial_control to change sculpt brush size
    def execute(self, context):
        prefs = preferences()
        if prefs.menu_style in {"fixed.bar"}:
            if prefs.gizmo_position in ["LEFT", "RIGHT"]:
                context.window.cursor_warp(math.floor(context.region.width / 2), self.mouse_y)
            else:
                context.window.cursor_warp(self.mouse_x, math.floor(context.region.height / 2))
        if context.mode in [
            "PAINT_GPENCIL",
            "EDIT_GPENCIL",
            "SCULPT_GPENCIL",
            "WEIGHT_GPENCIL",
            "VERTEX_GPENCIL",
        ]:
            return self.resize2d(context)
        return self.resize3d(context)

    def resize2d(self, context):
        data_path = "tool_settings.gpencil_paint.brush.size"
        if context.mode == "SCULPT_GPENCIL":
            data_path = "tool_settings.gpencil_sculpt_paint.brush.size"
        if context.mode == "WEIGHT_GPENCIL":
            data_path = "tool_settings.gpencil_weight_paint.brush.size"
        if context.mode == "VERTEX_GPENCIL":
            data_path = "tool_settings.gpencil_vertex_paint.brush.size"
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",  # type: ignore
            data_path_primary=data_path,
        )
        return FINISHED

    def resize3d(self, context):
        data_path = "tool_settings.sculpt.brush.size"
        if context.mode == "PAINT_VERTEX":
            data_path = "tool_settings.vertex_paint.brush.size"
        if context.mode == "PAINT_WEIGHT":
            data_path = "tool_settings.weight_paint.brush.size"
        if context.mode == "PAINT_IMAGE":
            data_path = "tool_settings.image_paint.brush.size"
        if context.mode == "PAINT_TEXTURE":
            data_path = "tool_settings.image_paint.brush.size"
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",  # type: ignore
            data_path_primary=data_path,
            data_path_secondary="tool_settings.unified_paint_settings.size",
            use_secondary=("tool_settings.unified_paint_settings.use_unified_size"),
            rotation_path="tool_settings.sculpt.brush.texture_slot.angle",
            color_path="tool_settings.sculpt.brush.cursor_color_add",
            image_id="tool_settings.sculpt.brush",
        )
        return FINISHED


class TOUCHVIEW_OT_brush_strength(Operator):
    """Brush Strength"""

    bl_label = "Brush Strength Adjust"
    bl_idname = "touchview.brush_strength"

    def invoke(self, context, event):
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y
        self.execute(context)
        return FINISHED

    # activate radial_control to change sculpt brush size
    def execute(self, context):
        prefs = preferences()
        if prefs.menu_style in {"fixed.bar"}:
            if prefs.gizmo_position in ["LEFT", "RIGHT"]:
                context.window.cursor_warp(math.floor(context.region.width / 2), self.mouse_y)
            else:
                context.window.cursor_warp(self.mouse_x, math.floor(context.region.height / 2))
        if context.mode in [
            "PAINT_GPENCIL",
            "EDIT_GPENCIL",
            "SCULPT_GPENCIL",
            "WEIGHT_GPENCIL",
            "VERTEX_GPENCIL",
        ]:
            return self.resize2d(context)
        return self.resize3d(context)

    def resize2d(self, context):
        data_path = "tool_settings.gpencil_paint.brush.gpencil_settings.pen_strength"
        if context.mode == "SCULPT_GPENCIL":
            data_path = "tool_settings.gpencil_sculpt_paint.brush.strength"
        if context.mode == "WEIGHT_GPENCIL":
            data_path = "tool_settings.gpencil_weight_paint.brush.strength"
        if context.mode == "VERTEX_GPENCIL":
            data_path = "tool_settings.gpencil_vertex_paint.brush.gpencil_settings.pen_strength"
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",  # type: ignore
            data_path_primary=data_path,
        )
        return FINISHED

    def resize3d(self, context):
        data_path = "tool_settings.sculpt.brush.strength"
        if context.mode == "PAINT_VERTEX":
            data_path = "tool_settings.vertex_paint.brush.strength"
        if context.mode == "PAINT_WEIGHT":
            data_path = "tool_settings.weight_paint.brush.strength"
        if context.mode == "PAINT_IMAGE":
            data_path = "tool_settings.image_paint.brush.strength"
        if context.mode == "PAINT_TEXTURE":
            data_path = "tool_settings.image_paint.brush.strength"
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",  # type: ignore
            data_path_primary=data_path,
            data_path_secondary=("tool_settings.unified_paint_settings.strength"),
            use_secondary=("tool_settings.unified_paint_settings.use_unified_strength"),
            rotation_path="tool_settings.sculpt.brush.texture_slot.angle",
            color_path="tool_settings.sculpt.brush.cursor_color_add",
            image_id="tool_settings.sculpt.brush",
        )
        return FINISHED


class TOUCHVIEW_OT_increase_multires(Operator):
    """Increment Multires by 1 or add subdivision"""

    bl_label = "Increment Multires modifier by 1 or add subdivision level"
    bl_idname = "touchview.increment_multires"

    def execute(self, context):
        prefs = preferences()
        if not context.active_object or not len(context.active_object.modifiers):
            return CANCEL
        for mod in context.active_object.modifiers:
            # if mod is type of bpy.types.MultiresModifier
            if isinstance(mod, bpy.types.MultiresModifier):
                if context.mode == "SCULPT":
                    if mod.sculpt_levels == mod.total_levels:
                        if mod.sculpt_levels < prefs.subdivision_limit:
                            bpy.ops.object.multires_subdivide(modifier=mod.name)
                    else:
                        mod.sculpt_levels += 1
                else:
                    if mod.levels == mod.total_levels:
                        if mod.levels < prefs.subdivision_limit:
                            bpy.ops.object.multires_subdivide(modifier=mod.name)
                    else:
                        mod.levels += 1
                return FINISHED
        return CANCEL


class TOUCHVIEW_OT_decrease_multires(Operator):
    """Decrement Multires by 1"""

    bl_label = "decrement Multires modifier by 1"
    bl_idname = "touchview.decrement_multires"

    def execute(self, context):
        if not context.active_object or not len(context.active_object.modifiers):
            return CANCEL
        for mod in context.active_object.modifiers:
            if not isinstance(mod, bpy.types.MultiresModifier):
                return FINISHED
            if context.mode == "SCULPT":
                if mod.sculpt_levels == 0:
                    bpy.ops.object.multires_unsubdivide(modifier=mod.name)
                else:
                    mod.sculpt_levels -= 1
            else:
                if mod.levels == 0:
                    bpy.ops.object.multires_unsubdivide(modifier=mod.name)
                else:
                    mod.levels -= 1
            return FINISHED
        return CANCEL


class TOUCHVIEW_OT_density_up(Operator):
    """Increase voxel density"""

    bl_label = "Increase voxel density and remesh"
    bl_idname = "touchview.density_up"

    def execute(self, context):
        if not context.active_object:
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, bpy.types.MultiresModifier):
                return CANCEL
        mesh = bpy.data.meshes[context.active_object.name]
        mesh.remesh_voxel_size *= 0.8
        bpy.ops.object.voxel_remesh()
        return FINISHED


class TOUCHVIEW_OT_density_down(Operator):
    """Decrease voxel density"""

    bl_label = "Decrease voxel density and remesh"
    bl_idname = "touchview.density_down"

    def execute(self, context):
        if not context.active_object:
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, bpy.types.MultiresModifier):
                return CANCEL
        mesh = bpy.data.meshes[context.active_object.name]
        mesh.remesh_voxel_size /= 0.8
        bpy.ops.object.voxel_remesh()
        return FINISHED


classes = (
    TOUCHVIEW_OT_brush_resize,
    TOUCHVIEW_OT_brush_strength,
    TOUCHVIEW_OT_decrease_multires,
    TOUCHVIEW_OT_density_down,
    TOUCHVIEW_OT_density_up,
    TOUCHVIEW_OT_flip_tools,
    TOUCHVIEW_OT_increase_multires,
    TOUCHVIEW_OT_next_pivot_mode,
    TOUCHVIEW_OT_toggle_floating_menu,
    TOUCHVIEW_OT_toggle_npanel,
    TOUCHVIEW_OT_toggle_touch_controls,
    TOUCHVIEW_OT_viewport_lock,
    TOUCHVIEW_OT_viewport_recenter,
)


register, unregister = bpy.utils.register_classes_factory(classes)
