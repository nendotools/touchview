import math

import bpy
from bpy import ops
from bpy.props import EnumProperty
from bpy.types import Context, Event, Operator
from bpy_extras import view3d_utils
from mathutils import Vector

from ..constants import (FINISHED, LMOUSE, PASSTHROUGH, PEN, PRESS, RMOUSE,
                         brush_modes, input_mode_items)
from ..utils import get_settings


def isTouch(event: Event):
    return event.pressure in [0.0,1.0]


class VIEW3D_OT_RightClick_Action(Operator):
    """ Viewport right-click shortcut """
    bl_idname = "nendo.rc_action"
    bl_label = "Viewport right-click shortcut"

    def execute(self, context: Context):
        settings = get_settings()
        op = settings.right_click_mode.split('.')
        if op[1] == 'transfer_mode' and context.area.type != 'VIEW_3D':
            return PASSTHROUGH
        if op[1] == 'transfer_mode' and context.mode == 'OBJECT':
            bpy.ops.view3d.select('INVOKE_DEFAULT')  # type: ignore
            return PASSTHROUGH
        opgrp = getattr(bpy.ops, op[0])
        getattr(opgrp, op[1])('INVOKE_DEFAULT')
        return FINISHED

    def invoke(self, context: Context, event: Event):
        settings = get_settings()
        if settings.right_click_source == "none":
            return PASSTHROUGH
        if event.type not in [RMOUSE]:
            return PASSTHROUGH
        if isTouch(event) and settings.right_click_source == "pen":
            return PASSTHROUGH
        if not isTouch(event) and settings.right_click_source == "mouse":
            return PASSTHROUGH
        if event.value == "DOUBLE_CLICK":
            return PASSTHROUGH
        self.execute(context)
        return FINISHED


class VIEW3D_OT_Doubletap_Action(Operator):
    """ Viewport double-tap shortcut """
    bl_idname = "nendo.dt_action"
    bl_label = "Viewport double-tap shortcut"

    def execute(self, context: Context):
        settings = get_settings()
        if not settings.enable_double_click:
            return PASSTHROUGH
        op = settings.double_click_mode.split('.')
        opgrp = getattr(bpy.ops, op[0])
        if op[1] == 'transfer_mode' and context.area.type != 'VIEW_3D':
            return PASSTHROUGH
        if op[1] == 'transfer_mode' and context.mode == 'OBJECT':
            bpy.ops.view3d.select('INVOKE_DEFAULT')  # type: ignore
            return PASSTHROUGH
        getattr(opgrp, op[1])('INVOKE_DEFAULT')
        return FINISHED

    def invoke(self, context: Context, event: Event):
        if event.type not in [PEN, LMOUSE]:
            return PASSTHROUGH
        if not isTouch(event):
            return PASSTHROUGH
        if event.value != "DOUBLE_CLICK":
            return PASSTHROUGH
        return self.execute(context)

    @classmethod
    def poll(cls, context: Context):
        return context.area.type in [
            'NODE_EDITOR', 'VIEW_2D', 'VIEW_3D', 'IMAGE_EDITOR'
        ] and context.region.type == 'WINDOW'


class VIEW2D_OT_TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "nendo.view_ops_2d"
    bl_label = "2D Viewport Control Regions"

    delta: tuple[float, float]

    mode: EnumProperty(  # type: ignore
        name="Mode",
        description="Sets the viewport control type",
        items=input_mode_items,
        default='PAN',
        options={"HIDDEN"}
    )

    def execute(self, context: Context):
        if context.area.type == 'IMAGE_EDITOR':
            return self.exec_image_editor(context)
        if self.mode == "DOLLY":
            bpy.ops.view2d.zoom('INVOKE_DEFAULT')  # type: ignore
        elif self.mode == "PAN":
            bpy.ops.view2d.pan('INVOKE_DEFAULT')  # type: ignore
        return FINISHED

    def exec_image_editor(self, _: Context):
        if self.mode == "PAN":
            bpy.ops.image.view_pan('INVOKE_DEFAULT')  # type: ignore
        elif self.mode == "DOLLY":
            bpy.ops.image.view_zoom('INVOKE_DEFAULT')  # type: ignore
        return FINISHED

    def invoke(self, context: Context, event: Event):
        settings = get_settings()
        if not settings.is_enabled:
            return PASSTHROUGH
        if (
            settings.input_mode == 'both'
            and (event.type == PEN or not isTouch(event))
        ):
            return PASSTHROUGH

        if event.value != PRESS:
            return PASSTHROUGH
        self.delta = (event.mouse_region_x, event.mouse_region_y)

        mid_point = Vector(
            (context.region.width / 2, context.region.height / 2)
        )

        dolly_scale = settings.getWidth()
        dolly_wid = mid_point.x * dolly_scale

        if (
            dolly_wid > self.delta[0]
            or self.delta[0] > context.region.width - dolly_wid
        ):
            self.mode = "DOLLY"
        else:
            self.mode = "PAN"

        if settings.swap_panrotate:
            if self.mode == "PAN":
                self.mode = "ORBIT"
            elif self.mode == "ORBIT":
                self.mode = "PAN"

        self.execute(context)
        return FINISHED

    @classmethod
    def poll(cls, context: Context):
        return (
            context.area.type in ['NODE_EDITOR', 'VIEW_2D', 'IMAGE_EDITOR']
            and context.region.type == 'WINDOW'
        )


