import bpy

TWEAK = 'TWEAK'
MOUSE = 'MOUSE'
PEN = 'PEN'
MMOUSE = 'MIDDLEMOUSE'
LMOUSE = 'LEFTMOUSE'
PRESS = 'PRESS'
DCLICK = 'DOUBLE_CLICK'

flat_modes = [ "Node Editor", "Image", "Image Paint", "UV Editor", "View2D" ]
top_level_names = ( "Node Editor", "UV Editor", "Image Editor", "Image Paint", "3D View", "Image", "View2D", "Grease Pencil" )
modes = ( "Object Mode", "Mesh", "Sculpt", "Vertex Paint", "Weight Paint", "Image Paint" )
g_modes = (
  'Grease Pencil Stroke Paint (Draw brush)', 'Grease Pencil Stroke Paint (Fill)', 'Grease Pencil Stroke Paint (Erase)',
  'Grease Pencil Stroke Paint (Tint)'
)

default_keymaps = []
modified_keymaps = []


# added timer to ensure Blender keyconfig is fully populated before running
def register_keymaps():
  bpy.app.timers.register( assign_keymaps, first_interval=0.2 )


# toggle active addon_keymaps and addon_tweaks
def toggle_keymaps( state: bool = True ):
  for _, kmi in modified_keymaps:
    if kmi.type == LMOUSE and kmi.value != DCLICK:
      kmi.active = state
    elif kmi.type == MMOUSE and bpy.context.preferences.addons[ 'touchview' ].preferences.include_mmb:
      kmi.active = state
  for kmi, original in default_keymaps:
    if not state:
      kmi.active = original
    else:
      kmi.active = False


# two main goals: preserve action from MOUSE to PEN, add viewport control to MOUSE
def assign_keymaps():
  wm = bpy.context.window_manager

  # add global default action
  km = wm.keyconfigs.addon.keymaps.new( name="3D View", space_type='VIEW_3D' )
  kmi = km.keymap_items.new( 'view3d.toggle_touch', type='T', value=PRESS, alt=True )
  modified_keymaps.append( ( km, kmi ) )

  # make menus draggable
  km = wm.keyconfigs.addon.keymaps.new( name='View2D Buttons List', space_type='EMPTY' )
  kmi = km.keymap_items.new( 'view2d.pan', LMOUSE, PRESS )
  modified_keymaps.append( ( km, kmi ) )

  # add LEFT MOUSE ACTION for view3d.view_ops
  for kmap in wm.keyconfigs[ 'Blender' ].keymaps:
    km = wm.keyconfigs.addon.keymaps.new( name=kmap.name, space_type=kmap.space_type, region_type=kmap.region_type )
    if kmap.name in top_level_names:
      main_action = "view2d.view_ops" if kmap.name in flat_modes else "view3d.view_ops"
      kmi = km.keymap_items.new( main_action, MMOUSE, PRESS )
      modified_keymaps.append( ( km, kmi ) )

      kmi = km.keymap_items.new( main_action, LMOUSE, PRESS )
      modified_keymaps.append( ( km, kmi ) )

      kmi = km.keymap_items.new( 'view3d.dt_action', LMOUSE, DCLICK )
      modified_keymaps.append( ( km, kmi ) )


# unset MOUSE viewport control, reset PEN to MOUSE input
def unregister_keymaps():
  for km, kmi in modified_keymaps:
    km.keymap_items.remove( kmi )

  for kmi, state in default_keymaps:
    kmi.active = state
  modified_keymaps.clear()
  default_keymaps.clear()
