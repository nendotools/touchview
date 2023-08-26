import bpy
from bpy.types import Context, Event, Operator, SpaceView3D
from mathutils import Vector

from ..constants import CANCEL, FINISHED, MODAL
from ..utils import buildSafeArea, get_settings


class VIEW3D_OT_MoveFloatMenu(Operator):
    bl_idname = "nendo.move_float_menu"
    bl_label = "Relocate Gizmo Menu"

    def execute(self, _: Context):
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))

        settings.menu_position[0] = min(
            max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0),
            100.0
        )
        settings.menu_position[1] = min(
            max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0),
            100.0
        )
        return FINISHED

    def modal(self, context: Context, event: Event):
        settings = get_settings()
        if event.type == 'MOUSEMOVE' and event.value != 'RELEASE':  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == 'RELEASE':  # Confirm
            if not self.__hasMoved():
                settings.menu_position[0] = self.init_x
                settings.menu_position[1] = self.init_y
                settings.show_gizmos = not settings.show_gizmos
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        settings = get_settings()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > settings.menu_spacing / 2:
            return True
        return False

    def invoke(self, context: Context, event: Event):
        self.has_moved = False
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))
        self.init_x = settings.menu_position[0]
        self.init_y = settings.menu_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector((
            (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
            (span.y * self.init_y * 0.01 + fence[0].y) - self.y
        ))
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL


class VIEW3D_OT_MenuController(Operator):
    bl_idname = "nendo.move_action_menu"
    bl_label = "Relocate Action Menu"

    def execute(self, _: Context):
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))

        settings.floating_position[0] = min(
            max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0),
            100.0
        )
        settings.floating_position[1] = min(
            max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0),
            100.0
        )
        return FINISHED

    def modal(self, context: Context, event: Event):
        settings = get_settings()
        if event.type == 'MOUSEMOVE' and event.value != 'RELEASE':  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == 'RELEASE':  # Confirm
            if not self.__hasMoved():
                settings.floating_position[0] = self.init_x
                settings.floating_position[1] = self.init_y
                bpy.ops.wm.call_menu_pie(
                    "INVOKE_DEFAULT",  # type: ignore
                    name="PIE_MT_Floating_Menu"
                )
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        settings = get_settings()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > settings.menu_spacing / 2:
            return True
        return False

    def invoke(self, context: Context, event: Event):
        self.has_moved = False
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))
        self.init_x = settings.floating_position[0]
        self.init_y = settings.floating_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector((
            (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
            (span.y * self.init_y * 0.01 + fence[0].y) - self.y
        ))
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL


class VIEW3D_OT_CycleControlGizmo(Operator):
    bl_idname = "nendo.cycle_control_gizmo"
    bl_label = "switch object control gizmo"

    def execute(self, context: Context):
        space = context.space_data
        if not isinstance(space, SpaceView3D):
            return CANCEL
        mode = self.getMode(space)
        self.clearControls(space)
        if mode == 'none':
            space.show_gizmo_object_translate = True
        if mode == 'translate':
            space.show_gizmo_object_rotate = True
        if mode == 'rotate':
            space.show_gizmo_object_scale = True
        return FINISHED

    def getMode(self, space: SpaceView3D):
        if space.show_gizmo_object_translate:
            return 'translate'
        if space.show_gizmo_object_rotate:
            return 'rotate'
        if space.show_gizmo_object_scale:
            return 'scale'
        return 'none'

    def clearControls(self, space: SpaceView3D):
        space.show_gizmo_object_translate = False
        space.show_gizmo_object_rotate = False
        space.show_gizmo_object_scale = False

    @classmethod
    def poll(cls, context: Context):
        return context.area.type in [
            'VIEW_2D', 'VIEW_3D'
        ] and context.region.type == 'WINDOW'


class VIEW3D_OT_FloatController(Operator):
    bl_idname = "nendo.move_toggle_button"
    bl_label = "Relocate Toggle Button"

    def execute(self, _: Context):
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))

        settings.toggle_position[0] = min(
            max((self.x - fence[0].x + self.offset.x) / (span.x) * 100.0, 0.0),
            100.0
        )
        settings.toggle_position[1] = min(
            max((self.y - fence[0].y + self.offset.y) / (span.y) * 100.0, 0.0),
            100.0
        )
        return FINISHED

    def modal(self, context: Context, event: Event):
        settings = get_settings()
        if event.type == 'MOUSEMOVE' and event.value != 'RELEASE':  # Apply
            context.region.tag_redraw()
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
        elif event.value == 'RELEASE':  # Confirm
            if not self.__hasMoved():
                settings.toggle_position[0] = self.init_x
                settings.toggle_position[1] = self.init_y
                settings.is_enabled = not settings.is_enabled
            return FINISHED
        return MODAL

    def __hasMoved(self) -> bool:
        settings = get_settings()
        init = Vector((self.mouse_init_x, self.mouse_init_y))
        final = Vector((self.x, self.y))
        if (final - init).length > settings.menu_spacing / 2:
            return True
        return False

    def invoke(self, context: Context, event: Event):
        self.has_moved = False
        settings = get_settings()
        fence = buildSafeArea()
        span = Vector((
            fence[1].x - fence[0].x,
            fence[1].y - fence[0].y
        ))
        self.init_x = settings.toggle_position[0]
        self.init_y = settings.toggle_position[1]
        self.mouse_init_x = self.x = event.mouse_region_x
        self.mouse_init_y = self.y = event.mouse_region_y
        self.offset = Vector((
            (span.x * self.init_x * 0.01 + fence[0].x) - self.x,
            (span.y * self.init_y * 0.01 + fence[0].y) - self.y
        ))
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return MODAL
