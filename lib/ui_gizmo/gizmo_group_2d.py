import bpy
from math import pi, radians, sin, cos
from mathutils import Vector
from bpy.types import Context, GizmoGroup
from .gizmo_2d import GizmoSet, GizmoSetBoolean 
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
  fullscreenToggleConfig,
  quadviewToggleConfig,
  rotLocToggleConfig,
  nPanelConfig,
  voxelSizeConfig,
  voxelRemeshConfig,
  subdivConfig,
  unsubdivConfig,
  brushResizeConfig,
  brushStrengthConfig
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
  def setup( self, context: Context ):
    self.gizmo_2d_sets = []
    self.__buildController(context)
    settings = self.__getSettings()
    self.spacing = settings.menu_spacing
    for conf in configs:
      if conf['type'] == "boolean":
        gizmo = GizmoSetBoolean()
        gizmo.setup(self, conf)
      else: #assume Type = Default
        gizmo = GizmoSet()
        gizmo.setup(self, conf)
      self.gizmo_2d_sets.append(gizmo)

  def __buildController(self, context:Context):
    self.controller = GizmoSet()
    self.controller.setup(self, controllerConfig)

  def draw_prepare( self, context: Context):
    self.context = context
    settings = self.__getSettings()
    self.__updateOrigin()
    self.controller.draw_prepare()
    self.__move_gizmo(self.controller, self.origin)
 
    visible_gizmos = []
    for gizmo in self.gizmo_2d_sets:
      gizmo.draw_prepare()
      if gizmo.visible:
        visible_gizmos.append(gizmo)

    if settings.menu_style == 'float.radial':
      self.__menuRadial(visible_gizmos)
    if settings.menu_style == 'float.bar':
      self.__menuBar(visible_gizmos, True)
    if settings.menu_style == 'fixed.bar':
      self.__menuBar(visible_gizmos, False)

  def __menuBar(self, visible_gizmos: list[GizmoSet], floating: bool):
    settings = self.__getSettings()
    origin = self.origin
    count = len(visible_gizmos)
    if not floating:
      safe_area = self.__buildFence()
      origin = Vector((
        (safe_area[0].x + safe_area[1].x) /2,
        (safe_area[0].y + safe_area[1].y) /2,
        0.0
      ))

      if settings.gizmo_position == 'TOP':
        origin.y = 30 * dpi_factor() + safe_area[1].y
      elif settings.gizmo_position == 'BOTTOM':
        origin.y = 30 * dpi_factor() + safe_area[0].y
      else:
        if settings.gizmo_position == 'LEFT':
            origin.x = safe_area[0].x
        elif settings.gizmo_position == 'RIGHT':
            origin.x = safe_area[1].x

    if ((settings.gizmo_position in ['TOP','BOTTOM'] and settings.menu_style == 'fixed.bar') or
      (settings.menu_orientation == 'HORIZONTAL' and settings.menu_style == 'float.bar')):
      start = origin.x - (count * (settings.menu_spacing/20) * 30 * dpi_factor()) / 2
      for i, gizmo in enumerate(visible_gizmos):
        self.__move_gizmo(
            gizmo,
            Vector((
            start + i * (settings.menu_spacing/20) * 30 * dpi_factor(),
            origin.y,
            0.0 
            ))
        )
    else:
      start = origin.y + (count * (settings.menu_spacing/20) * 30 * dpi_factor()) / 2
      for i, gizmo in enumerate(visible_gizmos):
        self.__move_gizmo(
            gizmo,
            Vector((
            origin.x,
            start - i * (settings.menu_spacing/20) * 30 * dpi_factor(),
            0.0 
            ))
        )

  def __menuRadial(self, visible_gizmos: list[GizmoSet]):
    settings = self.__getSettings()
    # calculate minimum radius to prevent overlapping buttons
    min_spacing = (len(visible_gizmos) * 30 * dpi_factor()) / (2 * pi)
    spacing = max( settings.menu_spacing * dpi_factor(), min_spacing )

    count = len(visible_gizmos)
    # reposition Gizmos to origin
    for i, gizmo in enumerate(visible_gizmos):
      if gizmo.skip_draw:
        continue

      if gizmo.has_dependent and i > count/2:
        self.__calcMove(gizmo, i+1, count, spacing)
        self.__calcMove(visible_gizmos[i+1], i, count, spacing)
        visible_gizmos[i+1].skip_draw = True
      else:
        self.__calcMove(gizmo, i, count, spacing)

  def __calcMove(self, gizmo: GizmoSet, step: int, size: int, spacing: float):
    distance = step / size 
    offset = Vector((
      sin(radians(distance * 360)),
      cos(radians(distance * 360)),
      0.0
    ))
    self.__move_gizmo(gizmo, self.origin + offset*spacing)

  def __updateOrigin(self):
    safe_area = self.__buildFence()
    settings = self.__getSettings()

    # distance across viewport between menus
    span = Vector((
        safe_area[1].x - safe_area[0].x,
        safe_area[1].y - safe_area[0].y
    ))

    # apply position ratio to safe area
    self.origin = Vector((
        safe_area[0].x + span.x * settings.menu_position[0] * 0.01,
        safe_area[0].y + span.y * settings.menu_position[1] * 0.01,
        0.0
    ))

  def __buildFence(self) -> tuple[Vector, Vector]:
    min = Vector((0.0,0.0))
    max = Vector((self.context.region.width, self.context.region.height))

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

