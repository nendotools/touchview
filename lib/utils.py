import bpy
from bpy.types import Context
from mathutils import Vector

# returns dpi scale factor for UI
def dpi_factor() -> float:
  systemPreferences = bpy.context.preferences.system
  retinaFactor = getattr( systemPreferences, "pixel_size", 1 )
  return int( systemPreferences.dpi * retinaFactor ) / 72

# iterates over UI regions in current context
def panel( type ) -> tuple:
  ''' Panel in the region.
    
    type (enum in ['WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS', 'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE', 'FOOTER', 'TOOL_HEADER', 'XR']) - Type of the region.
    return (tuple) - Dimension of the region.
    '''
  width = 0
  height = 0
  alignment = 'NONE'
  for region in bpy.context.area.regions:
    if region.type == type:
      width = region.width
      height = region.height
      alignment = region.alignment
  return ( width, height, alignment )

# returns a tuple (bottom-left, top-right) safe area in viewport for UI elements
def buildSafeArea() -> tuple[Vector, Vector]:
    buffer = 30  * dpi_factor()
    min = Vector((buffer, buffer))
    max = Vector((bpy.context.region.width-buffer, bpy.context.region.height-buffer))

    if (panel( 'TOOLS' )[2] == 'LEFT'):
        min.x += 22.0 * dpi_factor() + panel('TOOLS')[0]
    if (panel( 'TOOLS' )[2] == 'RIGHT'):
        max.x -= 22.0 * dpi_factor() + panel('TOOLS')[0]

    if (panel( 'UI' )[2] == 'LEFT'):
        min.x += 22.0 * dpi_factor() + panel('UI')[0]
    if (panel( 'UI' )[2] == 'RIGHT'):
        max.x -= 22.0 * dpi_factor() + panel('UI')[0]

    if (panel( 'HEADER' )[2] == 'BOTTOM'):
        min.y = panel('HEADER')[1]
    if (panel( 'HEADER' )[2] == 'TOP'):
        max.y -= panel('HEADER')[1]

    if (panel( 'TOOL_HEADER' )[2] == 'BOTTOM'):
        min.y = panel('TOOL_HEADER')[1]
    if (panel( 'TOOL_HEADER' )[2] == 'TOP'):
        max.y -= panel('TOOL_HEADER')[1]
    return (min, max)

