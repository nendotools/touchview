import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import PropertyGroup

class OverlaySettings(PropertyGroup):
    dolly_wid: FloatProperty(
        name="Width", 
        default=0.4, 
        min=0.1, 
        max=1
    )
    pan_rad: FloatProperty(
        name="Radius", 
        default=0.35, 
        min=0.1, 
        max=1.0
    )
    isVisible: BoolProperty(
        name="Show Overlay", 
        default=False 
    )

