import bpy
from mathutils import Matrix, Vector
from bpy.types import Context, Gizmo, GizmoGroup, bpy_prop_collection
from .items import pivot_items, pivot_icon_items

def dpi_factor() -> float:
    systemPreferences = bpy.context.preferences.system
    retinaFactor = getattr(systemPreferences, "pixel_size", 1)
    return int(systemPreferences.dpi * retinaFactor) / 72

def panel(type) -> tuple:
    ''' Panel in the region.
    
    type (enum in ['WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS', 'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE', 'FOOTER', 'TOOL_HEADER', 'XR']) - Type of the region.
    return (tuple) - Dimension of the region.
    '''
    width = 0
    height = 0
    for region in bpy.context.area.regions:
        if region.type == type:
            width = region.width
            height = region.height
    return (width, height)

######
###     CREATE GIZMO GROUP FOR FLOATING ACTION SET
######
class GIZMO_GT_FloatingGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_float_tool"
    bl_label = "Customizable floating viewport button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    def setup(self, context: Context):
        settings = context.preferences.addons['touchview'].preferences

        self.__buildGizmo("wm.call_menu_pie","SETTINGS")

    def draw_prepare(self, context: Context):
        region = context.region
        settings = self.__getSettings()
        size = Vector((region.width, region.height))

        position = self.__getGizmoOrientation(size)
        offset = 0
        gap = 2.2
        gizmo = self.gizmos[0]
        gizmo.matrix_basis = Matrix.Translation(position[0] + Vector(position[1]) * offset)
        offset += gizmo.scale_basis * 2 + gap
        if not context.space_data.show_gizmo_navigate or not settings.show_float_menu: gizmo.hide = True
        else: gizmo.hide = False

    # initialize each gizmo, add them to named list with icon name(s)
    def __buildGizmo(self, operator_name: str, on_icon: str) -> Gizmo:
        gizmo = self.gizmos.new("GIZMO_GT_button_2d")
        props = gizmo.target_set_operator(operator_name)
        props.name = "PIE_MT_Floating_Menu"
        gizmo.icon = on_icon
        gizmo.use_event_handle_all = True
        gizmo.draw_options = {'BACKDROP', 'OUTLINE'}
        self.__setColors(gizmo)
        gizmo.scale_basis = 14
        return gizmo

    # determine viewport position and spacing
    def __getGizmoOrientation(self, size:Vector) -> tuple[Vector, tuple[int, int]]:
        settings = self.__getSettings()
        position = (0.0,0.0,0.0)
        orientation = (0.0,0.0,0.0)
        fence = ((0,0), (size.x, size.y))

        position = (settings.floating_position[0]/100 * fence[1][0], settings.floating_position[1]/100 * fence[1][1],0)

#        if settings.gizmo_position == 'TOP':
#            position = (size.x / 2 - (gizmo_bar / 2 * dpi_factor()), size.y - (panel('HEADER')[1] + panel('TOOL_HEADER')[1]), 0)
#
#        elif settings.gizmo_position == 'RIGHT':
#            if bpy.context.preferences.view.mini_axis_type == 'GIZMO':
#                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - (171.2 + bpy.context.preferences.view.gizmo_size_navigate_v3d) * dpi_factor(), 0)
#            elif bpy.context.preferences.view.mini_axis_type == 'MINIMAL':
#                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - ((196.2 + bpy.context.preferences.view.mini_axis_size) + bpy.context.preferences.view.mini_axis_size) * dpi_factor(), 0)
#            else:
#                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - 168.2 * dpi_factor(), 0)
#
#        elif settings.gizmo_position == 'BOTTOM':
#            position = (size.x / 2 - (gizmo_bar / 2 * dpi_factor()), 22 * dpi_factor(), 0)
#
#        elif settings.gizmo_position == 'LEFT':
#            position = (22 * dpi_factor() + panel('TOOLS')[0], size.y / 2 + (gizmo_bar / 2 * dpi_factor()), 0)

        return (Vector(position), orientation)
    
    # fetch colors from config and assign to gizmo
    def __setColors(self, gizmo):
        settings = self.__getSettings()
        gizmo.color = settings.gizmo_colors["active"]["color"]
        gizmo.color_highlight = settings.gizmo_colors["active"]["color_highlight"]
        gizmo.alpha = settings.gizmo_colors["active"]["alpha"]
        gizmo.alpha_highlight = settings.gizmo_colors["active"]["alpha_highlight"]

    # get settings pointer
    def __getSettings(self):
        return bpy.context.preferences.addons['touchview'].preferences


