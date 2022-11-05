from .Overlay import Overlay
from .Operators import * 
from . import Panel

from . import ui_gizmo

__classes__ = (
    VIEW3D_OT_TouchInput,
    VIEW2D_OT_TouchInput,
    VIEW3D_OT_Doubletap_Action,
    VIEW3D_OT_RightClick_Action,
    VIEW3D_OT_FlipTools,
    VIEW3D_OT_NextPivotMode,
    VIEW3D_OT_BrushResize,
    VIEW3D_OT_BrushStrength,
    VIEW_3D_OT_CycleControlGizmo,
    VIEW3D_OT_ToggleNPanel,
    VIEW3D_OT_ToggleFloatingMenu,
    VIEW3D_OT_ToggleTouchControls,
    VIEW3D_OT_ViewportLock,
    VIEW3D_OT_ViewportRecenter,
    VIEW3D_OT_MoveFloatMenu,
    VIEW3D_OT_IncreaseMultires,
    VIEW3D_OT_DecreaseMultires,
    VIEW3D_OT_MenuController,
)
ov = Overlay()


def register():
    from bpy.utils import register_class
    from .touch_input import register_keymaps
    for cls in __classes__:
        register_class(cls)

    ui_gizmo.register()
    ov.drawUI()

    Panel.register()
    register_keymaps()


def unregister():
    from bpy.utils import unregister_class
    from .touch_input import unregister_keymaps

    Panel.unregister()
    unregister_keymaps()

    ov.clear_overlays()
    ui_gizmo.unregister()
    for cls in reversed(__classes__):
        unregister_class(cls)
