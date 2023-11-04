import math

import bpy
from bpy.types import Context, Event, MultiresModifier, Operator, SpaceView3D

from ..constants import CANCEL, FINISHED, pivot_items
from ..utils import get_settings


class VIEW3D_OT_FlipTools(Operator):
    """ Relocate Tools panel between left and right """
    bl_idname = "view3d.tools_region_flip"
    bl_label = "Tools Region Swap"

    def execute(self, context: Context):
        override: Context = context.copy()  # type: ignore
        for r in context.area.regions:
            if r.type == 'TOOLS':
                override["region"] = r
        bpy.ops.screen.region_flip(override)
        return FINISHED

    @classmethod
    def poll(cls, context: Context):
        return (
            context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'
        )


class VIEW3D_OT_NextPivotMode(Operator):
    """ Step through Pivot modes """
    bl_idname = "view3d.step_pivot_mode"
    bl_label = "Use next Pivot mode"

    def execute(self, context: Context):
        settings = get_settings()
        count = 0
        for enum, _, _ in pivot_items:
            if enum == settings.pivot_mode:
                count += 1
                if count == len(pivot_items):
                    count = 0
                pivot = pivot_items[count][0]
                bpy.ops.sculpt.set_pivot_position(mode=pivot)
                settings.pivot_mode = pivot
                context.area.tag_redraw()
                return FINISHED
            count += 1
        return FINISHED

    @classmethod
    def poll(cls, context: Context):
        return (
            context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'
        )


class VIEW3D_OT_ToggleTouchControls(Operator):
    """ Toggle Touch Controls """
    bl_idname = "nendo.toggle_touch"
    bl_label = "Toggle Touch Controls"

    def execute(self, context: Context):
        settings = get_settings()
        settings.is_enabled = not settings.is_enabled
        context.area.tag_redraw()
        return FINISHED


class VIEW3D_OT_ToggleNPanel(Operator):
    """ Toggle Settings Panel """
    bl_idname = "nendo.toggle_n_panel"
    bl_label = "Display settings Panel"

    def execute(self, context: Context):
        if not isinstance(context.space_data, SpaceView3D):
            return CANCEL
        context.space_data.show_region_ui ^= True
        return FINISHED

    @classmethod
    def poll(cls, context: Context):
        return (
            context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'
        )


class VIEW3D_OT_ToggleFloatingMenu(Operator):
    """ Toggle Floating Menu """
    bl_idname = "view3d.toggle_floating_menu"
    bl_label = "Toggle Floating Menu"

    def execute(self, _: Context):
        settings = get_settings()
        settings.show_float_menu = not settings.show_float_menu
        return FINISHED


class VIEW3D_OT_ViewportRecenter(Operator):
    """ Recenter Viewport and Cursor on Selected Object """
    bl_idname = "nendo.viewport_recenter"
    bl_label = "Recenter Viewport and Cursor on Selected"

    def execute(self, context: Context):
        current = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = "ACTIVE_ELEMENT"
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.view_center_cursor()
        bpy.ops.view3d.view_selected()
        context.scene.tool_settings.transform_pivot_point = current
        return FINISHED


class VIEW3D_OT_ViewportLock(Operator):
    """ Toggle Viewport Rotation """
    bl_idname = "nendo.viewport_lock"
    bl_label = "Viewport rotation lock toggle"

    region_ids = []

    def execute(self, context: Context):
        if not isinstance(context.area.spaces.active, SpaceView3D):
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


