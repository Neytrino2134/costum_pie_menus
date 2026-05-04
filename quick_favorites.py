import bpy


class WM_OT_call_quick_favorites_pie(bpy.types.Operator):
    bl_idname = "wm.costum_call_quick_favorites_pie"
    bl_label = "Quick Favorites Pie"
    bl_description = "Open Quick Favorites as a pie menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        return bpy.ops.wm.call_menu_pie("INVOKE_DEFAULT", name=WM_MT_quick_favorites_pie.bl_idname)

    def invoke(self, context, event):
        return self.execute(context)


class WM_MT_quick_favorites_pie(bpy.types.Menu):
    bl_idname = "WM_MT_costum_quick_favorites_pie"
    bl_label = "Quick Favorites Pie Menu"

    def draw(self, context):
        del context
        pie = self.layout.menu_pie()
        pie.menu_contents("SCREEN_MT_user_menu")


CLASSES = (
    WM_OT_call_quick_favorites_pie,
    WM_MT_quick_favorites_pie,
)