class GIZMO_GT_ViewportGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_touch_tools"
    bl_label = "Fast access tools for touch viewport"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    gizmo_actions: list[tuple[str, list[Gizmo], str, str]]

    # set up gizmo collection
    def setup(self, context: Context):
        self.gizmo_actions = []
        self.floating_actions = []

        self.__buildGizmo("fullscreen", "screen.screen_full_area", "FULLSCREEN_EXIT", "FULLSCREEN_ENTER", "show_fullscreen",  "screen")
        self.__buildGizmo("quadview", "screen.region_quadview", "IMGDISPLAY", "MESH_PLANE", "region_quadviews", context.space_data)
        self.__buildGizmo("snap_view", "view3d.viewport_recenter", "CURSOR")
        self.__buildEnumGizmo("pivot_mode", "view3d.step_pivot_mode", pivot_items, pivot_icon_items, "pivot_mode", context.preferences.addons["touchview"].preferences)
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
        offset = 0
        gap = 2.2
        for gizmo in active_gizmos:
            gizmo.matrix_basis = Matrix.Translation(position[0] + Vector(position[1]) * offset)
            offset += gizmo.scale_basis * 2 + gap
            if not context.space_data.show_gizmo_navigate:
                gizmo.hide = True

    # determine viewport position and spacing
    def __getGizmoOrientation(self, size:Vector) -> tuple[Vector, tuple[int, int]]:
        settings = self.__getSettings()
        active_gizmos = self.__getActive()
        gap = 2.2
        position = (0.0,0.0,0.0)
        orientation = (0.0,0.0,0.0)
        gizmo_bar = 0.0

        for gizmo in active_gizmos:
            gizmo_bar = (gizmo.scale_basis * 2 * len(active_gizmos) + (2.2 * len(active_gizmos) - 32 + gap))

        if settings.gizmo_position == 'TOP':
            position = (size.x / 2 - (gizmo_bar / 2 * dpi_factor()), size.y - (panel('HEADER')[1] + panel('TOOL_HEADER')[1]), 0)
            orientation = (1 * dpi_factor(), 0, 0)

        elif settings.gizmo_position == 'RIGHT':
            if bpy.context.preferences.view.mini_axis_type == 'GIZMO':
                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - (171.2 + bpy.context.preferences.view.gizmo_size_navigate_v3d) * dpi_factor(), 0)
            elif bpy.context.preferences.view.mini_axis_type == 'MINIMAL':
                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - ((196.2 + bpy.context.preferences.view.mini_axis_size) + bpy.context.preferences.view.mini_axis_size) * dpi_factor(), 0)
            else:
                position = (size.x - (panel('UI')[0] + 22 * dpi_factor()), size.y - 168.2 * dpi_factor(), 0)
            orientation = (0, -1 * dpi_factor(), 0)

        elif settings.gizmo_position == 'BOTTOM':
            position = (size.x / 2 - (gizmo_bar / 2 * dpi_factor()), 22 * dpi_factor(), 0)
            orientation = (1 * dpi_factor(), 0, 0)

        elif settings.gizmo_position == 'LEFT':
            position = (22 * dpi_factor() + panel('TOOLS')[0], size.y / 2 + (gizmo_bar / 2 * dpi_factor()), 0)
            orientation = (0, -1 * dpi_factor(), 0)

        return (Vector(position), orientation)

    # initialize each gizmo, add them to named list with icon name(s)
    def __buildGizmo(self, name: str, operator_name: str, on_icon: str, off_icon: str = "", watch_var:str = "", source = None, sub:bool = False) -> Gizmo:
        gizmo = self.gizmos.new("GIZMO_GT_button_2d")
        gizmo.target_set_operator(operator_name)
        gizmo.icon = on_icon
        gizmo.use_event_handle_all = True
        gizmo.draw_options = {'BACKDROP', 'OUTLINE'}
        self.__setColors(gizmo)
        gizmo.scale_basis = 14
        if sub: return gizmo

        group = [gizmo]
        if off_icon != "":
            off_gizmo = self.__buildGizmo(name, operator_name, off_icon, "", watch_var, source, True)
            group.append(off_gizmo)

        self.gizmo_actions.append((name, group, on_icon, off_icon, watch_var, source))
        return gizmo

    # initialize set of gizmos from enum list, add them to named list with icon name(s)
    def __buildEnumGizmo(self, name: str, operator_name: str, gizmo_list:list, gizmo_icons:list, watch_var:str, source) -> Gizmo:
        group = []
        for state in gizmo_list:
            icon = next((icon for icon in gizmo_icons if icon[0] == state[0]), ["","",""])
            gizmo = self.gizmos.new("GIZMO_GT_button_2d")
            gizmo.target_set_operator(operator_name)
            gizmo.icon = icon[1]
            gizmo.use_event_handle_all = True
            gizmo.draw_options = {'BACKDROP', 'OUTLINE'}
            self.__setColors(gizmo)
            gizmo.scale_basis = 14
            group.append(gizmo)
        self.gizmo_actions.append((name, group, gizmo_list, gizmo_icons, watch_var, source))
        return 

    # determine if each gizmo should be visible based on what edit mode is being used and toggle states
    def __validateMode(self):
        settings = self.__getSettings()
        mode = bpy.context.active_object.mode
        for name, gizmos, on_state, off_state, watch_var, source in self.gizmo_actions:
            if name not in settings.gizmo_sets[mode] and name not in settings.gizmo_sets["ALL"] or mode not in settings.gizmo_sets or not getattr(settings, "show_"+name):
                for gizmo in gizmos:
                    gizmo.hide = True
                    continue
            else:
                for gizmo in gizmos:
                    gizmo.hide = True
                    gizmo.hide = False

            if watch_var != "" and source is not None:
                # fix added to support string source from context changes to viewport
                if isinstance(source, str):
                    source = getattr(bpy.context, source)

                # Handle Boolean state toggling
                if len(gizmos) < 3:
                    data = getattr(source, watch_var)

                    for i, gizmo in enumerate(gizmos):
                        if type(data) == bpy_prop_collection:
                            if (len(data) == 0) == bool(i): gizmo.hide = True
                            else: gizmo.hide = False
                        else:
                            if data == bool(i): gizmo.hide = True
                            else: gizmo.hide = False

                # Handle Enum state toggling
                else: 
                    data = getattr(source, watch_var)

                    for i, gizmo in enumerate(gizmos):
                        gizmo.hide = True
                        icon = [icon for icon in off_state if icon[1] == gizmo.icon][0]
                        if icon[0] == data:
                            gizmo.hide = False

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
def touch_gizmo_display(panel, context:Context):
    layout = panel.layout

    col = layout.column()
    col.active = context.space_data.show_gizmo
    col.separator()

    col.label(text="Touch Gizmos")
    settings = bpy.context.preferences.addons['touchview'].preferences
    available_gizmos = settings.getGizmoSet(context.object.mode)

    for toggle in available_gizmos:
        col.prop(settings, 'show_'+toggle)
