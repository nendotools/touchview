import bpy
from mathutils import Vector


def panel(type) -> tuple:
    """Panel in the region.

    type (enum in ['WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS',
                   'TOOL_PROPS', 'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE',
                   'FOOTER', 'TOOL_HEADER', 'XR']) - Type of the region.
    return (tuple) - Dimension of the region.
    """
    width = 0
    height = 0
    alignment = "NONE"
    for region in bpy.context.area.regions:
        if region.type == type:
            width = region.width
            height = region.height
            alignment = region.alignment
    return (width, height, alignment)


def ui_scale() -> float:
    return bpy.context.preferences.system.ui_scale


# region types that may overlap the viewport and should be avoided by gizmos
overlay_regions = {"TOOLS", "UI", "HEADER", "TOOL_HEADER", "ASSET_SHELF", "ASSET_SHELF_HEADER"}


# returns a tuple (bottom-left, top-right)
# safe area in the current region for UI elements, relative to the region.
# Works per-region, so each quad view region gets its own safe area.
def safe_area_3d(padding: float = 28) -> tuple[Vector, Vector]:
    region = bpy.context.region
    buffer = padding * ui_scale()
    left, bottom = region.x, region.y
    right, top = region.x + region.width, region.y + region.height

    for overlay in bpy.context.area.regions:
        if overlay.type not in overlay_regions or overlay.width <= 1 or overlay.height <= 1:
            continue
        # skip panels that don't touch this region (e.g. other quad views)
        if (
            overlay.x >= right
            or overlay.x + overlay.width <= left
            or overlay.y >= top
            or overlay.y + overlay.height <= bottom
        ):
            continue
        if overlay.alignment == "LEFT":
            left = max(left, overlay.x + overlay.width)
        elif overlay.alignment == "RIGHT":
            right = min(right, overlay.x)
        elif overlay.alignment == "BOTTOM":
            bottom = max(bottom, overlay.y + overlay.height)
        elif overlay.alignment == "TOP":
            top = min(top, overlay.y)

    return (
        Vector((left - region.x + buffer, bottom - region.y + buffer)),
        Vector((right - region.x - buffer, top - region.y - buffer)),
    )


# approximate height of Blender's navigation gizmo column in the top-right corner
def navigation_gizmo_height() -> float:
    space = bpy.context.space_data
    if not getattr(space, "show_gizmo", False) or not getattr(space, "show_gizmo_navigate", False):
        return 0.0
    view = bpy.context.preferences.view
    axis = {"GIZMO": view.gizmo_size_navigate_v3d, "MINIMAL": 40}.get(view.mini_axis_type, 0)
    buttons = 4 * 40  # zoom, pan, camera, perspective toggle
    return (axis + buttons) * ui_scale()
