# Copy transform orientations from one object to another
# Author: Alex Grace
import bpy

bl_info = {
    "name": "Copy Transform Orientations",
    "author": "Alex Grace",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object Mode",
    "description": "Copies a transform orientation from one to another.",
    "warning": "",
    "wiki_url": "",
    "category": "View3D"}

def main(context):
    selObjs = bpy.context.selected_objects
    copyfromOb = bpy.context.active_object
    copytoOb = None

    for selOb in selObjs:
        if selOb != copytoOb:
            copytoOb = selOb

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = copyfromOb
    copyfromOb.select_set(True)
    bpy.ops.object.duplicate();
    bpy.context.active_object.location = copytoOb.location
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.convert(target='MESH')
    copytoOb.select_set(True)
    bpy.ops.object.join()


class CopyOrientation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.copy_transform_orientation"
    bl_label = "Copy Transform Orientation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CopyOrientation)


def unregister():
    bpy.utils.unregister_class(CopyOrientation)


if __name__ == "__main__":
    register()