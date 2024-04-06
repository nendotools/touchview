<div align="center" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
  <h1>TouchView</h1>
  <div>BLENDER 3D add-on</div>
  <div><sup>customizable rotate/pan/zoom</sup></div>
  <div style="display: flex; flex-direction: row;">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/nendotools/touchview?style=flat-square">
    <img alt="GitHub Workflow Status (with branch)" src="https://img.shields.io/github/actions/workflow/status/nendotools/touchview/linting.yml?style=flat-square">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/nendotools/touchview?style=flat-square">
    <img alt="GitHub" src="https://img.shields.io/github/license/nendotools/touchview?style=flat-square">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fake-bpy-module-latest?style=flat-square">
  </div>
</div>

### Table of Contents

- [Features](https://github.com/nendotools/touchview#features)
- [Building from Github](https://github.com/nendotools/touchview#building-from-github)
- [Installation](https://github.com/nendotools/touchview#installation)
- [Changelog](https://github.com/nendotools/touchview#changelog)

# Features

This add-on is designed to improve the user experience of Blender for users without immediate access to a keyboard or mouse. It provides many customizable UI improvements to cater to your workflow needs.

<div style="display:flex; flex-direction:row;">
<img align="right" src="/docs/simple_demo.gif" width="40%">
<div width="60%">
<h2>Viewport Touch Control</h2>

Pan, Rotate, and Zoom the viewport with your finger.

The viewport has be updated to use 3 interactive "hot regions" to control the camera position.

If you are a pen tablet user; the pen will still draw, while your finger can be used to control the camera.

If your tablet doesn't support touch; you can set the middle mouse button to activate the control regions in the add-on settings.

- Pan by dragging for the middle of the viewport
- Zoom by dragging along the left or right edge of the viewport
- Rotate by dragging the remaining space in the viewport

<h3>Additional Details</h3>

Touch Controls come with a toggleable overlay which can be assigned colors.

It is recommended to disable the overlay once you are comfortable with the size of each touch region, or set the transparency very low. (note: the overlay will not be shown in the render output)

You may chose to switch the Pan and Rotate regions. If you lock the viewport rotation, Panning can be done anywhere between the Zoom control regions.

</div>
</div>

## Customizable Double-tap Action

Double-tap to trigger one of the following actions:

- "Transfer Mode" to change the active object
- Toggle Touch Control
- Toggle Local View
- Toggle Full-screen Viewport

###### _note:_ this feature only works by tapping your finger or clicking to prevent the pen from accidentally triggering it while drawing

## Custom On-screen Buttons

![gizmo bar](/docs/gizmo_bar.png)

Important features have been made available directly in the viewport. Each button can be toggled on/off from the overlay menu.

The following on-screen buttons are currently available:

- Undo/Redo
- Toggle Fullscreen Viewport
- Toggle Quad-view
- Recenter Viewport
- Change Rotation Center Point
- Toggle N-panel
- Toggle Viewport Rotation Lock
- Topology Control
- Sculpt Brush Dynamics

### Additional Details

#### Toggle Quad-view

Quad-view may sometimes replace the perspective viewport with an orthographic viewport when toggled off and on. This may cause the main viewport rotation to be automatically locked. Simply unlock it with the on-screen button.

#### Recent Viewport

This attempts to bring the active object back into view. If the origin is misaligned, it may not work perfectly.

#### Viewport Rotation Lock

Locking the viewport rotation replaces viewport rotation with panning control.

###### _NOTE:_ Quad-view will default to rotation locking for isometric viewports (top, front, and side views)

#### Topology Control

This feature provides quick access to Retopology control in Sculpt mode and is not shown in any other mode.

If the selected object has a Multi-resolution modifier; the retopology controls change to subdivision level controls.

![subdivision level control](/docs/sub-div_level.png)

Quickly jump through subdivision levels, subdivide and unsubdivide right from the viewport.

![subdivision available](/docs/subdiv_available.png)

A yellow icon means the next subdivision step needs to be calculated. It will automatically try to subdivide/unsubdivide when clicked.

![subdivision limit](/docs/subdiv_limit.png)

A red icon means you have reached your subdivision limit and it will not try to subdivide further. You may change the maximum subdivision levels available for the on-screen buttons to limit accidental subdivision.

###### _note:_ the subdivision limit only applies to increasing subdivision levels. You may unsubdivide as much as Blender is able.

#### Sculpt Brush Dynamics

This feature allows you to quickly access the UI for brush resizing and strength control in sculpt mode.

## Fully Customizable Floating Menu

<img src="/docs/sample_menu.png" width="50%">

This button allows you to assign up to 8 commands, unique to each edit mode (object, sculpt, texture paint, weight paint, etc) and reposition it where ever you want, to best fit your workspace. If you don't need it, simply disable it in the settings menu.

# Feature Roadmap

If you have a suggestion for more features, please check if it's on this list before submitting a request on Github.

I'm continuing to look at features which could improve the experience of Blender without adding too much clutter to the UI.

Currently, I'm planning to add the following features:

> - better 3D gizmos for edit mode
> - control gizmo enum (flip through object gizmos in sculpt mode)

This list will change as I explore options and get more user feedback.

# Building from Github

Building the addon zip can be done by using the included `bundle.sh` script. Simply run:

```
./bundle.sh
```

It will output the files to include and generate a new ZIP file:

```
$ ./bundle.sh
  adding: touchview/ (stored 0%)
  adding: touchview/lib/ (stored 0%)
  adding: touchview/lib/Gizmos.py (deflated 77%)
  adding: touchview/lib/items.py (deflated 68%)
  adding: touchview/lib/Operators.py (deflated 80%)
  adding: touchview/lib/Overlay.py (deflated 73%)
  adding: touchview/lib/Panel.py (deflated 69%)
  adding: touchview/lib/touch_input.py (deflated 69%)
  adding: touchview/lib/__init__.py (deflated 70%)
  adding: touchview/Settings.py (deflated 76%)
  adding: touchview/__init__.py (deflated 51%)
```

The final ZIP can be found in:

```
./bin/touchview.zip
```

# Installation

In Blender, open `Edit` > `Preferences...`.

Navigate to the `Add-ons` tab.

Click `Install...` and navigate to the `touchview.zip` file.

Select it and click `Install Add-on`.

###### _note:_ You do not need to extract it, first. Simply install the ZIP, directly

# Changelog

<details open><summary><b>v4.0.2</b></summary><br>

- `ADDED` : Nendo Tools Menu (limited options) for Image Editor and Node Editor
- `REMOVED` : Right-Click Action for Image Editor and Node Editor

</details>

<details open><summary><b>v4.0.0</b></summary><br>
Compatibility update for Blender 4.0

- `ADDED` : support for Blender 4.0
- `ADDED` : auto-save/load preferences
- `UPDATED` : replace bgl module refs with gpu module implementation
- `UPDATED` : Swap Control Regions fixed context override implementation
- `UPDATED` : early exit when dragging gizmo near edge of viewport to prevent negative overflow
- `REMOVED` : argument renaming to disregard unused args (currently breaking CI/CD)

</details>

<details open><summary><b>v2.12.0</b></summary><br>

- `UPDATED` : fixed bug with unindexed modes breaking gizmo menus
- `UPDATED` : updated resize and change strength for 2D views
- `UPDATED` : improved support for multi-mode devices

</details>

<details open><summary><b>v2.11.0</b></summary><br>

- `UPDATED` : added various GPENCIL modes to edit mode list
- `UPDATED` : updated viewport gizmo panel to support v3.6 changes

</details>

<details open><summary><b>v2.10.0</b></summary><br>

- `ADDED` : lazy camera control toggle in sculpt mode
- `UPDATED` : add support for Weylus (\*nix) sending 0.0 for pressure on touch events
- `UPDATED` : changed all new operator namespaces to `nendo` for easier identification
- `ADDED` : control mode icon when using signle-input mode
- `UPDATED` : control mode toggle and floating action button now use same sizing as gizmos
- `ADDED` : additional fine-tuning controls for gizmo spacing

</details>

<details open><summary><b>v2.9.0</b></summary><br>

- `UPDATED` : additional changes to gizmo spacing
- `UPDATED` : fixed bug preventing custom actions being assigned for radial menu

</details>

<details open><summary><b>v2.8.0</b></summary><br>

- `UPDATED` : fixed issues with menu bar spacing
- `REMOVED` : floating menu bar

</details>

<details open><summary><b>v2.7.1</b></summary><br>

- `UPDATED` : replaced region_full_area with window_fullscreen

</details>

<details open><summary><b>v2.7.0</b></summary><br>

- `ADDED` : relative remesh
- `UPDATED` : fixed error when disabling add-on

</details>

<details open><summary><b>v2.6.0</b></summary><br>

- `UPDATED` : code spec now based on flake8
- `UPDATED` : added alternative action for TransferMode when used in OBJECT mode
- `UPDATED` : fixed desktop scaling issue with radial gizmo menu
- `UPDATED` : fixed toggle touch gizmo and RC/DC action
- `UPDATED` : fixed error message when rotation locked and pan/rotate swapped

</details>

<details><summary><b>v2.5.0</b></summary><br>

- `ADDED` : Gizmo size control
- `UPDATED` : moved operators into folder

</details>

<details><summary><b>v2.4.0</b></summary><br>

- `UPDATED` : preferences access simplified with utility function
- `ADDED` : single-input mode now activates large floating toggle button

</details>

<details><summary><b>v2.3.0</b></summary><br>

- `ADDED` : Input Mode selection (for devices with only touch or pen support)

</details>

<details><summary><b>v2.2.0</b></summary><br>

- `ADDED` : Toggle control gizmo (translate, rotate, scale, none)
- `UPDATED` : Added Brush dynamics (from sculpt mode) to paint modes
  - <span style="font-size: 0.6em">NOTE: some paint/sculpt modes when in 2D/Draw canvas mode aren't yet hooked up to brush dynamics </span>

</details>

<details><summary><b>v2.1.0</b></summary><br>

- `ADDED` : Right Click Actions
- `UPDATED` : Preferences and N-Panel restructure

</details>

<details><summary><b>v2.0.0</b></summary><br>

- `UPDATED` : Gizmos-related code simplified and reorganized for easier management
- `ADDED` : floating gizmo bar and floating gizmo radial menu modes
- `ADDED` : customizable gizmo menu spacing
- `UPDATED` : viewport safe area calculation
- `UPDATED` : floating action menu to use same move/access functionality as floating radial menu
- `ADDED` : 8th custom action for floating action menu

</details>

<details><summary><b>v1.2.4</b></summary><br>

- `ADDED` : Toggle Double-tap action on/off

</details>

<details><summary><b>v1.2.3</b></summary><br>

- `ADDED` : Sculpt Brush Dynamics
- `UPDATED` : Viewport rotation in sculpt mode automatically sets pivot to mesh under touch point

</details>

<details><summary><b>v1.2.2</b></summary><br>

- `UPDATED` : Gizmo panel layout split

</details>

<details><summary><b>v1.2.1</b></summary><br>

- `REMOVED` : Middle Mouse keybind
- `REMOVED` : viewport rotation lock when using the Grease Pencil

</details>

<details><summary><b>v1.2.0</b></summary><br>

- `BREAKING`: This version requires previous version to be disabled before install
- `UPDATED` : Improved Pen detection and simplified key configs
- `ADDED` : Support for various 2D and 2D-like views (Image Editor, UV Editor, 2D Animation, Compositing, etc)

</details>

<details><summary><b>v1.1.2</b></summary><br>

- `ADDED` : Support for Node Editor

</details>

<details><summary><b>v1.1.1</b></summary><br>

- `ADDED` : minor fix to pen detection

</details>

<details><summary><b>v1.1.0</b></summary><br>

- `ADDED` : Independent toggle for entire gizmo bar
- `ADDED` : Customizable double-tap actions
- `ADDED` : Multi-resolution level limiter and gizmo status color

</details>

<details><summary><b>v1.0.1</b></summary><br>

- `ADDED` : Optional include for MIDDLEMOUSE when disabling/enabling touch controls
- `FIXED` : Preferences bug preventing toggle of floating Gizmo

</details>

<details><summary><b>v1.0.0</b></summary><br>

- `ADDED` : Toggle swap pan/rotate regions
- `ADDED` : Toggle floating menu button to N Panel
- `UPDATED` : Disabling touch controls no longer removes overlay (hot regions still work with custom keybinds and MIDDLEMOUSE)
- `UPDATED` : Disabling touch controls restores default LEFTMOUSE functionality

</details>

<details><summary><b>v0.9.6</b></summary><br>

- `ADDED` : undo/redo gizmo
- `ADDED` : overlay color selection
- `ADDED` : touch control toggle in settings
- `ADDED` : Alt+T to toggle touch controls
- `UPDATED` : N Panel now includes extra settings from addon menu
- `UPDATED` : Lock Rotation now addresses quadview data replication bug
- `UPDATED` : Limited floating gizmo to viewport area
- `UPDATED` : code cleanup and additional structure tweaks
- `REMOVED` : Gizmo Tooltips

</details>

<details><summary><b>v0.9.5</b></summary><br>

- `ADDED` : multires modifier support to gizmo bar (shows retopology tools when no modifier is present)
- `FIXED` : Gizmos now properly follow mode visibility rules
- `FIXED` : Double-tap selection now only runs in appropriate viewport modes

</details>

<details><summary><b>v0.9.4</b></summary><br>

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

> Please [report any issues](https://github.com/nendotools/touchview/issues) you find and I'll do my best to address them.

> The add-on is free, but if it helps you, please consider [supporting me](https://nendo.gumroad.com/l/touchview).
