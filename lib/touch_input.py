import bpy

from .constants import (DCLICK, LMOUSE, PRESS, RMOUSE, flat_modes,
                        top_level_names)

default_keymaps = []
modified_keymaps = []


# added timer to ensure Blender keyconfig is fully populated before running
def register_keymaps():
    bpy.app.timers.register(assign_keymaps, first_interval=0.2)


# two main goals: preserve action from MOUSE to PEN,
# add viewport control to MOUSE
def assign_keymaps():
    wm = bpy.context.window_manager

    # add global default action
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new(
        'nendo.toggle_touch',
        type='T',
        value=PRESS,
        alt=True
    )
    modified_keymaps.append((km, kmi))

    # make menus draggable
    km = wm.keyconfigs.addon.keymaps.new(name='View2D Buttons List',
                                         space_type='EMPTY')
    kmi = km.keymap_items.new('view2d.pan', LMOUSE, PRESS)
    modified_keymaps.append((km, kmi))

    # add LEFT MOUSE ACTION for view3d.view_ops
    for kmap in wm.keyconfigs['Blender'].keymaps:
        km = wm.keyconfigs.addon.keymaps.new(name=kmap.name,
                                             space_type=kmap.space_type,
                                             region_type=kmap.region_type)
        if kmap.name in top_level_names:
            if kmap.name in flat_modes:
                main_action = "nendo.view_ops_2d"
            else:
                main_action = "nendo.view_ops_3d"
            kmi = km.keymap_items.new(main_action, LMOUSE, PRESS)
            modified_keymaps.append((km, kmi))

            kmi = km.keymap_items.new('nendo.dt_action', LMOUSE, DCLICK)
            modified_keymaps.append((km, kmi))

            kmi = km.keymap_items.new('nendo.rc_action', RMOUSE, PRESS)
            modified_keymaps.append((km, kmi))


# unset MOUSE viewport control, reset PEN to MOUSE input
def unregister_keymaps():
    for km, kmi in modified_keymaps:
        km.keymap_items.remove(kmi)

    for kmi, state in default_keymaps:
        kmi.active = state
    modified_keymaps.clear()
    default_keymaps.clear()
