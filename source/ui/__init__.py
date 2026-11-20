from . import gizmo_group_2d, panel


def register():
    gizmo_group_2d.register()
    panel.register()


def unregister():
    gizmo_group_2d.unregister()
    panel.unregister()
