###
# Gizmo structure update
#
# Refactor the gizmo structure to be more modular and easier to maintain.
# Gizmo context (UI, space, etc), state (2-mode, 3-mode, etc),
# layout (vertical, horizontal, etc)
# to be managed through inheritance.
###
from .gizmo_group_2d import GIZMO_GT_ViewportGizmoGroup

__classes__ = (GIZMO_GT_ViewportGizmoGroup)


def register():
    from bpy.utils import register_class
    register_class(GIZMO_GT_ViewportGizmoGroup)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(GIZMO_GT_ViewportGizmoGroup)
