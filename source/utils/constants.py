# INPUT EVENTS
TWEAK = "TWEAK"
MOUSE = "MOUSE"
PEN = "PEN"
MMOUSE = "MIDDLEMOUSE"
LMOUSE = "LEFTMOUSE"
RMOUSE = "RIGHTMOUSE"
PRESS = "PRESS"
DCLICK = "DOUBLE_CLICK"

# OPERATOR RESPONSES
FINISHED = {"FINISHED"}
MODAL = {"RUNNING_MODAL"}
CANCEL = {"CANCELLED"}
PASSTHROUGH = {"PASS_THROUGH"}

# DICTIONARIES
flat_modes = [
    "Node Editor",
    "Image",
    "Image Paint",
    "UV Editor",
    "View2D",
]

top_level_names = (
    "Node Editor",
    "UV Editor",
    "Image Editor",
    "Image Paint",
    "3D View",
    "Image",
    "View2D",
    "Grease Pencil",
)

input_mode_items = [
    ("ORBIT", "Rotate", "Rotate the viewport"),
    ("PAN", "Pan", "Move the viewport"),
    ("DOLLY", "Zoom", "Zoom in/out the viewport"),
]

position_items = [
    ("TOP", "Top", "Set Gizmo position to top of viewport"),
    ("RIGHT", "Right", "Set Gizmo position to right of viewport"),
    ("BOTTOM", "Bottom", "Set Gizmo position to bottom of viewport"),
    ("LEFT", "Left", "Set Gizmo position to left of viewport"),
]

pivot_items = [
    ("SURFACE", "Surface", "Sets the pivot position to the surface under the cursor."),
    (
        "ACTIVE",
        "Active Vertex",
        "Sets the pivot position to the active vertex position.",
    ),
    (
        "UNMASKED",
        "Unmasked",
        """
        Sets the pivot position to the average position of the unmasked
        vertices.
     """,
    ),
    ("ORIGIN", "Origin", "Sets the pivot to the origin of the sculpt."),
    (
        "BORDER",
        "Mask Border",
        "Sets the pivot position to the center of the border of the mask.",
    ),
]

pivot_icon_items = [
    ("BORDER", "PIVOT_BOUNDBOX"),
    ("ORIGIN", "PIVOT_CURSOR"),
    ("UNMASKED", "CLIPUV_HLT"),
    ("ACTIVE", "PIVOT_ACTIVE"),
    ("SURFACE", "PIVOT_MEDIAN"),
]

# context.mode -> tool_settings attribute holding the paint settings
paint_settings = {
    "SCULPT": "sculpt",
    "PAINT_VERTEX": "vertex_paint",
    "PAINT_WEIGHT": "weight_paint",
    "PAINT_TEXTURE": "image_paint",
    "SCULPT_CURVES": "curves_sculpt",
    "PAINT_GREASE_PENCIL": "gpencil_paint",
    "SCULPT_GREASE_PENCIL": "gpencil_sculpt_paint",
    "WEIGHT_GREASE_PENCIL": "gpencil_weight_paint",
    "VERTEX_GREASE_PENCIL": "gpencil_vertex_paint",
    # legacy grease pencil mode names
    "PAINT_GPENCIL": "gpencil_paint",
    "SCULPT_GPENCIL": "gpencil_sculpt_paint",
    "WEIGHT_GPENCIL": "gpencil_weight_paint",
    "VERTEX_GPENCIL": "gpencil_vertex_paint",
}


def paint_settings_name(mode: str) -> str | None:
    return paint_settings.get(mode)


brush_modes = list(paint_settings)

edit_modes = [
    ("OBJECT", "Object Mode", ""),
    ("EDIT_MESH", "Edit Mode", ""),
    ("SCULPT", "Sculpt Mode", ""),
    ("PAINT_VERTEX", "Vertex Paint Mode", ""),
    ("PAINT_WEIGHT", "Weight Paint Mode", ""),
    ("PAINT_TEXTURE", "Texture Paint Mode", ""),
    ("PAINT_GPENCIL", "2D Paint Mode", ""),
]

menu_defaults = {
    "OBJECT": ("VIEW3D_MT_add", "object.shade_smooth", "", "", "", ""),
    "EDIT_MESH": ("mesh.loop_multi_select", "", "", "", "", ""),
    "SCULPT": ("object.quadriflow_remesh", "", "", "", "", ""),
    "PAINT_VERTEX": ("", "", "", "", "", ""),
    "PAINT_WEIGHT": ("", "", "", "", "", ""),
    "PAINT_TEXTURE": ("", "", "", "", "", ""),
}

double_click_items = [
    ("object.transfer_mode", "Transfer Mode", ""),
    ("touchview.toggle_touch", "Toggle Touch View", ""),
    ("view3d.localview", "Toggle Local View", ""),
    ("wm.window_fullscreen_toggle", "Toggle Full Screen", ""),
]

menu_style_items = [
    ("float.radial", "Floating Radial", ""),
    ("fixed.bar", "Fixed Bar", ""),
]

menu_orientation_items = [
    ("HORIZONTAL", "Horizontal", ""),
    ("VERTICAL", "Vertical", ""),
]

control_gizmo_items = [
    ("none", "", "disable_gizmo"),
    ("translate", "show_gizmo_object_translate", ""),
    ("rotate", "show_gizmo_object_rotate", ""),
    ("scale", "show_gizmo_object_scale", ""),
]

gizmo_sets = {
    # ALL includes only the modes in this list
    "ALL": {
        "undoredo",
        "show_fullscreen",
        "region_quadviews",
        "snap_view",
        "n_panel",
        "lock_rotation",
    },
    "SCULPT": {
        "control_gizmo",
        "pivot_mode",
        "voxel_remesh",
        "multires",
        "brush_dynamics",
    },
    "OBJECT": {"control_gizmo", "multires"},
    "EDIT_MESH": {"control_gizmo"},
    "POSE": {},
    "NODE_EDITOR": {"control_gizmo"},
    "PAINT_TEXTURE": {"brush_dynamics"},
    "PAINT_VERTEX": {"brush_dynamics"},
    "PAINT_WEIGHT": {"brush_dynamics"},
    "SCULPT_CURVES": {"brush_dynamics"},
    "PAINT_GREASE_PENCIL": {"brush_dynamics"},
    "SCULPT_GREASE_PENCIL": {"brush_dynamics"},
    "WEIGHT_GREASE_PENCIL": {"brush_dynamics"},
    "VERTEX_GREASE_PENCIL": {"brush_dynamics"},
    "WEIGHT_GPENCIL": {"brush_dynamics"},
    "VERTEX_GPENCIL": {"brush_dynamics"},
    "SCULPT_GPENCIL": {"brush_dynamics"},
    "PAINT_GPENCIL": {"brush_dynamics"},
}
