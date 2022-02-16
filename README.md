![touch view header](/docs/header.jpg?raw=true)

###### _EXPECT BUGS_

Control the viewport with your finger in Sculpt Mode. Adds overlay regions for rotate, pan, and zoom.

![demo gif](/docs/demo.gif?raw=true)

##### Features:

v0.1
- Camera dolly on left and right of viewport
- Camera pan from center of viewport
- Camera rotate in any other area of viewport
- Toggleable overlay to simplify resizing controls

v0.2 (unpublished)
- minor bug fixes and code cleanup

v0.3
- Double-tap to toggle "focus" mode
- Toggle Tools LEFT/RIGHT in UI
- Fixed incorrect viewport calculation when N-panel is open
- refactored screen/area management code (additional major refactor needed)

v0.5
- fixed Quad-view overlay compatibility
- added camera rotation lock in N-panel
- replace rotation with panning when rotation is locked
- fixed issue when locking view to Object or 3D Cursor

v0.6 hotfix
- addressed issues with determining locked state with quadviews
- changed scale of viewport overlay settings for more precision

v0.7
- added Gizmos for key features
- added hide/show Gizmo and layout options
- locked viewport rotation for isometric viewports in quadview to address lock/unlock inconsistencies
- Fullscreen Toggle no longer maximizes the window, only expands the View3D region

v0.8
- relocated settings to addon preferences to save across projects and scenes
- addressed a handful of bugs impacting user experience
- added gizmo to toggle fullscreen mode
- doubletap now selects/activates tapped object instead of triggering fullscreen

v0.9
- code restructure
- added N Panel gizmo
- fixed dragging over gizmo moves selected object

v0.9.1
- added tap for menu scroll

v0.9.2
- removed viewport manager class
- fixed issue delaying overlay viewport binding
- fixed gizmo tools/panel overlap issue when "Region Overlap" enabled


*many more features are planned for the final version.*

##### KNOWN ISSUES:

Please [report any issues](https://github.com/nendotools/touchview/issues) you find and I'll do my best to address them.

The add-on is free, but if it helps you, please consider [supporting me](https://nendo.gumroad.com/l/touchview).
