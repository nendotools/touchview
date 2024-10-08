# flake8: noqa
from . import actions
from . import touch
from . import gizmo


def register():
    actions.register()
    touch.register()
    gizmo.register()


def unregister():
    actions.unregister()
    touch.unregister()
    gizmo.unregister()
