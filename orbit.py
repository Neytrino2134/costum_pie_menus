import bpy

from .constants import ORBIT_ROTATE_METHODS
from .utils import get_addon_preferences


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
)
