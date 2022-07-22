import bpy
from items import pivot_items, pivot_icon_items
###
#  Config Standard
#  ( NAME  COMMAND  ICON )
#  @NAME    - used to group icons for hide/show UI Toggle
#  @COMMAND - operator to call when activated
#  @ICON    - icon to show on Gizmo
#  @PROPS   - used to call menu when using wm.call_pie_menu
###

# Simple 2D Gizmo
undoConfig = {
  "binding": {
    "location": "prefs",
    "name": "undoredo"
  },
  "command": "ed.undo",
  "icon": "LOOP_BACK"
}

redoConfig = {
  "binding": {
    "location": "prefs",
    "name": "undoredo"
  },
  "command": "ed.redo",
  "icon": "LOOP_FORWARDS"
}

snapViewConfig = {
  "binding": {
    "location": "prefs",
    "name": "snap_view"
  },
  "command": "view3d.viewport_recenter",
  "icon": "CURSOR"
}

nPanelConfig = {
  "binding": {
    "location": "prefs",
    "name": "n_panel"
  },
  "command": "view3d.toggle_n_panel",
  "icon": "EVENT_N"
}


# Boolean 2D Gizmo
fullscreenToggleConfig = {
  "binding": {
    "location": "screen",
    "name": "show_fullscreen"
  }, # property location, watch-boolean
  "command": "screen.screen_full_area",
  "onIcon": "FULLSCREEN_EXIT", # on-state
  "offIcon": "FULLSCREEN_ENTER" # off-state
}
quadviewToggleConfig = {
  "binding": {
    "location": "space_data",
    "name": "region_quadviews"
  },
  "command": "screen.region_quadview",
  "onIcon": "IMGDISPLAY",
  "offIcon": "MESH_PLANE"
}

rotLocToggleConfig = {
  "binding": {
    "location": "region_data",
    "name": "lock_rotation"
  },
  "command": "view3d.viewport_lock",
  "onIcon": "LOCKED",
  "offIcon": "UNLOCKED"
}

# Enum 2D Gizmo
pivotModeConfig = [
  (bpy.context.preferences.addons["touchview"].preferences, "pivot_mode"), # property location, watch-enum
  ("view3d.step_pivot_mode", pivot_items, pivot_icon_items)                # enum stepper, enum mode, enum icon
]



# binding used to group for hide-show, but these gizmos are primitives
# binding toggles between the set depending on a modifier being present
voxelSizeConfig   = ("voxel_remesh", "object.voxel_size_edit", "MESH_GRID")
voxelRemeshConfig = ("voxel_remesh", "object.voxel_remesh", "MOD_UVPROJECT")

subdivConfig   = ("multires", "object.increment_multires", "TRIA_UP")
ubsubdivConfig = ("multires", "object.decrement_multires", "TRIA_DOWN")

bindingToggle = [
  ("active_object.modifiers.type", "MULTIRES"), # watch-property, target-value
  ("voxel_remesh", "multires")                  # groups to toggle
]


#  Boolean/parameter binding handled the same way.
#  Single config per button, paired after with binding config
# 
# - Generate Gizmos
# - set on state, off state
# 
# Enums need a different solution: list binding
# - I'm not sure yet... 
