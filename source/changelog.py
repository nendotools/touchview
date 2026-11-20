import os
import re
from collections import defaultdict

import bpy
from bpy.types import Operator

from .utils.addon import version_str

# Section keys rendered in the changelog popup, in display order, with icons.
CHANGE_SECTIONS = (
    ("added", "ADD"),
    ("fixed", "MODIFIER_DATA"),
    ("changed", "TRACKING_FORWARDS_SINGLE"),
    ("improved", "SHADERFX"),
    ("removed", "REMOVE"),
)


def parse_changelog(text: str) -> defaultdict:
    """Parse CHANGELOG.md text into ``{section: [change, ...]}``.

    Sections are ``**Added**``-style headers (matched case-insensitively);
    items are ``- `` bullet lines under the current section. Text before the
    first header is ignored.

    Args:
        text: Full changelog file content

    Returns:
        defaultdict(list): Changes keyed by lowercased section name
    """
    changes = defaultdict(list)
    key = None
    for line in text.splitlines():
        line = line.strip()

        if line.startswith("**"):
            parts = line.split("**")
            if len(parts) > 1:
                key = parts[1].lower()

        if key is None:
            continue

        if line.startswith("-"):
            # lstrip only: stripping both ends would eat trailing dashes
            changes[key].append(line.lstrip("- "))
    return changes


class TOUCHVIEW_OT_changelog(Operator):
    """Get latest changelog"""

    bl_label = "Changelog"
    bl_idname = "touchview.changelog"

    def draw(self, context):
        layout = self.layout

        layout.label(
            text=f"Changelog - v{version_str}",
            icon="RECOVER_LAST",
        )

        for change_type, icon in CHANGE_SECTIONS:
            if self.changes[change_type]:
                layout.label(text=change_type.title())
                self.draw_changes(layout, self.changes[change_type], icon)

    def draw_changes(self, layout, changes, icon):
        box = layout.box()
        col = box.column(align=True)
        for change in changes:
            row = col.row()
            if "https://discord.com" in change:
                match = re.search(r"/(\d+)\)", change)
                if match:
                    thread = match.group(1)
                    row.label(
                        text=change.replace(
                            f"(https://discord.com/channels/959138815602229389/{thread})",
                            "",
                        ),
                        icon=icon,
                    )
                    row.operator(
                        "wm.url_open", icon="LINKED", emboss=False
                    ).url = f"https://discord.com/channels/959138815602229389/{thread}"
                else:
                    row.label(text=change, icon=icon)
            else:
                row.label(text=change, icon=icon)

    def invoke(self, context, event):
        self.execute(context)
        return context.window_manager.invoke_popup(self, width=500)

    def execute(self, context):
        self.changes = defaultdict(list)
        changelog_path = os.path.join(os.path.dirname(__file__), "../CHANGELOG.md")

        if os.path.exists(changelog_path):
            try:
                with open(changelog_path, "r", encoding="utf-8") as file:
                    self.changes = parse_changelog(file.read())
            except OSError:
                pass

        return {"FINISHED"}


classes = (TOUCHVIEW_OT_changelog,)

register, unregister = bpy.utils.register_classes_factory(classes)
