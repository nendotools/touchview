from math import ceil, cos, radians, sin

import bpy
from bpy.types import GizmoGroup
from mathutils import Vector

from ..utils.addon import preferences
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
        self._build_controller(context)
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

    def _build_controller(self, context):
        self.controller = GizmoSet()
        self.controller.setup(self, controllerConfig)
        self.action_menu = GizmoSet()
        self.action_menu.setup(self, floatingConfig)
        self.toggle = GizmoSetBoolean()
        self.toggle.setup(self, floatingToggleConfig)

    def draw_prepare(self, context):
        self.context = context
        prefs = preferences()
        self._update_origin()
        self._update_action_origin()
        self._update_toggle_origin()
        self.toggle.draw_prepare()
        self.controller.draw_prepare()
        self.action_menu.draw_prepare()
        self._move_gizmo(self.controller, self.origin)
        self._move_gizmo(self.action_menu, self.action_origin)
        self._move_gizmo(self.toggle, self.toggle_origin)

        visible_gizmos = []
        for gizmo in self.gizmo_2d_sets:
            gizmo.draw_prepare()
            if gizmo.visible:
                visible_gizmos.append(gizmo)

        if prefs.menu_style == "float.radial":
            self._menu_radial(visible_gizmos)
        if prefs.menu_style == "fixed.bar":
            self._menu_bar(visible_gizmos)

    def _menu_bar(self, visible_gizmos: list[GizmoSet]):
        prefs = preferences()
        safe_area = safe_area_3d()
        spacing = ((36 * prefs.gizmo_scale) + 2 * prefs.gizmo_padding) * ui_scale()
        center = (safe_area[0] + safe_area[1]) / 2
        # keep the bottom corners free for the floating toggle and action menu
        bottom = safe_area[0].y + spacing

        # side bars stay in the lower half and below the navigation gizmo,
        # so they don't overlap Blender's own UI
        if prefs.gizmo_position in {"LEFT", "RIGHT"}:
            is_left = prefs.gizmo_position == "LEFT"
            top = center.y
            if not is_left:
                top = min(top, safe_area[1].y - navigation_gizmo_height() - spacing / 2)
            top = max(top, bottom)
            start = Vector(
                (
                    safe_area[0].x if is_left else safe_area[1].x,
                    (bottom + top) / 2,
                    0.0,
                )
            )
            axis = Vector((0.0, -1.0, 0.0))
            wrap = Vector((1.0 if is_left else -1.0, 0.0, 0.0))
            length = top - bottom
        else:
            is_top = prefs.gizmo_position == "TOP"
            start = Vector((center.x, safe_area[1].y if is_top else safe_area[0].y, 0.0))
            axis = Vector((1.0, 0.0, 0.0))
            wrap = Vector((0.0, -1.0 if is_top else 1.0, 0.0))
            length = safe_area[1].x - safe_area[0].x - 2 * spacing

        self._layout_lines(visible_gizmos, start, axis, wrap, length, spacing)

    # center gizmos along `axis` around `start`, wrapping onto new lines
    # (offset towards `wrap`) whenever a line would exceed `length`
    def _layout_lines(
        self,
        gizmos: list[GizmoSet],
        start: Vector,
        axis: Vector,
        wrap: Vector,
        length: float,
        spacing: float,
    ):
        per_line = max(1, int(length // spacing) + 1)
        for line in range(ceil(len(gizmos) / per_line)):
            row = gizmos[line * per_line : (line + 1) * per_line]
            offset = -(len(row) - 1) * spacing / 2
            for i, gizmo in enumerate(row):
                self._move_gizmo(gizmo, start + axis * (offset + i * spacing) + wrap * (line * spacing))

    def _menu_radial(self, visible_gizmos: list[GizmoSet]):
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
                self._calc_move(gizmo, i + 1, count, spacing)
                self._calc_move(visible_gizmos[i + 1], i, count, spacing)
                visible_gizmos[i + 1].skip_draw = True
            else:
                self._calc_move(gizmo, i, count, spacing)

    def _calc_move(self, gizmo: GizmoSet, step: int, size: int, spacing: float):
        distance = step / size
        offset = Vector(
            (
                sin(radians(distance * 360)),
                cos(radians(distance * 360)),
                0.0,
            )
        )
        self._move_gizmo(gizmo, self.origin + offset * spacing)

    def _update_origin(self):
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

    def _update_action_origin(self):
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

    def _update_toggle_origin(self):
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

    def _move_gizmo(self, gizmo: GizmoSet, position: Vector):
        gizmo.move(position)


classes = (GIZMO_GT_viewport_gizmo_group,)


register, unregister = bpy.utils.register_classes_factory(classes)
