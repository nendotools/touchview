from . import Panel, operators, ui_gizmo
from .Overlay import Overlay

ov = Overlay()


def register():
    from .touch_input import register_keymaps

    operators.register()
    ui_gizmo.register()
    ov.drawUI()

    Panel.register()
    register_keymaps()


def unregister():
    from .touch_input import unregister_keymaps

    Panel.unregister()
    unregister_keymaps()

    ov.clear_overlays()
    ui_gizmo.unregister()
    operators.unregister()
