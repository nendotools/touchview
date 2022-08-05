import bpy
from math import pi, radians, sin, cos
from mathutils import Vector
from bpy.types import Context, GizmoGroup
from .gizmo_2d import GizmoSet 
from .gizmo_config import *

def dpi_factor() -> float:
  systemPreferences = bpy.context.preferences.system
  retinaFactor = getattr( systemPreferences, "pixel_size", 1 )
  return int( systemPreferences.dpi * retinaFactor ) / 72

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

configs = [
  undoConfig,
  redoConfig,
  snapViewConfig,
  nPanelConfig,
  voxelSizeConfig,
  voxelRemeshConfig,
  subdivConfig,
  unsubdivConfig
]

###
# GizmoGroup
#  - hold reference to available Gizmos
#  - generate new Gizmos
#  - position Gizmos during draw_@prepare()
#
# Gizmo 
#  - hold Icon (cannot change)
#  - set color
#  - set visible
# 
# 2DGizmo (Custom Gizmo definition)
#  - holds reference to Gizmos for related action
#  - position applied to references
#  - hold state to determine what icons,actions to provide
#  - applies color and visibility based on settings
# 
###

class GIZMO_GT_ViewportGizmoGroup( GizmoGroup ):
  bl_idname = "GIZMO_GT_touch_tools"
  bl_label = "Fast access tools for touch viewport"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'WINDOW'
  bl_options = { 'PERSISTENT', 'SCALE' }

  def __getSettings(self):
    return bpy.context.preferences.addons[ 'touchview' ].preferences

  # set up gizmo collection
  def setup( self, _: Context ):
    self.gizmo_2d_sets = []
    settings = self.__getSettings()
    self.spacing = settings.menu_spacing
    for conf in configs:
      if conf['type'] == "default":
        gizmo = GizmoSet()
        gizmo.setup(self, conf)
        self.gizmo_2d_sets.append(gizmo)

  def draw_prepare( self, context: Context):
    settings = self.__getSettings()
    self.__updateOrigin(context)
    visible_gizmos = []
    for gizmo in self.gizmo_2d_sets:
      gizmo.draw_prepare()
      if gizmo.visible:
        visible_gizmos.append(gizmo)

    # calculate minimum radius to prevent overlapping buttons
    min_spacing = (len(visible_gizmos) * 30 * dpi_factor()) / (2 * pi)
    spacing = max( settings.menu_spacing * dpi_factor(), min_spacing )

    # reposition Gizmos to origin
    for i, gizmo in enumerate(visible_gizmos):
      step = i / len(visible_gizmos)
      offset = Vector((
        sin(radians(step * 360)) * spacing,
        cos(radians(step * 360)) * spacing,
        0.0
      ))
      self.__move_gizmo(gizmo, self.origin + offset)

  def __updateOrigin(self, context: Context):
    safe_area = self.__buildFence(context)
    settings = self.__getSettings()

    # distance across viewport between menus
    span = Vector((
        safe_area[1].x - safe_area[0].x,
        safe_area[1].y - safe_area[0].y
    ))

    # apply position ratio to safe area
    self.origin = Vector((
        safe_area[0].x + span.x * settings.floating_position[0] * 0.01,
        safe_area[0].y + span.y * settings.floating_position[1] * 0.01,
        0.0
    ))

  def __buildFence(self, context: Context) -> tuple[Vector, Vector]:
    min = Vector((0.0,0.0))
    max = Vector((context.region.width, context.region.height))

    if (panel( 'TOOLS' )[2] == 'LEFT'):
      min.x += 22.0 * dpi_factor() + panel('TOOLS')[0]
    if (panel( 'TOOLS' )[2] == 'RIGHT'):
      max.x -= 22.0 * dpi_factor() + panel('TOOLS')[0]

    if (panel( 'UI' )[2] == 'LEFT'):
      min.x += 22.0 * dpi_factor() + panel('UI')[0]
    if (panel( 'UI' )[2] == 'RIGHT'):
      max.x -= 22.0 * dpi_factor() + panel('UI')[0]

    if (panel( 'HEADER' )[2] == 'BOTTOM'):
      min.y = 22.0 * dpi_factor() + panel('HEADER')[1]
    if (panel( 'HEADER' )[2] == 'TOP'):
      max.y -= 22.0 * dpi_factor() + panel('HEADER')[1]

    if (panel( 'TOOL_HEADER' )[2] == 'BOTTOM'):
      min.y = 22.0 * dpi_factor() + panel('TOOL_HEADER')[1]
    if (panel( 'TOOL_HEADER' )[2] == 'TOP'):
      max.y -= 22.0 * dpi_factor() + panel('TOOL_HEADER')[1]
    return (min, max)

  def __move_gizmo(self, gizmo: GizmoSet, position: Vector):
    gizmo.move(position)

