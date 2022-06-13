import bpy, math
from mathutils import Vector

from bpy import ops
from bpy.props import EnumProperty
from bpy.types import Context, Event, Operator

from .Gizmos import dpi_factor, panel
from .items import input_mode_items, pivot_items
from .touch_input import toggle_keymaps


class VIEW3D_OT_Doubletap_Action( Operator ):
  """ Viewport double-tap shortcut """
  bl_idname = "view3d.dt_action"
  bl_label = "Viewport double-tap shortcut"

  def execute( self, context: Context ):
    settings = bpy.context.preferences.addons[ 'touchview' ].preferences
    if context.mode in { 'OBJECT', 'SCULPT', 'EDIT_MESH', 'PAINT_TEXTURE', 'PAINT_VERTEX', 'PAINT_WEIGHT' }:
      op = settings.double_click_mode.split( '.' )
      opgrp = getattr( bpy.ops, op[ 0 ] )
      getattr( opgrp, op[ 1 ] )( 'INVOKE_DEFAULT' )
    return { 'FINISHED' }

  def invoke( self, context: Context, event: Event ):
    if event.type not in [ 'PEN', 'LEFTMOUSE' ]:
      return { 'CANCELLED' }
    if event.pressure != 1.0:
      return { 'PASS_THROUGH' }
    if event.value != "DOUBLE_CLICK":
      return { 'CANCELLED' }
    self.execute( context )
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type in [
      'NODE_EDITOR', 'VIEW_2D', 'VIEW_3D', 'IMAGE_EDITOR'
    ] and context.region.type == 'WINDOW'


class VIEW2D_OT_TouchInput( Operator ):
  """ Active Viewport control zones """
  bl_idname = "view2d.view_ops"
  bl_label = "2D Viewport Control Regions"

  delta: tuple[ float, float ]

  mode: EnumProperty(
    name="Mode",
    description="Sets the viewport control type",
    items=input_mode_items,
    default='PAN',
    options={ "HIDDEN" }
  )

  def execute( self, context: Context ):
    if context.area.type == 'IMAGE_EDITOR':
      return self.exec_image_editor( context )
    if self.mode == "DOLLY":
      bpy.ops.view2d.zoom( 'INVOKE_DEFAULT' )
    elif self.mode == "PAN":
      bpy.ops.view2d.pan( 'INVOKE_DEFAULT' )
    return { 'FINISHED' }

  def exec_image_editor( self, _: Context ):
    if self.mode == "PAN":
      bpy.ops.image.view_pan( 'INVOKE_DEFAULT' )
    elif self.mode == "DOLLY":
      bpy.ops.image.view_zoom( 'INVOKE_DEFAULT' )
    return { 'FINISHED' }

  def invoke( self, context: Context, event: Event ):
    if event.type == "PEN" or event.pressure != 1.0: return { 'PASS_THROUGH' }
    settings = bpy.context.preferences.addons[ 'touchview' ].preferences
    if not settings.is_enabled and event.type == "LEFTMOUSE": return { 'PASS_THROUGH' }
    if event.value != "PRESS": return { 'FINISHED' }
    self.delta = ( event.mouse_region_x, event.mouse_region_y )

    mid_point = Vector( ( context.region.width / 2, context.region.height / 2 ) )

    dolly_scale = settings.getWidth()
    dolly_wid = mid_point.x * dolly_scale

    if dolly_wid > self.delta[ 0 ] or self.delta[ 0 ] > context.region.width - dolly_wid:
      self.mode = "DOLLY"
    else:
      self.mode = "PAN"

    if settings.swap_panrotate:
      if self.mode == "PAN":
        self.mode = "ORBIT"
      elif self.mode == "ORBIT":
        self.mode = "PAN"

    self.execute( context )
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type in [ 'NODE_EDITOR', 'VIEW_2D', 'IMAGE_EDITOR' ] and context.region.type == 'WINDOW'


