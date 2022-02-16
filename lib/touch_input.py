import bpy

addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager   
    km = wm.keyconfigs.addon.keymaps.new(name='', space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'MIDDLEMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi)) 

    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt', space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'PEN', 'PRESS')
    kmi.properties.mode = "NORMAL"
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'ERASER', 'PRESS')
    kmi.properties.mode = "INVERT"
    addon_keymaps.append((km, kmi))

    # bpy.context.window_manager.keyconfigs.active.keymaps.find('View2D Buttons List')
    km = wm.keyconfigs.addon.keymaps.new(name='View2D Buttons List', space_type='EMPTY')
    kmi = km.keymap_items.new('view2d.pan', 'LEFTMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
