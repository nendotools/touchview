# AGENTS.md

Addon-agnostic boilerplate guide. Applies to the template and every fork alike. Never bake one add-on's specifics into the shared modules.

## 1. Hard Rules

Agents **write and edit code only**. Commit, build, and release belong to the user.

| Category        | Allowed                                   | Never                                                                                                       |
| --------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Git             | `git status`, `git diff`, `git log`       | `git commit`, `git push`, `make commit`                                                                     |
| Build / release | —                                         | `make build`, `make release`, `build.bat`, `make create_pr`, `make merge_pr`, `make create_release`, `gh …` |
| Working tree    | Leave changes uncommitted; summarize them | Anything that mutates history, branches, or the tree                                                        |

## 2. Architecture

```
__init__.py            # bl_info only; delegates to source
blender_manifest.toml  # extension metadata (id, version, blender_version_min)
source/
  changelog.py         # XX_OT_changelog operator; parses CHANGELOG.md into a popup
  ops/                 # Operators (XX_OT_*)
  ui/                  # Panels (XX_PT_*), UILists (XX_UL_*), Menus (XX_MT_*)
  utils/
    addon.py           # package, version, version_str, preferences(), tag_redraw(), timer
    log.py             # PREFIX tag + log(); worker stdout markers parsed by the parent
    icon.py            # loads icons/*.png into `icons` dict (name -> icon_id)
    preview.py         # loads previews/*.png into EnumProperty items
    props.py           # PropertyGroups (XX_PG_*); attaches Scene pointer properties
    prefs.py           # AddonPreferences (XX_AP_*)
    keymap.py          # addon keymaps; register in keyconfigs.addon, not user
    manual.py          # online manual map (bpy.ops idname -> docs page)
```

- **Registration pattern** — every module exposes `register()`/`unregister()`; each package `__init__.py` calls its children in order. Register classes via `bpy.utils.register_classes_factory(classes)` (explicit loops when scene properties must be attached, as in `props.py`). New module → add import + call in the parent `__init__.py`.
- **Panel mixin** — `ui/panels.py` defines an `Addon` mixin (`bl_space_type`, `bl_region_type`, `bl_category`) all panels inherit from; the sidebar category changes once there.

## 3. Conventions

| Area             | Rule                                                                                                                                                                                                                                                                                                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Naming           | `{ADDON}_{TYPE}_{NAME}`. Template prefix is `XX_` (`XX_OT_`, `XX_PT_`, `XX_UL_`, `XX_MT_`, `XX_AP_`, `XX_PG_`; idnames `xx.*`) — replace consistently across all files when forking.                                                                                                                                                                  |
| Operators        | Implement `poll()` (guard context) and `description()` classmethods; format keymap hints with `\n` + `•` (see `ops/test.py`).                                                                                                                                                                                                                         |
| Properties       | Attach to `bpy.types.Scene` in `props.py` via `PointerProperty`; delete in `unregister()` before unregistering classes.                                                                                                                                                                                                                               |
| Icons            | PNGs in `icons/` (auto-loaded, recursive) referenced as `icons["NAME"]` → `icon_value=`. Name the add-on mark `LOGO.png` — it also brands the 5.2+ sidebar tab through `bl_icon_value`. Previews in `previews/`, exposed by the `enum_previews` callback.                                                                                             |
| Changelog format | `CHANGELOG.md` uses `**Added**` / `**Fixed**` / `**Changed**` / `**Improved**` / `**Removed**` sections with `- ` items — the operator parses this exact format.                                                                                                                                                                                      |
| Docs URLs        | Three intentionally separate URLs — never sync or unify. `doc_url` in `bl_info` = add-on docs page (Help → Documentation, read via `utils/addon.py`); `website` in `blender_manifest.toml` = marketplace/project site; base URL in `utils/manual.py` = per-operator manual map (`bpy.utils.register_manual_map`, powers right-click → Online Manual). |

## 4. Coding Principles

