---
name: blender-api
description: "Blender Python API (bpy) knowledge base: data access, context, operators, panels, properties, class registration, and version-to-version API changes. Use when writing or debugging any Blender add-on code, using bpy.data or bpy.context, registering classes, drawing UI, resolving poll/context errors, or handling API differences between Blender versions."
---

# Blender Python API

Distilled knowledge from the official API docs. Each reference file covers one doc
page and links to the live documentation for full details.

## When to Use

- Writing or debugging code that touches `bpy`, `mathutils`, `bmesh`, or `bpy_extras`
- Registering classes, attaching properties, drawing panels/menus
- Resolving `RuntimeError: ... poll() failed` or context errors
- Supporting multiple Blender versions (legacy `bl_info` 3.3+ and extension manifest 4.2+)

## Core Rules

### Data access

- `bpy.data` — blend-file data by name or index (`bpy.data.objects["Cube"]`); index order is
  not stable across a session, prefer name lookups
- `bpy.context` — user state (`active_object`, `selected_objects`, `mode`); the container is
  read-only: `bpy.context.active_object = obj` raises — use `context.view_layer.objects.active = obj`
- Data-blocks are created/removed through collections (`bpy.data.meshes.new(...)`,
  `bpy.data.meshes.remove(...)`), never by calling `bpy.types.Mesh()`
- `mathutils` values are live references to Blender data — `.copy()` before storing or mutating

### Operators

- Always implement `poll()`; calling an operator whose poll fails raises `RuntimeError` —
  check `bpy.ops.<module>.<idname>.poll()` before calling other operators
- `bpy.ops.xxx()` calls `execute()` directly, skipping `invoke()` — never put required state
  computation only in `invoke()`
- Report to the user with `self.report({'WARNING', 'INFO'}, "message")`

### Registration

- Every module exposes symmetric `register()`/`unregister()`; unregister mirrors register in reverse
- Classes are validated on registration — wrong argument counts or bad `bl_` types raise immediately
- PropertyGroups must be registered before being referenced by a `PointerProperty`
- Delete attached properties (`del bpy.types.Scene.xxx`) BEFORE unregistering their class

### Style (Blender-specific)

- Single quotes for enums, double quotes for strings
- 4-space indentation, explicit imports (no wildcard `*`)
- UI layout variable names: `row`, `col`, `split`, `flow`, `sub`

## References

| File                                                  | Topic                                                        | Live docs                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [quickstart.md](./references/quickstart.md)           | Data access, context, operators, first operator/panel        | [Quickstart](https://docs.blender.org/api/current/info_quickstart.html)             |
| [overview.md](./references/overview.md)               | Environment, script loading, class integration, registration | [API Overview](https://docs.blender.org/api/current/info_overview.html)             |
| [api-reference.md](./references/api-reference.md)     | Finding data paths, ID data-blocks, nested properties        | [API Reference Usage](https://docs.blender.org/api/current/info_api_reference.html) |
| [best-practice.md](./references/best-practice.md)     | Style conventions, UI layout, script efficiency              | [Best Practice](https://docs.blender.org/api/current/info_best_practice.html)       |
| [tips-and-tricks.md](./references/tips-and-tricks.md) | Terminal, headless runs, external editors                    | [Tips & Tricks](https://docs.blender.org/api/current/info_tips_and_tricks.html)     |
| [gotchas.md](./references/gotchas.md)                 | Crashes, operator misuse, modes, threading, data lifetime    | [Gotchas](https://docs.blender.org/api/current/info_gotcha.html)                    |
| [advanced.md](./references/advanced.md)               | Blender as a Python module                                   | [Advanced](https://docs.blender.org/api/current/info_advanced.html)                 |
| [changelog.md](./references/changelog.md)             | API changes between Blender releases                         | [Change Log](https://docs.blender.org/api/current/change_log.html)                  |
