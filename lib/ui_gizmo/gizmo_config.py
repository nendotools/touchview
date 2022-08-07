import bpy
from ..items import pivot_items, pivot_icon_items
###
#  Config Standard
#  ( TYPE  BINDING  COMMAND  ICON )
#  @TYPE    - button type to instance (enum, bool, simple/default)
#  @BINDING - used to determine context and visibility 
#  @COMMAND - operator to call when activated
#  @ICON    - icon to show on Gizmo
###

# Simple 2D Gizmo
controllerConfig = {
  "type": "default",
  "binding": {
    "location": "",
    "name": "menu_controller"
  },
  "command": "view3d.controller",
  "icon": "BLANK1",
  "use_grab_cursor": True
}

floatingConfig = {
  "type": "default",
  "binding": {
    "location": "",
    "name": "float_menu"
  },
  "command": "view3d.move_float_menu",
  "icon": "SETTINGS",
  "use_grab_cursor": True
}

undoConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "undoredo"
  },
  "has_dependent": True,
  "command": "ed.undo",
  "icon": "LOOP_BACK"
}

redoConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "undoredo"
  },
  "command": "ed.redo",
  "icon": "LOOP_FORWARDS"
}

snapViewConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "snap_view"
  },
  "command": "view3d.viewport_recenter",
  "icon": "CURSOR"
}

nPanelConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "n_panel"
  },
  "command": "view3d.toggle_n_panel",
  "icon": "EVENT_N"
}

voxelSizeConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "voxel_remesh",
    "attribute": {
      "path":"active_object.modifiers.type",
      "value": "MULTIRES",
      "state":False 
    }
  },
  "command": "object.voxel_size_edit",
  "icon": "MESH_GRID"
}

voxelRemeshConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "voxel_remesh",
    "attribute": {
      "path":"active_object.modifiers.type",
      "value": "MULTIRES",
      "state":False 
    }
  },
  "command": "object.voxel_remesh",
  "icon": "MOD_UVPROJECT"
}

subdivConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "multires",
    "attribute": {
      "path":"active_object.modifiers.type",
      "value": "MULTIRES",
      "state": True
    }
  },
  "has_dependent": True,
  "command": "object.increment_multires",
  "icon": "TRIA_UP"
}

unsubdivConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "multires",
    "attribute": {
      "path":"active_object.modifiers.type",
      "value": "MULTIRES",
      "state": True
    }
  },
  "command": "object.decrement_multires",
  "icon": "TRIA_DOWN"
}

brushResizeConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "brush_dynamics"
  },
  "command": "view3d.brush_resize",
  "icon": "ANTIALIASED"
}

brushStrengthConfig = {
  "type": "default",
  "binding": {
    "location": "prefs",
    "name": "brush_dynamics"
  },
  "command": "view3d.brush_strength",
  "icon": "SMOOTHCURVE"
}

# Boolean 2D Gizmo
fullscreenToggleConfig = {
  "type": "boolean",
  "binding": {
    "location": "screen",
    "name": "show_fullscreen"
  }, # property location, watch-boolean
  "command": "screen.screen_full_area",
  "onIcon": "FULLSCREEN_EXIT", # on-state
  "offIcon": "FULLSCREEN_ENTER" # off-state
}

quadviewToggleConfig = {
  "type": "boolean",
  "binding": {
    "location": "space_data",
    "name": "region_quadviews"
  },
  "command": "screen.region_quadview",
  "onIcon": "IMGDISPLAY",
  "offIcon": "MESH_PLANE"
}

rotLocToggleConfig = {
  "type": "boolean",
  "binding": {
    "location": "region_data",
    "name": "lock_rotation"
  },
  "command": "view3d.viewport_lock",
  "onIcon": "LOCKED",
  "offIcon": "UNLOCKED"
}
gizmo_sets = {
# ALL includes only the modes in this list
    "ALL": { "undoredo", "show_fullscreen", "region_quadviews", "snap_view", "n_panel", "lock_rotation" },
    "SCULPT": { "pivot_mode", "voxel_remesh", "multires", "brush_dynamics" },
    "OBJECT": { "multires" },
    "EDIT_MESH": {},
    "POSE": {},
    "PAINT_TEXTURE": {},
    "PAINT_VERTEX": {},
    "PAINT_WEIGHT": {},
    "PAINT_GPENCIL": {}
}

gizmo_colors = {
    "disabled": {
        "color": [ 0.0, 0.0, 0.0 ],
        "color_highlight": [ 0.0, 0.0, 0.0 ],
        "alpha": 0.3,
        "alpha_highlight": 0.3
    },
    "active": {
        "color": [ 0.0, 0.0, 0.0 ],
        "alpha": 0.5,
        "color_highlight": [ 0.5, 0.5, 0.5 ],
        "alpha_highlight": 0.5
    },
    "error": {
        "color": [ 0.3, 0.0, 0.0 ],
        "alpha": 0.15,
        "color_highlight": [ 1.0, 0.2, 0.2 ],
        "alpha_highlight": 0.5
    },
    "warn": {
        "color": [ 0.35, 0.3, 0.14 ],
        "alpha": 0.15,
        "color_highlight": [ 0.8, 0.7, 0.3 ],
        "alpha_highlight": 0.3
    }
}
# Enum 2D Gizmo
pivotModeConfig = [
  (bpy.context.preferences.addons["touchview"].preferences, "pivot_mode"), # property location, watch-enum
  ("view3d.step_pivot_mode", pivot_items, pivot_icon_items)                # enum stepper, enum mode, enum icon
]


#  Boolean/parameter binding handled the same way.
#  Single config per button, paired after with binding config
# 
# - Generate Gizmos
# - set on state, off state
# 
# Enums need a different solution: list binding
# - I'm not sure yet... 
