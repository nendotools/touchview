import bpy
from bpy.types import Operator

from mathutils import Vector

from ..utils.blender import *
from ..utils.constants import CANCEL, FINISHED, MODAL


class TOUCHVIEW_OT_move_float_menu(Operator):
    bl_label = "Relocate Gizmo Menu"
    bl_idname = "touchview.move_float_menu"

    def invoke(self, context, event):
        self.has_moved = False
        prefs = preferences()
        fence = safe_area_3d(padding=90)
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))

        self.init_x = prefs.menu_position[0]
        self.init_y = prefs.menu_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector(
            (
                (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
                (span.y * self.init_y * 0.01 + fence[0].y) - self.y,
            )
        )
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL

    def execute(self, context):
        prefs = preferences()
        fence = safe_area_3d(padding=90)
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))

        prefs.menu_position[0] = min(max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0), 100.0)
        prefs.menu_position[1] = min(max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0), 100.0)
        return FINISHED

    def modal(self, context, event):
        prefs = preferences()
        if event.type == "MOUSEMOVE" and event.value != "RELEASE":  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == "RELEASE":  # Confirm
            if not self.__hasMoved():
                prefs.menu_position[0] = self.init_x
                prefs.menu_position[1] = self.init_y
                prefs.show_gizmos = not prefs.show_gizmos
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        prefs = preferences()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > prefs.menu_spacing / 2:
            return True
        return False


class TOUCHVIEW_OT_menu_controller(Operator):
    bl_label = "Relocate Action Menu"
    bl_idname = "touchview.move_action_menu"

    def invoke(self, context, event):
        self.has_moved = False
        prefs = preferences()
        fence = safe_area_3d()

        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))
        self.init_x = prefs.floating_position[0]
        self.init_y = prefs.floating_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector(
            (
                (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
                (span.y * self.init_y * 0.01 + fence[0].y) - self.y,
            )
        )
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL

    def execute(self, context):
        prefs = preferences()
        fence = safe_area_3d()
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))

        prefs.floating_position[0] = min(max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0), 100.0)
        prefs.floating_position[1] = min(max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0), 100.0)
        return FINISHED

    def modal(self, context, event):
        prefs = preferences()
        if event.type == "MOUSEMOVE" and event.value != "RELEASE":  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == "RELEASE":  # Confirm
            if not self.__hasMoved():
                prefs.floating_position[0] = self.init_x
                prefs.floating_position[1] = self.init_y
                bpy.ops.wm.call_menu_pie(
                    "INVOKE_DEFAULT",  # type: ignore
                    name="TOUCHVIEW_MT_floating",
                )
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        prefs = preferences()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > prefs.menu_spacing / 2:
            return True
        return False


class TOUCHVIEW_OT_cycle_controlGizmo(Operator):
    bl_label = "switch object control gizmo"
    bl_idname = "touchview.cycle_control_gizmo"

    @classmethod
    def poll(cls, context):
        return context.area.type in ["VIEW_2D", "VIEW_3D"] and context.region.type == "WINDOW"

    def execute(self, context):
        space = context.space_data
        if not isinstance(space, bpy.types.SpaceView3D):
            return CANCEL
        mode = self.getMode(space)
        self.clearControls(space)
        if mode == "none":
            space.show_gizmo_object_translate = True
        if mode == "translate":
            space.show_gizmo_object_rotate = True
        if mode == "rotate":
            space.show_gizmo_object_scale = True
        return FINISHED

    def getMode(self, space: bpy.types.SpaceView3D):
        if space.show_gizmo_object_translate:
            return "translate"
        if space.show_gizmo_object_rotate:
            return "rotate"
        if space.show_gizmo_object_scale:
            return "scale"
        return "none"

    def clearControls(self, space: bpy.types.SpaceView3D):
        space.show_gizmo_object_translate = False
        space.show_gizmo_object_rotate = False
        space.show_gizmo_object_scale = False


class TOUCHVIEW_OT_float_controller(Operator):
    bl_label = "Relocate Toggle Button"
    bl_idname = "touchview.move_toggle_button"

    def invoke(self, context, event):
        self.has_moved = False
        prefs = preferences()
        fence = safe_area_3d()

        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))
        self.init_x = prefs.toggle_position[0]
        self.init_y = prefs.toggle_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector(
            (
                (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
                (span.y * self.init_y * 0.01 + fence[0].y) - self.y,
            )
        )
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL

    def execute(self, context):
        prefs = preferences()
        fence = safe_area_3d()
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))

        prefs.toggle_position[0] = min(max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0), 100.0)
        prefs.toggle_position[1] = min(max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0), 100.0)
        return FINISHED

    def modal(self, context, event):
        prefs = preferences()
        if (
            event.mouse_region_x < 0
            or event.mouse_region_y < 0
            or event.mouse_region_x > context.area.width
            or event.mouse_region_y > context.area.height
        ):
            # mouse out of region area broken in Blender 4.x, exit early
            return FINISHED
        if event.type == "MOUSEMOVE" and event.value != "RELEASE":  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == "RELEASE":  # Confirm
            if not self.__hasMoved():
                prefs.toggle_position[0] = self.init_x
                prefs.toggle_position[1] = self.init_y
                prefs.is_enabled = not prefs.is_enabled
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        prefs = preferences()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > prefs.menu_spacing / 2:
            return True
        return False


classes = (
    TOUCHVIEW_OT_move_float_menu,
    TOUCHVIEW_OT_menu_controller,
    TOUCHVIEW_OT_cycle_controlGizmo,
    TOUCHVIEW_OT_float_controller,
)


register, unregister = bpy.utils.register_classes_factory(classes)
