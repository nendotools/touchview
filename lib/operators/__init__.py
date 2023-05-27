# flake8: noqa
from .actions import *
from .touch import *
from .ui import *

__classes__ = (
    VIEW3D_OT_TouchInput,
    VIEW2D_OT_TouchInput,
    VIEW3D_OT_Doubletap_Action,
    VIEW3D_OT_RightClick_Action,
    VIEW3D_OT_CycleControlGizmo,
    VIEW3D_OT_FloatController,
    VIEW3D_OT_MoveFloatMenu,
    VIEW3D_OT_MenuController,
    VIEW3D_OT_FlipTools,
    VIEW3D_OT_NextPivotMode,
    VIEW3D_OT_BrushResize,
    VIEW3D_OT_BrushStrength,
    VIEW3D_OT_ToggleNPanel,
    VIEW3D_OT_ToggleFloatingMenu,
    VIEW3D_OT_ToggleTouchControls,
    VIEW3D_OT_ViewportLock,
    VIEW3D_OT_ViewportRecenter,
    VIEW3D_OT_IncreaseMultires,
    VIEW3D_OT_DecreaseMultires,
    VIEW3D_OT_DensityUp,
    VIEW3D_OT_DensityDown,
)


def register():
    from bpy.utils import register_class
    for cls in __classes__:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(__classes__):
        unregister_class(cls)
