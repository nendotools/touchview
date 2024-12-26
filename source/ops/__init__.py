# flake8: noqa
from . import actions, gizmo, touch


def register():
    actions.register()
    touch.register()
    gizmo.register()


def unregister():
    actions.unregister()
    touch.unregister()
    gizmo.unregister()
