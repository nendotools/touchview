# Quickstart (distilled)

Live docs: <https://docs.blender.org/api/current/info_quickstart.html>

## Data access

- Access blend data via `bpy.data`: `bpy.data.objects`, `bpy.data.scenes`, `bpy.data.materials`
- Collections support index and string access; indexes may change while Blender runs — prefer names
- Data-blocks cannot be constructed directly (`bpy.types.Mesh()` raises `TypeError`);
  create/remove via collections: `bpy.data.meshes.new(name=...)`, `bpy.data.meshes.remove(mesh)`
- Custom properties (ID properties): `obj["MyProp"] = 42`, `obj.get("MyProp", "fallback")`;
  only basic types (int/float/str, arrays, dicts with string keys, max 1024 nesting levels)

## Context

- `bpy.context` holds user state: `object`, `selected_objects`, `active_object`, `mode`
- Read-only container: assign through the data API instead (`context.view_layer.objects.active = obj`)
- Context members differ per editor — guard access when the calling context is unknown

## Operators

- Call as `bpy.ops.mesh.flip_normals()`; returns a set like `{'FINISHED'}`
- Poll failures raise `RuntimeError` — check `bpy.ops.<op>.poll()` before calling
- Use `self.report({'WARNING', 'INFO'}, "message")` for user feedback

## Integration

- Subclass `bpy.types.Operator` / `bpy.types.Panel` with `bl_` attributes
- Register/unregister classes in module-level `register()`/`unregister()`
- Append to menus via `bpy.types.VIEW3D_MT_object.append(menu_func)`; remove on unregister

## Types

- Blender floats/ints/bools map to Python natives; enums map to strings; multi-enums to sets of strings
- `bpy_struct` wraps live data — changes apply immediately
- `mathutils` types reference live data; `.copy()` to detach before modifying

## Animation

- High level: `obj.keyframe_insert(data_path="location", frame=10.0, index=2)`
- Low level (5.x): create action → slot → layer → strip → channelbag → fcurve
