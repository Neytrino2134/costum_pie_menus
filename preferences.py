import bpy

from .constants import ADDON_ID, KEY_ITEMS
from .keymaps import update_addon_state
from .utils import build_shortcut_label


class CostumPieMenusPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    show_orbit_settings: bpy.props.BoolProperty(
        name="Orbit Pie Menu Settings",
        default=True,
    )
    show_sculpt_settings: bpy.props.BoolProperty(
        name="Sculpt Brush Pie Menu Settings",
        default=True,
    )
    show_quick_favorites_settings: bpy.props.BoolProperty(
        name="Quick Favorites Pie Menu Settings",
        default=True,
    )

    enable_orbit_menu: bpy.props.BoolProperty(
        name="Enable Orbit Pie Menu",
        default=True,
        update=update_addon_state,
    )
    orbit_hotkey: bpy.props.EnumProperty(
        name="Key",
        description="Key used to open the Orbit pie menu",
        items=KEY_ITEMS,
        default="T",
        update=update_addon_state,
    )
    orbit_use_shift: bpy.props.BoolProperty(
        name="Shift",
        default=True,
        update=update_addon_state,
    )
    orbit_use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        default=False,
        update=update_addon_state,
    )
    orbit_use_alt: bpy.props.BoolProperty(
        name="Alt",
        default=False,
        update=update_addon_state,
    )

    enable_sculpt_menu: bpy.props.BoolProperty(
        name="Enable Sculpt Brush Pie Menu",
        default=True,
        update=update_addon_state,
    )
    sculpt_hotkey: bpy.props.EnumProperty(
        name="Key",
        description="Key used to open the Sculpt brush pie menu",
        items=KEY_ITEMS,
        default="B",
        update=update_addon_state,
    )
    sculpt_use_shift: bpy.props.BoolProperty(
        name="Shift",
        default=False,
        update=update_addon_state,
    )
    sculpt_use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        default=False,
        update=update_addon_state,
    )
    sculpt_use_alt: bpy.props.BoolProperty(
        name="Alt",
        default=False,
        update=update_addon_state,
    )
    sculpt_popup_hotkey: bpy.props.EnumProperty(
        name="Popup Key",
        description="Key used to open Blender's default Sculpt brush popup",
        items=KEY_ITEMS,
        default="SPACE",
        update=update_addon_state,
    )
    sculpt_popup_use_shift: bpy.props.BoolProperty(
        name="Shift",
        default=False,
        update=update_addon_state,
    )
    sculpt_popup_use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        default=False,
        update=update_addon_state,
    )
    sculpt_popup_use_alt: bpy.props.BoolProperty(
        name="Alt",
        default=False,
        update=update_addon_state,
    )
    enable_quick_favorites_menu: bpy.props.BoolProperty(
        name="Enable Quick Favorites Pie Menu",
        default=True,
        update=update_addon_state,
    )
    quick_favorites_hotkey: bpy.props.EnumProperty(
        name="Key",
        description="Key used to open the Quick Favorites pie menu",
        items=KEY_ITEMS,
        default="Q",
        update=update_addon_state,
    )
    quick_favorites_use_shift: bpy.props.BoolProperty(
        name="Shift",
        default=True,
        update=update_addon_state,
    )
    quick_favorites_use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        default=False,
        update=update_addon_state,
    )
    quick_favorites_use_alt: bpy.props.BoolProperty(
        name="Alt",
        default=False,
        update=update_addon_state,
    )

    def draw(self, context):
        del context
        layout = self.layout

        orbit_box = layout.box()
        orbit_header = orbit_box.row()
        orbit_header.prop(
            self,
            "show_orbit_settings",
            text="Orbit Pie Menu",
            icon="TRIA_DOWN" if self.show_orbit_settings else "TRIA_RIGHT",
            emboss=False,
        )
        orbit_header.prop(self, "enable_orbit_menu", text="Enabled")

        if self.show_orbit_settings:
            orbit_col = orbit_box.column()
            orbit_col.enabled = self.enable_orbit_menu

            hotkey_box = orbit_col.box()
            hotkey_box.label(text="Orbit Pie Menu Hotkey")
            row = hotkey_box.row(align=True)
            row.prop(self, "orbit_use_ctrl", toggle=True)
            row.prop(self, "orbit_use_shift", toggle=True)
            row.prop(self, "orbit_use_alt", toggle=True)
            row.prop(self, "orbit_hotkey", text="")
            hotkey_box.label(
                text=f"Current shortcut: {build_shortcut_label(self.orbit_hotkey, self.orbit_use_ctrl, self.orbit_use_shift, self.orbit_use_alt)}"
            )

            info_box = orbit_col.box()
            info_box.label(text="Orbit Menu Contents")
            info_box.label(text="Turntable, Trackball, Perspective / Ortho")
            info_box.label(text="Front, Back, Left, Right")

        sculpt_box = layout.box()
        sculpt_header = sculpt_box.row()
        sculpt_header.prop(
            self,
            "show_sculpt_settings",
            text="Sculpt Brush Pie Menu",
            icon="TRIA_DOWN" if self.show_sculpt_settings else "TRIA_RIGHT",
            emboss=False,
        )
        sculpt_header.prop(self, "enable_sculpt_menu", text="Enabled")

        if self.show_sculpt_settings:
            sculpt_col = sculpt_box.column()
            sculpt_col.enabled = self.enable_sculpt_menu

            sculpt_pie_box = sculpt_col.box()
            sculpt_pie_box.label(text="Sculpt Brush Pie Hotkey")
            row = sculpt_pie_box.row(align=True)
            row.prop(self, "sculpt_use_ctrl", toggle=True)
            row.prop(self, "sculpt_use_shift", toggle=True)
            row.prop(self, "sculpt_use_alt", toggle=True)
            row.prop(self, "sculpt_hotkey", text="")
            sculpt_pie_box.label(
                text=f"Current shortcut: {build_shortcut_label(self.sculpt_hotkey, self.sculpt_use_ctrl, self.sculpt_use_shift, self.sculpt_use_alt)}"
            )

            sculpt_popup_box = sculpt_col.box()
            sculpt_popup_box.label(text="Default Sculpt Brush Popup Hotkey")
            row = sculpt_popup_box.row(align=True)
            row.prop(self, "sculpt_popup_use_ctrl", toggle=True)
            row.prop(self, "sculpt_popup_use_shift", toggle=True)
            row.prop(self, "sculpt_popup_use_alt", toggle=True)
            row.prop(self, "sculpt_popup_hotkey", text="")
            sculpt_popup_box.label(
                text=f"Current shortcut: {build_shortcut_label(self.sculpt_popup_hotkey, self.sculpt_popup_use_ctrl, self.sculpt_popup_use_shift, self.sculpt_popup_use_alt)}"
            )

            sculpt_info_box = sculpt_col.box()
            sculpt_info_box.label(text="Sculpt Menu Contents")
            sculpt_info_box.label(text="Brush, Texture, Stroke, Falloff")
            sculpt_info_box.label(text="Cursor, Symmetry")

        quick_box = layout.box()
        quick_header = quick_box.row()
        quick_header.prop(
            self,
            "show_quick_favorites_settings",
            text="Quick Favorites Pie Menu",
            icon="TRIA_DOWN" if self.show_quick_favorites_settings else "TRIA_RIGHT",
            emboss=False,
        )
        quick_header.prop(self, "enable_quick_favorites_menu", text="Enabled")

        if self.show_quick_favorites_settings:
            quick_col = quick_box.column()
            quick_col.enabled = self.enable_quick_favorites_menu

            quick_hotkey_box = quick_col.box()
            quick_hotkey_box.label(text="Quick Favorites Pie Hotkey")
            row = quick_hotkey_box.row(align=True)
            row.prop(self, "quick_favorites_use_ctrl", toggle=True)
            row.prop(self, "quick_favorites_use_shift", toggle=True)
            row.prop(self, "quick_favorites_use_alt", toggle=True)
            row.prop(self, "quick_favorites_hotkey", text="")
            quick_hotkey_box.label(
                text=f"Current shortcut: {build_shortcut_label(self.quick_favorites_hotkey, self.quick_favorites_use_ctrl, self.quick_favorites_use_shift, self.quick_favorites_use_alt)}"
            )

            quick_info_box = quick_col.box()
            quick_info_box.label(text="Quick Favorites Menu Contents")
            quick_info_box.label(text="Uses the current mode's Quick Favorites")
            quick_info_box.label(text="Standard Q stays unchanged")


CLASSES = (CostumPieMenusPreferences,)
