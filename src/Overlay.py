import bpy
from bpy.types import Area, Region, SpaceView3D
import math
from mathutils import Vector
import gpu
from bgl import glEnable, glDisable, GL_BLEND
from gpu_extras.batch import batch_for_shader

class Overlay:
    def __init__(self):
        self.meshes = []

    def clear_overlays(self):
        for mesh in self.meshes:
            SpaceView3D.draw_handler_remove(mesh, 'WINDOW')
        self.meshes = []

    def getMidpoint(self, view: Region) -> Vector:
        return self.getSize(view, 0.5)

    def getSize(self, view:Region, scalar: float = 1) -> Vector:
        return Vector((view.width * scalar, view.height * scalar))

    def drawUI(self, view: Area):
        _handle = SpaceView3D.draw_handler_add(
            self.renderCircle, 
            (view, (1,1,1,0.01)), 
            'WINDOW', 
            'POST_PIXEL'
        )
        self.meshes.append(_handle)
        _handle = SpaceView3D.draw_handler_add(
            self.renderRailing, 
            (view, (1,1,1,0.01)), 
            'WINDOW', 
            'POST_PIXEL'
        )
        self.meshes.append(_handle)

    def renderRailing(self, view: Area, color: tuple):
        settings = bpy.context.screen.overlay_settings
        if not settings.isVisible: return
        for region in view.regions:
            if bpy.context.region.as_pointer() == region.as_pointer():
                self.makeBox(region, color)

    def makeBox(self, view: Region, color:tuple):
        settings = bpy.context.screen.overlay_settings
        mid = self.getMidpoint(view)
        dimensions = self.getSize(view)
        left_rail = (
            Vector((0.0,0.0)), 
            Vector((mid.x*settings.getWidth(), dimensions.y))
        )
        right_rail = (
            Vector((dimensions.x, 0.0)), 
            Vector((dimensions.x - mid.x*settings.getWidth(), dimensions.y))
        )
        
        self.drawVectorBox(left_rail[0], left_rail[1], color)
        self.drawVectorBox(right_rail[0], right_rail[1], color)

    def drawVectorBox(self, a, b, color):
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


    def renderCircle(self, view: Area, color: tuple):
        settings = bpy.context.screen.overlay_settings
        if not settings.isVisible: return
        for region in view.regions:
            if bpy.context.region.as_pointer() == region.as_pointer() and not region.data.lock_rotation:
                self.makeCircle(region, color)

    def makeCircle(self, view: Region, color:tuple):
        settings = bpy.context.screen.overlay_settings
        mid = self.getMidpoint(view)
        radius = math.dist((0,0), mid) * (settings.getRadius() * 0.5)
        self.drawCircle(mid, radius, color)

    def drawCircle(self, mid: Vector, radius:float, color: tuple):
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


class OverlayManager:
    def __init__(self):
        self.overlays = []
