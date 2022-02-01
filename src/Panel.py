import bpy
from bpy.types import Panel

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NENDO"
    
class NendoViewport(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_view_ops"
    bl_label = "Viewport Settings"

    def draw(self, context):
        settings = context.scene.overlay_settings
        self.layout.label(text="Control Zones")
        self.layout.row()
        self.layout.prop(settings, "dolly_wid")
        self.layout.row()
        self.layout.prop(settings, "pan_rad")
        self.layout.row()
        self.layout.prop(settings, "isVisible", text="Show Overlay")
        
        self.layout.label(text="Viewoprt Options")
        self.layout.row()

        self.layout.operator("view3d.tools_region_flip", text="Flip Tools")

