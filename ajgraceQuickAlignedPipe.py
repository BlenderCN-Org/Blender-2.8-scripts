# Generate quick pipe aligned to a selected face
# Author: Alex Grace

import bpy, bmesh, mathutils
from bpy.props import IntProperty, FloatProperty
from math import pi

bl_info = {
    "name": "Quick Aligned Pipe",
    "author": "Alex Grace, based upon quickpipe by Jeremy Mitchell",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode",
    "description": "Quickly aligns an extruded curve to a face.",
    "warning": "",
    "wiki_url": "",
    "category": "View3D"}


class quickAlignedPipe(bpy.types.Operator):
    """Create an extruded curve from a selection of edges"""
    bl_idname = "object.quickalignedpipe"
    bl_label = "Quick Aligned Pipe"

    first_mouse_x = IntProperty()
    first_value = FloatProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.data.bevel_depth = abs(self.first_value + delta * 0.01)
        elif event.type == 'WHEELUPMOUSE':
            bpy.context.object.data.bevel_resolution += 1
        elif event.type == 'WHEELDOWNMOUSE':
            if bpy.context.object.data.bevel_resolution > 0:
                bpy.context.object.data.bevel_resolution -= 1

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            if( context.object.type == 'MESH' ):         
                obj = bpy.context.object
                bm = bmesh.from_edit_mesh(obj.data)

                pos = bm.faces.active.calc_center_median() # or calc_center_bounds?
                normal = bm.faces.active.normal

                mat = obj.matrix_world

                matInv = mat.inverted()
                matInvTranspose = matInv.transposed().to_3x3()

                worldNormal = matInvTranspose * normal
                worldPos = mat * pos

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.curve.primitive_nurbs_path_add()
                bpy.context.object.data.fill_mode = 'FULL'
                bpy.context.object.data.bevel_resolution = 1
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.transform.rotate(value = (pi / 2), axis = (0,1,0))
                bpy.ops.transform.translate(value = (0,0,2))
                bpy.ops.object.mode_set(mode='OBJECT')

                DirectionVector = mathutils.Vector(worldNormal)
                bpy.context.object.location = worldPos
                bpy.context.object.rotation_euler = DirectionVector.to_track_quat('Z','Y').to_euler()

                self.pipe = bpy.context.scene.objects[0]
                self.pipe.select = True
                bpy.context.scene.objects.active = self.pipe                
                self.pipe.data.fill_mode = 'FULL'
                self.pipe.data.splines[0].use_smooth = True
                self.pipe.data.bevel_resolution = 2
                self.pipe.data.bevel_depth = 0.1

            elif( context.object.type == 'CURVE' ):
                self.pipe = context.object
                        
            self.first_value = self.pipe.data.bevel_depth

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(quickAlignedPipe)


def unregister():
    bpy.utils.unregister_class(quickAlignedPipe)


if __name__ == "__main__":
    register()
