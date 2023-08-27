from ..constants import pivot_icon_items

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
    "command": "nendo.move_float_menu",
    "icon": "BLANK1",
    "use_grab_cursor": True
}

floatingConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "float_menu"
    },
    "command": "nendo.move_action_menu",
    "icon": "SETTINGS",
    "use_grab_cursor": True
}

floatingToggleConfig = {
    "type": "boolean",
    "binding": {
        "location": "",
        "name": "float_toggle"
    },
    "command": "nendo.move_toggle_button",
    "onIcon": "OUTLINER_DATA_CAMERA",
    "offIcon": "GREASEPENCIL",
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

touchViewConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "is_enabled",
    },
    "command": "nendo.toggle_touch",
    "icon": "VIEW_PAN"
}

controlGizmoConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "control_gizmo",
    },
    "command": "nendo.cycle_control_gizmo",
    "icon": "ORIENTATION_LOCAL"
}

snapViewConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "snap_view"
    },
    "command": "nendo.viewport_recenter",
    "icon": "CURSOR"
}

nPanelConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "n_panel"
    },
    "command": "nendo.toggle_n_panel",
    "icon": "EVENT_N"
}

voxelSizeConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "voxel_remesh",
        "attribute": {
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": False
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
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": False
        }
    },
    "command": "object.voxel_remesh",
    "icon": "MOD_UVPROJECT"
}

voxelStepDownConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "voxel_remesh",
        "attribute": {
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": False
        }
    },
    "command": "nendo.density_down",
    "icon": "TRIA_DOWN"
}

voxelStepUpConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "voxel_remesh",
        "attribute": {
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": False
        }
    },
    "command": "nendo.density_up",
    "icon": "TRIA_UP"
}

subdivConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "multires",
        "attribute": {
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": True
        }
    },
    "has_dependent": True,
    "command": "nendo.increment_multires",
    "icon": "TRIA_UP"
}

unsubdivConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "multires",
        "attribute": {
            "path": "active_object.modifiers.type",
            "value": "MULTIRES",
            "state": True
        }
    },
    "command": "nendo.decrement_multires",
    "icon": "TRIA_DOWN"
}

brushResizeConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "brush_dynamics"
    },
    "command": "nendo.brush_resize",
    "icon": "ANTIALIASED"
}

brushStrengthConfig = {
    "type": "default",
    "binding": {
        "location": "prefs",
        "name": "brush_dynamics"
    },
    "command": "nendo.brush_strength",
    "icon": "SMOOTHCURVE"
}

# Boolean 2D Gizmo
fullscreenToggleConfig = {
    "type": "boolean",
    "binding": {
        "location": "screen",
        "name": "show_fullscreen"
    },  # property location, watch-boolean
    "command": "screen.screen_full_area",
    "onIcon": "FULLSCREEN_EXIT",  # on-state
    "offIcon": "FULLSCREEN_ENTER"  # off-state
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
    "command": "nendo.viewport_lock",
    "onIcon": "LOCKED",
    "offIcon": "UNLOCKED"
}

gizmo_colors = {
    "disabled": {
        "color": [0.0, 0.0, 0.0],
        "color_highlight": [0.0, 0.0, 0.0],
        "alpha": 0.3,
        "alpha_highlight": 0.3
    },
    "active": {
        "color": [0.0, 0.0, 0.0],
        "alpha": 0.5,
        "color_highlight": [0.5, 0.5, 0.5],
        "alpha_highlight": 0.5
    },
    "error": {
        "color": [0.3, 0.0, 0.0],
        "alpha": 0.15,
        "color_highlight": [1.0, 0.2, 0.2],
        "alpha_highlight": 0.5
    },
    "warn": {
        "color": [0.35, 0.3, 0.14],
        "alpha": 0.15,
        "color_highlight": [0.8, 0.7, 0.3],
        "alpha_highlight": 0.3
    }
}

toggle_colors = {
    "active": {
        "color": [0.1, 0.1, 0.2],
        "alpha": 0.5,
        "color_highlight": [0.15, 0.15, 0.3],
        "alpha_highlight": 0.7
    },
    "inactive": {
        "color": [0.0, 0.0, 0.0],
        "alpha": 0.5,
        "color_highlight": [0.05, 0.05, 0.05],
        "alpha_highlight": 0.7
    }
}

# Enum 2D Gizmo
#
# not implemented yet
pivotModeConfig = {
    "type": "enum",
    "binding": {
        "location": "prefs",
        "name": "pivot_mode"
    },
    "command": "",
    "icons": pivot_icon_items
}
