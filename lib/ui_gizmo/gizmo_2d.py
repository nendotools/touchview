import bpy
from bpy.types import Gizmo, GizmoGroup, bpy_prop_collection
from mathutils import Matrix, Vector

def dpi_factor() -> float:
  systemPreferences = bpy.context.preferences.system
  retinaFactor = getattr( systemPreferences, "pixel_size", 1 )
  return int( systemPreferences.dpi * retinaFactor ) / 72

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
  
  def setup(self, group:GizmoGroup, config: dict ):
    self.has_dependent = 'has_dependent' in config or False
    self.group = group
    self.scale =  config['scale'] if ('scale' in config) else 14
    self.binding = config['binding']
    self.has_attribute_bind = self.binding['attribute'] if 'attribute' in self.binding else False
    self.primary = self.__buildGizmo( config['command'], config['icon'] )

  def __getSettings( self ):
    return bpy.context.preferences.addons[ 'touchview' ].preferences

  def draw_prepare(self):
    settings = self.__getSettings()
    self.hidden = not settings.show_menu
    self.skip_draw = False
    self.__updatevisible()

    if self.binding['name'] == 'menu_controller':
      self.primary.hide = 'float' not in settings.menu_style
      gui_scale = 22 * dpi_factor()
      self.primary.scale_basis = max( settings.menu_spacing - gui_scale/1.5, gui_scale/2)

  def move(self, position: Vector):
    self.primary.matrix_basis = Matrix.Translation(position) 

  def __updatevisible(self):
    if(self.binding['location'] == "prefs"):
      self.visible = getattr(bpy.context.preferences.addons["touchview"].preferences, 'show_'+self.binding['name']);
    if self.visible:
      self.visible = self.__visibilityLock() and not self.__checkAttributeBind()
    self.primary.hide = not self.visible

  def __visibilityLock(self) -> bool:
    return self.hidden and self.__getSettings().menu_style != 'fixed.bar'

  def __checkAttributeBind(self):
    if not self.has_attribute_bind:
      return False
    bind = self.binding['attribute']
    state = self.__findAttribute(bind['path'], bind['value']) == bind['state']
    return not state

  # search for attribute, value through context.
  # will traverse bpy_prop_collection entries by next attr to value comparison
  def __findAttribute(self, path: str, value: any):
    names = path.split( "." )
    current = bpy.context
    for i, prop in enumerate( names ):
        current = getattr( current, prop )
        if current == None:
            return False 

        if isinstance( current, bpy_prop_collection ):
            item = ''
            for item in current:
                if getattr(item, names[i+1]) == value:
                    return True
            return False
    return getattr(current, value) 

  # initialize each gizmo, add them to named list with icon name(s)
  def __buildGizmo( self, command: str, icon: str ) -> Gizmo:
    gizmo = self.group.gizmos.new( "GIZMO_GT_button_2d" )
    gizmo.target_set_operator( command )
    gizmo.icon = icon
    gizmo.use_tooltip = False
    gizmo.use_event_handle_all = True
    gizmo.draw_options = { 'BACKDROP', 'OUTLINE' }
    self.__setColors( gizmo )
    gizmo.scale_basis = self.scale or 14
    return gizmo

  def __setColors(self, gizmo: Gizmo):
    settings = self.__getSettings()
    gizmo.color = settings.gizmo_colors[ "active" ][ "color" ]
    gizmo.color_highlight = settings.gizmo_colors[ "active" ][ "color_highlight" ]
    gizmo.alpha = settings.gizmo_colors[ "active" ][ "alpha" ]
    gizmo.alpha_highlight = settings.gizmo_colors[ "active" ][ "alpha_highlight" ]


class GizmoSetBoolean( GizmoSet ):
  def setup(self, group:GizmoGroup, config: dict ):
    self.has_dependent = 'has_dependent' in config or False
    self.group = group
    self.scale =  config['scale'] if ('scale' in config) else 14
    self.binding = config['binding']
    self.has_attribute_bind = self.binding['attribute'] if 'attribute' in self.binding else False
    self.onGizmo = self._GizmoSet__buildGizmo( config['command'], config['onIcon'] )
    self.offGizmo = self._GizmoSet__buildGizmo( config['command'], config['offIcon'] )
    self.__setActiveGizmo(True)

  def __setActiveGizmo(self, state: bool):
    self.onGizmo.hide = True
    self.offGizmo.hide = True
    self.primary = self.onGizmo if state else self.offGizmo

  def draw_prepare(self):
    settings = self._GizmoSet__getSettings()
    self.hidden = not settings.show_menu
    self.skip_draw = False
    self.__updatevisible()

  def __updatevisible(self):
    self.visible = getattr(bpy.context.preferences.addons["touchview"].preferences, 'show_'+self.binding['name']);
    if self.visible:
      self.visible = self._GizmoSet__visibilityLock() and not self._GizmoSet__checkAttributeBind()

    bind = self.binding
    self.__setActiveGizmo(self._GizmoSet__findAttribute(bind['location'], bind['name']))
    self.primary.hide = not self.visible


class GizmoSetEnum( GizmoSet ):
    gizmos: list[Gizmo]
    def setup(self, group:GizmoGroup, config):
      pass