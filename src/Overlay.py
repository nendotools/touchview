import bpy
from bpy.types import SpaceView3D
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

    def renderShape(self, name, shape, args, color):
        if shape == "CIRC":
            _handle = SpaceView3D.draw_handler_add(
                self.drawVectorCircle, 
                (args[0],args[1], color), 
                'WINDOW', 
                'POST_PIXEL'
            )
        elif shape == "RECT":
            _handle = SpaceView3D.draw_handler_add(
                self.drawVectorBox, 
                (args[0],args[1], color), 
                'WINDOW', 
                'POST_PIXEL'
            )
        else:
            return {"INVALID_SHAPE"}

        self.meshes.append(_handle)

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
        
    def drawVectorCircle(self, mid, rad, color):
        segments = 100
        vertices = [Vector(mid)]
        indices = []
        p = 0
        for p in range(segments):
            if p > 0:
                point = Vector((
                    mid.x + rad * math.cos(math.radians(360/segments)*p),
                    mid.y + rad * math.sin(math.radians(360/segments)*p)
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
