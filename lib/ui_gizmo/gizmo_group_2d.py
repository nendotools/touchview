from math import cos, radians, sin

from bpy.types import Context, GizmoGroup
from mathutils import Vector

from ..utils import buildSafeArea, dpi_factor, get_settings
from .gizmo_2d import GizmoSet, GizmoSetBoolean
from .gizmo_config import *

__module__ = __name__.split('.')[0]


configs = [
    undoConfig, redoConfig, touchViewConfig, controlGizmoConfig,
    snapViewConfig, fullscreenToggleConfig, quadviewToggleConfig,
    rotLocToggleConfig, nPanelConfig, voxelSizeConfig, voxelRemeshConfig,
    voxelStepDownConfig, voxelStepUpConfig,
    subdivConfig, unsubdivConfig, brushResizeConfig, brushStrengthConfig
]

###
# GizmoGroup
#  - hold reference to available Gizmos
#  - generate new Gizmos
#  - position Gizmos during draw_@prepare()
#
# Gizmo
#  - hold Icon (cannot change)
#  - set color
#  - set visible
#
# 2DGizmo (Custom Gizmo definition)
#  - holds reference to Gizmos for related action
#  - position applied to references
#  - hold state to determine what icons,actions to provide
#  - applies color and visibility based on settings
#
###


class GIZMO_GT_ViewportGizmoGroup(GizmoGroup):
    bl_idname = "GIZMO_GT_touch_tools"
    bl_label = "Fast access tools for touch viewport"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    # set up gizmo collection
    def setup(self, context: Context):
        self.gizmo_2d_sets = []
        self.__buildController(context)
        settings = get_settings()
        self.spacing = settings.menu_spacing
        for conf in configs:
            if conf['type'] == "boolean":
                gizmo = GizmoSetBoolean()
                gizmo.setup(self, conf)
            else:  # assume Type = Default
                gizmo = GizmoSet()
                gizmo.setup(self, conf)
            self.gizmo_2d_sets.append(gizmo)

    def __buildController(self, _: Context):
        self.controller = GizmoSet()
        self.controller.setup(self, controllerConfig)
        self.action_menu = GizmoSet()
        self.action_menu.setup(self, floatingConfig)
        self.toggle = GizmoSetBoolean()
        self.toggle.setup(self, floatingToggleConfig)

    def draw_prepare(self, context: Context):
        self.context = context
        settings = get_settings()
        self.__updateOrigin()
        self.__updateActionOrigin()
        self.__updateToggleOrigin()
        self.toggle.draw_prepare()
        self.controller.draw_prepare()
        self.action_menu.draw_prepare()
        self.__move_gizmo(self.controller, self.origin)
        self.__move_gizmo(self.action_menu, self.action_origin)
        self.__move_gizmo(self.toggle, self.toggle_origin)

        visible_gizmos = []
        for gizmo in self.gizmo_2d_sets:
            gizmo.draw_prepare()
            if gizmo.visible:
                visible_gizmos.append(gizmo)

        if settings.menu_style == 'float.radial':
            self.__menuRadial(visible_gizmos)
        if settings.menu_style == 'fixed.bar':
            self.__menuBar(visible_gizmos)

    def __menuBar(self, visible_gizmos: list[GizmoSet]):
        settings = get_settings()
        origin = self.origin
        scalar = 22 * dpi_factor()
        count = len(visible_gizmos)
        safe_area = buildSafeArea()
        origin = Vector(((safe_area[0].x + safe_area[1].x) / 2,
                            (safe_area[0].y + safe_area[1].y) / 2, 0.0))

        if settings.gizmo_position == 'TOP':
            origin.y = safe_area[1].y
        elif settings.gizmo_position == 'BOTTOM':
            origin.y = safe_area[0].y
        else:
            if settings.gizmo_position == 'LEFT':
                origin.x = safe_area[0].x
            elif settings.gizmo_position == 'RIGHT':
                origin.x = safe_area[1].x

        gizmo_spacing = (settings.menu_spacing + scalar)
        if ((settings.gizmo_position in ['TOP', 'BOTTOM']
            and settings.menu_style == 'fixed.bar')):
            start = origin.x - ((count - 1) * gizmo_spacing) / 2
            for i, gizmo in enumerate(visible_gizmos):
                self.__move_gizmo(
                    gizmo, Vector((start + (i * gizmo_spacing), origin.y, 0.0)))
        else:
            start = origin.y + (count * gizmo_spacing) / 2
            for i, gizmo in enumerate(visible_gizmos):
                self.__move_gizmo(
                    gizmo, Vector((origin.x, start - (i * gizmo_spacing), 0.0)))

    def __menuRadial(self, visible_gizmos: list[GizmoSet]):
        settings = get_settings()
        # calculate minimum radius to prevent overlapping buttons
        gui_scale = dpi_factor() * 3
        radial_size = (gui_scale + settings.menu_spacing)
        spacing = radial_size + (gui_scale * settings.gizmo_scale) + settings.gizmo_padding

        count = len(visible_gizmos)
        # reposition Gizmos to origin
        for i, gizmo in enumerate(visible_gizmos):
            if gizmo.skip_draw:
                continue

            if gizmo.has_dependent and i > count / 2:
                self.__calcMove(gizmo, i + 1, count, spacing)
                self.__calcMove(visible_gizmos[i + 1], i, count, spacing)
                visible_gizmos[i + 1].skip_draw = True
            else:
                self.__calcMove(gizmo, i, count, spacing)

    def __calcMove(self, gizmo: GizmoSet, step: int, size: int,
                   spacing: float):
        distance = step / size
        offset = Vector(
            (sin(radians(distance * 360)), cos(radians(distance * 360)), 0.0))
        self.__move_gizmo(gizmo, self.origin + offset * spacing)

    def __updateOrigin(self):
        safe_area = buildSafeArea()
        settings = get_settings()

        # distance across viewport between menus
        span = Vector(
            (safe_area[1].x - safe_area[0].x, safe_area[1].y - safe_area[0].y))

        # apply position ratio to safe area
        self.origin = Vector(
            (safe_area[0].x + span.x * settings.menu_position[0] * 0.01,
             safe_area[0].y + span.y * settings.menu_position[1] * 0.01, 0.0))

    def __updateActionOrigin(self):
        safe_area = buildSafeArea()
        settings = get_settings()

        # distance across viewport between menus
        span = Vector(
            (safe_area[1].x - safe_area[0].x, safe_area[1].y - safe_area[0].y))

        # apply position ratio to safe area
        self.action_origin = Vector(
            (safe_area[0].x + span.x * settings.floating_position[0] * 0.01,
             safe_area[0].y + span.y * settings.floating_position[1] * 0.01,
             0.0))

    def __updateToggleOrigin(self):
        safe_area = buildSafeArea()
        settings = get_settings()

        # distance across viewport between menus
        span = Vector(
            (safe_area[1].x - safe_area[0].x, safe_area[1].y - safe_area[0].y))

        # apply position ratio to safe area
        self.toggle_origin = Vector(
            (safe_area[0].x + span.x * settings.toggle_position[0] * 0.01,
             safe_area[0].y + span.y * settings.toggle_position[1] * 0.01,
             0.0))

    def __move_gizmo(self, gizmo: GizmoSet, position: Vector):
        gizmo.move(position)
