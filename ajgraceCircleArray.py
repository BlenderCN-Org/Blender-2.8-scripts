# Generate circular array using a helper empty
# Author: Alex Grace

import bpy
from bpy.props import IntProperty, FloatProperty
from math import pi

bl_info = {
    "name": "Circular Array",
    "author": "Alex Grace",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object Mode",
    "description": "Creates a circular array centered around the pivot.",
    "warning": "",
    "wiki_url": "",
    "category": "View3D"}


class CircularArray(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.circle_array"
    bl_label = "Circular Array"

    first_mouse_x = IntProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            numCopies = max(1,abs(int(delta/10)))
            self.arrayModifier.count = numCopies
            self.emptyOb.rotation_euler = (0,0,360 / numCopies * pi / 180)

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.currOb = bpy.context.view_layer.objects.active # Unsure about this, may need to be string
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.empty_add(type='PLAIN_AXES')
            self.emptyOb = bpy.context.view_layer.objects.active 
            bpy.context.view_layer.objects.active = self.currOb
            self.emptyOb.location = self.currOb.location
            bpy.ops.object.modifier_add(type='ARRAY')
            self.arrayModifier = self.currOb.modifiers[-1]
            self.arrayModifier.use_object_offset = True
            self.arrayModifier.use_relative_offset = False
            self.arrayModifier.offset_object = self.emptyOb
 
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(CircularArray)


def unregister():
    bpy.utils.unregister_class(CircularArray7)


if __name__ == "__main__":
    register()