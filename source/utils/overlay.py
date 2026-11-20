import math

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from .addon import preferences


def _prefs():
    """Add-on preferences, or None while the add-on is (un)registering."""
    try:
        return preferences()
    except KeyError:
        return None


class Overlay:
    def __init__(self):
        self.meshes = []

    def clear_overlays(self):
        for mesh in self.meshes:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(mesh, "WINDOW")
            except (ValueError, RuntimeError):
                pass
        self.meshes = []

    def draw_ui(self):
        self.meshes.append(bpy.types.SpaceView3D.draw_handler_add(self._render_circle, (), "WINDOW", "POST_PIXEL"))
        self.meshes.append(bpy.types.SpaceView3D.draw_handler_add(self._render_railing, (), "WINDOW", "POST_PIXEL"))

    def _render_railing(self):
        prefs = _prefs()
        if prefs is None or not prefs.show_overlay:
            return

        view = bpy.context.area
        current = bpy.context.region
        if view is None or current is None:
            return
        for region in view.regions:
            if current.as_pointer() == region.as_pointer():
                self._make_box(region, self._get_colors("main"))

    def _make_box(self, view: bpy.types.Region, color: tuple[float, float, float, float]):
        prefs = _prefs()
        if prefs is None:
            return
        mid = self._get_midpoint(view)
        dimensions = self._get_size(view)
        left_rail = (
            Vector((0.0, 0.0)),
            Vector((mid.x * prefs.get_width(), dimensions.y)),
        )
        right_rail = (
            Vector((dimensions.x, 0.0)),
            Vector((dimensions.x - mid.x * prefs.get_width(), dimensions.y)),
        )

        self._draw_vector_box(left_rail[0], left_rail[1], color)
        self._draw_vector_box(right_rail[0], right_rail[1], color)

    def _draw_vector_box(self, a, b, color):
        vertices = ((a.x, a.y), (b.x, a.y), (a.x, b.y), (b.x, b.y))
        indices = ((0, 1, 2), (2, 3, 1))

        self._draw_geometry(vertices, indices, color, "TRIS")

    def _render_circle(self):
        prefs = _prefs()
        if prefs is None or not prefs.show_overlay:
            return

        view = bpy.context.area
        current = bpy.context.region
        if view is None or current is None:
            return
        for region in view.regions:
            if current.as_pointer() == region.as_pointer() and not region.data.lock_rotation:
                self._make_circle(region, self._get_colors("secondary"))

    def _make_circle(self, view: bpy.types.Region, color: tuple[float, float, float, float]):
        prefs = _prefs()
        if prefs is None:
            return
        mid = self._get_midpoint(view)
        radius = math.dist((0, 0), mid) * (prefs.get_radius() * 0.5)  # type: ignore
        self._draw_circle(mid, radius, color)

    def _draw_circle(self, mid: Vector, radius: float, color: tuple):
        segments = 100
        vertices = [mid]
        indices = []
        p = 0
        for p in range(segments):
            if p > 0:
                point = Vector(
                    (
                        mid.x + radius * math.cos(math.radians(360 / segments) * p),
                        mid.y + radius * math.sin(math.radians(360 / segments) * p),
                    )
                )
                vertices.append(point)
                indices.append((0, p - 1, p))
        indices.append((0, 1, p))

        self._draw_geometry(vertices, indices, color, "TRIS")

    def _draw_geometry(self, vertices, indices, color, draw_type):
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        batch = batch_for_shader(shader, draw_type, {"pos": vertices}, indices=indices)
        shader.bind()
        gpu.state.blend_set("ALPHA")
        shader.uniform_float("color", color)
        batch.draw(shader)

    def _get_midpoint(self, view: bpy.types.Region) -> Vector:
        return self._get_size(view, 0.5)

    def _get_size(self, view: bpy.types.Region, scalar: float = 1) -> Vector:
        return Vector((view.width * scalar, view.height * scalar))

    def _get_colors(self, color_type: str):
        prefs = _prefs()
        if prefs is None or (not prefs.is_enabled and not prefs.lazy_mode):
            return (0.0, 0.0, 0.0, 0.0)
        if color_type == "main" or not prefs.use_multiple_colors:
            return prefs.overlay_main_color
        elif color_type == "secondary":
            return prefs.overlay_secondary_color
        else:
            return (0.0, 0.0, 0.0, 0.0)
