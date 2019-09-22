# Quick Auto Smooth, similar to S Sharpen in HardOps, but looks cleaner
# Author: Alex Grace

import bpy

bl_info = {
    "name": "Set Auto Smooth",
    "author": "Alex Grace",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object Mode",
    "description": "Set Auto Smooth.",
    "warning": "",
    "wiki_url": "",
    "category": "View3D"}       

def main(context):

    if not bpy.context.object.data.use_auto_smooth:
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.object.editmode_toggle()
    bpy.context.object.data.use_auto_smooth = not bpy.context.object.data.use_auto_smooth



class AutoSmooth(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_auto_smooth"
    bl_label = "Set Auto Smooth"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AutoSmooth)


def unregister():
    bpy.utils.unregister_class(AutoSmooth)


if __name__ == "__main__":
    register()