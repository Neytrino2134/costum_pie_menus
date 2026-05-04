bl_info = {
    "name": "Costum Pie Menus",
    "author": "OpenAI Codex",
    "version": (1, 0, 0),
    "blender": (5, 1, 0),
    "location": "3D View",
    "category": "3D View",
    "description": "Combined Orbit and Sculpt pie menus with configurable hotkeys",
}

import bpy


ADDON_ID = __name__

ORBIT_ROTATE_METHODS = {
    "TURNTABLE": {
        "label": "Turntable",
        "description": "Set orbit navigation mode to Turntable",
    },
    "TRACKBALL": {
        "label": "Trackball",
        "description": "Set orbit navigation mode to Trackball",
    },
}

SCULPT_PANEL_ITEMS = (
    ("VIEW3D_PT_tools_brush_settings_advanced", "Brush"),
    ("VIEW3D_PT_tools_brush_texture", "Texture"),
    ("VIEW3D_PT_tools_brush_stroke", "Stroke"),
    ("VIEW3D_PT_tools_brush_falloff", "Falloff"),
    ("VIEW3D_PT_tools_brush_display", "Cursor"),
    ("VIEW3D_PT_sculpt_symmetry_for_topbar", "Symmetry"),
)

KEY_ITEMS = [
    ("A", "A", ""),
    ("B", "B", ""),
    ("C", "C", ""),
    ("D", "D", ""),
    ("E", "E", ""),
    ("F", "F", ""),
    ("G", "G", ""),
    ("H", "H", ""),
    ("I", "I", ""),
    ("J", "J", ""),
    ("K", "K", ""),
    ("L", "L", ""),
    ("M", "M", ""),
    ("N", "N", ""),
    ("O", "O", ""),
    ("P", "P", ""),
    ("Q", "Q", ""),
    ("R", "R", ""),
    ("S", "S", ""),
    ("T", "T", ""),
    ("U", "U", ""),
    ("V", "V", ""),
    ("W", "W", ""),
    ("X", "X", ""),
    ("Y", "Y", ""),
    ("Z", "Z", ""),
    ("SPACE", "Space", ""),
    ("ZERO", "0", ""),
    ("ONE", "1", ""),
    ("TWO", "2", ""),
    ("THREE", "3", ""),
    ("FOUR", "4", ""),
    ("FIVE", "5", ""),
    ("SIX", "6", ""),
    ("SEVEN", "7", ""),
    ("EIGHT", "8", ""),
    ("NINE", "9", ""),
]

addon_keymaps = []
header_registered = False


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


def clear_keymaps():
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        addon_keymaps.clear()
        return

    keyconfig = wm.keyconfigs.addon
    if keyconfig is None:
        addon_keymaps.clear()
        return

    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (ReferenceError, RuntimeError, ValueError):
            pass
    addon_keymaps.clear()


def ensure_header_state():
    global header_registered

    prefs = get_addon_preferences()
    should_register = bool(prefs and prefs.enable_orbit_menu)

    if should_register and not header_registered:
        bpy.types.VIEW3D_HT_header.append(draw_orbit_header_buttons)
        header_registered = True
    elif not should_register and header_registered:
        try:
            bpy.types.VIEW3D_HT_header.remove(draw_orbit_header_buttons)
        except ValueError:
            pass
        header_registered = False


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
        addon_keymaps.append((km, kmi))

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
        addon_keymaps.append((km, kmi))

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
        addon_keymaps.append((km, kmi))


def refresh_ui_and_keymaps():
    ensure_header_state()
    if not bpy.app.background:
        register_keymaps()


def update_addon_state(self, context):
    refresh_ui_and_keymaps()


class VIEW3D_OT_set_rotate_method(bpy.types.Operator):
    bl_idname = "view3d.costum_set_rotate_method"
    bl_label = "Set Orbit Navigation"
    bl_description = "Change the viewport orbit navigation mode"
    bl_options = {"REGISTER", "INTERNAL"}

    method: bpy.props.EnumProperty(
        name="Rotate Method",
        description="Viewport orbit navigation mode",
        items=[
            ("TURNTABLE", "Turntable", "Use turntable orbit navigation"),
            ("TRACKBALL", "Trackball", "Use trackball orbit navigation"),
        ],
        default="TURNTABLE",
    )

    def execute(self, context):
        context.preferences.inputs.view_rotate_method = self.method
        self.report({"INFO"}, f"Orbit mode: {ORBIT_ROTATE_METHODS[self.method]['label']}")
        return {"FINISHED"}


class VIEW3D_OT_toggle_perspective(bpy.types.Operator):
    bl_idname = "view3d.costum_toggle_perspective"
    bl_label = "Toggle Perspective"
    bl_description = "Toggle between perspective and orthographic view"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        bpy.ops.view3d.view_persportho()
        return {"FINISHED"}


class VIEW3D_OT_view_axis(bpy.types.Operator):
    bl_idname = "view3d.costum_view_axis"
    bl_label = "Set View Axis"
    bl_description = "Switch the viewport to a specific axis view"
    bl_options = {"REGISTER", "INTERNAL"}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ("LEFT", "Left", "View from the left"),
            ("RIGHT", "Right", "View from the right"),
            ("FRONT", "Front", "View from the front"),
            ("BACK", "Back", "View from the back"),
        ],
        default="FRONT",
    )

    def execute(self, context):
        bpy.ops.view3d.view_axis(type=self.axis)
        return {"FINISHED"}


