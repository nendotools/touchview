import bpy
from bpy.types import Context, Panel, Menu, VIEW3D_PT_gizmo_display


class VIEW3D_PT_NendoPanel:
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "NENDO"


class VIEW3D_PT_NendoViewport( VIEW3D_PT_NendoPanel, Panel ):
  bl_idname = "VIEW3D_PT_view_ops"
  bl_label = "Viewport Settings"

  def draw( self, context ):
    settings = bpy.context.preferences.addons[ 'touchview' ].preferences
    view = context.space_data
    space = context.area.spaces.active

    col = self.layout.column()
    col.label( text="Control Zones" )
    col.prop( settings, "is_enabled", toggle=1 )
    col.prop( settings, "enable_double_click", toggle=1 )
    col.prop( settings, "swap_panrotate" )
    col.prop( settings, "isVisible", text="Show Overlay" )
    col.prop( settings, "use_multiple_colors" )
    col.prop( settings, "overlay_main_color", text="Main Color" )
    if settings.use_multiple_colors:
      col.prop( settings, "overlay_secondary_color", text="Secondary Color" )
    col.prop( settings, "width" )
    col.prop( settings, "radius" )

    col.separator()

    col.label( text="Viewport Options" )
    col.label(text="Gizmo Menu Style")
    tabs = col.grid_flow()
    tabs.props_enum(settings, "menu_style")

    if settings.menu_style == 'fixed.bar':
        col.prop_menu_enum( settings, "gizmo_position" )
    col.prop( settings, "menu_spacing", slider=True )
    col.operator( "view3d.tools_region_flip", text="Flip Tools" )

    if len( space.region_quadviews ) > 0:
      col.operator( "screen.region_quadview", text="Disable Quadview" )
    else:
      col.operator( "screen.region_quadview", text="Enable Quadview" )
      col.prop( space, "lock_cursor", text="Lock to Cursor" )
      col.prop( view.region_3d, "lock_rotation", text="Lock Rotation" )

    col.separator()
    col.prop( settings, "subdivision_limit" )
    col.prop_menu_enum( settings, "double_click_mode" )
    col.separator()

    if not settings.show_float_menu:
      col.operator( "view3d.toggle_floating_menu", text="Show Floating Menu" )
    else:
      col.operator( "view3d.toggle_floating_menu", text="Hide Floating Menu", depress=True )
      col.label( text="Floating Menu Settings" )
      col.prop( settings, "active_menu", text="" )
      box = col.box()
      mList = settings.getMenuSettings( settings.active_menu )
      for i in range( 7 ):
        box.prop( mList, "menu_slot_" + str( i + 1 ), text="" )
    context.area.tag_redraw()


class PIE_MT_Floating_Menu( Menu ):
  """ Open a custom menu """
  bl_idname = "PIE_MT_Floating_Menu"
  bl_label = "Floating Menu"
  bl_description = "Customized Floating Menu"

  def draw( self, context: Context ):
    settings = context.preferences.addons[ 'touchview' ].preferences
    menu = settings.getMenuSettings( context.mode )

    layout = self.layout
    pie = layout.menu_pie()
    for i in range( 8 ):
      op = getattr( menu, "menu_slot_" + str( i + 1 ) )
      if op == "":
        continue
      elif "_MT_" in op:
        pie.menu( op )
        continue
      elif self.__operator_exists( op ):
        pie.operator( op )

  def __operator_exists( self, idname ):
    try:
      names = idname.split( "." )
      a = bpy.ops
      for prop in names:
        a = getattr( a, prop )
      a.__repr__()
    except:
      return False
    return True


# UI panel to append Gizmo menu
class VIEW3D_PT_gizmo_panel( VIEW3D_PT_gizmo_display ):
    bl_label = "Gizmo display control"
    bl_idname = "VIEW3D_PT_gizmo_display"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Gizmos"
    bl_ui_units_x = 16

    def draw( self, context: Context ):
        layout = self.layout
        scene = context.scene
        view = context.space_data

        split = layout.split( factor=0.5 )
        left_col = split.column()
        left_col.label( text="Touch Gizmos" )
        settings = bpy.context.preferences.addons[ 'touchview' ].preferences
        available_gizmos = settings.getGizmoSet( context.object.mode )

        col = left_col.column( align=True )
        col.active = context.space_data.show_gizmo
        col.prop( settings, "show_menu" )
        col = left_col.column()
        col.active = settings.show_menu
        for toggle in available_gizmos:
            col.prop( settings, 'show_' + toggle )

        right_col = split.column()
        right_col.label(text="Viewport Gizmos")
        right_col.separator()

        col = right_col.column()
        col.active = view.show_gizmo
        colsub = col.column()
        colsub.prop(view, "show_gizmo_navigate", text="Navigate")
        colsub.prop(view, "show_gizmo_tool", text="Active Tools")
        colsub.prop(view, "show_gizmo_context", text="Active Object")

        right_col.separator()

        col = right_col.column()
        col.active = view.show_gizmo and view.show_gizmo_context
        col.label(text="Object Gizmos")
        col.prop(scene.transform_orientation_slots[1], "type", text="")
        col.prop(view, "show_gizmo_object_translate", text="Move")
        col.prop(view, "show_gizmo_object_rotate", text="Rotate")
        col.prop(view, "show_gizmo_object_scale", text="Scale")

        right_col.separator()

        # Match order of object type visibility
        col = right_col.column()
        col.active = view.show_gizmo
        col.label(text="Empty")
        col.prop(view, "show_gizmo_empty_image", text="Image")
        col.prop(view, "show_gizmo_empty_force_field", text="Force Field")
        col.label(text="Light")
        col.prop(view, "show_gizmo_light_size", text="Size")
        col.prop(view, "show_gizmo_light_look_at", text="Look At")
        col.label(text="Camera")
        col.prop(view, "show_gizmo_camera_lens", text="Lens")
        col.prop(view, "show_gizmo_camera_dof_distance", text="Focus Distance")

