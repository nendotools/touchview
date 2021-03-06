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
  "description":
  "Creates active touch zones over View 3D areas for easier viewport navigation with touch screens and pen tablets.",
  "author": "NENDO",
  "version": ( 1, 2, 4 ),
  "blender": ( 2, 80, 0 ),
  "location": "View3D > Tools > NENDO",
  "warning": "",
  "doc_url": "",
  "tracker_url": "https://github.com/nendotools/touchview/issues",
  "category": "3D View",
}

import bpy
from . import lib
from .Settings import OverlaySettings, MenuModeGroup


def register():
  lib.register()
  bpy.utils.register_class( MenuModeGroup )
  bpy.utils.register_class( OverlaySettings )


def unregister():
  lib.unregister()
  bpy.utils.unregister_class( MenuModeGroup )
  bpy.utils.unregister_class( OverlaySettings )
