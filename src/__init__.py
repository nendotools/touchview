import bpy
from . Overlay import Overlay
from . Operators import TouchInput, FlipTools, ToggleNPanel
from . Panel import NendoViewport
from . Gizmos import ViewportGizmoGroup, ViewportRecenter, ViewportLock, gizmo_toggle

__classes__ = (
    TouchInput,
    FlipTools,
    ToggleNPanel,
    NendoViewport,
    ViewportLock,
    ViewportRecenter,
    ViewportGizmoGroup
)

ov = Overlay()

def register():
    from bpy.utils import register_class
    from . touch_input import register_keymaps
    for cls in __classes__:
        register_class(cls)

    bpy.types.VIEW3D_PT_gizmo_display.append(gizmo_toggle)
    ov.drawUI()

    register_keymaps()

def unregister():
    from bpy.utils import unregister_class
    from . touch_input import unregister_keymaps

    ov.clear_overlays()
    bpy.types.VIEW3D_PT_gizmo_display.remove(gizmo_toggle)
    for cls in __classes__:
        unregister_class(cls)

    unregister_keymaps()