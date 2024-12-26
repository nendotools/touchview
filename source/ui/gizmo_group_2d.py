import bpy
from bpy.types import GizmoGroup

from math import cos, radians, sin
from mathutils import Vector

from ..utils.blender import *
from .gizmo_2d import GizmoSet, GizmoSetBoolean
from .gizmo_config import (
    brushResizeConfig,
    brushStrengthConfig,
    controlGizmoConfig,
    controllerConfig,
    floatingConfig,
    floatingToggleConfig,
    fullscreenToggleConfig,
    nPanelConfig,
    quadviewToggleConfig,
    redoConfig,
    rotLocToggleConfig,
    snapViewConfig,
    subdivConfig,
    touchViewConfig,
    undoConfig,
    unsubdivConfig,
    voxelRemeshConfig,
    voxelSizeConfig,
    voxelStepDownConfig,
    voxelStepUpConfig,
)

__module__ = __name__.split(".")[0]


configs = [
    undoConfig,
    redoConfig,
    touchViewConfig,
    controlGizmoConfig,
    snapViewConfig,
    fullscreenToggleConfig,
    quadviewToggleConfig,
    rotLocToggleConfig,
    nPanelConfig,
    voxelSizeConfig,
    voxelRemeshConfig,
    voxelStepDownConfig,
    voxelStepUpConfig,
    subdivConfig,
    unsubdivConfig,
    brushResizeConfig,
    brushStrengthConfig,
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
#  - applies color and visibility based on prefs
#
###


class GIZMO_GT_viewport_gizmo_group(GizmoGroup):
    bl_label = "Fast access tools for touch viewport"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {"PERSISTENT", "SCALE"}

    # set up gizmo collection
    def setup(self, context):
        self.gizmo_2d_sets = []
        self.__buildController(context)
        prefs = preferences()
        self.spacing = prefs.menu_spacing
        for conf in configs:
            if conf["type"] == "boolean":
                gizmo = GizmoSetBoolean()
                gizmo.setup(self, conf)
            else:  # assume Type = Default
                gizmo = GizmoSet()
                gizmo.setup(self, conf)
            self.gizmo_2d_sets.append(gizmo)

    def __buildController(self, context):
        self.controller = GizmoSet()
        self.controller.setup(self, controllerConfig)
        self.action_menu = GizmoSet()
        self.action_menu.setup(self, floatingConfig)
        self.toggle = GizmoSetBoolean()
        self.toggle.setup(self, floatingToggleConfig)

    def draw_prepare(self, context):
        self.context = context
        prefs = preferences()
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

        if prefs.menu_style == "float.radial":
            self.__menuRadial(visible_gizmos)
        if prefs.menu_style == "fixed.bar":
            self.__menuBar(visible_gizmos)

    def __menuBar(self, visible_gizmos: list[GizmoSet]):
        prefs = preferences()
        origin = self.origin
        count = len(visible_gizmos)
        safe_area = safe_area_3d()
        origin = Vector(
            (
                (safe_area[0].x + safe_area[1].x) / 2,
                (safe_area[0].y + safe_area[1].y) / 2,
                0.0,
            )
        )

        if prefs.gizmo_position == "TOP":
            origin.y = safe_area[1].y
        elif prefs.gizmo_position == "BOTTOM":
            origin.y = safe_area[0].y
        elif prefs.gizmo_position == "LEFT":
            origin.x = safe_area[0].x
        elif prefs.gizmo_position == "RIGHT":
            origin.x = safe_area[1].x  # - 54  # to avoid overlapping

        gizmo_scale = (36 * prefs.gizmo_scale) + prefs.gizmo_padding
        gizmo_padding = prefs.gizmo_padding
        spacing = (gizmo_scale + gizmo_padding) * ui_scale()

        if prefs.gizmo_position in {"TOP", "BOTTOM"} and prefs.menu_style == "fixed.bar":
            start = origin.x - ((count - 1) * spacing) / 2
            for i, gizmo in enumerate(visible_gizmos):
                self.__move_gizmo(gizmo, Vector((start + (i * spacing), origin.y, 0.0)))
        else:
            start = origin.y + (count * spacing) / 2
            for i, gizmo in enumerate(visible_gizmos):
                self.__move_gizmo(gizmo, Vector((origin.x, start - (i * spacing), 0.0)))

    def __menuRadial(self, visible_gizmos: list[GizmoSet]):
        prefs = preferences()
        # calculate minimum radius to prevent overlapping buttons
        menu_spacing = (36 * prefs.menu_spacing) * prefs.gizmo_scale + prefs.gizmo_padding
        gizmo_scale = 18 * prefs.gizmo_scale
        gizmo_padding = prefs.gizmo_padding
        spacing = (menu_spacing + gizmo_scale + gizmo_padding) * ui_scale()

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

    def __calcMove(self, gizmo: GizmoSet, step: int, size: int, spacing: float):
        distance = step / size
        offset = Vector(
            (
                sin(radians(distance * 360)),
                cos(radians(distance * 360)),
                0.0,
            )
        )
        self.__move_gizmo(gizmo, self.origin + offset * spacing)

    def __updateOrigin(self):
        prefs = preferences()
        safe_area = safe_area_3d(padding=90)

        # distance across viewport between menus
        span = Vector(
            (
                safe_area[1].x - safe_area[0].x,
                safe_area[1].y - safe_area[0].y,
            )
        )

        # apply position ratio to safe area
        self.origin = Vector(
            (
                safe_area[0].x + span.x * prefs.menu_position[0] * 0.01,
                safe_area[0].y + span.y * prefs.menu_position[1] * 0.01,
                0.0,
            )
        )

    def __updateActionOrigin(self):
        prefs = preferences()
        safe_area = safe_area_3d()

        # distance across viewport between menus
        span = Vector(
            (
                safe_area[1].x - safe_area[0].x,
                safe_area[1].y - safe_area[0].y,
            )
        )

        # apply position ratio to safe area
        self.action_origin = Vector(
            (
                safe_area[0].x + span.x * prefs.floating_position[0] * 0.01,
                safe_area[0].y + span.y * prefs.floating_position[1] * 0.01,
                0.0,
            )
        )

    def __updateToggleOrigin(self):
        prefs = preferences()
        safe_area = safe_area_3d()

        # distance across viewport between menus
        span = Vector(
            (
                safe_area[1].x - safe_area[0].x,
                safe_area[1].y - safe_area[0].y,
            )
        )

        # apply position ratio to safe area
        self.toggle_origin = Vector(
            (
                safe_area[0].x + span.x * prefs.toggle_position[0] * 0.01,
                safe_area[0].y + span.y * prefs.toggle_position[1] * 0.01,
                0.0,
            )
        )

    def __move_gizmo(self, gizmo: GizmoSet, position: Vector):
        gizmo.move(position)


classes = (GIZMO_GT_viewport_gizmo_group,)


register, unregister = bpy.utils.register_classes_factory(classes)
