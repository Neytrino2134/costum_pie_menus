import bpy

from .keymaps import clear_keymaps, disable_header, refresh_ui_and_keymaps
from .orbit import CLASSES as ORBIT_CLASSES
from .preferences import CLASSES as PREFERENCE_CLASSES
from .quick_favorites import CLASSES as QUICK_FAVORITES_CLASSES
from .sculpt import CLASSES as SCULPT_CLASSES


CLASSES = ORBIT_CLASSES + SCULPT_CLASSES + QUICK_FAVORITES_CLASSES + PREFERENCE_CLASSES


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    refresh_ui_and_keymaps()


def unregister():
    clear_keymaps()
    disable_header()

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
