import bpy
from mathutils import Matrix, Vector
from bpy.types import Context, Gizmo, GizmoGroup, Operator, bpy_prop_collection

class ViewportGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_navigate_lock"
    bl_label = "Tools Region Swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    gizmo_actions: list[tuple[str, Gizmo, str, str]]

    # set up gizmo collection
    def setup(self, context: Context):
        self.gizmo_actions = []
        self.__buildGizmo("fullscreen", "screen.screen_full_area", "FULLSCREEN_EXIT", "FULLSCREEN_ENTER", "show_fullscreen",  bpy.context.screen)
        self.__buildGizmo("quadview", "screen.region_quadview", "IMGDISPLAY", "MESH_PLANE", "region_quadviews", context.space_data)
        self.__buildGizmo("snap_view", "view3d.viewport_recenter", "CURSOR")
        self.__buildGizmo("n_panel", "view3d.toggle_n_panel", "EVENT_N")
        self.__buildGizmo("rotation_lock", "view3d.viewport_lock", "LOCKED", "UNLOCKED", "lock_rotation", context.region_data)
        self.__buildGizmo("voxel_resize", "object.voxel_size_edit", "MESH_GRID")
        self.__buildGizmo("voxel_remesh", "object.voxel_remesh", "MOD_UVPROJECT")
 
    # handle redraw call
    def draw_prepare(self, context:Context):
        region = context.region
        size = Vector((region.width, region.height))
        self.__validateMode()
        active_gizmos = self.__getActive()

        position = self.__getGizmoOrientation(size)
        for i, gizmo in enumerate(active_gizmos):
            gizmo_bar = (len(active_gizmos) * gizmo.scale_basis * -5)/2
            offset = gizmo_bar + i * gizmo.scale_basis * 6
            gizmo.matrix_basis = Matrix.Translation(position[0] + Vector(position[1])*offset)

    # determine viewport position and spacing
    def __getGizmoOrientation(self, size:Vector) -> tuple[Vector, tuple[int, int]]:
        position = (0,0,0)
        settings = self.__getSettings()
        scale_basis = (80 * 0.35) / 2
        orientation = (0,0,0)

        if settings.gizmo_position == "BOTTOM":
            position = ( size.x/2, scale_basis * 4, 0)
            orientation = (1,0,0)
        elif settings.gizmo_position == "TOP":
            position = (size.x/2, size.y - scale_basis * 4, 0)
            orientation = (1,0,0)
        elif settings.gizmo_position == "LEFT":
            position = (scale_basis * 4, size.y/2, 0)
            orientation = (0,1,0)
        elif settings.gizmo_position == "RIGHT":
            position = (size.x - scale_basis * 4, size.y/2, 0)
            orientation = (0,1,0)

        return (Vector(position), orientation)

    # initialize each gizmo, add them to named list with icon name(s)
    def __buildGizmo(self, name: str, operator_name: str, on_icon: str, off_icon: str = "", watch_var:str = "", source = None) -> Gizmo:
        if off_icon != "":
            self.__buildGizmo(name, operator_name, off_icon, "", watch_var, source)
        gizmo = self.gizmos.new("GIZMO_GT_button_2d")
        self.gizmo_actions.append((name, gizmo, on_icon, off_icon, watch_var, source))
        gizmo.target_set_operator(operator_name)
        gizmo.icon = on_icon
        gizmo.use_event_handle_all = True
        gizmo.draw_options = {'BACKDROP', 'OUTLINE'}
        self.__setColors(gizmo)
        gizmo.scale_basis = (80 * 0.35) / 2
        return gizmo

    # determine if each gizmo should be visible based on what edit mode is being used and toggle states
    def __validateMode(self):
        settings = self.__getSettings()
        mode = bpy.context.active_object.mode
        for name, gizmo, on_state, off_state, watch_var, source in self.gizmo_actions:
            if name not in settings.gizmo_sets[mode] and name not in settings.gizmo_sets["ALL"] or mode not in settings.gizmo_sets or not getattr(settings, "show_"+name):
                gizmo.hide = True
                continue
            else:
                gizmo.hide = False

            if watch_var != "" and source is not None:
                data = getattr(source, watch_var)
                state = (off_state == "")

                if type(data) == bpy_prop_collection:
                    if (len(data) == 0) == state: gizmo.hide = True
                    else: gizmo.hide = False
                else:
                    if data == state: gizmo.hide = True
                    else: gizmo.hide = False

    # build list of active gizmos to begin draw step
    def __getActive(self):
        active = []
        for g in self.gizmos:
            if not g.hide:
                active.append(g)
        return active

    # get settings pointer
    def __getSettings(self):
        return bpy.context.preferences.addons['touchview'].preferences
    
    # fetch colors from config and assign to gizmo
    def __setColors(self, gizmo):
        settings = self.__getSettings()
        gizmo.color = settings.gizmo_colors["active"]["color"]
        gizmo.color_highlight = settings.gizmo_colors["active"]["color_highlight"]
        gizmo.alpha = settings.gizmo_colors["active"]["alpha"]
        gizmo.alpha_highlight = settings.gizmo_colors["active"]["alpha_highlight"]

    # UI panel to append Gizmo menu
def gizmo_toggle(panel, context:Context):
    layout = panel.layout
    settings = bpy.context.preferences.addons['touchview'].preferences
    row = layout.row()
    col = row.column()
    col.label(text="Touchview Buttons")
    col.prop(settings, 'show_fullscreen')
    col.prop(settings, 'show_quadview')
    col.prop(settings, 'show_snap_view')
    col.prop(settings, 'show_n_panel')
    col.prop(settings, 'show_rotation_lock')
    col.prop(settings, 'show_voxel_resize')
    col.prop(settings, 'show_voxel_remesh')

class ViewportRecenter(Operator):
    """ Recenter Viewport and Cursor on Selected Object """
    bl_idname = "view3d.viewport_recenter"
    bl_label = "Recenter Viewport and Cursor on Selected"

    def execute(self, context: Context):
        current = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = "ACTIVE_ELEMENT"
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.view_center_cursor()
        bpy.ops.view3d.view_selected()
        context.scene.tool_settings.transform_pivot_point = current
        return {'FINISHED'}

class ViewportLock(Operator):
    """ Toggle Viewport Rotation """
    bl_idname = "view3d.viewport_lock"
    bl_label = "Viewport rotation lock toggle"

    def execute(self, context: Context):
        if len(context.area.spaces.active.region_quadviews) == 0:
            context.region.data.lock_rotation^=True
            return {'FINISHED'}

        context.region.data.lock_rotation=False
        return {'FINISHED'}
