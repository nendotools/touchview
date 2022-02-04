import bpy
from bpy.types import Area, Panel

from . constants import OverlaySettings

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NENDO"
    
class NendoViewport(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_view_ops"
    bl_label = "Viewport Settings"

    def draw(self, context):
        settings = context.screen.overlay_settings
        self.layout.label(text="Control Zones")
        self.layout.row()
        self.layout.prop(settings, "width")
        self.layout.row()
        self.layout.prop(settings, "radius")
        self.layout.row()
        self.layout.prop(settings, "isVisible", text="Show Overlay")
        
        self.layout.label(text="Viewport Options")
        self.layout.row()

        self.layout.operator("view3d.tools_region_flip", text="Flip Tools")

        view = context.space_data
        self.layout.row()
        self.layout.operator("screen.region_quadview", text="Toggle Quadview")
        self.layout.row()
        self.layout.prop(view.region_3d, "lock_rotation", text="Lock Rotation")

