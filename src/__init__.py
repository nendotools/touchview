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
    "version": (0, 9, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > NENDO",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/nendotools/touchview/issues",
    "category": "3D View",
}

import bpy
from . Overlay import Overlay
from . Settings import OverlaySettings
from . Operators import TouchInput, FlipTools, ToggleNPanel
from . Panel import NendoViewport
from . Gizmos import ViewportGizmoGroup, ViewportRecenter, ViewportLock, gizmo_toggle

__classes__ = (
        OverlaySettings,
        TouchInput,
        FlipTools,
        ToggleNPanel,
        NendoViewport,
        ViewportLock,
        ViewportRecenter,
        ViewportGizmoGroup
    )

ov = Overlay()

def register():
    from bpy.utils import register_class
    from . touch_input import register_keymaps    
    for cls in __classes__:
        register_class(cls)

    bpy.types.VIEW3D_PT_gizmo_display.append(gizmo_toggle)
    ov.drawUI()

    register_keymaps()

def unregister():
    from bpy.utils import unregister_class
    from . touch_input import unregister_keymaps

    ov.clear_overlays()
    bpy.types.VIEW3D_PT_gizmo_display.remove(gizmo_toggle)
    for cls in __classes__:
        unregister_class(cls)

    unregister_keymaps()

if __name__ == "__main__":
    register()
