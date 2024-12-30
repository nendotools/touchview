# Built-in modules
import math

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy_extras.view3d_utils import (region_2d_to_origin_3d,
                                     region_2d_to_vector_3d)
from mathutils import Vector

# Local modules
from ..utils.blender import preferences
from ..utils.constants import (FINISHED, LMOUSE, PASSTHROUGH, PEN, PRESS,
                               RMOUSE, brush_modes, input_mode_items)


def is_touch(event):
    return event.pressure in [0.0, 1.0]


class TOUCHVIEW_OT_right_click_action(Operator):
    """Viewport right-click shortcut"""

    bl_label = "Viewport right-click shortcut"
    bl_idname = "touchview.rc_action"

    @classmethod
    def poll(cls, context):
        return context.area.type in {"VIEW_2D", "VIEW_3D"} and context.region.type == "WINDOW"

    def invoke(self, context, event):
        prefs = preferences()
        if prefs.right_click_source == "NONE":
            return PASSTHROUGH
        if event.type not in [RMOUSE]:
            return PASSTHROUGH
        if is_touch(event) and prefs.right_click_source == "PEN":
            return PASSTHROUGH
        if not is_touch(event) and prefs.right_click_source == "MOUSE":
            return PASSTHROUGH
        if event.value == "DOUBLE_CLICK":
            return PASSTHROUGH
        self.execute(context)
        return FINISHED

    def execute(self, context):
        prefs = preferences()
        op = prefs.right_click_mode.split(".")
        if op[1] == "transfer_mode" and context.area.type != "VIEW_3D":
            return PASSTHROUGH
        if op[1] == "transfer_mode" and context.mode == "OBJECT":
            bpy.ops.view3d.select("INVOKE_DEFAULT")  # type: ignore
            return PASSTHROUGH
        opgrp = getattr(bpy.ops, op[0])
        getattr(opgrp, op[1])("INVOKE_DEFAULT")
        return FINISHED


class TOUCHVIEW_OT_double_click_action(Operator):
    """Viewport double-tap shortcut"""

    bl_label = "Viewport double-tap shortcut"
    bl_idname = "touchview.dt_action"

    @classmethod
    def poll(cls, context):
        return context.area.type in {"NODE_EDITOR", "VIEW_2D", "VIEW_3D", "IMAGE_EDITOR"} and context.region.type == "WINDOW"

    def invoke(self, context, event):
        if event.type not in [PEN, LMOUSE]:
            return PASSTHROUGH
        if not is_touch(event):
            return PASSTHROUGH
        if event.value != "DOUBLE_CLICK":
            return PASSTHROUGH
        return self.execute(context)

    def execute(self, context):
        prefs = preferences()
        if not prefs.enable_double_click:
            return PASSTHROUGH
        op = prefs.double_click_mode.split(".")
        opgrp = getattr(bpy.ops, op[0])
        if op[1] == "transfer_mode" and context.area.type != "VIEW_3D":
            return PASSTHROUGH
        if op[1] == "transfer_mode" and context.mode == "OBJECT":
            bpy.ops.view3d.select("INVOKE_DEFAULT")  # type: ignore
            return PASSTHROUGH
        getattr(opgrp, op[1])("INVOKE_DEFAULT")
        return FINISHED


class TOUCHVIEW_OT_touch_input_2d(Operator):
    """Active Viewport control zones"""

    bl_label = "2D Viewport Control Regions"
    bl_idname = "touchview.view_ops_2d"

    delta: tuple[float, float]

    mode: EnumProperty(  # type: ignore
        name="Mode",
        description="Sets the viewport control type",
        items=input_mode_items,
        default="PAN",
        options={"HIDDEN"},
    )

    @classmethod
    def poll(cls, context):
        return context.area.type in {"NODE_EDITOR", "VIEW_2D", "IMAGE_EDITOR"} and context.region.type == "WINDOW"

    def invoke(self, context, event):
        prefs = preferences()
        if not prefs.is_enabled:
            return PASSTHROUGH
        if prefs.input_mode == "FULL" and (event.type == PEN or not is_touch(event)):
            return PASSTHROUGH

        if event.value != PRESS:
            return PASSTHROUGH
        self.delta = (event.mouse_region_x, event.mouse_region_y)

        mid_point = Vector((context.region.width / 2, context.region.height / 2))

        dolly_scale = prefs.getWidth()
        dolly_wid = mid_point.x * dolly_scale

        if dolly_wid > self.delta[0] or self.delta[0] > context.region.width - dolly_wid:
            self.mode = "DOLLY"
        else:
            self.mode = "PAN"

        if prefs.swap_panrotate:
            if self.mode == "PAN":
                self.mode = "ORBIT"
            elif self.mode == "ORBIT":
                self.mode = "PAN"

        self.execute(context)
        return FINISHED

    def execute(self, context):
        if context.area.type == "IMAGE_EDITOR":
            return self.exec_image_editor(context)
        if self.mode == "DOLLY":
            bpy.ops.view2d.zoom("INVOKE_DEFAULT")  # type: ignore
        elif self.mode == "PAN":
            bpy.ops.view2d.pan("INVOKE_DEFAULT")  # type: ignore
        return FINISHED

    def exec_image_editor(self, context):
        if self.mode == "PAN":
            bpy.ops.image.view_pan("INVOKE_DEFAULT")  # type: ignore
        elif self.mode == "DOLLY":
            bpy.ops.image.view_zoom("INVOKE_DEFAULT")  # type: ignore
        return FINISHED


