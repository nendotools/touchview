import bpy
from mathutils import Matrix, Vector

from ..utils.addon import preferences
from ..utils.blender import *
from .gizmo_config import gizmo_colors, toggle_colors

##
# GizmoSet
#   - single-state
#     - one icon
#     - one action
#     - possible toggle by variable state
#
#   - 2-state (boolean)
#     - 2 icons
#     - 2 actions (or 1 action for both icons)
#
##


class GizmoSet:
    group: bpy.types.GizmoGroup

    def setup(self, group: bpy.types.GizmoGroup, config: dict):
        self._init(group, config)
        self.primary = self._build_gizmo(config["command"], config["icon"])

    def _init(self, group: bpy.types.GizmoGroup, config: dict):
        self.visible = True
        self.config = config
        self.has_dependent = config.get("has_dependent", False)
        self.group = group
        self.scale = config.get("scale", 14)
        self.binding = config["binding"]
        self.has_attribute_bind = self.binding.get("attribute", False)

    def draw_prepare(self):
        prefs = preferences()
        self.hidden = not prefs.show_gizmos
        self.skip_draw = False
        self._update_visible()

        if self.binding["name"] == "float_menu":
            self.primary.hide = not prefs.show_float_menu
            self.primary.use_grab_cursor = False
            self.primary.scale_basis = 18 * prefs.gizmo_scale
        elif self.binding["name"] == "menu_controller":
            self.primary.hide = "float" not in prefs.menu_style or not prefs.show_menu
            self.primary.use_grab_cursor = False
            self.primary.show_drag = True
            self.primary.scale_basis = (36 * prefs.menu_spacing) * prefs.gizmo_scale
        else:
            self.primary.scale_basis = 18 * prefs.gizmo_scale

    def move(self, position: Vector):
        self.primary.matrix_basis = Matrix.Translation(position)

    def _update_visible(self):
        prefs = preferences()
        if not prefs.show_menu and self.binding["name"] not in ["float_menu"]:
            self.visible = False
            self.primary.hide = True
            return
        if self.binding["location"] == "prefs":
            self.visible = self._binding_enabled() and self.binding["name"] in prefs.get_gizmo_set(bpy.context.mode)

        if self.visible:
            self.visible = self._visibility_lock() and not self._check_attribute_bind()
        self.primary.hide = not self.visible

    def _binding_enabled(self) -> bool:
        return getattr(preferences(), "show_" + self.binding["name"])

    def _visibility_lock(self) -> bool:
        if preferences().menu_style == "fixed.bar":
            return True
        return not self.hidden

    # if an attribute being assigned to active_object should hide/show bpy.types.Gizmo
    def _check_attribute_bind(self):
        if not self.has_attribute_bind:
            return False
        bind = self.binding["attribute"]
        state = self._find_attribute(bind["path"], bind["value"]) == bind["state"]
        return not state

    # search for attribute, value through context.
    # will traverse bpy.types.bpy_prop_collection entries
    # by next attr to value comparison
    def _find_attribute(self, path: str, value: str):
        names = path.split(".")
        current = bpy.context
        for i, prop in enumerate(names):
            current = getattr(current, prop)
            if current is None:
                return False

            if isinstance(current, bpy.types.bpy_prop_collection):
                item = ""
                for item in current:
                    if getattr(item, names[i + 1]) == value:
                        return True
                return False
        return getattr(current, value)

    # initialize each gizmo, add them to named list with icon name(s)
    def _build_gizmo(self, command: str, icon: str) -> bpy.types.Gizmo:
        gizmo = self.group.gizmos.new("GIZMO_GT_button_2d")
        gizmo.target_set_operator(command)
        gizmo.icon = icon  # type: ignore
        gizmo.use_tooltip = True  # show operator description on hover
        gizmo.use_event_handle_all = True  # don't pass events e.g. shift+a to add
        gizmo.use_grab_cursor = "use_grab_cursor" in self.config
        gizmo.show_drag = False  # show default cursor
        gizmo.line_width = 5.0
        gizmo.use_draw_modal = True  # show gizmo while dragging
        gizmo.draw_options = {"BACKDROP", "OUTLINE"}  # type: ignore
        self._set_colors(gizmo)
        gizmo.scale_basis = 0.1
        return gizmo

    def _set_colors(self, gizmo: bpy.types.Gizmo):
        gizmo.color = gizmo_colors["active"]["color"]
        gizmo.color_highlight = gizmo_colors["active"]["color_highlight"]
        gizmo.alpha = gizmo_colors["active"]["alpha"]
        gizmo.alpha_highlight = gizmo_colors["active"]["alpha_highlight"]


class GizmoSetBoolean(GizmoSet):
    def setup(self, group: bpy.types.GizmoGroup, config: dict):
        self._init(group, config)
        self.on_gizmo = self._build_gizmo(config["command"], config["onIcon"])
        self.off_gizmo = self._build_gizmo(config["command"], config["offIcon"])
        self._set_active_gizmo(True)

    def _set_active_gizmo(self, state: bool):
        self.on_gizmo.hide = True
        self.off_gizmo.hide = True
        self.primary = self.on_gizmo if state else self.off_gizmo

    def draw_prepare(self):
        prefs = preferences()
        self.hidden = not prefs.show_gizmos
        self.skip_draw = False
        self._update_visible()
        self.primary.scale_basis = 18 * prefs.gizmo_scale
        self.primary.use_grab_cursor = False
        if self.binding["name"] == "float_toggle":
            self._set_toggle_colors(self.primary)

    def _update_visible(self):
        prefs = preferences()
        bind = self.binding
        # the floating toggle is a standalone button, independent of the gizmo menu
        if bind["name"] == "float_toggle":
            self.visible = prefs.input_mode != "FULL" or prefs.enable_floating_toggle
            self._set_active_gizmo(prefs.is_enabled)
            self.primary.hide = not self.visible
            return

        if not prefs.show_menu and bind["name"] not in ["float_menu"]:
            self.visible = False
            self.primary.hide = True
            return
        self.visible = self._binding_enabled()

        if self.visible:
            self.visible = self._visibility_lock() and not self._check_attribute_bind()

        self._set_active_gizmo(self._find_attribute(bind["location"], bind["name"]))
        self.primary.hide = not self.visible

    def _set_toggle_colors(self, gizmo: bpy.types.Gizmo):
        mode = "active" if preferences().is_enabled else "inactive"
        gizmo.color = toggle_colors[mode]["color"]
        gizmo.color_highlight = toggle_colors[mode]["color_highlight"]
        gizmo.alpha = toggle_colors[mode]["alpha"]
        gizmo.alpha_highlight = toggle_colors[mode]["alpha_highlight"]
