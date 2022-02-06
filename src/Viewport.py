import bpy
from mathutils import Vector
from bpy.types import Area, Region, RegionView3D, SpaceView3D, Window

from . Overlay import Overlay

class Viewport:
    """ Container Object for Window Areas and related view Regions """
    window: Window
    area: Area
    view: Region
    ui: Region
    tools: Region
    overlay: Overlay
    quadview: list[RegionView3D]

    def __init__(self):
        self.window = bpy.context.window

    def tag_redraw(self):
        self.area.tag_redraw()

    def setRegionContext(self, region: Region):
        self.view = region

    def getMidpoint(self) -> Vector:
        return self.getSize(0.5)

    def getSize(self, scalar: float = 1, ignore_region: bool = False) -> Vector:
        if len(self.quadview) > 0 and not ignore_region:
            scalar *= 0.5
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
            if v.area == area: return v

        viewport = Viewport()
        viewport.area = area
        viewport.quadview = area.spaces.active.region_quadviews
        for region in area.regions:
            if region.type == "WINDOW":
                viewport.view = region
            if region.type == "UI":
                viewport.ui = region
            if region.type == "TOOLS":
                viewport.tools = region
        viewport.overlay = Overlay()
        viewport.overlay.drawUI(viewport.area)

        self.viewports.append(viewport)
        return viewport

    def update_viewport(self) -> bool:
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
