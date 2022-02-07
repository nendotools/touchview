import bpy
import math
from mathutils import Matrix, Vector
from bpy.types import Context, Gizmo, GizmoGroup, Operator

class ViewportGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_navigate_lock"
    bl_label = "Tools Region Swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    gizmo_actions: list[tuple[str, Gizmo, str, str]]

    def setup(self, context: Context):
        self.gizmo_actions = []
        view = context.space_data
        size = Vector((context.region.width, context.region.height, 0))

        viewport = context.window.vm.getViewport(context.area)
        viewport.setRegionContext(context.region)

        settings = self.__getSettings()
        size = viewport.getSize(1, True)
        
        self.__buildGizmo("quadview", "screen.region_quadview", "IMGDISPLAY", "MESH_PLANE")
        self.__buildGizmo("snap_view", "view3d.viewport_recenter", "CURSOR")
        self.__buildGizmo("rotation_lock", "view3d.viewport_lock", "LOCKED", "UNLOCKED")
        self.__buildGizmo("voxel_resize", "object.voxel_size_edit", "MESH_GRID")
        self.__buildGizmo("voxel_remesh", "object.voxel_remesh", "MOD_UVPROJECT")
        
    def draw_prepare(self, context:Context):
        viewport = context.window.vm.getViewport(context.area)
        viewport.setRegionContext(context.region)

        settings = self.__getSettings()
        size = viewport.getSize(1, True)
        offset = 0
        self.__validateMode()
        active_gizmos = self.__getActive()
        for i, gizmo in enumerate(active_gizmos):
            bottom = gizmo.scale_basis * 4
            top = size.y - gizmo.scale_basis * 4
            offset = len(active_gizmos) * gizmo.scale_basis * 5 
            position = i * gizmo.scale_basis * 6 
            position = Vector((size.x/2 - offset/2 + position, bottom, 0))
            gizmo.matrix_basis = Matrix.Translation(position)

    def __validateMode(self):
        settings = self.__getSettings()
        mode = bpy.context.active_object.mode
        for name, gizmo, on_state, off_state in self.gizmo_actions:
            if name not in settings.gizmo_sets[mode] and name not in settings.gizmo_sets["ALL"] or mode not in settings.gizmo_sets or not getattr(settings, "show_"+name):
                gizmo.hide = True
            else:
                gizmo.hide = False

    def __getActive(self):
        active = []
        for g in self.gizmos:
            if not g.hide:
                active.append(g)
        return active

    def __getSettings(self):
        return bpy.context.screen.overlay_settings

    def __enableGizmo(self, gizmo:Gizmo):
        gizmo.hide_select = False
        gizmo.alpha = 0.3

    def __disableGizmo(self, gizmo:Gizmo):
        gizmo.hide_select = True
        gizmo.alpha = 0.1

    def __buildGizmo(self, name: str, operator_name: str, on_icon: str, off_icon: str = "") -> Gizmo:
        gizmo = self.gizmos.new("GIZMO_GT_button_2d")
        self.gizmo_actions.append((name, gizmo, on_icon, off_icon))
        gizmo.target_set_operator(operator_name)
        gizmo.icon = on_icon
        gizmo.draw_options = {'BACKDROP', 'OUTLINE'}
        self.__setColors(gizmo)
        gizmo.scale_basis = (80 * 0.35) / 2
        return gizmo
    
    def __setColors(self, gizmo):
        settings = self.__getSettings()
        gizmo.color = settings.gizmo_colors["active"]["color"]
        gizmo.color_highlight = settings.gizmo_colors["active"]["color_highlight"]
        gizmo.alpha = settings.gizmo_colors["active"]["alpha"]
        gizmo.alpha_highlight = settings.gizmo_colors["active"]["alpha_highlight"]

class ViewportRecenter(Operator):
    """ Recenter Viewport and Cursor on Selected Object """
    bl_idname = "view3d.viewport_recenter"
    bl_label = "Recenter Viewport and Cursor on Selected"

    def execute(self, context: Context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.view_center_cursor()
        return {'FINISHED'}

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

    row.label(text="Touchview Buttons")
    row = layout.row()

    col = row.column()
    col.prop(settings, 'show_quadview')
    col.prop(settings, 'show_snap_view')
    col.prop(settings, 'show_rotation_lock')
    col.prop(settings, 'show_voxel_resize')
    col.prop(settings, 'show_voxel_remesh')
