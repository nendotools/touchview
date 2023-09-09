# INPUT EVENTS
TWEAK = 'TWEAK'
MOUSE = 'MOUSE'
PEN = 'PEN'
MMOUSE = 'MIDDLEMOUSE'
LMOUSE = 'LEFTMOUSE'
RMOUSE = 'RIGHTMOUSE'
PRESS = 'PRESS'
DCLICK = 'DOUBLE_CLICK'

# OPERATOR RESPONSES
FINISHED = {'FINISHED'}
MODAL = {'RUNNING_MODAL'}
CANCEL = {'CANCELLED'}
PASSTHROUGH = {'PASS_THROUGH'}

# DICTIONARIES
flat_modes = ["Node Editor", "Image", "Image Paint", "UV Editor", "View2D"]
top_level_names = ("Node Editor", "UV Editor", "Image Editor", "Image Paint",
                   "3D View", "Image", "View2D", "Grease Pencil")

input_mode_items = [('ORBIT', 'rotate', 'Rotate the viewport'),
                    ('PAN', 'pan', 'Move the viewport'),
                    ('DOLLY', 'zoom', 'Zoom in/out the viewport')]

position_items = [
    ('TOP', 'top', 'Set Gizmo position to top of viewport'),
    ('RIGHT', 'right', 'Set Gizmo position to right of viewport'),
    ('BOTTOM', 'bottom', 'Set Gizmo position to bottom of viewport'),
    ('LEFT', 'left', 'Set Gizmo position to left of viewport')
]

pivot_items = [
    ("SURFACE", "Surface",
     "Sets the pivot position to the surface under the cursor."),
    ("ACTIVE", "Active Vertex",
     "Sets the pivot position to the active vertex position."),
    ("UNMASKED", "Unmasked",
     """
        Sets the pivot position to the average position of the unmasked
        vertices.
     """
     ), ("ORIGIN", "Origin", "Sets the pivot to the origin of the sculpt."),
    ("BORDER", "Mask Border",
     "Sets the pivot position to the center of the border of the mask.")
]

pivot_icon_items = [("BORDER", "PIVOT_BOUNDBOX"), ("ORIGIN", "PIVOT_CURSOR"),
                    ("UNMASKED", "CLIPUV_HLT"), ("ACTIVE", "PIVOT_ACTIVE"),
                    ("SURFACE", "PIVOT_MEDIAN")]

brush_modes = ['SCULPT','PAINT_VERTEX','PAINT_WEIGHT','PAINT_TEXTURE']
edit_modes = [("OBJECT", "Object Mode", ""),
              ("EDIT_MESH", "Edit Mode", ""),
              ("SCULPT", "Sculpt Mode", ""),
              ("PAINT_VERTEX", "Vertex Paint Mode", ""),
              ("PAINT_WEIGHT", "Weight Paint Mode", ""),
              ("PAINT_TEXTURE", "Texture Paint Mode", ""),
              ("PAINT_GPENCIL", "2D Paint Mode", "")]

menu_defaults = {
    "OBJECT": ("VIEW3D_MT_add", "object.shade_smooth", "", "", "", ""),
    "EDIT_MESH": ("mesh.loop_multi_select", "", "", "", "", ""),
    "SCULPT": ("object.quadriflow_remesh", "", "", "", "", ""),
    "PAINT_VERTEX": ("", "", "", "", "", ""),
    "PAINT_WEIGHT": ("", "", "", "", "", ""),
    "PAINT_TEXTURE": ("", "", "", "", "", "")
}

double_click_items = [("object.transfer_mode", "Transfer Mode", ""),
                      ("nendo.toggle_touch", "Toggle Touch View", ""),
                      ("view3d.localview", "Toggle Local View", ""),
                      ("wm.window_fullscreen_toggle", "Toggle Full Screen", "")]

menu_style_items = [("fixed.bar", "Fixed Bar", ""),
                    ("float.radial", "Floating Radial", "")]

menu_orientation_items = [("HORIZONTAL", "Horizontal", ""),
                          ("VERTICAL", "Vertical", "")]

control_gizmo_items = [("none", "", "disable_gizmo"),
                       ("translate", "show_gizmo_object_translate", ""),
                       ("rotate", "show_gizmo_object_rotate", ""),
                       ("scale", "show_gizmo_object_scale", "")]

gizmo_sets = {
    # ALL includes only the modes in this list
    "ALL": {
        "undoredo", "show_fullscreen", "region_quadviews",
        "snap_view", "n_panel", "lock_rotation"
    },
    "SCULPT": {
        "control_gizmo", "pivot_mode", "voxel_remesh", "multires",
        "brush_dynamics"
    },
    "OBJECT": {"control_gizmo", "multires"},
    "EDIT_MESH": {"control_gizmo"},
    "POSE": {},
    "PAINT_TEXTURE": {"brush_dynamics"},
    "PAINT_VERTEX": {"brush_dynamics"},
    "PAINT_WEIGHT": {"brush_dynamics"},
    "WEIGHT_GPENCIL": {"brush_dynamics"},
    "VERTEX_GPENCIL": {"brush_dynamics"},
    "SCULPT_GPENCIL": {"brush_dynamics"},
    "PAINT_GPENCIL": {"brush_dynamics"},
    "EDIT_GPENCIL": {"brush_dynamics"}
}
