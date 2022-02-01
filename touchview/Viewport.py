import bpy
from bpy.types import Area, Context, Region, Screen, Window
from .Overlay import OverlayManager, Overlay

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

class ViewportManager:
    """ Object responsible for storing and recalling viewports by Area references """
    viewports: list[Viewport]
    def __init__(self):
        self.viewports = []

    def getViewport(self, context: Context):
        area = context.area
        if area.type != "VIEW_3D": return (False)

        for v in self.viewports:
            if v._area == area: return v

        viewport = Viewport()
        viewport._area = area

        for region in area.regions:
            if region.type == "WINDOW":
                viewport.view = region
            if region.type == "UI":
                viewport.ui = region
            if region.type == "TOOLS":
                viewport.tools = region

        self.viewports.append(viewport)

        return viewport
