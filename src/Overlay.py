import bpy
from bpy.types import Region, SpaceView3D
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

    def drawUI(self, view: Region):
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
        view.tag_redraw()

    def verifySpace(self, view: Region, origin: Region):
        view_check = view.as_pointer()
        origin_check = origin.as_pointer()
        if view_check != origin_check: return False
        return True

    def renderRailing(self, view: Region, color: tuple):
        settings = bpy.context.scene.overlay_settings
        if not settings.isVisible: return
        if not self.verifySpace(view, bpy.context.region): return

        mid = self.getMidpoint(view)
        dimensions = self.getSize(view)
        left_rail = (
            Vector((0.0,0.0)), 
            Vector((mid.x*settings.dolly_wid, dimensions.y))
        )
        right_rail = (
            Vector((dimensions.x, 0.0)), 
            Vector((dimensions.x - mid.x*settings.dolly_wid, dimensions.y))
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


    def renderCircle(self, view: Region, color: tuple):
        settings = bpy.context.scene.overlay_settings
        if not settings.isVisible: return
        if not self.verifySpace(view, bpy.context.region): return

        segments = 100
        mid = self.getMidpoint(view)
        radius = math.dist((0,0), mid) * (settings.pan_rad * 0.4)
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