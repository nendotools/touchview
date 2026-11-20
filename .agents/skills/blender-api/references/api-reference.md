# API Reference Usage (distilled)

Live docs: <https://docs.blender.org/api/current/info_api_reference.html>

## Finding data paths

- Button tooltips show the `Python: ...` path; right-click → Online Python Reference
- Right-click → Copy Data Path gives the path from an ID data-block to a property
- Follow the "References" section at the bottom of a type's docs page to find where it is
  accessed from
- Convention: `active_*` members (`active_object`, `active_bone`, `active_node`) hold the
  user's current selection

## ID data-blocks

- Top-level containers: Scene, Collection, Object, Mesh, Workspace, World, Armature, Image,
  Texture — full list: subclasses of `bpy.types.ID`
- Accessible from `bpy.data.*`; unique `.name`; animation in `.animation_data`; only ID types
  can be linked between blend-files
- `bpy.data` is an instance of `bpy.types.BlendData` — the docs list its collections there

## Nested properties

- Compose paths step by step, e.g.
  `bpy.context.tool_settings.sculpt.brush.texture.contrast`
- Use `bpy.context` for user-facing tools (operate on the selection);
  use `bpy.data` for automation (specific data regardless of selection)

## Operators

- Hover a button → tooltip shows the `bpy.ops...` call; Ctrl-C copies it
- The Info editor records executed operators (those with `REGISTER`); `--debug-wm` shows all
