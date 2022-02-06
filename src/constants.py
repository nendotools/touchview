import bpy
from bpy.types import Context
from bpy.props import BoolProperty, FloatProperty

class OverlaySettings(bpy.types.PropertyGroup):
    def updateSubscribers(self, context:Context):
        try:
            len(self.subscribers)
        except:
            return
        for subscriber in self.subscribers:
            subscriber()

    subscribers: list
    width: FloatProperty(
        name="Width", 
        default=40.0, 
        min=10.0, 
        max=100,
        update=updateSubscribers
    )
    radius: FloatProperty(
        name="Radius", 
        default=35.0, 
        min=10.0, 
        max=100.0,
        update=updateSubscribers
    )
    isVisible: BoolProperty(
        name="Show Overlay", 
        default=False, 
        update=updateSubscribers
    )
    show_lock: BoolProperty(
        name="Show Lock Button", 
        default=True 
    )

    def subscribe(self, function):
        try:
            len(self.subscribers)
        except:
            self.subscribers = []
        self.subscribers.append(function)

    def getShowLock(self):
        return self.show_lock

    def getWidth(self):
        return self.width / 100

    def getRadius(self):
        return self.radius / 100
