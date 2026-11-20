---
name: blender-conventions
description: "Coding conventions for this Blender add-on template: SOLID principles, unabbreviated clean names, the no-comments-unless-needed rule, Blender class naming (XX_OT_/XX_PT_/XX_UL_/XX_MT_/XX_AP_/XX_PG_), registration patterns, panel mixin, operator poll/description, and rules against unnecessary abstractions. Use when writing, refactoring, or reviewing any Python code in this add-on, adding operators/panels/properties, or forking the template for a new add-on."
---

# Blender Add-on Conventions

How code is written in this template. Follow these for every change, and keep the
template itself **addon-agnostic** — it is the base for forking new add-ons, so never
bake one add-on's specifics into shared modules.

## When to Use

- Writing or modifying any Python in `source/`
- Adding operators, panels, menus, UILists, property groups, preferences, keymaps
- Reviewing code for SOLID/naming/flow/comment compliance
- Forking the template into a new add-on (the `XX_` prefix rename)

## Comments

- **No comments unless the code cannot speak for itself** — names and structure carry
  the meaning
- Comment only what a reader cannot infer: intent behind a non-obvious decision, a Blender
  API quirk, a version-specific workaround (with the reason), or a deprecation
- Never restate the next line, narrate the obvious, use banners/section dividers, or park
  commented-out code — delete it or fix the name instead
- Docstrings are the exception: Google style with `Args:`/`Returns:` blocks and type
  annotations (see `source/utils/addon.py`)

## Naming

- **No abbreviations**: `matching_keymap_items`, not `kmis`; `convert_keymap_item_to_string`,
  not `conv_kmi`. If a name needs a comment to explain, rename it.
- **Blender class naming**: `{ADDON}_{TYPE}_{NAME}` — `XX_OT_test` (operator, idname `xx.test`),
  `XX_PT_object_mode` (panel), `XX_UL_demo_list` (UIList), `XX_MT_preset_menu` (menu),
  `XX_AP_preference` (AddonPreferences), `XX_PG_test` (PropertyGroup)
- `XX_` is the placeholder prefix — replace consistently across ALL files when forking
- Modules: lowercase underscore (`ops/`, `ui/`, `utils/`); one concern per module

## SOLID

- **Single responsibility**: one operator = one user action; one panel = one UI section;
  one util module = one concern (`icon.py` icons, `keymap.py` keymaps). Never let an operator
  also draw UI or manage registration.
- **Open/closed**: extend via the `Addon` panel mixin and the per-module
  `register()`/`unregister()` pattern; don't modify working shared modules to add a feature —
  add a new module and wire it into the parent `__init__.py`.
- **Liskov/Interface segregation**: panels inherit `(Panel, Addon)`; the mixin provides
  `bl_space_type`/`bl_region_type`/`bl_category` and shared helpers like `draw_list()` —
  change the sidebar category once in `ui/panels.py`.
- **Dependency inversion**: UI reads helpers from `utils/` (`addon.preferences()`,
  `addon.tag_redraw()`, `icons[...]`) instead of reaching into `bpy` internals directly.

## Flow & Structure

- Linear, obvious execution; **early returns** over nesting
- `register()`/`unregister()` must stay **symmetric** — unregister mirrors register in exact
  reverse order at every level (module → package → root)
- New module → add import + call in the parent package `__init__.py`
- Classes registered via `bpy.utils.register_classes_factory(classes)`; the exception is
  `props.py`, which uses explicit loops so scene pointers can be attached/detached around
  class registration
- Scene properties: attach with `PointerProperty` in `props.py` `register()`;
  `del bpy.types.Scene.xxx` in `unregister()` BEFORE unregistering the class

## Operators

- Implement `poll()` (guard context/mode) and `description()` — both as classmethods
- Tooltip keymap hints use `\n` + `•` formatting (see `source/ops/test.py`)
- No `bpy.ops` calls inside `draw()` code
- Guard `context.area` before `tag_redraw()` so operators also work headless

## Avoid Unnecessary Abstractions

- Prefer direct, readable Blender API calls over wrapper layers
- Add a helper only when used more than once AND it removes real duplication
- No speculative "just in case" parameters, no config systems for values used once
- If a function is a one-line pass-through to `bpy`, delete it and call `bpy` directly

## Template Assets

- Icons: drop PNGs into `icons/` (auto-loaded, recursive) → `icons["NAME"]` as `icon_value=`
- Preview thumbnails: `previews/` → exposed via the `enum_previews` callback
- Changelog: `CHANGELOG.md` sections `**Added**`/`**Fixed**`/`**Changed**`/`**Improved**`/
  `**Removed**` with `- ` items — the changelog operator parses this exact format
- Docs: keep `doc_url` (in `bl_info` AND `blender_manifest.toml`), `manual.py`, and the Help
  panel links in sync
- Version lives in **both** `bl_info["version"]` and `blender_manifest.toml` — bump together

## Related

- API knowledge: the `blender-api` skill
- Project structure and build commands: `AGENTS.md`
