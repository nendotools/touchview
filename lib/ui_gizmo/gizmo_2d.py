import bpy
from bpy.types import Gizmo, GizmoGroup
from mathutils import Matrix, Vector

##
# GizmoSet
# - multi-state object
#   - single-state
#     - one icon
#     - one action
#     - possible toggle by variable state
# 
#   - 2-state (boolean)
#     - 2 icons
#     - 2 actions (or 1 action for both icons)
# 
##

class GizmoSet:
  group: GizmoGroup;
  visible: bool = True;
  alpha: float = 0.4;
  alpha_highlight: float = 0.8;
  color: list[float] = [1,1,1];
  color_highlight: list[float] = [1,1,1];
  group: GizmoGroup
  primary: Gizmo
  binding: tuple[str]
  
  def setup(self, group:GizmoGroup, config: dict ):
    self.group = group
    self.binding = config['binding']
    self.primary = self.__buildGizmo( config['command'], config['icon'] )

  def __getSettings( self ):
    return bpy.context.preferences.addons[ 'touchview' ].preferences

  def draw_prepare(self):
    self.__updatevisible()

  def move(self, position: Vector):
    self.primary.matrix_basis = Matrix.Translation(position) 

  def __updatevisible(self):
    if(self.binding['location'] == "prefs"):
      self.visible = getattr(bpy.context.preferences.addons["touchview"].preferences, 'show_'+self.binding['name']);
    self.primary.hide = not self.visible

  # initialize each gizmo, add them to named list with icon name(s)
  def __buildGizmo( self, command: str, icon: str ) -> Gizmo:
    gizmo = self.group.gizmos.new( "GIZMO_GT_button_2d" )
    gizmo.target_set_operator( command )
    gizmo.icon = icon
    gizmo.use_tooltip = False
    gizmo.use_event_handle_all = True
    gizmo.draw_options = { 'BACKDROP', 'OUTLINE' }
    self.__setColors( gizmo )
    gizmo.scale_basis = 14
    return gizmo

  def __setColors(self, gizmo: Gizmo):
    settings = self.__getSettings()
    gizmo.color = settings.gizmo_colors[ "active" ][ "color" ]
    gizmo.color_highlight = settings.gizmo_colors[ "active" ][ "color_highlight" ]
    gizmo.alpha = settings.gizmo_colors[ "active" ][ "alpha" ]
    gizmo.alpha_highlight = settings.gizmo_colors[ "active" ][ "alpha_highlight" ]


class GizmoSetBoolean( GizmoSet ):
  secondary: Gizmo

  def setup(self, group:GizmoGroup, config: tuple[tuple]):
    self.group = group
    bindingConfig = config[0]
    primaryConfig = config[1]
    secondaryConfig = config[2]
    self.primary = self.__buildGizmo( primaryConfig[0], primaryConfig[1] )
    self.secondary = self.__buildGizmo( secondaryConfig[0]. secondaryConfig[1] )
    
    # handle binding setup
    self.__setBinding(bindingConfig, self.primary, self.secondary)

    self.secondary.hidden = True


class GizmoSetEnum( GizmoSet ):
    gizmos: list[Gizmo]
    def setup(self, group:GizmoGroup, config):
      pass
