import math

import bpy
from bpy.types import Operator

from ..utils.blender import preferences
from ..utils.constants import (CANCEL, FINISHED, paint_settings_name,
                               pivot_items)


class TOUCHVIEW_OT_flip_tools(Operator):
    """Relocate Tools panel between left and right"""

    bl_label = "Tools Region Swap"
    bl_idname = "touchview.tools_region_flip"

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
    bl_idname = "touchview.step_pivot_mode"

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
    """Toggle the sidebar (N panel)"""

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
    bl_idname = "touchview.toggle_floating_menu"

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
    """Toggle viewport rotation lock"""

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


class BrushRadialControl:
    """Shared radial control for brush properties, mirroring Blender's own keymap"""

    prop = ""

    def invoke(self, context, event):
        prefs = preferences()
        # move the cursor away from the bar so the radial control has room
        if prefs.menu_style in {"fixed.bar"}:
            if prefs.gizmo_position in ["LEFT", "RIGHT"]:
                context.window.cursor_warp(
                    context.region.x + math.floor(context.region.width / 2),
                    context.region.y + event.mouse_region_y,
                )
            else:
                context.window.cursor_warp(
                    context.region.x + event.mouse_region_x,
                    context.region.y + math.floor(context.region.height / 2),
                )
        return self.execute(context)

    def execute(self, context):
        paint = paint_settings_name(context.mode)
        if paint is None:
            return CANCEL
        brush_path = f"tool_settings.{paint}.brush"
        # grease pencil draw mode ignores unified settings, same as Blender's keymap
        if paint == "gpencil_paint":
            bpy.ops.wm.radial_control(
                "INVOKE_DEFAULT",  # type: ignore
                data_path_primary=f"{brush_path}.{self.prop}",
            )
            return FINISHED

        unified_path = f"tool_settings.{paint}.unified_paint_settings"
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",  # type: ignore
            data_path_primary=f"{brush_path}.{self.prop}",
            data_path_secondary=f"{unified_path}.{self.prop}",
            use_secondary=f"{unified_path}.use_unified_{self.prop}",
            rotation_path=f"{brush_path}.texture_slot.angle",
            color_path=f"{brush_path}.cursor_color_add",
            image_id=brush_path,
        )
        return FINISHED


class TOUCHVIEW_OT_brush_resize(BrushRadialControl, Operator):
    """Adjust the brush size"""

    bl_label = "Brush Size Adjust"
    bl_idname = "touchview.brush_resize"

    prop = "size"


class TOUCHVIEW_OT_brush_strength(BrushRadialControl, Operator):
    """Adjust the brush strength"""

    bl_label = "Brush Strength Adjust"
    bl_idname = "touchview.brush_strength"

    prop = "strength"


class TOUCHVIEW_OT_increase_multires(Operator):
    """Increase the Multires level, subdividing when at the highest level"""

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
    """Decrease the Multires level, unsubdividing when at the lowest level"""

    bl_label = "decrement Multires modifier by 1"
    bl_idname = "touchview.decrement_multires"

    def execute(self, context):
        if not context.active_object or not len(context.active_object.modifiers):
            return CANCEL
        for mod in context.active_object.modifiers:
            if not isinstance(mod, bpy.types.MultiresModifier):
                continue
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
    """Increase voxel density and remesh"""

    bl_label = "Increase voxel density and remesh"
    bl_idname = "touchview.density_up"

    def execute(self, context):
        if not context.active_object or context.active_object.type != "MESH":
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, bpy.types.MultiresModifier):
                return CANCEL
        mesh = context.active_object.data
        mesh.remesh_voxel_size *= 0.8
        bpy.ops.object.voxel_remesh()
        return FINISHED


class TOUCHVIEW_OT_density_down(Operator):
    """Decrease voxel density and remesh"""

    bl_label = "Decrease voxel density and remesh"
    bl_idname = "touchview.density_down"

    def execute(self, context):
        if not context.active_object or context.active_object.type != "MESH":
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, bpy.types.MultiresModifier):
                return CANCEL
        mesh = context.active_object.data
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
