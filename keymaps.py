import bpy

from . import state
from .orbit import VIEW3D_OT_call_orbit_pie, draw_orbit_header_buttons
from .quick_favorites import WM_OT_call_quick_favorites_pie
from .sculpt import SCULPT_OT_call_brush_pie, SCULPT_OT_call_default_brush_popup
from .utils import get_addon_preferences


def clear_keymaps():
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        state.addon_keymaps.clear()
        return

    keyconfig = wm.keyconfigs.addon
    if keyconfig is None:
        state.addon_keymaps.clear()
        return

    for km, kmi in state.addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (ReferenceError, RuntimeError, ValueError):
            pass
    state.addon_keymaps.clear()


def ensure_header_state():
    prefs = get_addon_preferences()
    should_register = bool(prefs and prefs.enable_orbit_menu)

    if should_register and not state.header_registered:
        bpy.types.VIEW3D_HT_header.append(draw_orbit_header_buttons)
        state.header_registered = True
    elif not should_register and state.header_registered:
        disable_header()


def disable_header():
    if not state.header_registered:
        return
    try:
        bpy.types.VIEW3D_HT_header.remove(draw_orbit_header_buttons)
    except ValueError:
        pass
    state.header_registered = False


def register_keymaps():
    clear_keymaps()

    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return

    keyconfig = wm.keyconfigs.addon
    if keyconfig is None:
        return

    prefs = get_addon_preferences()
    if prefs is None:
        return

    if prefs.enable_orbit_menu:
        km = keyconfig.keymaps.new(name="3D View Generic", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            VIEW3D_OT_call_orbit_pie.bl_idname,
            type=prefs.orbit_hotkey,
            value="PRESS",
            ctrl=prefs.orbit_use_ctrl,
            shift=prefs.orbit_use_shift,
            alt=prefs.orbit_use_alt,
        )
        state.addon_keymaps.append((km, kmi))

    if prefs.enable_sculpt_menu:
        km = keyconfig.keymaps.new(name="3D View Generic", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            SCULPT_OT_call_brush_pie.bl_idname,
            type=prefs.sculpt_hotkey,
            value="PRESS",
            ctrl=prefs.sculpt_use_ctrl,
            shift=prefs.sculpt_use_shift,
            alt=prefs.sculpt_use_alt,
        )
        state.addon_keymaps.append((km, kmi))

        km = keyconfig.keymaps.new(name="Sculpt", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            SCULPT_OT_call_default_brush_popup.bl_idname,
            type=prefs.sculpt_popup_hotkey,
            value="PRESS",
            ctrl=prefs.sculpt_popup_use_ctrl,
            shift=prefs.sculpt_popup_use_shift,
            alt=prefs.sculpt_popup_use_alt,
            head=True,
        )
        state.addon_keymaps.append((km, kmi))

    if prefs.enable_quick_favorites_menu:
        km = keyconfig.keymaps.new(name="Window", space_type="EMPTY")
        kmi = km.keymap_items.new(
            WM_OT_call_quick_favorites_pie.bl_idname,
            type=prefs.quick_favorites_hotkey,
            value="PRESS",
            ctrl=prefs.quick_favorites_use_ctrl,
            shift=prefs.quick_favorites_use_shift,
            alt=prefs.quick_favorites_use_alt,
        )
        state.addon_keymaps.append((km, kmi))


def refresh_ui_and_keymaps():
    ensure_header_state()
    if not bpy.app.background:
        register_keymaps()


def update_addon_state(self, context):
    del self, context
    refresh_ui_and_keymaps()
