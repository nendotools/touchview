import bpy
import math
from mathutils import Vector
import time

from bpy import ops
from bpy.props import EnumProperty
from bpy.types import Context, Event, Operator

from . items import input_mode_items, pivot_items

class TouchInput(Operator):
    """ Active Viewport control zones """
    bl_idname = "view3d.view_ops"
    bl_label = "Viewport Control Regions"

    start_time: float = time.time()

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

# consider adding gestures. requires handling moving manually rather than relying on built-in operators.
    def handle_swipe(self, event: Event):
        if event.value == "PRESS" and event.type == "LEFTMOUSE":
            self.start_time = time.time()
        if event.value == "RELEASE" and event.type == "LEFTMOUSE" and self.start_time:
            pass
        return False

    def handle_doubletap(self, event: Event):
        if event.value == "DOUBLE_CLICK" and event.type != "PEN":
            bpy.ops.object.transfer_mode('INVOKE_DEFAULT')
            return True
        return False

    def invoke(self, context: Context, event: Event):
        if self.handle_doubletap(event): return {'FINISHED'}
        if self.handle_swipe(event): return {'FINISHED'}
        if event.value != "PRESS": return {'FINISHED'}
        self.delta = (event.mouse_region_x, event.mouse_region_y)

        settings = bpy.context.preferences.addons['touchview'].preferences
        mid_point = Vector((context.region.width/2 , context.region.height/2))

        dolly_scale = settings.getWidth()
        pan_scale = settings.getRadius()
        
        dolly_wid = mid_point.x * dolly_scale
        pan_diameter = math.dist((0,0), mid_point) * (pan_scale * 0.5)

        is_quadview_orthographic = context.region.data.is_orthographic_side_view and context.region.alignment == "QUAD_SPLIT"
        is_locked = context.region.data.lock_rotation | is_quadview_orthographic
        
        if dolly_wid > self.delta[0] or self.delta[0] > context.region.width-dolly_wid:
            self.mode = "DOLLY"
        elif math.dist(self.delta, mid_point) < pan_diameter or is_locked:
            self.mode = "PAN"
        else:
            self.mode = "ORBIT"
        
        if context.object.mode == "SCULPT":
            bpy.ops.sculpt.set_pivot_position(mode=settings.pivot_mode)
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

class NextPivotMode(Operator):
    """ Step through Pivot modes """
    bl_idname = "view3d.step_pivot_mode"
    bl_label = "Use next Pivot mode"

    def execute(self, context: Context):
        settings = context.preferences.addons["touchview"].preferences
        count = 0
        for enum, name, desc in pivot_items:
            if enum == settings.pivot_mode:
                count += 1
                if count == len(pivot_items): count = 0
                pivot = pivot_items[count][0]
                bpy.ops.sculpt.set_pivot_position(mode=pivot)
                settings.pivot_mode = pivot
                context.area.tag_redraw()
                return {'FINISHED'}
            count+=1
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context: Context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'

class ToggleNPanel(Operator):
    """ Toggle Settings Panel """
    bl_idname = "view3d.toggle_n_panel"
    bl_label = "Display settings Panel"

    def execute(self, context: Context):
        context.space_data.show_region_ui ^= True
        return {'FINISHED'}
        
    @classmethod
    def poll(cls, context: Context):
        return context.area.type == 'VIEW_3D' and context.region.type == 'WINDOW'