- **SOLID** — single-purpose operators/panels/utils; open for extension via the mixin + registration pattern, closed for modification.
- **Clean names** — descriptive, unabbreviated (`matching_keymap_items`, not `kmis`). Match the existing Args/Returns docstring style.
- **No unnecessary abstractions** — prefer direct, readable Blender API calls over wrapper layers; add a helper only when used more than once and it removes real duplication.
- **Maintainable flow** — linear, obvious execution; early returns over nesting; keep `register`/`unregister` symmetric.
- **No comments unless the code cannot speak for itself** — names and structure carry the meaning. Comment only what a reader cannot infer: intent behind a non-obvious decision, a Blender API quirk, a version-specific workaround (with the reason), or a deprecation. Never restate the next line, narrate the obvious, use banners/section dividers, or park commented-out code — delete it or fix the name instead. Docstrings are the exception: keep the Google style from **Clean names**.
- **Blender best practices** — follow the [style guide](https://docs.blender.org/api/current/info_best_practice.html): correct `poll`, no `bpy.ops` in draw code, safe `bpy.context` access.

## 5. Gotchas

| File                     | Gotcha                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `keymap.py`              | Register in `keyconfigs.addon` (never `user`), store in `addon_keymaps`, remove on unregister — else they leak between sessions.     |
| `icon.py` / `preview.py` | Remove preview collections in `unregister()` or Blender leaks memory; `icon.register()` defensively unregisters first on re-run.     |
| `changelog.py`           | Reads `CHANGELOG.md` relative to the module file — keep it at repo root.                                                             |
| `bl_info`                | Required for legacy installs even with a manifest; keep metadata duplicated and consistent — bump `version` in both places together. |

## 6. Supported Blender Versions

Support is **each add-on's declared minimum through the latest Blender API release (maximum, currently 5.2)** — the add-on must work across that whole span. The minimum comes from the fork's own `bl_info` (this repo: 3.3; a fork may declare 4.2).

- **Minimum** — read `bl_info["blender"]` from `__init__.py` ((3, 3, 0) here). If `bl_info` is absent, fall back to `blender_version_min`. **Never edit `blender_version_min` in `blender_manifest.toml`** — it stays `4.2.0`, the Extensions platform floor, independent of the legacy `bl_info` minimum.
- **Maximum** — latest API release, currently 5.2. Verify at [docs.blender.org/api/current/](https://docs.blender.org/api/current/) and bump when a new API ships.
- **Version gates** — gate version-specific APIs with `bpy.app.version`; see the "Blender version dispatch" section of `README.md` for the `_v3`/`_v4` sibling-file pattern.
- **Keep `README.md` current** in the same change whenever host architecture changes — it is the host-add-on reference this document defers to.

## 7. Headless Testing

Local builds live in `%USERPROFILE%\Downloads\Blender\stable\` (the Windows user profile's Downloads folder) — one folder per release (the hash suffix changes each build). Do not hardcode versions: enumerate the folder and run the test script against **every** build present at or above the declared minimum, so version-gated code is checked at each step of the LTS ladder.

```powershell
Get-ChildItem "$env:USERPROFILE\Downloads\Blender\stable" -Directory | ForEach-Object {
    & "$($_.FullName)\blender.exe" -b --factory-startup --python path\to\script.py
}
```

- Pay extra attention to the declared minimum and the latest build; the intermediate builds catch regressions in version-gated APIs (socket names, EEVEE, Grease Pencil, snapping) that are easy to miss.
- `preferences.system.ui_scale` reports `0.0` in background mode (GUI-only) — stub it when testing pixel-sized math.

## 8. Changelog Entries

Draft concise `CHANGELOG.md` entries so release notes are review-ready — the user still runs the release flow.

- **Host add-on only** — never draft entries for `qbpy` submodule changes.
- **Release delta only** — describe what the working branch has that `main` does not (`git log main..HEAD`, `git diff main...HEAD`). Add the entry once the work is committed to `dev`.
- **No work-in-progress entries** — never add one for unreleased `dev` work or a fix to code not yet on `main`; update the existing draft entry instead.
- **User-visible changes** get their own entry; hidden/internal changes go under the best-fitting section (`**Added**` / `**Fixed**` / `**Changed**` / `**Improved**` / `**Removed**`), not all folded into `**Fixed**`.
- **`**Fixed**`** keeps the ~10–12 most important user-visible fixes; merge related fixes into one entry.
- **One line each** — target ≤ ~60 characters so it does not wrap in the popup (fixed 500 px width; see `source/changelog.py`).

## 9. References

**Skills** (`.agents/skills/`) — load on demand:

- **`blender-api`** — distilled bpy knowledge (data access, context, operators, registration, gotchas, version changes) with per-doc-page references; load when writing or debugging `bpy` instead of re-fetching docs.
- **`blender-conventions`** — SOLID, naming, no-comments-unless-needed, registration patterns, and no-unnecessary-abstraction rules for this codebase.

**Blender API docs:**

- [Quickstart](https://docs.blender.org/api/current/info_quickstart.html) · [Overview](https://docs.blender.org/api/current/info_overview.html) · [API Reference](https://docs.blender.org/api/current/info_api_reference.html)
- [Best Practice](https://docs.blender.org/api/current/info_best_practice.html) · [Tips & Tricks](https://docs.blender.org/api/current/info_tips_and_tricks.html) · [Gotchas](https://docs.blender.org/api/current/info_gotcha.html)
- [Advanced](https://docs.blender.org/api/current/info_advanced.html) · [API Changelog](https://docs.blender.org/api/current/change_log.html)

Host-add-on specifics (architecture, naming, version dispatch, background bake) live in `README.md`.
