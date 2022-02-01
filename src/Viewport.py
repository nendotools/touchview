import bpy
import math
from bpy.types import Area, Context, Region, Screen, Window
from bpy.app import timers

from mathutils import Vector

from . constants import OverlaySettings
from . Overlay import OverlayManager, Overlay

class Viewport:
    """ Container Object for Window Areas and related view Regions """
    window: Window
    _area: Area
    view: Region
    ui: Region
    tools: Region
    overlay: Overlay

    def __init__(self):
        self.window = bpy.context.window

    def tag_redraw(self):
        self._area.tag_redraw()

    def getMidpoint(self) -> Vector:
        return self.getSize(0.5)

    def getSize(self, scalar: float = 1) -> Vector:
        return Vector((self.view.width * scalar, self.view.height * scalar))

class ViewportManager:
    """ Object responsible for storing and recalling viewports by Area references """
    viewports: list[Viewport]
    def __init__(self):
        self.viewports = []

        if not timers.is_registered(self.handle_redraw):
            timers.register(self.handle_redraw, first_interval=1)

    def unload(self):
        if timers.is_registered(self.handle_redraw):
            timers.unregister(self.handle_redraw)
        self.clearAll()


    def getViewport(self, area: Area) -> Viewport:
        if area.type != "VIEW_3D":
            raise TypeError('Area type must be VIEW_3D! {} provided.'.format(area.type))

        for v in self.viewports:
            if v._area == area: return v

        viewport = Viewport()
        viewport._area = area

        for region in area.regions:      #type: ignore
            if region.type == "WINDOW":
                viewport.view = region
            if region.type == "UI":
                viewport.ui = region
            if region.type == "TOOLS":
                viewport.tools = region
        viewport.overlay = Overlay()

        self.viewports.append(viewport)
        return viewport

    def update_viewport(self):
        self.clearAll()
        if not hasattr(bpy.context.scene, "overlay_settings"): return False
        settings = bpy.context.scene.overlay_settings

        if settings.isVisible:
            for area in bpy.context.window.screen.areas:
                if area.type != "VIEW_3D": continue
                vp = self.getViewport(area)

                dimensions = vp.getSize()
                mid_point = vp.getMidpoint()

                pan_diameter = math.dist((0,0), mid_point) * (settings.pan_rad * 0.4)
                
                left_rail = (
                    Vector((0.0,0.0)), 
                    Vector((dimensions.x/2*settings.dolly_wid, dimensions.y))
                )
                right_rail = (
                    Vector((dimensions.x, 0.0)), 
                    Vector((dimensions.x - dimensions.x/2*settings.dolly_wid, dimensions.y))
                )

                mid_ring = (
                    mid_point,
                    pan_diameter
                )
                vp.overlay.renderShape(
                    "left_rail", "RECT", left_rail, (1,1,1,0.01)
                )
                vp.overlay.renderShape(
                    "right_rail",
                    "RECT",
                    right_rail,
                    (1,1,1,0.01)
                )
                vp.overlay.renderShape(
                    "mid_ring",
                    "CIRC",
                    mid_ring,
                    (1,1,1,0.01)
                )
                return True
        return False

    def clearAll(self):
        for vp in self.viewports:
            vp.overlay.clear_overlays()
            vp.tag_redraw()

    def handle_redraw(self):
        self.update_viewport()
        return 0.1
