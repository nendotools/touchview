# Advanced (distilled)

Live docs: <https://docs.blender.org/api/current/info_advanced.html>

## Blender as a Python module

- Special build option produces `bpy` as an importable Python module (`import bpy` outside Blender)
- Enables IDE debugging (breakpoints, variable inspection) and autocompletion of Blender modules
- Requires building Blender with the Python-module target; see
  [Building Blender as a Python module](https://developer.blender.org/docs/handbook/building_blender/python_module/)
- For this template's workflow, prefer headless validation instead:
  `blender.exe -b -P script.py` (no special build needed)
