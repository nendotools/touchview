import bpy

from mathutils import Vector

from ... import __package__ as package  # relative import from the root directory


def preferences() -> dict:
    """Get the addon preferences."""
    return bpy.context.preferences.addons[package].preferences  # type: ignore


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


# used in text drawing
def dpi() -> int:
    return bpy.context.preferences.system.dpi


# returns a tuple (bottom-left, top-right)
# safe area in viewport for UI elements
def safe_area_3d(padding: float = 28) -> tuple[Vector, Vector]:
    buffer = padding * ui_scale()
    min = Vector((buffer, buffer))
    max = Vector(
        (
            bpy.context.area.width - buffer,
            bpy.context.area.height - buffer,
        )
    )

    if panel("TOOLS")[2] == "LEFT":
        min.x += panel("TOOLS")[0]
    elif panel("TOOLS")[2] == "RIGHT":
        max.x -= panel("TOOLS")[0]

    if panel("UI")[2] == "LEFT":
        min.x += panel("UI")[0]
    elif panel("UI")[2] == "RIGHT":
        max.x -= panel("UI")[0]

    if panel("HEADER")[2] == "BOTTOM":
        min.y += panel("HEADER")[1]
    elif panel("HEADER")[2] == "TOP":
        max.y -= panel("HEADER")[1]

    if panel("TOOL_HEADER")[2] == "BOTTOM":
        min.y += panel("TOOL_HEADER")[1]
    elif panel("TOOL_HEADER")[2] == "TOP":
        max.y -= panel("TOOL_HEADER")[1]
    return (min, max)
