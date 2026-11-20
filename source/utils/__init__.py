from . import keymaps, prefs
from .overlay import Overlay

ov = Overlay()


def register():
    keymaps.register()
    prefs.register()
    ov.draw_ui()


def unregister():
    ov.clear_overlays()
    prefs.unregister()
    keymaps.unregister()
