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
    "version": (0, 8),
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

from bpy.types import Context, Event, Operator, Window
from bpy.props import EnumProperty

from . Viewport import ViewportManager
from . items import input_mode_items
from . Settings import OverlaySettings
from . Panel import NendoViewport
from . Gizmos import ViewportGizmoGroup, ViewportRecenter, ViewportLock, draw_lock

class TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.view_ops"
    bl_label = "Viewport Control Regions"

    delta: tuple[float, float]

    mode: EnumProperty(
        name="Mode", 
        description="Sets the viewport control type",
        items=input_mode_items,
        default='ORBIT',
        options={"HIDDEN"}
    )

    def execute(self, context: Context):
        if self.mode == "DOLLY":
            ops.view3d.zoom('INVOKE_DEFAULT')
        elif self.mode == "ORBIT":
            ops.view3d.rotate('INVOKE_DEFAULT')
        else:
            bpy.ops.view3d.move('INVOKE_DEFAULT')
        return {'FINISHED'}

    # NEED TO ADD A CHECK FOR CURRENT STATE AND SYNC INTENDED MODE
    def handle_doubletap(self, event: Event):
        if event.value == "DOUBLE_CLICK" and event.type != "PEN":
            bpy.ops.object.transfer_mode('INVOKE_DEFAULT')
            return True
        return False

    def invoke(self, context: Context, event: Event):
        if self.handle_doubletap(event): return {'FINISHED'}
        self.delta = (event.mouse_region_x, event.mouse_region_y)

        viewport = context.window.vm.getViewport(context.area)
        viewport.setRegionContext(context.region)

        settings = bpy.context.preferences.addons['touchview'].preferences
        mid_point = viewport.getMidpoint()

        dolly_scale = settings.getWidth()
        pan_scale = settings.getRadius()
        
        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist((0,0), mid_point) * (pan_scale * 0.5)

        is_quadview_orthographic = context.region.data.is_orthographic_side_view and len(viewport.quadview) > 0
        is_locked = context.region.data.lock_rotation | is_quadview_orthographic
        
        if dolly_wid > self.delta[0] or self.delta[0] > viewport.view.width-dolly_wid:
            self.mode = "DOLLY"
        elif math.dist(self.delta, mid_point) < pan_diameter or is_locked:
            self.mode = "PAN"
        else:
            self.mode = "ORBIT"
        
        self.execute(context)
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context: Context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'

class FlipTools(Operator):
    """ Relocate Tools panel between left and right """
    bl_idname = "view3d.tools_region_flip"
    bl_label = "Tools Region Swap"

    def execute(self, context: Context):
        override = bpy.context.copy()
        for r in context.area.regions:
            if r.type == 'TOOLS':
                override["region"] = r
        bpy.ops.screen.region_flip(override)
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context: Context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'

__classes__ = (
        OverlaySettings,
        TouchInput,
        FlipTools,
        NendoViewport,
        ViewportLock,
        ViewportRecenter,
        ViewportGizmoGroup
    )

def register():
    from bpy.utils import register_class
    from . touch_input import register_keymaps    
    for cls in __classes__:
        register_class(cls)

    bpy.types.VIEW3D_PT_gizmo_display.append(draw_lock)

    register_keymaps()
    Window.vm = ViewportManager()

def unregister():
    from bpy.utils import unregister_class
    from . touch_input import unregister_keymaps

    bpy.types.VIEW3D_PT_gizmo_display.remove(draw_lock)
    for cls in __classes__:
        unregister_class(cls)

    Window.vm.unload()
    del Window.vm

    unregister_keymaps()

if __name__ == "__main__":
    register()
