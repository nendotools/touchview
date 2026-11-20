# Gotchas (distilled)

Live docs: <https://docs.blender.org/api/current/info_gotcha.html>
Sub-pages: [crashes](https://docs.blender.org/api/current/info_gotchas_crashes.html),
[threading](https://docs.blender.org/api/current/info_gotchas_threading.html),
[internal data](https://docs.blender.org/api/current/info_gotchas_internal_data_and_python_objects.html),
[operators](https://docs.blender.org/api/current/info_gotchas_operators.html),
[meshes](https://docs.blender.org/api/current/info_gotchas_meshes.html),
[armatures](https://docs.blender.org/api/current/info_gotchas_armatures_and_bones.html),
[file paths](https://docs.blender.org/api/current/info_gotchas_file_paths_and_encoding.html)

## Data lifetime

- Python variables can outlive the Blender data they reference (undo, file load, `bpy.data.remove`)
- Stale references raise `ReferenceError` at best, crash Blender at worst — never cache
  `bpy.data`/`bpy.context` objects across redraws or file loads; re-fetch them each use

## Operators

- Operators depend on context; calling them from the wrong context fails or silently does nothing
- Prefer direct data manipulation over `bpy.ops` in non-interactive code; when you must call
  an operator, check its `poll()` first
- `bpy.ops` calls have overhead and can trigger redraws — avoid them in loops and in `draw()`

## Modes and mesh access

- Mesh data access rules change between Object/Edit mode; some data is only valid in one mode
- Switching modes (`bpy.ops.object.mode_set`) invalidates BMesh and mesh references

## Threading

- Python threads are NOT supported for Blender API access — only the main thread may touch
  `bpy`. Use `bpy.app.timers` for deferred/periodic work instead

## Crashes

- Accessing freed data crashes rather than raising — enable `WITH_PYTHON_SAFETY` builds to
  convert these into exceptions when debugging

## File paths

- Always use `bpy.path.abspath("//relative.blend")` for blend-relative paths; never assume CWD
