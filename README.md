# Costum Pie Menus

`Costum Pie Menus` is a Blender 5.1 add-on that combines two workflow-oriented pie menus into one package:

- `Orbit Pie Menu`
- `Sculpt Brush Pie Menu`

The goal is simple: keep common viewport and sculpt actions close to the cursor and easy to trigger with custom hotkeys.

## Features

### Orbit Pie Menu

- Switch between `Turntable` and `Trackball`
- Toggle `Perspective / Orthographic`
- Jump to `Front`, `Back`, `Left`, and `Right` views
- Optional header buttons in the 3D View
- Independent enable/disable toggle
- Custom hotkey with `Ctrl`, `Shift`, and `Alt` modifiers

### Sculpt Brush Pie Menu

- Quick access to built-in sculpt popovers:
  - `Brush`
  - `Texture`
  - `Stroke`
  - `Falloff`
  - `Cursor`
  - `Symmetry`
- Separate hotkey for the custom sculpt pie menu
- Separate hotkey for Blender's default sculpt brush popup
- Independent enable/disable toggle

## Requirements

- Blender `5.1+`

## Installation

### Option 1: Install from the add-ons folder

Place the `costum_pie_menus` folder into your Blender add-ons directory:

```text
C:\Users\<YourUser>\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons
```

Then in Blender:

1. Open `Edit > Preferences > Add-ons`
2. Click `Refresh`
3. Enable `Costum Pie Menus`

### Option 2: Install from a ZIP

1. Pack the `costum_pie_menus` folder into a ZIP archive
2. In Blender open `Edit > Preferences > Add-ons`
3. Use `Install from Disk...`
4. Select the ZIP file
5. Enable `Costum Pie Menus`

## Add-on Settings

The preferences are split into clear sections:

- `Orbit Pie Menu`
- `Orbit Pie Menu Hotkey`
- `Orbit Menu Contents`
- `Sculpt Brush Pie Menu`
- `Sculpt Brush Pie Hotkey`
- `Default Sculpt Brush Popup Hotkey`
- `Sculpt Menu Contents`

Each menu can be enabled or disabled independently.

## Default Hotkeys

- `Orbit Pie Menu`: `Shift + T`
- `Sculpt Brush Pie Menu`: `B`
- `Default Sculpt Brush Popup`: `Space`

All of them can be changed in the add-on preferences.

## Notes

- If you previously used the standalone `Orbit` or `Sculpt Brush Pie` add-ons, disable them to avoid duplicate hotkeys or overlapping UI.
- The add-on name intentionally follows the current project naming: `Costum Pie Menus`.

## Repository

GitHub:

- <https://github.com/Neytrino2134/costum_pie_menus>