class VIEW3D_OT_call_orbit_pie(bpy.types.Operator):
    bl_idname = "view3d.costum_call_orbit_pie"
    bl_label = "Orbit Navigation Pie"
    bl_description = "Open the orbit navigation pie menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        return bpy.ops.wm.call_menu_pie("INVOKE_DEFAULT", name=VIEW3D_MT_orbit_pie.bl_idname)

    def invoke(self, context, event):
        return self.execute(context)


class VIEW3D_MT_orbit_pie(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_costum_orbit_pie"
    bl_label = "Orbit Pie Menu"

    def draw(self, context):
        pie = self.layout.menu_pie()

        op = pie.operator(VIEW3D_OT_set_rotate_method.bl_idname, text="Turntable")
        op.method = "TURNTABLE"

        op = pie.operator(VIEW3D_OT_set_rotate_method.bl_idname, text="Trackball")
        op.method = "TRACKBALL"

        pie.operator(VIEW3D_OT_toggle_perspective.bl_idname, text="Perspective / Ortho")

        op = pie.operator(VIEW3D_OT_view_axis.bl_idname, text="Front")
        op.axis = "FRONT"

        op = pie.operator(VIEW3D_OT_view_axis.bl_idname, text="Left")
        op.axis = "LEFT"

        op = pie.operator(VIEW3D_OT_view_axis.bl_idname, text="Right")
        op.axis = "RIGHT"

        op = pie.operator(VIEW3D_OT_view_axis.bl_idname, text="Back")
        op.axis = "BACK"


class SCULPT_OT_call_brush_panel(bpy.types.Operator):
    bl_idname = "sculpt.costum_call_brush_panel"
    bl_label = "Open Sculpt Brush Panel"
    bl_description = "Open a Sculpt brush settings popover"
    bl_options = {"INTERNAL"}

    panel_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            bpy.ops.wm.call_panel(name=self.panel_name, keep_open=True)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class SCULPT_MT_brush_popovers_pie(bpy.types.Menu):
    bl_idname = "SCULPT_MT_costum_brush_popovers_pie"
    bl_label = "Sculpt Brush Pie Menu"

    def draw(self, context):
        pie = self.layout.menu_pie()

        for panel_name, label in SCULPT_PANEL_ITEMS:
            op = pie.operator(SCULPT_OT_call_brush_panel.bl_idname, text=label)
            op.panel_name = panel_name


class SCULPT_OT_call_brush_pie(bpy.types.Operator):
    bl_idname = "sculpt.costum_call_brush_pie"
    bl_label = "Sculpt Brush Pie"
    bl_description = "Open the Sculpt brush popover pie menu"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None and
            context.area.type == "VIEW_3D" and
            context.mode == "SCULPT"
        )

    def execute(self, context):
        return bpy.ops.wm.call_menu_pie("INVOKE_DEFAULT", name=SCULPT_MT_brush_popovers_pie.bl_idname)

    def invoke(self, context, event):
        return self.execute(context)


class SCULPT_OT_call_default_brush_popup(bpy.types.Operator):
    bl_idname = "sculpt.costum_call_default_brush_popup"
    bl_label = "Sculpt Default Brush Popup"
    bl_description = "Open Blender's default Sculpt brush popup"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None and
            context.area.type == "VIEW_3D" and
            context.mode == "SCULPT"
        )

    def execute(self, context):
        try:
            return bpy.ops.wm.call_asset_shelf_popover(
                "INVOKE_DEFAULT",
                name="VIEW3D_AST_brush_sculpt",
            )
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

    def invoke(self, context, event):
        return self.execute(context)


class CostumPieMenusPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

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

    def draw(self, context):
        layout = self.layout

        orbit_box = layout.box()
        orbit_box.prop(self, "enable_orbit_menu", text="Orbit Pie Menu")
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
        sculpt_box.prop(self, "enable_sculpt_menu", text="Sculpt Brush Pie Menu")
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


def draw_orbit_header_buttons(self, context):
    prefs = get_addon_preferences(context)
    if not prefs or not prefs.enable_orbit_menu:
        return

    inputs = context.preferences.inputs
    current_method = inputs.view_rotate_method

    layout = self.layout
    row = layout.row(align=True)

    for method, data in ORBIT_ROTATE_METHODS.items():
        icon = "RADIOBUT_ON" if current_method == method else "RADIOBUT_OFF"
        op = row.operator(
            VIEW3D_OT_set_rotate_method.bl_idname,
            text=data["label"],
            icon=icon,
        )
        op.method = method


CLASSES = (
    VIEW3D_OT_set_rotate_method,
    VIEW3D_OT_toggle_perspective,
    VIEW3D_OT_view_axis,
    VIEW3D_OT_call_orbit_pie,
    VIEW3D_MT_orbit_pie,
    SCULPT_OT_call_brush_panel,
    SCULPT_MT_brush_popovers_pie,
    SCULPT_OT_call_brush_pie,
    SCULPT_OT_call_default_brush_popup,
    CostumPieMenusPreferences,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    refresh_ui_and_keymaps()


def unregister():
    global header_registered

    clear_keymaps()

    if header_registered:
        try:
            bpy.types.VIEW3D_HT_header.remove(draw_orbit_header_buttons)
        except ValueError:
            pass
        header_registered = False

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
