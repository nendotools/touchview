# Change Log (how to use)

Live docs: <https://docs.blender.org/api/current/change_log.html>

The official change log lists API additions/removals/renames per Blender release
(e.g. "5.1 to 5.2" sections organized by `bpy.types.*` class).

## When to consult it

- An attribute or function that used to work now raises `AttributeError` after a Blender upgrade
- Supporting a range of Blender versions and unsure when an API appeared
- Writing version guards (e.g. `if bpy.app.version >= (4, 2, 0):`)

## Practical notes for this template

- The template targets Blender 3.3+ (legacy `bl_info`) and 4.2+ (extension manifest) —
  API differences across that span are significant (e.g. `bl_info` vs manifest,
  extension permissions, node interface API changes in 4.0)
- Known cross-version quirks (from project experience):
  - `tree.interface.new_socket(..., socket_type=...)` takes the `bl_idname` enum
    (`"NodeSocketBool"`, NOT `"NodeSocketBoolean"`)
  - `node.inputs["Subsurface IOR"]` key lookup can fail on Principled BSDF in 5.2 even
    though the socket exists — iterate `node.inputs` and match by `.name`
  - Material Output input socket is named `"Surface"` (not `"Shader"`) in 5.x
- When bumping `blender_version_min` in `blender_manifest.toml`, re-check the change log
  for removed/renamed APIs used by the add-on
