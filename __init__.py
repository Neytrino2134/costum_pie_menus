bl_info = {
    "name": "Costum Pie Menus",
    "author": "OpenAI Codex",
    "version": (1, 0, 0),
    "blender": (5, 1, 0),
    "location": "3D View",
    "category": "3D View",
    "description": "Combined Orbit and Sculpt pie menus with configurable hotkeys",
}

from .addon import register, unregister
