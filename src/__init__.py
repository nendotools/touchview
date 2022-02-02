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

import bpy
import math
from bpy import ops

from bpy.types import Operator, Scene
from bpy.props import EnumProperty

from bpy.utils import register_class, unregister_class
from bpy.app import timers

from . Viewport import Viewport, ViewportManager
from . items import input_mode_items
from . constants import OverlaySettings
from . Panel import NendoViewport, View3DPanel

class TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.view_ops"
    bl_label = "Viewport Control Regions"

    mode: EnumProperty(
        name="Mode", 
        description="Sets the viewport control type",
        items=input_mode_items,
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

    def invoke(self, context, event):
        if self.handle_doubletap(event): return {'FINISHED'}
        self.delta = (event.mouse_region_x, event.mouse_region_y)

        viewport = context.scene.vm.getViewport(context.area)

        settings = bpy.context.scene.overlay_settings
        mid_point = viewport.getMidpoint()
        dolly_scale = settings.dolly_wid
        pan_scale = settings.pan_rad
        
        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist((0,0), mid_point) * (pan_scale*0.4)
        
        if dolly_wid > self.delta[0] or self.delta[0] > viewport.view.width-dolly_wid:
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
    register_class(OverlaySettings)
    register_class(NendoViewport)
    Scene.overlay_settings = bpy.props.PointerProperty(type=OverlaySettings)
    Scene.vm = ViewportManager()
    
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
    Scene.vm.unload()
    del Scene.vm

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    unregister_class(OverlaySettings)
    unregister_class(NendoViewport)
    unregister_class(TouchInput)
    unregister_class(FlipTools)

if __name__ == "__main__":
    register()