class VIEW3D_OT_TouchInput( Operator ):
  """ Active Viewport control zones """
  bl_idname = "view3d.view_ops"
  bl_label = "Viewport Control Regions"

  delta: tuple[ float, float ]

  mode: EnumProperty(
    name="Mode",
    description="Sets the viewport control type",
    items=input_mode_items,
    default='ORBIT',
    options={ "HIDDEN" }
  )

  def execute( self, _: Context ):
    if self.mode == "DOLLY":
      ops.view3d.zoom( 'INVOKE_DEFAULT' )
    elif self.mode == "ORBIT":
      ops.view3d.rotate( 'INVOKE_DEFAULT' )
    elif self.mode == "PAN":
      bpy.ops.view3d.move( 'INVOKE_DEFAULT' )
    return { 'FINISHED' }

  def invoke( self, context: Context, event: Event ):
    if event.type == "PEN" or event.pressure != 1.0: return { 'PASS_THROUGH' }
    settings = bpy.context.preferences.addons[ 'touchview' ].preferences
    if not settings.is_enabled and event.type == "LEFTMOUSE": return { 'PASS_THROUGH' }
    if event.value != "PRESS": return { 'FINISHED' }
    self.delta = ( event.mouse_region_x, event.mouse_region_y )
    is_paint_mode = context.mode == 'PAINT_GPENCIL'

    mid_point = Vector( ( context.region.width / 2, context.region.height / 2 ) )

    dolly_scale = settings.getWidth()
    pan_scale = settings.getRadius()

    dolly_wid = mid_point.x * dolly_scale
    pan_diameter = math.dist( ( 0, 0 ), mid_point ) * ( pan_scale * 0.5 )

    is_quadview_orthographic = context.region.data.is_orthographic_side_view and context.region.alignment == "QUAD_SPLIT"
    is_locked = context.region.data.lock_rotation or is_quadview_orthographic or is_paint_mode

    if dolly_wid > self.delta[ 0 ] or self.delta[ 0 ] > context.region.width - dolly_wid:
      self.mode = "DOLLY"
    elif math.dist( self.delta, mid_point ) < pan_diameter or is_locked:
      self.mode = "PAN"
    else:
      self.mode = "ORBIT"

    if settings.swap_panrotate:
      if self.mode == "PAN":
        self.mode = "ORBIT"
      elif self.mode == "ORBIT":
        self.mode = "PAN"

    if context.mode == "SCULPT":
      bpy.ops.sculpt.set_pivot_position( mode=settings.pivot_mode )
    self.execute( context )
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'


class VIEW3D_OT_FlipTools( Operator ):
  """ Relocate Tools panel between left and right """
  bl_idname = "view3d.tools_region_flip"
  bl_label = "Tools Region Swap"

  def execute( self, context: Context ):
    override = bpy.context.copy()
    for r in context.area.regions:
      if r.type == 'TOOLS':
        override[ "region" ] = r
    bpy.ops.screen.region_flip( override )
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'


class VIEW3D_OT_NextPivotMode( Operator ):
  """ Step through Pivot modes """
  bl_idname = "view3d.step_pivot_mode"
  bl_label = "Use next Pivot mode"

  def execute( self, context: Context ):
    settings = context.preferences.addons[ 'touchview' ].preferences
    count = 0
    for enum, _, _ in pivot_items:
      if enum == settings.pivot_mode:
        count += 1
        if count == len( pivot_items ): count = 0
        pivot = pivot_items[ count ][ 0 ]
        bpy.ops.sculpt.set_pivot_position( mode=pivot )
        settings.pivot_mode = pivot
        context.area.tag_redraw()
        return { 'FINISHED' }
      count += 1
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'


class VIEW3D_OT_ToggleTouchControls( Operator ):
  """ Toggle Touch Controls """
  bl_idname = "view3d.toggle_touch"
  bl_label = "Toggle Touch Controls"

  def execute( self, context: Context ):
    context.preferences.addons[ 'touchview' ].preferences.is_enabled ^= True
    toggle_keymaps( context.preferences.addons[ 'touchview' ].preferences.is_enabled )
    context.area.tag_redraw()
    return { 'FINISHED' }


class VIEW3D_OT_ToggleNPanel( Operator ):
  """ Toggle Settings Panel """
  bl_idname = "view3d.toggle_n_panel"
  bl_label = "Display settings Panel"

  def execute( self, context: Context ):
    context.space_data.show_region_ui ^= True
    return { 'FINISHED' }

  @classmethod
  def poll( cls, context: Context ):
    return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'


class VIEW3D_OT_ToggleFloatingMenu( Operator ):
  """ Toggle Floating Menu """
  bl_idname = "view3d.toggle_floating_menu"
  bl_label = "Toggle Floating Menu"

  def execute( self, context: Context ):
    context.preferences.addons[ 'touchview' ].preferences.show_float_menu ^= True
    return { 'FINISHED' }


