import os
from SCons.Script import *

# NVDA Add-on Build Script

addon_name = "nvoice"
addon_version = "1.0.0"

# Build the add-on
env = Environment()

# Create .nvda-addon file
addon_target = f"{addon_name}-{addon_version}.nvda-addon"

# Copy addon folder to build directory
env.Command(
    addon_target,
    Glob("addon/**/*"),
    [
        "mkdir -p build/addon",
        "cp -r addon/* build/addon/",
        f"cd build && zip -r ../{addon_target} addon",
    ]
)

Default(addon_target)
