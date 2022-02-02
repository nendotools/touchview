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
        self.view.tag_redraw()

    def getMidpoint(self) -> Vector:
        return self.getSize(0.5)

    def getSize(self, scalar: float = 1) -> Vector:
        return Vector((self.view.width * scalar, self.view.height * scalar))

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

        for region in area.regions:      #type: ignore
            if region.type == "WINDOW":
                viewport.view = region
            if region.type == "UI":
                viewport.ui = region
            if region.type == "TOOLS":
                viewport.tools = region
        viewport.overlay = Overlay()
        viewport.overlay.drawUI(viewport.view)

        self.viewports.append(viewport)
        return viewport

    def update_viewport(self):
        print("update triggered")
        if not hasattr(bpy.context.scene, "overlay_settings"): return False
        for area in bpy.context.window.screen.areas:
            if area.type != "VIEW_3D": continue
            vp = self.getViewport(area)
            vp.tag_redraw()
        return True

    def clearAll(self):
        for vp in self.viewports:
            vp.overlay.clear_overlays()
            vp.tag_redraw()