class VIEW3D_OT_MoveFloatMenu( Operator ):
  bl_idname = "view3d.move_float_menu"
  bl_label = "Relocate Floating Gizmo"

  def execute( self, context ):
    settings = context.preferences.addons[ 'touchview' ].preferences
    fence = self.__calcFence( Vector( ( context.region.width, context.region.height ) ) )
    settings.floating_position[ 0 ] = min(
      max( ( self.x - fence[ 0 ][ 0 ] ) / ( fence[ 1 ][ 0 ] - fence[ 0 ][ 0 ] ) * 100, 0 ), 100
    )
    settings.floating_position[ 1 ] = min(
      max( ( self.y - fence[ 0 ][ 1 ] ) / ( fence[ 1 ][ 1 ] - fence[ 0 ][ 1 ] ) * 100, 0 ), 100
    )
    return { 'FINISHED' }

  def modal( self, context, event ):
    if event.type == 'MOUSEMOVE':  # Apply
      context.region.tag_redraw()
      self.x = event.mouse_x
      self.y = event.mouse_y - 22 * dpi_factor()
      self.execute( context )
    elif event.type == 'LEFTMOUSE':  # Confirm
      return { 'FINISHED' }
    elif event.type in { 'RIGHTMOUSE', 'ESC' }:  # Cancel
      settings = context.preferences.addons[ 'touchview' ].preferences
      settings.floating_position[ 0 ] = self.init_x
      settings.floating_position[ 1 ] = self.init_y
      return { 'CANCELLED' }

    return { 'RUNNING_MODAL' }

  def invoke( self, context, event ):
    settings = context.preferences.addons[ 'touchview' ].preferences
    self.init_x = settings.floating_position[ 0 ]
    self.init_y = settings.floating_position[ 1 ]
    self.x = event.mouse_x
    self.y = event.mouse_y
    self.execute( context )

    context.window_manager.modal_handler_add( self )
    return { 'RUNNING_MODAL' }

  def __calcFence( self, size: Vector ) -> tuple[ tuple[ int, int ] ]:
    if bpy.context.preferences.view.mini_axis_type == 'GIZMO':
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )
    elif bpy.context.preferences.view.mini_axis_type == 'MINIMAL':
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )
    else:
      right = size.x - ( panel( 'UI' )[ 0 ] + 22 * dpi_factor() )

    left = 22 * dpi_factor() + panel( 'TOOLS' )[ 0 ]

    return ( ( left, 22 * dpi_factor() ), ( right, size.y - ( panel( 'HEADER' )[ 1 ] + panel( 'TOOL_HEADER' )[ 1 ] ) ) )


class VIEW3D_OT_ViewportRecenter( Operator ):
  """ Recenter Viewport and Cursor on Selected Object """
  bl_idname = "view3d.viewport_recenter"
  bl_label = "Recenter Viewport and Cursor on Selected"

  def execute( self, context: Context ):
    current = context.scene.tool_settings.transform_pivot_point
    context.scene.tool_settings.transform_pivot_point = "ACTIVE_ELEMENT"
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.view3d.view_center_cursor()
    bpy.ops.view3d.view_selected()
    context.scene.tool_settings.transform_pivot_point = current
    return { 'FINISHED' }


class VIEW3D_OT_ViewportLock( Operator ):
  """ Toggle Viewport Rotation """
  bl_idname = "view3d.viewport_lock"
  bl_label = "Viewport rotation lock toggle"

  region_ids = []

  def execute( self, context: Context ):
    if len( context.area.spaces.active.region_quadviews ) == 0:
      context.region_data.lock_rotation ^= True
      return { 'FINISHED' }

    for region in context.area.spaces.active.region_quadviews:
      self.region_ids.append( ( region.as_pointer(), region.lock_rotation ) )

    start_change = False
    regions = dict( self.region_ids )
    for i in range( 3, -1, -1 ):
      region_data = context.area.spaces.active.region_quadviews[ i ]
      if context.region_data.as_pointer() == region_data.as_pointer():
        start_change = True
        context.region_data.lock_rotation ^= True
        continue

      if start_change:
        region_data.lock_rotation = regions[ region_data.as_pointer() ]
    self.region_ids = []
    return { 'FINISHED' }


class VIEW3D_OT_IncreaseMultires( Operator ):
  """ Increment Multires by 1 or add subdivision """
  bl_idname = "object.increment_multires"
  bl_label = "Increment Multires modifier by 1 or add subdivision level"

  def execute( self, context: Context ):
    settings = context.preferences.addons[ 'touchview' ].preferences
    if not context.active_object: return { 'CANCELLED' }
    if not len( context.active_object.modifiers ): return { 'CANCELLED' }
    for mod in context.active_object.modifiers:
      if mod.type == 'MULTIRES':
        if context.mode == 'SCULPT':
          if mod.sculpt_levels == mod.total_levels:
            if mod.sculpt_levels < settings.subdivision_limit:
              bpy.ops.object.multires_subdivide( modifier=mod.name )
          else:
            mod.sculpt_levels += 1
        else:
          if mod.levels == mod.total_levels:
            if mod.levels < settings.subdivision_limit:
              bpy.ops.object.multires_subdivide( modifier=mod.name )
          else:
            mod.levels += 1
        return { 'FINISHED' }
    return { 'CANCELLED' }


class VIEW3D_OT_DecreaseMultires( Operator ):
  """ Decrement Multires by 1 """
  bl_idname = "object.decrement_multires"
  bl_label = "decrement Multires modifier by 1"

  def execute( self, context: Context ):
    if not context.active_object: return { 'CANCELLED' }
    if not len( context.active_object.modifiers ): return { 'CANCELLED' }
    for mod in context.active_object.modifiers:
      if mod.type == 'MULTIRES':
        if context.mode == 'SCULPT':
          if mod.sculpt_levels == 0:
            try:
              bpy.ops.object.multires_unsubdivide( modifier=mod.name )
            except:
              #let it go
              pass
          else:
            mod.sculpt_levels -= 1
        else:
          if mod.levels == 0:
            try:
              bpy.ops.object.multires_unsubdivide( modifier=mod.name )
            except:
              #let it go
              pass
          else:
            mod.levels -= 1
        return { 'FINISHED' }
    return { 'CANCELLED' }
