import bpy

modes = ("Object Mode", "Mesh", "Sculpt", "Vertex Paint", "Weight Paint", "Image Paint")

addon_keymaps = []
addon_tweaks = []

# added timer to ensure Blender keyconfig is fully populated before running
def register_keymaps():
    bpy.app.timers.register(assign_keymaps, first_interval=0.2)

# two main goals: preserve action from MOUSE to PEN, add viewport control to MOUSE
def assign_keymaps():
    wm = bpy.context.window_manager   

# add global default action
    km = wm.keyconfigs.addon.keymaps.new(name="", space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'MIDDLEMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi)) 

    kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi))

# add LEFT MOUSE ACTION for view3d.view_ops
    for kmap in wm.keyconfigs['Blender'].keymaps:
        # isolate modes where we can use pen and mouse for different actions
        if "3D View" in kmap.name or kmap.name in modes:
            flipped = False
            commands = []
            for item in kmap.keymap_items:
                if item.map_type in ("MOUSE","TWEAK") and item.type in ("LEFTMOUSE", "EVT_TWEAK_L") and not any((item.oskey, item.ctrl, item.alt, item.shift)):
                    flipped = True
                    addon_tweaks.append((item, item.active))
                    item.active = False
                    commands.append(item.idname)

            # if we flipped a mouse to pen action, add mouse control
            if flipped or kmap.name in modes:
                km = wm.keyconfigs.addon.keymaps.new(name=kmap.name, space_type=kmap.space_type)
                kmi = km.keymap_items.new('view3d.view_ops', 'MIDDLEMOUSE', 'PRESS')
                addon_keymaps.append((km, kmi)) 

                kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'PRESS')
                addon_keymaps.append((km, kmi))
                
                kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'DOUBLE_CLICK')
                addon_keymaps.append((km, kmi)) 
                
                # reassign default action to PEN
                if len(commands) == 0:
                    commands.append("view3d.select")
                    continue
                kmi = km.keymap_items.new(commands[0], 'PEN', 'PRESS')
                addon_keymaps.append((km, kmi)) 
                
                kmi = km.keymap_items.new(commands[0], 'ERASER', 'PRESS')
                addon_keymaps.append((km, kmi)) 

    # make menus draggable
    km = wm.keyconfigs.addon.keymaps.new(name='View2D Buttons List', space_type='EMPTY')
    kmi = km.keymap_items.new('view2d.pan', 'LEFTMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi))

# unset MOUSE viewport control, reset PEN to MOUSE input
def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    for kmi, state in addon_tweaks:
        kmi.active = state
    addon_keymaps.clear()
    addon_tweaks.clear()