class VIEW3D_OT_BrushResize(Operator):
    """ Brush Resize """
    bl_idname = "nendo.brush_resize"
    bl_label = "Brush Size Adjust"

    # activate radial_control to change sculpt brush size
    def execute(self, context: Context):
        settings = get_settings()
        if settings.menu_style in ['fixed.bar']:
            if settings.gizmo_position in ["LEFT", "RIGHT"]:
                context.window.cursor_warp(
                    math.floor(context.region.width / 2), self.mousey
                )
            else:
                context.window.cursor_warp(
                    self.mousex, math.floor(context.region.height / 2)
                )
        if context.mode in ['PAINT_GPENCIL', 'EDIT_GPENCIL','SCULPT_GPENCIL','WEIGHT_GPENCIL','VERTEX_GPENCIL']:
            return self.resize2d(context)
        return self.resize3d(context)

    def resize2d(self, context: Context):
        data_path = "tool_settings.gpencil_paint.brush.size"
        if context.mode == 'SCULPT_GPENCIL':
            data_path = "tool_settings.gpencil_sculpt_paint.brush.size"
        if context.mode == 'WEIGHT_GPENCIL':
            data_path = "tool_settings.gpencil_weight_paint.brush.size"
        if context.mode == 'VERTEX_GPENCIL':
            data_path = "tool_settings.gpencil_vertex_paint.brush.size"
        bpy.ops.wm.radial_control(
            'INVOKE_DEFAULT',  # type: ignore
            data_path_primary=data_path,
        )
        return FINISHED

    def resize3d(self, context: Context):
        data_path = "tool_settings.sculpt.brush.size"
        if context.mode == 'PAINT_VERTEX':
            data_path = "tool_settings.vertex_paint.brush.size"
        if context.mode == 'PAINT_WEIGHT':
            data_path = "tool_settings.weight_paint.brush.size"
        if context.mode == 'PAINT_IMAGE':
            data_path = "tool_settings.image_paint.brush.size"
        if context.mode == 'PAINT_TEXTURE':
            data_path = "tool_settings.image_paint.brush.size"
        bpy.ops.wm.radial_control(
            'INVOKE_DEFAULT',  # type: ignore
            data_path_primary=data_path,
            data_path_secondary="tool_settings.unified_paint_settings.size",
            use_secondary=(
                "tool_settings.unified_paint_settings.use_unified_size"
            ),
            rotation_path="tool_settings.sculpt.brush.texture_slot.angle",
            color_path="tool_settings.sculpt.brush.cursor_color_add",
            image_id="tool_settings.sculpt.brush",
        )
        return FINISHED

    def invoke(self, context: Context, event: Event):
        self.mousex = event.mouse_region_x
        self.mousey = event.mouse_region_y
        self.execute(context)
        return FINISHED


class VIEW3D_OT_BrushStrength(Operator):
    """ Brush Strength """
    bl_idname = "nendo.brush_strength"
    bl_label = "Brush Strength Adjust"

    # activate radial_control to change sculpt brush size
    def execute(self, context: Context):
        settings = get_settings()
        if settings.menu_style in ['fixed.bar']:
            if settings.gizmo_position in ["LEFT", "RIGHT"]:
                context.window.cursor_warp(
                    math.floor(context.region.width / 2), self.mousey
                )
            else:
                context.window.cursor_warp(
                    self.mousex, math.floor(context.region.height / 2)
                )
        if context.mode in ['PAINT_GPENCIL', 'EDIT_GPENCIL','SCULPT_GPENCIL','WEIGHT_GPENCIL','VERTEX_GPENCIL']:
            return self.resize2d(context)
        return self.resize3d(context)

    def resize2d(self, context: Context):
        data_path = "tool_settings.gpencil_paint.brush.gpencil_settings.pen_strength"
        if context.mode == 'SCULPT_GPENCIL':
            data_path = "tool_settings.gpencil_sculpt_paint.brush.strength"
        if context.mode == 'WEIGHT_GPENCIL':
            data_path = "tool_settings.gpencil_weight_paint.brush.strength"
        if context.mode == 'VERTEX_GPENCIL':
            data_path = "tool_settings.gpencil_vertex_paint.brush.gpencil_settings.pen_strength"
        bpy.ops.wm.radial_control(
            'INVOKE_DEFAULT',  # type: ignore
            data_path_primary=data_path,
        )
        return FINISHED

    def resize3d(self, context: Context):
        data_path = "tool_settings.sculpt.brush.strength"
        if context.mode == 'PAINT_VERTEX':
            data_path = "tool_settings.vertex_paint.brush.strength"
        if context.mode == 'PAINT_WEIGHT':
            data_path = "tool_settings.weight_paint.brush.strength"
        if context.mode == 'PAINT_IMAGE':
            data_path = "tool_settings.image_paint.brush.strength"
        if context.mode == 'PAINT_TEXTURE':
            data_path = "tool_settings.image_paint.brush.strength"
        bpy.ops.wm.radial_control(
            'INVOKE_DEFAULT',  # type: ignore
            data_path_primary=data_path,
            data_path_secondary=(
                "tool_settings.unified_paint_settings.strength"
            ),
            use_secondary=(
                "tool_settings.unified_paint_settings.use_unified_strength"
            ),
            rotation_path="tool_settings.sculpt.brush.texture_slot.angle",
            color_path="tool_settings.sculpt.brush.cursor_color_add",
            image_id="tool_settings.sculpt.brush",
        )
        return FINISHED

    def invoke(self, context: Context, event: Event):
        self.mousex = event.mouse_region_x
        self.mousey = event.mouse_region_y
        self.execute(context)
        return FINISHED


