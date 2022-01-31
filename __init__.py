# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Touch Viewport",
    "description": "Creates active touch zones over View 3D areas for easier viewport navigation with touch screens and pen tablets.",
    "author": "NENDO",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > NENDO",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

import bpy
import math
from mathutils import Vector
import gpu
from bgl import *
from gpu_extras.batch import batch_for_shader    

class TouchInput(bpy.types.Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.view_ops"
    bl_label = "Viewport Control Regions"
    
    mode: bpy.props.EnumProperty(
        name="Mode", 
        description="Sets the viewport control type",
        items={
            ('ORBIT','rotate','Rotate the viewport'),
            ('PAN','pan','Move the viewport'),
            ('DOLLY','zoom','Zoom in/out the viewport')
        },
        default="ORBIT")

    def execute(self, context):    
        if self.mode == "ORBIT":
            bpy.ops.view3d.rotate('INVOKE_DEFAULT')
        elif self.mode == "PAN":
            bpy.ops.view3d.move('INVOKE_DEFAULT')
        elif self.mode == "DOLLY":
            bpy.ops.view3d.dolly('INVOKE_DEFAULT')
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.delta = Vector((event.mouse_region_x, event.mouse_region_y))
        wm = bpy.context.window_manager
        mid_point = self.getMidPoint(context.area)
        dolly_scale = wm.dolly_wid
        pan_scale = wm.pan_rad
        
        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist((0,0), mid_point) * (pan_scale*0.4)
        
        if dolly_wid > self.delta.x or self.delta.x > context.area.width-dolly_wid:
            self.mode = "DOLLY"
        elif math.dist(self.delta, mid_point) < pan_diameter:
            self.mode = "PAN"
        else:
            self.mode = "ORBIT"
        
        self.execute(context)
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'
    
    def getArea(self, area):
        return Vector(( area.width, area.height))
    
    def getMidPoint(self, area):
        return self.getArea(area)/2

class Overlay:
    def __init__(self, area):
        self.area = area
        self.pointer = str(area.as_pointer())
        self.overlays = []
        
    def get(self, attr):
        wm = bpy.types.WindowManager.viewops_conf
        return wm[self.pointer+attr]

    def add_overlay(self, overlay):
        self.overlays.append(overlay)

    def clear_overlays(self):
        for ol in self.overlays:
            bpy.types.SpaceView3D.draw_handler_remove(ol, 'WINDOW')
        self.overlays = []

class OverlayAgent:
    def __init__(self):
        self.views = []
        
    def indexView(self, area):
        ao = (area, Overlay(area))
        self.views.append(ao)
        return ao
    
    def findView(self, view):
        for area, overlay in self.views:
            if area == view: return (area, overlay)
        return False

    def init_viewport(self, view):
        ao = self.findView(view)
        if ao == False: return self.indexView(view)
        return ao

    def update_overlay(self):
        self.clearAll()
        wm = bpy.context.window_manager
        if not hasattr(wm, "isVisible"): return

        if wm.isVisible:
            for area in bpy.context.window.screen.areas.values():
                if area.type != "VIEW_3D": continue
                a, ov = self.init_viewport(area)
                wd = a.width
                ht = a.height
                pan_diameter = math.dist((0,0), (wd/2, ht/2)) * (wm.pan_rad * 0.4)
                
                left_rail = (
                    Vector((0.0,0.0)), 
                    Vector((wd/2*wm.dolly_wid, ht))
                )
                right_rail = (
                    Vector((wd,0.0)), 
                    Vector((wd - wd/2*wm.dolly_wid, ht))
                )
                mid_ring = (
                    Vector((wd/2, ht/2)),
                    pan_diameter
                )
                ov.add_overlay(
                    overlay_manager.renderShape(
                        "left_rail", "RECT", left_rail, (1,1,1,0.01)
                ))
                ov.add_overlay(
                    overlay_manager.renderShape(
                        "right_rail",
                        "RECT",
                        right_rail,
                        (1,1,1,0.01)
                ))
                ov.add_overlay(
                    overlay_manager.renderShape(
                        "mid_ring",
                        "CIRC",
                        mid_ring,
                        (1,1,1,0.01)
                ))
                return True

    def clearAll(self):
        for area, overlay in self.views:
            overlay.clear_overlays()
            area.tag_redraw()
        self.views = []

    def renderShape(self, name, shape, args, color):
        # create draw call
        if shape == "CIRC":
            _handle = bpy.types.SpaceView3D.draw_handler_add(
                self.drawVectorCircle, 
                (args[0],args[1], color), 
                'WINDOW', 
                'POST_PIXEL'
            )
        elif shape == "RECT":
            _handle = bpy.types.SpaceView3D.draw_handler_add(
                self.drawVectorBox, 
                (args[0],args[1], color), 
                'WINDOW', 
                'POST_PIXEL'
            )
        else:
            return {"INVALID_SHAPE"}

        return _handle

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

def handle_redraw():
    global overlay_manager
    overlay_manager.update_overlay()
    return 0.1

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NENDO"
    
class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_view_ops"
    bl_label = "Viewport Settings"

    def draw(self, context):
        overlay_manager.update_overlay()
        wm = context.window_manager
        self.layout.label(text="Control Zones")
        self.layout.row()
        self.layout.prop(wm, "dolly_wid")
        self.layout.row()
        self.layout.prop(wm, "pan_rad")
        self.layout.row()
        self.layout.prop(wm, "isVisible", text="Show Overlay")

addon_keymaps = []

def register():
    bpy.utils.register_class(TouchInput)
    bpy.utils.register_class(PanelOne)

    global overlay_manager
    overlay_manager = OverlayAgent()
    if not bpy.app.timers.is_registered(handle_redraw):
        bpy.app.timers.register(handle_redraw, first_interval=1)
    
    bpy.types.WindowManager.dolly_wid = bpy.props.FloatProperty(
        name="Width", 
        default=0.4, 
        min=0.1, 
        max=1
    )
    bpy.types.WindowManager.pan_rad = bpy.props.FloatProperty(
        name="Radius", 
        default=0.35, 
        min=0.1, 
        max=1.0
    )
    bpy.types.WindowManager.isVisible = bpy.props.BoolProperty(
        name="Show Overlay", 
        default=False 
    )
    
    wm = bpy.context.window_manager   
    km = wm.keyconfigs.addon.keymaps.new(name='', space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'MIDDLEMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi)) 
    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt', space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'PRESS')
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'PEN', 'PRESS')
    kmi.properties.mode = "NORMAL"
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'ERASER', 'PRESS')
    kmi.properties.mode = "INVERT"
    addon_keymaps.append((km, kmi))

def unregister():
    global overlay_manager
    if bpy.app.timers.is_registered(handle_redraw):
        bpy.app.timers.unregister(handle_redraw)
    overlay_manager.clearAll()
    del overlay_manager
    del bpy.types.WindowManager.dolly_wid
    del bpy.types.WindowManager.pan_rad
    del bpy.types.WindowManager.isVisible

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(PanelOne)
    bpy.utils.unregister_class(TouchInput)
    

if __name__ == "__main__":
    register()
