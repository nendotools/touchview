import bpy
from . Overlay import Overlay
from . Operators import VIEW3D_OT_DecreaseMultires, VIEW3D_OT_IncreaseMultires, VIEW3D_OT_ToggleTouchControls, VIEW3D_OT_TouchInput, VIEW3D_OT_ToggleFloatingMenu, VIEW3D_OT_MoveFloatMenu, VIEW3D_OT_NextPivotMode, VIEW3D_OT_FlipTools, VIEW3D_OT_ToggleNPanel, VIEW3D_OT_ViewportRecenter, VIEW3D_OT_ViewportLock
from . Panel import VIEW3D_PT_NendoViewport, PIE_MT_Floating_Menu
from . Gizmos import GIZMO_GT_FloatingGizmoGroup, GIZMO_GT_ViewportGizmoGroup, touch_gizmo_display

__classes__ = (
    VIEW3D_OT_TouchInput,
    VIEW3D_OT_FlipTools,
    VIEW3D_OT_NextPivotMode,
    VIEW3D_OT_ToggleNPanel,
    VIEW3D_OT_ToggleFloatingMenu,
    VIEW3D_OT_ToggleTouchControls,
    VIEW3D_PT_NendoViewport,
    VIEW3D_OT_ViewportLock,
    VIEW3D_OT_ViewportRecenter,
    VIEW3D_OT_MoveFloatMenu,
    VIEW3D_OT_IncreaseMultires,
    VIEW3D_OT_DecreaseMultires,
    PIE_MT_Floating_Menu,
    GIZMO_GT_FloatingGizmoGroup,
    GIZMO_GT_ViewportGizmoGroup
)
ov = Overlay()


def register():
    from bpy.utils import register_class
    from . touch_input import register_keymaps
    for cls in __classes__:
        register_class(cls)

    bpy.types.VIEW3D_PT_gizmo_display.append(touch_gizmo_display)
    ov.drawUI()

    register_keymaps()

def unregister():
    from bpy.utils import unregister_class
    from . touch_input import unregister_keymaps

    ov.clear_overlays()
    bpy.types.VIEW3D_PT_gizmo_display.remove(touch_gizmo_display)
    for cls in __classes__:
        unregister_class(cls)

    unregister_keymaps()
