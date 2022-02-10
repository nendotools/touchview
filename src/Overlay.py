import bpy
from bpy.types import Area, Region, SpaceView3D
import math
from mathutils import Vector
import gpu
from bgl import glEnable, glDisable, GL_BLEND
from gpu_extras.batch import batch_for_shader

from . constants import OverlaySettings

class Overlay:
    meshes: list[object]

    def __init__(self):
        self.meshes = []

    def clear_overlays(self):
        for mesh in self.meshes:
            SpaceView3D.draw_handler_remove(mesh, 'WINDOW')
        self.meshes = []

    def __getSettings(self) -> OverlaySettings:
        return bpy.context.preferences.addons['touchview'].preferences

    def __getMidpoint(self, view: Region) -> Vector:
        return self.__getSize(view, 0.5)

    def __getSize(self, view:Region, scalar: float = 1) -> Vector:
        return Vector((view.width * scalar, view.height * scalar))

    def drawUI(self, view: Area):
        _handle = SpaceView3D.draw_handler_add(
            self.__renderCircle, 
            (view, (1,1,1,0.01)), 
            'WINDOW', 
            'POST_PIXEL'
        )
        self.meshes.append(_handle)

        _handle = SpaceView3D.draw_handler_add(
            self.__renderRailing, 
            (view, (1,1,1,0.01)), 
            'WINDOW', 
            'POST_PIXEL'
        )
        self.meshes.append(_handle)

    def __renderRailing(self, view: Area, color: tuple[float, float, float, float]):
        settings = self.__getSettings()
        if not settings.isVisible: return
        for region in view.regions:
            if bpy.context.region.as_pointer() == region.as_pointer():
                self.__makeBox(region, color)

    def __makeBox(self, view: Region, color: tuple[float, float, float, float]):
        settings = self.__getSettings()
        mid = self.__getMidpoint(view)
        dimensions = self.__getSize(view)
        left_rail = (
            Vector((0.0,0.0)), 
            Vector((mid.x*settings.getWidth(), dimensions.y))
        )
        right_rail = (
            Vector((dimensions.x, 0.0)), 
            Vector((dimensions.x - mid.x*settings.getWidth(), dimensions.y))
        )
        
        self.__drawVectorBox(left_rail[0], left_rail[1], color)
        self.__drawVectorBox(right_rail[0], right_rail[1], color)

    def __drawVectorBox(self, a, b, color):
        vertices = (
            (a.x,a.y),(b.x,a.y),
            (a.x,b.y),(b.x,b.y)
        )
        indices = ((0, 1, 2), (2, 3, 1))
        
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
        glEnable(GL_BLEND)
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
        glDisable(GL_BLEND)


    def __renderCircle(self, view: Area, color: tuple[float, float, float, float]):
        settings = self.__getSettings()
        if not settings.isVisible: return
        for region in view.regions:
            if bpy.context.region.as_pointer() == region.as_pointer() and not region.data.lock_rotation:
                self.__makeCircle(region, color)

    def __makeCircle(self, view: Region, color: tuple[float, float, float, float]):
        settings = self.__getSettings()
        mid = self.__getMidpoint(view)
        radius = math.dist((0,0), mid) * (settings.getRadius() * 0.5)
        self.__drawCircle(mid, radius, color)

    def __drawCircle(self, mid: Vector, radius:float, color: tuple):
        segments = 40
        vertices = [mid]
        indices = []
        p = 0
        for p in range(segments):
            if p > 0:
                point = Vector((
                    mid.x + radius * math.cos(math.radians(360/segments)*p),
                    mid.y + radius * math.sin(math.radians(360/segments)*p)
                ))
                vertices.append(point)
                indices.append((0,p-1, p))
        indices.append((0,1, p))
        
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
        glEnable(GL_BLEND)
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
        glDisable(GL_BLEND)

