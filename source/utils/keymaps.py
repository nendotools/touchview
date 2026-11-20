import bpy

from .constants import DCLICK, LMOUSE, PRESS, RMOUSE, flat_modes, top_level_names

default_keymaps = []
modified_keymaps = []

_retry_attempts = 0
_MAX_RETRY_ATTEMPTS = 20  # ~5 seconds at 0.25s intervals


# added timer to ensure Blender keyconfig is fully populated before running
def register():
    global _retry_attempts
    _retry_attempts = 0
    if not assign_keymaps():
        bpy.app.timers.register(_retry_assign, first_interval=0.25)


def _retry_assign():
    global _retry_attempts
    _retry_attempts += 1
    if assign_keymaps() or _retry_attempts >= _MAX_RETRY_ATTEMPTS:
        return None
    return 0.25


# two main goals: preserve action from MOUSE to PEN,
# add viewport control to MOUSE
def assign_keymaps():
    """Assign the add-on keymaps.

    Returns False when the Blender keyconfig is not ready yet, so the caller
    can retry. Returns True when the keymaps are in place (also a no-op when
    they were already assigned).
    """
    if modified_keymaps:
        return True

    wm = bpy.context.window_manager
    try:
        blender_keymaps = wm.keyconfigs["Blender"].keymaps
    except (KeyError, AttributeError):
        return False

    # add global default action
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new("touchview.toggle_touch", type="T", value=PRESS, alt=True)
    modified_keymaps.append((km, kmi))

    # make menus draggable
    km = wm.keyconfigs.addon.keymaps.new(name="View2D Buttons List", space_type="EMPTY")
    kmi = km.keymap_items.new("view2d.pan", LMOUSE, PRESS)
    modified_keymaps.append((km, kmi))

    # add LEFT MOUSE ACTION for touchview.view_ops
    for kmap in blender_keymaps:
        km = wm.keyconfigs.addon.keymaps.new(name=kmap.name, space_type=kmap.space_type, region_type=kmap.region_type)
        if kmap.name in top_level_names:
            if kmap.name in flat_modes:
                main_action = "touchview.view_ops_2d"
            else:
                main_action = "touchview.view_ops_3d"
            kmi = km.keymap_items.new(main_action, LMOUSE, PRESS)
            modified_keymaps.append((km, kmi))

            kmi = km.keymap_items.new("touchview.dt_action", LMOUSE, DCLICK)
            modified_keymaps.append((km, kmi))

            kmi = km.keymap_items.new("touchview.rc_action", RMOUSE, PRESS)
            modified_keymaps.append((km, kmi))

    return True


# unset MOUSE viewport control, reset PEN to MOUSE input
def unregister():
    if bpy.app.timers.is_registered(_retry_assign):
        bpy.app.timers.unregister(_retry_assign)

    for km, kmi in modified_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (ReferenceError, RuntimeError):
            pass

    for kmi, state in default_keymaps:
        kmi.active = state
    modified_keymaps.clear()
    default_keymaps.clear()
