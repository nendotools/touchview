![touch view header](/docs/header.jpg?raw=true)

# Features

Control the viewport with your finger in Sculpt Mode. Adds overlay regions for rotate, pan, and zoom.

![demo gif](/docs/demo.gif?raw=true)

# Changelogs

<details open><summary><b>v0.9.4</b></summary><br>

- `ADDED` : Support for menus in floating gizmo
- `ADDED` : Mode-specific options for floating gizmo
- `UPDATED` : Dependence on active_object for mode detection
- `UPDATED` : Classes to follow Blender naming conventions
- `UPDATED` : Keymaps for touchview in all context
- `UPDATED` : Keymaps for context action assigned to pen

</details>

<details><summary><b>v0.9.3</b></summary><br>

- `ADDED` : Sculpt pivot mode gizmo
- `ADDED` : Customizable floating menu

</details>

<details><summary><b>v0.9.2</b></summary><br>

- `FIXED` : Issue delaying overlay viewport binding
- `FIXED` : Gizmo tools/panel overlap issue when "Region Overlap" enabled
- `REMOVED` : Viewport manager class
- `REMOVED` : Default keymap causing Move Operator to trigger when dragging over non-modal gizmos

</details>

<details><summary><b>v0.9.1</b></summary><br>

- `ADDED` : Tap for menu scroll

</details>

<details><summary><b>v0.9</b></summary><br>

- `ADDED` : N-Panel gizmo
- `UPDATED` : Code restructure
- `FIXED` : Dragging over gizmo moves selected object

</details>

<details><summary><b>v0.8</b></summary><br>

- `ADDED` : Gizmo to toggle fullscreen mode
- `UPDATED` : Settings to addon preferences to save across projects and scenes
- `FIXED` : Bugs impacting user experience
- `FIXED` : Doubletap now selects/activates tapped object instead of triggering fullscreen

</details>

<details><summary><b>v0.7</b></summary><br>

- `ADDED` : Gizmos for key features
- `ADDED` : Hide/show Gizmo and layout options
- `ADDED` : Locked viewport rotation for isometric viewports in quadview to address lock/unlock inconsistencies
- `FIXED` : Fullscreen Toggle no longer maximizes the window, only expands the View3D region

</details>

<details><summary><b>v0.6</b></summary><br>

- `UPDATED` : Scale of viewport overlay settings for more precision
- `FIXED` : Issues with determining locked state with quadviews

</details>

<details><summary><b>v0.5</b></summary><br>

- `ADDED` : Camera rotation lock in N-panel
- `FIXED` : Quad-view overlay compatibility
- `FIXED` : Rotation with panning when rotation is locked
- `FIXED` : Issue when locking view to Object or 3D Cursor

</details>

<details><summary><b>v0.4</b></summary><br>

- `ADDED` : Double-tap to toggle "focus" mode
- `ADDED` : Toggle Tools LEFT/RIGHT in UI

</details>

<details><summary><b>v0.3</b></summary><br>

- `FIXED` : Incorrect viewport calculation when N-panel is open
- `FIXED` : Refactored screen/area management code (additional major refactor needed)

</details>

<details><summary><b>v0.2</b></summary><br/>

- `FIXED` : Minor bug fixes and code cleanup

</details>

<details><summary><b>v0.1</b></summary><br>

- `ADDED` : Camera dolly on left and right of viewport
- `ADDED` : Camera pan from center of viewport
- `ADDED` : Camera rotate in any other area of viewport
- `ADDED` : Toggleable overlay to simplify resizing controls

</details>

# Issues

- `LOW` : Quadview breaks space_data bindings for locking viewport
- `HIGH` : Need better coverage for edit modes in ops and gizmos

> Please [report any issues](https://github.com/nendotools/touchview/issues) you find and I'll do my best to address them.

> The add-on is free, but if it helps you, please consider [supporting me](https://nendo.gumroad.com/l/touchview).
