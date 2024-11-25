import os
import math
import bpy


P = bpy.props
T = bpy.types
U = bpy.utils
O = bpy.ops

################# Интерфейс #################
#############################################

class A3OBE_PT_AutoLOD(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Builder'
    bl_label = 'Auto LODs Generator'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        L = self.layout
        L.label(icon='FORCE_VORTEX')

    def draw(self, ctx):

        L = self.layout
        S = ctx.scene

        EPR = S.a3obe_resolution_lods
        EPG = S.a3obe_geometry_lod
        EPM = S.a3obe_memory_lod

        row = L.row(align=True)
        row.prop(EPR, 'active')

        if EPR.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPR, 'lod_prefix')

            row = box.row(align=True)
            row.prop(EPR, 'first_lod', expand=True)

            row = box.row(align=True)
            row.prop(EPR, 'preset', expand=True)

            match EPR.first_lod:
                case 'LOD0':
                    first_lod = 1
                case 'LOD1':
                    first_lod = 2

            match EPR.preset:
                case 'CUSTOM':
                    decimate_values = 'custom_decimate_values'
                case 'TRIS':
                    decimate_values = 'tris_decimate_values'
                case 'QUADS':
                    decimate_values = 'quads_decimate_values'

            for i in range(first_lod, first_lod + 4):

                row = box.row(align=True)
                row.enabled = EPR.preset == 'CUSTOM'

                row.prop(EPR, decimate_values, index=i-first_lod, text=f'LOD{i}')

            row = box.row(align=True)
            row.prop(EPR, 'autocenter_property')

            row = box.row(align=True)
            row.prop(EPR, 'lodnoshadow_property')

        row = L.row(align=True)
        row.prop(EPG, 'active')

        if EPG.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPG, 'lod_name')

            row = box.row(align=True)
            row.prop(EPG, 'convex_hull_mesh')

            row = box.row(align=True)
            row.prop(EPG, 'autocenter_property')

        row = L.row(align=True)
        row.prop(EPM, 'active')

        if EPM.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPM, 'lod_name')

            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_min_point')

            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_max_point')

            row = box.row(align=True)
            row.prop(EPM, 'create_invview_point')

            row = box.row(align=True)
            row.prop(EPM, 'autocenter_property')

        row = L.row(align=True)
        row.scale_y = 2.0
        row.operator('a3obe.generate_lods')

########## Здесь будет реализация! ##########
#############################################

################ Объявление #################
#############################################

class A3OBE_PG_ResolutionLODs(T.PropertyGroup):

    active: P.BoolProperty(
        name='Generate Resolution LODs',
        default=True)

    lod_prefix: P.StringProperty(
        name='',
        description='Resolution LOD prefix',
        default='resolution_lod_')

    first_lod: P.EnumProperty(
        description='First LOD',
        items=[
            ('LOD0', 'LOD 0', ''),
            ('LOD1', 'LOD 1', ''),
        ], default='LOD1')

    preset: P.EnumProperty(
        description='Preset',
        items=[
            ('CUSTOM', 'Custom', ''),
            ('TRIS', 'Tris', ''),
            ('QUADS', 'Quads', ''),
        ], default='QUADS')

    custom_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.75, 0.50, 0.25, 0.10))

    tris_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.80, 0.60, 0.40, 0.20))

    quads_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.50, 0.30, 0.20, 0.10))

    autocenter_property: P.BoolProperty(
        name='Disable "autocenter = 0" property',
        default=True)

    lodnoshadow_property: P.BoolProperty(
        name='Disable "lodnoshadow = 1" property',
        default=True)


class A3OBE_PG_GeometryLOD(T.PropertyGroup):

    active: P.BoolProperty(
        name = 'Generate Geometry LOD [WIP]',
        default = False)

    lod_name: P.StringProperty(
        name = '',
        description = 'Geometry LOD name',
        default = 'geometry_lod')

    convex_hull_mesh: P.BoolProperty(
        name = 'Create Convex Hull mesh',
        default = True)

    autocenter_property: P.BoolProperty(
        name = 'Disable "autocenter = 0" property',
        default = True)
    


class A3OBE_PG_MemoryLOD(T.PropertyGroup):

    active: P.BoolProperty(
        name = 'Generate Memory LOD [WIP]',
        default = False)

    lod_name: P.StringProperty(
        name = '',
        description = 'Memory LOD name',
        default = 'memory_lod')

    create_boundingbox_min_point: P.BoolProperty(
        name = 'Create BoundingBox_Min point',
        default = True)

    create_boundingbox_max_point: P.BoolProperty(
        name = 'Create BoundingBox_Max point',
        default = True)

    create_invview_point: P.BoolProperty(
        name = 'Create InvView point',
        default = True)

    autocenter_property: P.BoolProperty(
        name = 'Disable "autocenter = 0" property',
        default = True)

################ Регистрация ################
#############################################

def register():
    T.Scene.a3obe_resolution_lods = P.PointerProperty(type=A3OBE_PG_ResolutionLODs)
    T.Scene.a3obe_geometry_lod = P.PointerProperty(type=A3OBE_PG_GeometryLOD)
    T.Scene.a3obe_memory_lod = P.PointerProperty(type=A3OBE_PG_MemoryLOD)
