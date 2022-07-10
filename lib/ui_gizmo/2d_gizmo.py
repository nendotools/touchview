import bpy
from bpy.types import Gizmo, GizmoGroup

##
# GizmoSet
# - multi-state object
#   - single-state
#     - one icon
#     - one action
#     - possible toggle by variable state
# 
#   - 2-state (boolean)
#     - 
# 
##

class GizmoSet:
  group: GizmoGroup;
  alpha: float = 0.4;
  alpha_highlight: float = 0.8;
  color: list[float] = [1,1,1];
  color_highlight: list[float] = [1,1,1];
  group: GizmoGroup
  primary: Gizmo
  binding: tuple[str]
  
  def setup(self, group:GizmoGroup, config: tuple ):
    self.group = group
    self.binding = config[0]
    self.primary = self.__buildGizmo( config[1], config[2] )

  def draw(self):
    self.__updatevisible()

  def __updatevisible(self):
    if(self.binding[0] == "prefs"):
      self.visible = getattr(bpy.context.preferences.addons["touchview"].preferences, self.binding[1]);

  # initialize each gizmo, add them to named list with icon name(s)
  def __buildGizmo( self, config: tuple ) -> Gizmo:
    opname = config[0]
    icon = config[1]
    gizmo = self.group.gizmos.new( "GIZMO_GT_button_2d" )
    props = gizmo.target_set_operator( opname )
    props.name = "PIE_MT_Floating_Menu"
    gizmo.icon = icon
    gizmo.use_tooltip = False
    gizmo.use_event_handle_all = True
    gizmo.draw_options = { 'BACKDROP', 'OUTLINE' }
    self.__setColors( gizmo )
    gizmo.scale_basis = 14
    return gizmo


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
