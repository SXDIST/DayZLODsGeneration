bl_info = {
    "name" : "DayZ LODs Generation",
    "description" : "A set of usefull extensions for Arma 3 Object Builder addon | For RKIS Lab",
    "author" : "SXDIST, Do_Nat",
    "blender" : (4, 2, 0),
    "category" : "3D View"
}

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()