# Tips and Tricks (distilled)

Live docs: <https://docs.blender.org/api/current/info_tips_and_tricks.html>

## Terminal

- Run Blender from a terminal to see `print()` output and full tracebacks — many errors
  never surface in the UI
- Ctrl-C in the terminal kills a runaway script

## Interface tricks

- Ctrl-C over any button copies its `bpy.ops...` command
- Right-click → Copy Data Path gives the animation-style path to a property
- `--debug-wm` (or `bpy.app.debug_wm = True`) logs every operator call

## External editor / reloading

- Reload a module under test: `importlib.reload(myscript)` — otherwise the cached
  `sys.modules` version is used
- Add the script's directory to `sys.path` before importing

## Headless runs

- `blender --background --python myscript.py` — fastest iteration loop for non-interactive code
- Optionally open a blend-file first: `blender myscene.blend --background --python myscript.py`
- Check results by rendering to a fixed image path, saving a blend, or printing values

## Bundled Python

- Blender ships its own Python; system packages are not visible to it
- Match the exact Python (major, minor) version when mixing environments

## Debugging

- Drop an interactive interpreter anywhere in a script:
  `__import__('code').interact(local=dict(globals(), **locals()))`
- `IPython.embed()` if IPython is available
