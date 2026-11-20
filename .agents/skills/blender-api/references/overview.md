# API Overview (distilled)

Live docs: <https://docs.blender.org/api/current/info_overview.html>

## Environment

- Blender embeds a Python interpreter; `bpy` and `mathutils` are importable from any script
- Startup scripts live in `scripts/startup/` and are imported on launch

## Script loading

- Prefer importing scripts as modules over executing them directly — registered classes stay
  reachable inside the module for later unregister
- Add-ons are modules enabled from preferences; extensions additionally require
  `blender_manifest.toml`
- This template ships both metadata modes: legacy `bl_info` (3.3+) and manifest (4.2+)

## Integration through classes

- Supported integration points: `Panel`, `Menu`, `Operator`, `PropertyGroup`, `KeyingSet`,
  `RenderEngine` — intentionally limited; anything deeper needs C/C++
- `bl_` prefix distinguishes Blender-defined attributes from your own
- Do not define `__init__`/`__del__` unless required (e.g. `RenderEngine`); if defined, the
  Blender parent constructor MUST be called (hard requirement since 4.4)
- Class mix-ins work; registration checks use attributes/functions from parent classes
- You cannot instantiate registered classes yourself — Blender does; run operators via `bpy.ops`

## Registration

- `register()`/`unregister()` are the only functions Blender calls in your module
- Register order matters for property groups: lowest class first; `unregister()` is the exact mirror
- Attach properties after registering their group:
  `bpy.types.Material.my_custom_props = bpy.props.PointerProperty(type=MyMaterialGroupProps)`
- `del` the attached property BEFORE unregistering its class
- Sanity checks run at registration: wrong function signatures or `bl_` types raise immediately,
  e.g. `ValueError: expected Operator ... "execute" function to have 2 args, found 3`
