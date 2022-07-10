import bpy
from mathutils import Matrix, Vector
from bpy.types import Context, Gizmo, GizmoGroup

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
  for region in bpy.context.area.regions:
    if region.type == type:
      width = region.width
      height = region.height
  return ( width, height )

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

class GIZMO_GT_FloatingGizmoGroup( GizmoGroup ):
  bl_idname = "GIZMO_GT_float_tool"
  bl_label = "Customizable floating viewport button"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'WINDOW'
  bl_options = { 'PERSISTENT', 'SCALE' }

  def setup( self, _: Context ):
    self.__buildGizmo( "wm.call_menu_pie", "SETTINGS" )

  def draw_prepare( self, context: Context ):
    region = context.region
    settings = self.__getSettings()
    size = Vector( ( region.width, region.height ) )

    position = self.__getGizmoOrientation( size )
    offset = 0
    gap = 2.2
    gizmo = self.gizmos[ 0 ]
    gizmo.matrix_basis = Matrix.Translation( position[ 0 ] + Vector( position[ 1 ] ) * offset )
    offset += gizmo.scale_basis * 2 + gap
    if not context.space_data.show_gizmo_navigate or not settings.show_float_menu:
      gizmo.hide = True
    else:
      gizmo.hide = False

  # initialize each gizmo, add them to named list with icon name(s)
  def __buildGizmo( self, operator_name: str, on_icon: str ) -> Gizmo:
    gizmo = self.gizmos.new( "GIZMO_GT_button_2d" )
    props = gizmo.target_set_operator( operator_name )
    props.name = "PIE_MT_Floating_Menu"
    gizmo.icon = on_icon
    gizmo.use_tooltip = False
    gizmo.use_event_handle_all = True
    gizmo.draw_options = { 'BACKDROP', 'OUTLINE' }
    self.__setColors( gizmo )
    gizmo.scale_basis = 14
    return gizmo

  # determine viewport position and spacing
  def __getGizmoOrientation( self, size: Vector ) -> tuple[ Vector, tuple[ int, int ] ]:
    settings = self.__getSettings()
    position = ( 0.0, 0.0, 0.0 )
    orientation = ( 0.0, 0.0, 0.0 )

    if bpy.context.preferences.view.mini_axis_type == 'GIZMO':
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )
    elif bpy.context.preferences.view.mini_axis_type == 'MINIMAL':
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )
    else:
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )

    left = 22 * dpi_factor() + panel( 'TOOLS' )[ 0 ]

    fence = ( ( left, 22 * dpi_factor() ), (
      right - left, size.y - ( 22 * dpi_factor() ) - ( panel( 'HEADER' )[ 1 ] + panel( 'TOOL_HEADER' )[ 1 ] )
    ) )

    position = (
      left + settings.floating_position[ 0 ] / 100 * fence[ 1 ][ 0 ],
      fence[ 0 ][ 1 ] + settings.floating_position[ 1 ] / 100 * fence[ 1 ][ 1 ], 0
    )

    return ( Vector( position ), orientation )

  # fetch colors from config and assign to gizmo
  def __setColors( self, gizmo ):
    settings = self.__getSettings()
    gizmo.color = settings.gizmo_colors[ "active" ][ "color" ]
    gizmo.color_highlight = settings.gizmo_colors[ "active" ][ "color_highlight" ]
    gizmo.alpha = settings.gizmo_colors[ "active" ][ "alpha" ]
    gizmo.alpha_highlight = settings.gizmo_colors[ "active" ][ "alpha_highlight" ]

  # get settings pointer
  def __getSettings( self ):
    return bpy.context.preferences.addons[ 'touchview' ].preferences


