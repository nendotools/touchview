import bpy
from bpy.props import BoolProperty, CollectionProperty, FloatProperty

class OverlaySettings(bpy.types.PropertyGroup):
    def updateSubscribers(self, context):
        try:
            len(self.subscribers)
        except:
            return
        for subscriber in self.subscribers:
            subscriber()

    subscribers: list
    dolly_wid: FloatProperty(
        name="Width", 
        default=0.4, 
        min=0.1, 
        max=1,
        update=updateSubscribers
    )
    pan_rad: FloatProperty(
        name="Radius", 
        default=0.35, 
        min=0.1, 
        max=1.0,
        update=updateSubscribers
    )
    isVisible: BoolProperty(
        name="Show Overlay", 
        default=False, 
        update=updateSubscribers
    )

    def subscribe(self, function):
        try:
            len(self.subscribers)
        except:
            self.subscribers = []
        self.subscribers.append(function)
