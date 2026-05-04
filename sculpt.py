import bpy

from .constants import SCULPT_PANEL_ITEMS


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


CLASSES = (
    SCULPT_OT_call_brush_panel,
    SCULPT_MT_brush_popovers_pie,
    SCULPT_OT_call_brush_pie,
    SCULPT_OT_call_default_brush_popup,
)