class TOUCHVIEW_OT_touch_input_3d(Operator):
    """Active Viewport control zones"""

    bl_label = "Viewport Control Regions"
    bl_idname = "touchview.view_ops_3d"

    delta: tuple[float, float]

    mode: EnumProperty(  # type: ignore
        name="Mode",
        description="Sets the viewport control type",
        items=input_mode_items,
        options={"HIDDEN"},
        default="ORBIT",
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D" and context.region.type == "WINDOW"

    def invoke(self, context, event):
        prefs = preferences()
        passcheck = self.should_pass(context, event)
        if passcheck:
            return PASSTHROUGH

        self.delta = (event.mouse_region_x, event.mouse_region_y)

        mid_point = Vector((context.region.width / 2, context.region.height / 2))

        dolly_scale = prefs.getWidth()
        pan_scale = prefs.getRadius()

        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist(
            (0, 0),
            mid_point,  # type: ignore
        ) * (pan_scale * 0.5)

        is_quadview_orthographic = context.region_data.is_orthographic_side_view and context.region.alignment == "QUAD_SPLIT"
        is_locked = context.region_data.lock_rotation or is_quadview_orthographic

        if dolly_wid > self.delta[0] or self.delta[0] > context.region.width - dolly_wid:
            self.mode = "DOLLY"
        elif (
            math.dist(
                self.delta,
                mid_point,  # type: ignore
            )
            < pan_diameter
            or is_locked
        ):
            self.mode = "PAN"
        else:
            self.mode = "ORBIT"

        if prefs.swap_panrotate and not is_locked:
            if self.mode == "PAN":
                self.mode = "ORBIT"
            elif self.mode == "ORBIT":
                self.mode = "PAN"

        if context.mode == "SCULPT":
            bpy.ops.sculpt.set_pivot_position(mode=prefs.pivot_mode)
        self.execute(context)
        return FINISHED

    def execute(self, context):
        if self.mode == "DOLLY":
            bpy.ops.view3d.zoom("INVOKE_DEFAULT")  # type: ignore
        elif self.mode == "ORBIT":
            if context.mode == "SCULPT":
                bpy.ops.sculpt.set_pivot_position(mode="SURFACE", mouse_x=self.delta[0], mouse_y=self.delta[1])
            bpy.ops.view3d.rotate("INVOKE_DEFAULT")  # type: ignore
        elif self.mode == "PAN":
            bpy.ops.view3d.move("INVOKE_DEFAULT")  # type: ignore
        return FINISHED

    def should_pass(self, context, event):
        prefs = preferences()

        # experimental passthrough in drawing mode
        if (
            prefs.lazy_mode
            and not prefs.is_enabled
            and event.value == PRESS
            and brush_modes.__contains__(context.mode)
            and self.mouseTarget(context, event) != context.active_object
        ):
            return False

        if not prefs.is_enabled:
            return True

        if prefs.input_mode == "FULL" and (event.type == PEN or not is_touch(event)):
            return True

        if event.value != PRESS:
            return True
        return False

    def mouseTarget(self, context, event):
        # get the context arguments
        region = context.region
        rv3d = context.region_data
        coord = Vector((event.mouse_region_x, event.mouse_region_y))

        # get the ray from the viewport and mouse
        view_vector = region_2d_to_vector_3d(region, rv3d, coord)
        self.ray_origin = region_2d_to_origin_3d(region, rv3d, coord)

        self.ray_target = self.ray_origin + view_vector
        return self.isCurrentObject(context)

    def visible_objects_and_duplicates(self, context):
        depsgraph = context.evaluated_depsgraph_get()
        for dup in depsgraph.object_instances:
            if dup.is_instance:  # Real dupli instance
                obj = dup.instance_object
                yield (obj, dup.matrix_world.copy())  # type: ignore
            else:  # Usual object
                obj = dup.object
                yield (obj, obj.matrix_world.copy())  # type: ignore

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

    def isCurrentObject(self, context):
        # cast rays and find the closest object
        best_length_squared = -1.0
        best_obj = None

        for obj, matrix in self.visible_objects_and_duplicates(context):
            if obj.type == "MESH":
                hit, _, _ = self.obj_ray_cast(obj, matrix)
                if hit is not None:
                    hit_world = matrix @ hit
                    length_squared = (hit_world - self.ray_origin).length_squared
                    if best_obj is None or length_squared < best_length_squared:
                        best_length_squared = length_squared
                        best_obj = obj

        return best_obj.original if best_obj is not None else None


classes = (
    TOUCHVIEW_OT_right_click_action,
    TOUCHVIEW_OT_double_click_action,
    TOUCHVIEW_OT_touch_input_2d,
    TOUCHVIEW_OT_touch_input_3d,
)


register, unregister = bpy.utils.register_classes_factory(classes)