class VIEW3D_OT_IncreaseMultires(Operator):
    """ Increment Multires by 1 or add subdivision """
    bl_idname = "nendo.increment_multires"
    bl_label = "Increment Multires modifier by 1 or add subdivision level"

    def execute(self, context: Context):
        settings = get_settings()
        if (
            not context.active_object
            or not len(context.active_object.modifiers)
        ):
            return CANCEL
        for mod in context.active_object.modifiers:
            # if mod is type of MultiresModifier
            if isinstance(mod, MultiresModifier):
                if context.mode == 'SCULPT':
                    if mod.sculpt_levels == mod.total_levels:
                        if mod.sculpt_levels < settings.subdivision_limit:
                            bpy.ops.object.multires_subdivide(
                                modifier=mod.name
                            )
                    else:
                        mod.sculpt_levels += 1
                else:
                    if mod.levels == mod.total_levels:
                        if mod.levels < settings.subdivision_limit:
                            bpy.ops.object.multires_subdivide(
                                modifier=mod.name
                            )
                    else:
                        mod.levels += 1
                return FINISHED
        return CANCEL


class VIEW3D_OT_DecreaseMultires(Operator):
    """ Decrement Multires by 1 """
    bl_idname = "nendo.decrement_multires"
    bl_label = "decrement Multires modifier by 1"

    def execute(self, context: Context):
        if (
            not context.active_object
            or not len(context.active_object.modifiers)
        ):
            return CANCEL
        for mod in context.active_object.modifiers:
            if not isinstance(mod, MultiresModifier):
                return FINISHED
            if context.mode == 'SCULPT':
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


class VIEW3D_OT_DensityUp(Operator):
    """ Increase voxel density """
    bl_idname = "nendo.density_up"
    bl_label = "Increase voxel density and remesh"

    def execute(self, context: Context):
        if (not context.active_object):
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, MultiresModifier):
                return CANCEL
        mesh = bpy.data.meshes[context.active_object.name]
        mesh.remesh_voxel_size *= 0.8
        bpy.ops.object.voxel_remesh()
        return FINISHED


class VIEW3D_OT_DensityDown(Operator):
    """ Decrease voxel density """
    bl_idname = "nendo.density_down"
    bl_label = "Decrease voxel density and remesh"

    def execute(self, context: Context):
        if (not context.active_object):
            return CANCEL
        for mod in context.active_object.modifiers:
            if isinstance(mod, MultiresModifier):
                return CANCEL
        mesh = bpy.data.meshes[context.active_object.name]
        mesh.remesh_voxel_size /= 0.8
        bpy.ops.object.voxel_remesh()
        return FINISHED
