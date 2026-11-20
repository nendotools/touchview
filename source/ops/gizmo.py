import bpy
from bpy.types import Operator
from mathutils import Vector

from ..utils.addon import preferences
from ..utils.blender import *
from ..utils.constants import CANCEL, FINISHED, MODAL


class TOUCHVIEW_OT_modal_move(Operator):
    """Shared drag-to-reposition behaviour for floating UI elements."""

    position_attr = ""
    padding = 28
    exit_on_mouse_exit = False

    def invoke(self, context, event):
        prefs = preferences()
        fence = safe_area_3d(padding=self.padding)
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))

        self.initial = Vector(getattr(prefs, self.position_attr))
        self.mouse_initial = Vector((event.mouse_region_x, event.mouse_region_y))
        self.mouse = self.mouse_initial.copy()
        self.offset = Vector(
            (
                (span.x * self.initial.x * 0.01 + fence[0].x) - self.mouse.x,
                (span.y * self.initial.y * 0.01 + fence[0].y) - self.mouse.y,
            )
        )
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL

    def execute(self, context):
        prefs = preferences()
        fence = safe_area_3d(padding=self.padding)
        span = Vector((fence[1].x - fence[0].x, fence[1].y - fence[0].y))
        position = getattr(prefs, self.position_attr)

        position[0] = min(max((self.mouse.x - fence[0].x + self.offset.x) / span.x * 100.0, 0.0), 100.0)
        position[1] = min(max((self.mouse.y - fence[0].y + self.offset.y) / span.y * 100.0, 0.0), 100.0)
        return FINISHED

    def modal(self, context, event):
        if self.exit_on_mouse_exit and self._mouse_outside(context, event):
            # mouse leaving the region is not reported reliably in Blender 4.x
            return FINISHED

        if event.type == "MOUSEMOVE" and event.value != "RELEASE":  # Apply
            context.region.tag_redraw()
            self.mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            self.execute(context)
        elif event.value == "RELEASE":  # Confirm
            if not self._has_moved():
                prefs = preferences()
                position = getattr(prefs, self.position_attr)
                position[0] = self.initial[0]
                position[1] = self.initial[1]
                self.on_click(context)
            return FINISHED
        return MODAL

    def _mouse_outside(self, context, event) -> bool:
        return (
            event.mouse_region_x < 0
            or event.mouse_region_y < 0
            or event.mouse_region_x > context.region.width
            or event.mouse_region_y > context.region.height
        )

    def _has_moved(self) -> bool:
        return (self.mouse - self.mouse_initial).length > preferences().menu_spacing / 2

    def on_click(self, context):
        pass


class TOUCHVIEW_OT_move_float_menu(TOUCHVIEW_OT_modal_move):
    """Tap to show/hide the menu buttons, drag to move the menu"""

    bl_label = "Relocate Gizmo Menu"
    bl_idname = "touchview.move_float_menu"

    position_attr = "menu_position"
    padding = 90

    def on_click(self, context):
        preferences().show_gizmos = not preferences().show_gizmos


class TOUCHVIEW_OT_menu_controller(TOUCHVIEW_OT_modal_move):
    """Tap to open the action menu, drag to move it"""

    bl_label = "Relocate Action Menu"
    bl_idname = "touchview.move_action_menu"

    position_attr = "floating_position"

    def on_click(self, context):
        bpy.ops.wm.call_menu_pie(
            "INVOKE_DEFAULT",  # type: ignore
            name="TOUCHVIEW_MT_floating",
        )


class TOUCHVIEW_OT_float_controller(TOUCHVIEW_OT_modal_move):
    """Tap to toggle touch controls, drag to move this button"""

    bl_label = "Relocate Toggle Button"
    bl_idname = "touchview.move_toggle_button"

    position_attr = "toggle_position"
    exit_on_mouse_exit = True

    def on_click(self, context):
        preferences().is_enabled = not preferences().is_enabled


class TOUCHVIEW_OT_cycle_control_gizmo(Operator):
    """Cycle the object gizmo between move, rotate, scale and none"""

    bl_label = "switch object control gizmo"
    bl_idname = "touchview.cycle_control_gizmo"

    @classmethod
    def poll(cls, context):
        return context.area.type in ["VIEW_2D", "VIEW_3D"] and context.region.type == "WINDOW"

    def execute(self, context):
        space = context.space_data
        if not isinstance(space, bpy.types.SpaceView3D):
            return CANCEL
        mode = self.get_mode(space)
        self.clear_controls(space)
        if mode == "none":
            space.show_gizmo_object_translate = True
        if mode == "translate":
            space.show_gizmo_object_rotate = True
        if mode == "rotate":
            space.show_gizmo_object_scale = True
        return FINISHED

    def get_mode(self, space: bpy.types.SpaceView3D):
        if space.show_gizmo_object_translate:
            return "translate"
        if space.show_gizmo_object_rotate:
            return "rotate"
        if space.show_gizmo_object_scale:
            return "scale"
        return "none"

    def clear_controls(self, space: bpy.types.SpaceView3D):
        space.show_gizmo_object_translate = False
        space.show_gizmo_object_rotate = False
        space.show_gizmo_object_scale = False


classes = (
    TOUCHVIEW_OT_move_float_menu,
    TOUCHVIEW_OT_menu_controller,
    TOUCHVIEW_OT_cycle_control_gizmo,
    TOUCHVIEW_OT_float_controller,
)


register, unregister = bpy.utils.register_classes_factory(classes)
