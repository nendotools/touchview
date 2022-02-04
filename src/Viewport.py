import bpy
import math
from bpy.types import Area, Context, Region, RegionView3D, Screen, Window
from bpy.app import timers

from mathutils import Vector

from . constants import OverlaySettings
from . Overlay import OverlayManager, Overlay

class Viewport:
    """ Container Object for Window Areas and related view Regions """
    window: Window
    _area: Area
    views: list[Region]
    ui: Region
    tools: Region
    overlay: Overlay
    quadview: list[RegionView3D]

    def __init__(self):
        self.window = bpy.context.window

    def tag_redraw(self):
        self._area.tag_redraw()

    def getMidpoint(self) -> Vector:
        return self.getSize(0.5)

    def getSize(self, scalar: float = 1) -> Vector:
        if len(self.quadview) > 0:
            scalar *= 0.5
        return Vector((self._area.width * scalar, self._area.height * scalar))

class ViewportManager:
    """ Object responsible for storing and recalling viewports by Area references """
    viewports: list[Viewport]
    def __init__(self):
        self.viewports = []

    def unload(self):
        self.clearAll()


    def getViewport(self, area: Area) -> Viewport:
        if area.type != "VIEW_3D":
            raise TypeError('Area type must be VIEW_3D! {} provided.'.format(area.type))

        for v in self.viewports:
            if v._area == area: return v

        viewport = Viewport()
        viewport._area = area

#############
####    Need changes here to address multi-viewport situations
#############
        viewport.quadview = area.spaces[0].region_quadviews
        for region in area.regions:      #type: ignore
            if region.type == "WINDOW":
                viewport.view = region
            if region.type == "UI":
                viewport.ui = region
            if region.type == "TOOLS":
                viewport.tools = region
        viewport.overlay = Overlay()
        viewport.overlay.drawUI(viewport._area)

        self.viewports.append(viewport)
        return viewport

    def update_viewport(self):
        if not hasattr(bpy.context.screen, "overlay_settings"): return False
        for area in bpy.context.window.screen.areas:
            if area.type != "VIEW_3D": continue
            vp = self.getViewport(area)
            vp.tag_redraw()
        return True

    def clearAll(self):
        for vp in self.viewports:
            vp.overlay.clear_overlays()
            vp.tag_redraw()