class VIEW3D_OT_TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "nendo.view_ops_3d"
    bl_label = "Viewport Control Regions"

    delta: tuple[float, float]

    mode: EnumProperty(  # type: ignore
        name="Mode",
        description="Sets the viewport control type",
        items=input_mode_items,
        default='ORBIT',
        options={"HIDDEN"}
    )

    def execute(self, context: Context):
        if self.mode == "DOLLY":
            ops.view3d.zoom('INVOKE_DEFAULT')  # type: ignore
        elif self.mode == "ORBIT":
            if context.mode == "SCULPT":
                ops.sculpt.set_pivot_position(
                    mode="SURFACE",
                    mouse_x=self.delta[0],
                    mouse_y=self.delta[1]
                )
            ops.view3d.rotate('INVOKE_DEFAULT')  # type: ignore
        elif self.mode == "PAN":
            bpy.ops.view3d.move('INVOKE_DEFAULT')  # type: ignore
        return FINISHED

    def should_pass(self, context: Context, event: Event):
        settings = get_settings()

        # experimental passthrough in drawing mode
        if (settings.lazy_mode
            and not settings.is_enabled
            and brush_modes.__contains__(context.mode)
            and self.mouseTarget(context, event) != context.active_object):
            return False

        if not settings.is_enabled:
            return True

        if (
            settings.input_mode == 'full'
            and (event.type == PEN or not isTouch(event))
        ):
            return True 

        if event.value != PRESS:
            return True 
        return False

    def invoke(self, context: Context, event: Event):
        settings = get_settings()
        passcheck = self.should_pass(context, event)
        if passcheck: return PASSTHROUGH

        self.delta = (event.mouse_region_x, event.mouse_region_y)

        mid_point = Vector(
            (context.region.width / 2, context.region.height / 2)
        )

        dolly_scale = settings.getWidth()
        pan_scale = settings.getRadius()

        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist(
            (0, 0), mid_point  # type: ignore
        ) * (pan_scale * 0.5)

        is_quadview_orthographic = (
            context.region_data.is_orthographic_side_view
            and context.region.alignment == "QUAD_SPLIT"
        )
        is_locked = (
            context.region_data.lock_rotation or is_quadview_orthographic
        )

        if (
            dolly_wid > self.delta[0]
            or self.delta[0] > context.region.width - dolly_wid
        ):
            self.mode = "DOLLY"
        elif math.dist(
            self.delta, mid_point  # type: ignore
        ) < pan_diameter or is_locked:
            self.mode = "PAN"
        else:
            self.mode = "ORBIT"

        if settings.swap_panrotate and not is_locked:
            if self.mode == "PAN":
                self.mode = "ORBIT"
            elif self.mode == "ORBIT":
                self.mode = "PAN"

        if context.mode == "SCULPT":
            bpy.ops.sculpt.set_pivot_position(mode=settings.pivot_mode)
        self.execute(context)
        return FINISHED

    def mouseTarget(self, context:Context, event: Event):
        # get the context arguments
        region = context.region
        rv3d = context.region_data
        coord = Vector((event.mouse_region_x, event.mouse_region_y))

        # get the ray from the viewport and mouse
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        self.ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

        self.ray_target = self.ray_origin + view_vector
        return self.isCurrentObject(context)

    def visible_objects_and_duplis(self, context:Context):
        depsgraph = context.evaluated_depsgraph_get()
        for dup in depsgraph.object_instances:
            if dup.is_instance:  # Real dupli instance
                obj = dup.instance_object
                yield (obj, dup.matrix_world.copy()) # type: ignore
            else:  # Usual object
                obj = dup.object
                yield (obj, obj.matrix_world.copy()) # type: ignore

    def obj_ray_cast(self, obj, matrix):
        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv @ self.ray_origin
        ray_target_obj = matrix_inv @ self.ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj

        # cast the ray
        success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

        if success:
            return location, normal, face_index
        else:
            return None, None, None

    def isCurrentObject(self, context:Context):
        # cast rays and find the closest object
        best_length_squared = -1.0
        best_obj = None

        for obj, matrix in self.visible_objects_and_duplis(context):
            if obj.type == 'MESH':
                hit, _, _= self.obj_ray_cast(obj, matrix)
                if hit is not None:
                    hit_world = matrix @ hit
                    length_squared = (hit_world - self.ray_origin).length_squared
                    if best_obj is None or length_squared < best_length_squared:
                        best_length_squared = length_squared
                        best_obj = obj

        return best_obj.original if best_obj is not None else None

    @classmethod
    def poll(cls, context: Context):
        return (
            context.area.type == 'VIEW_3D'
            and context.region.type == 'WINDOW'
        )
