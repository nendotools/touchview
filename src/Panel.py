from bpy.types import Panel

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NENDO"
    
class NendoViewport(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_view_ops"
    bl_label = "Viewport Settings"

    def draw(self, context):
        settings = context.screen.overlay_settings
        view = context.space_data
        space = context.area.spaces.active

        self.layout.column()
        self.layout.label(text="Control Zones")
        self.layout.prop(settings, "width")
        self.layout.prop(settings, "radius")
        self.layout.prop(settings, "isVisible", text="Show Overlay")
        
        self.layout.label(text="Viewport Options")
        self.layout.prop_menu_enum(settings, "gizmo_position")
        self.layout.operator("view3d.tools_region_flip", text="Flip Tools")
        if len(space.region_quadviews) > 0:
            self.layout.operator("screen.region_quadview", text="Disable Quadview")
        else:
            self.layout.operator("screen.region_quadview", text="Enable Quadview")
            self.layout.prop(space, "lock_cursor", text="Lock to Cursor")
            self.layout.prop(view.region_3d, "lock_rotation", text="Lock Rotation")
        context.area.tag_redraw()
