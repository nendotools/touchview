<!-- order: Added, Fixed, Changed, Improved, Removed -->

**Added**

- Tooltips on all on-screen buttons
- Brush Dynamics in Grease Pencil 3 and Curves Sculpt modes

**Fixed**

- Pen no longer moves the camera in Touch/Full input modes
- Finger and mouse now control the view in Pen input mode
- Viewport controls detect thin and sculpted geometry
- Custom action menu settings survive a restart
- Overlay no longer crashes when switching windows
- Density and multires controls step without skipping
- Action menu and gizmo panel work in edge-case modes
- 2D panning works when Swap Pan/Rotate is enabled
- Touch toggle shows on a fresh install and in the gizmo bar
- Brush size had no effect in Blender 5.x
- On-screen buttons no longer hide or overlap other controls
- Viewport redraws when gizmo preferences change
- Brush cursor warp used region instead of window coordinates

**Changed**

- Input, gizmo and overlay code cleaned up and renamed
- Controls and keymaps recover after a failed startup
- Brush controls adapt to Blender 4.x and 5.x paint settings

**Improved**

- Gizmo order is now stable across sessions
- Safe area avoids toolbar, sidebar, headers and asset shelf
- Clearer description for the Floating Toggle option

**Removed**

- Unused duplicate gizmo modules
