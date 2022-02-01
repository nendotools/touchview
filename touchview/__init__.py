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
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > NENDO",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/nendotools/touchview/issues",
    "category": "3D View",
}

from types import SimpleNamespace
import bpy
from bpy import ops
import math
from mathutils import Vector
import gpu
from bgl import glEnable, glDisable, GL_BLEND
from gpu_extras.batch import batch_for_shader    

from bpy.types import Operator, Panel, Region, WindowManager
from bpy.props import EnumProperty, BoolProperty, IntProperty, FloatProperty, StringProperty

from bpy.utils import register_class, unregister_class
from bpy.app import timers

class TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.view_ops"
    bl_label = "Viewport Control Regions"
    
    mode: EnumProperty(
        name="Mode", 
        description="Sets the viewport control type",
        items={
            ('ORBIT','rotate','Rotate the viewport'),
            ('PAN','pan','Move the viewport'),
            ('DOLLY','zoom','Zoom in/out the viewport')
        },
        default='ORBIT',
        options={"HIDDEN"}
    )

    def execute(self, context):    
        if self.mode == "ORBIT":
            ops.view3d.rotate('INVOKE_DEFAULT')
        elif self.mode == "PAN":
            ops.view3d.move('INVOKE_DEFAULT')
        elif self.mode == "DOLLY":
            ops.view3d.dolly('INVOKE_DEFAULT')
        return {'FINISHED'}

    # NEED TO ADD A CHECK FOR CURRENT STATE AND SYNC INTENDED MODE
    def handle_doubletap(self, event):
        if event.value == "DOUBLE_CLICK" and event.type != "PEN":
            ops.screen.screen_full_area()
            ops.wm.window_fullscreen_toggle()
            return True
        return False

    def getViewport(self, context):
        area = context.area
        if area.type != "VIEW_3D": return (False)

        viewport = {
                "view": Region,
                "ui": Region,
                "tools": Region
        }
        for region in area.regions:
            if region.type == "WINDOW":
                viewport["view"] = region
            if region.type == "UI":
                viewport["ui"] = region
            if region.type == "TOOLS":
                viewport["tools"] = region

        return SimpleNamespace(**viewport)

    
    def invoke(self, context, event):
        if self.handle_doubletap(event): return {'FINISHED'}

        self.delta = Vector((event.mouse_region_x, event.mouse_region_y))

        viewport = self.getViewport(context)

        wm = bpy.context.window_manager
        mid_point = self.getMidPoint(viewport.view)
        dolly_scale = wm.dolly_wid
        pan_scale = wm.pan_rad
        
        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist((0,0), mid_point) * (pan_scale*0.4)
        
        if dolly_wid > self.delta.x or self.delta.x > viewport.view.width-dolly_wid:
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

## PLEASE IMPLEMENT THIS
##  --- will need a lot of cleanup and address possible double assignment
    def getViewport(self, context):
        area = context.area
        if area.type != "VIEW_3D": return (False)

        viewport = {
                "view": Region,
                "ui": Region,
                "tools": Region
        }
        for region in area.regions:
            if region.type == "WINDOW":
                viewport["view"] = region
            if region.type == "UI":
                viewport["ui"] = region
            if region.type == "TOOLS":
                viewport["tools"] = region

        return SimpleNamespace(**viewport)


    def update_overlay(self):
        self.clearAll()
        wm = bpy.context.window_manager
        if not hasattr(wm, "isVisible"): return

        if wm.isVisible:
            for area in bpy.context.window.screen.areas.values():
                if area.type != "VIEW_3D": continue
                a, ov = self.init_viewport(area)

## bpy.context.window may be global window
## area.region[WINDOW] is the actual viewport, subtracting the UI sizes
                ui_wd = 0
                w_wd = 0
                for r in a.regions:
                    if r.type == "WINDOW":
                        w_wd = r.width
                    if r.type == "UI":
                        ui_wd = r.width
                wd = w_wd
                ht = a.height


                pan_diameter = math.dist((0,0), (wd/2, ht/2)) * (wm.pan_rad * 0.4)
                
                left_rail = (
                    Vector((0.0,0.0)), 
                    Vector((wd/2*wm.dolly_wid, ht))
                )
                right_rail = (
                    Vector((wd, 0.0)), 
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
    
class PanelOne(View3DPanel, Panel):
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
        
        self.layout.label(text="Viewoprt Options")
        self.layout.row()

        op = self.layout.operator("view3d.tools_region_flip", text="Flip Tools")

class FlipTools(Operator):
    """ Relocate Tools panel between left and right """
    bl_idname = "view3d.tools_region_flip"
    bl_label = "Tools Region Swap"

    def execute(self, context):
        override = bpy.context.copy()
        for r in context.area.regions:
            if r.type == 'TOOLS':
                override["region"] = r
        bpy.ops.screen.region_flip(override)
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'

addon_keymaps = []

def register():
    register_class(TouchInput)
    register_class(FlipTools)
    register_class(PanelOne)

    global overlay_manager
    overlay_manager = OverlayAgent()
    if not timers.is_registered(handle_redraw):
        timers.register(handle_redraw, first_interval=1)
    
    WindowManager.dolly_wid = FloatProperty(
        name="Width", 
        default=0.4, 
        min=0.1, 
        max=1
    )
    WindowManager.pan_rad = FloatProperty(
        name="Radius", 
        default=0.35, 
        min=0.1, 
        max=1.0
    )
    WindowManager.isVisible = BoolProperty(
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

    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt', space_type='EMPTY')
    kmi = km.keymap_items.new('view3d.view_ops', 'LEFTMOUSE', 'DOUBLE_CLICK')
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'PEN', 'PRESS')
    kmi.properties.mode = "NORMAL"
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('sculpt.brush_stroke', 'ERASER', 'PRESS')
    kmi.properties.mode = "INVERT"
    addon_keymaps.append((km, kmi))

def unregister():
    global overlay_manager
    if timers.is_registered(handle_redraw):
        timers.unregister(handle_redraw)
    overlay_manager.clearAll()
    del overlay_manager
    del WindowManager.dolly_wid
    del WindowManager.pan_rad
    del WindowManager.isVisible

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    unregister_class(PanelOne)
    unregister_class(FlipTools)
    unregister_class(TouchInput)
    

if __name__ == "__main__":
    register()
