import bpy
from mathutils import Matrix, Vector
from bpy.types import Context, Gizmo, GizmoGroup, Operator

class ViewportGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_navigate_lock"
    bl_label = "Tools Region Swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    def setup(self, context: Context):
        view = context.space_data
        size = Vector((context.region.width, context.region.height, 0))

        viewport = context.window.vm.getViewport(context.area)
        viewport.setRegionContext(context.region)

        settings = bpy.context.screen.overlay_settings
        size = viewport.getSize(1, True)
        
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.target_set_operator("view3d.viewport_lock")
        mpr.icon = 'LOCKED'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        mpr.alpha = 0.3
        mpr.color_highlight = 0.8, 0.8, 0.8
        mpr.alpha_highlight = 0.2
        mpr.scale_basis = (80 * 0.35) / 2
        mpr.matrix_basis = Matrix.Translation((size.x/2, size.y - mpr.scale_basis * 4, 0))
        
    def draw_prepare(self, context:Context):
        viewport = context.window.vm.getViewport(context.area)
        viewport.setRegionContext(context.region)

        settings = bpy.context.screen.overlay_settings
        size = viewport.getSize(1, True)
        for gizmo in self.gizmos:
            gizmo.matrix_basis = Matrix.Translation((size.x/2, size.y - gizmo.scale_basis * 4, 0))

class ViewportLock(Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.viewport_lock"
    bl_label = "Viewport lock toggle"

    def execute(self, context: Context):
        if len(context.area.spaces.active.region_quadviews) == 0:
            context.region.data.lock_rotation^=True
            return {'FINISHED'}

        context.region.data.lock_rotation=False
        return {'FINISHED'}

        
def draw_lock(panel, context):
    layout = panel.layout
    settings = bpy.context.screen.overlay_settings
    row = layout.row()

    # display label and button
    row.label(text="Touchview Buttons")
    row = layout.row()
    
    col = row.column()
    col.prop(settings, 'show_lock')
