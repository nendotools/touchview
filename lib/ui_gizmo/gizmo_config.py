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
undoConfig     = ("undoredo", "ed.undo", "LOOP_BACK")
redoConfig     = ("undoredo", "ed.redo", "LOOP_FORWARDS")
snapViewConfig = ("snap_view", "view3d.viewport_recenter", "CURSOR")
nPanelConfig   = ("n_panel", "view3d.toggle_n_panel", "EVENT_N")


# Boolean 2D Gizmo
fullscreenToggleConfig = [
  ("screen", "show_fullscreen"), # property location, watch-boolean
  ("fullscreen", "screen.screen_full_area", "FULLSCREEN_EXIT"), # on-state
  ("fullscreen", "screen.screen_full_area", "FULLSCREEN_ENTER") # off-state
]
quadviewToggleConfig = [
  ("space_data", "region_quadviews"),
  ("quadview", "screen.region_quadview", "IMGDISPLAY"),
  ("quadview", "screen.region_quadview", "MESH_PLANE")
]
rotLocToggleConfig = [
  ("region_data", "lock_rotation"),
  ("rotation_lock", "view3d.viewport_lock", "LOCKED"),
  ("rotation_lock", "view3d.viewport_lock", "UNLOCKED")
]

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