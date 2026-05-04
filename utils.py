import bpy

from .constants import ADDON_ID


def get_addon_preferences(context=None):
    context = context or bpy.context
    prefs = getattr(context, "preferences", None)
    if prefs is None:
        return None
    addon = prefs.addons.get(ADDON_ID)
    return addon.preferences if addon else None


def format_hotkey_label(key):
    number_map = {
        "ZERO": "0",
        "ONE": "1",
        "TWO": "2",
        "THREE": "3",
        "FOUR": "4",
        "FIVE": "5",
        "SIX": "6",
        "SEVEN": "7",
        "EIGHT": "8",
        "NINE": "9",
    }
    return number_map.get(key, key)


def build_shortcut_label(key, use_ctrl, use_shift, use_alt):
    parts = []
    if use_ctrl:
        parts.append("Ctrl")
    if use_shift:
        parts.append("Shift")
    if use_alt:
        parts.append("Alt")
    parts.append(format_hotkey_label(key))
    return "+".join(parts)
