# Fast modal tool for remesh, mimicking dynamesh functionality in Zbrush
# Author: Alex Grace

import bpy
import bmesh

bl_info = {
    "name": "Quick Remesh",
    "author": "Alex Grace",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Object / Sculpt Mode",
    "description": "Applies a Remesh Modifier",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}


class QuickRemesh(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.quick_remesh"
    bl_label = "Quick Remesh"
    remeshLevel = 5;

    def modal(self, context, event):
        if event.type == 'WHEELUPMOUSE':
            QuickRemesh.remeshLevel = QuickRemesh.remeshLevel + 1
            self.report({'INFO'}, "Current remesh level (adjust with scroll wheel) %d" % (QuickRemesh.remeshLevel))

        if event.type == 'WHEELDOWNMOUSE':
            QuickRemesh.remeshLevel = QuickRemesh.remeshLevel - 1
            self.report({'INFO'}, "Current remesh level (adjust with scroll wheel) %d" % (QuickRemesh.remeshLevel))

        elif event.type in {'LEFTMOUSE', 'MIDDLEMOUSE'}:
            bpy.ops.object.convert(target='MESH')
            mod = context.object.modifiers.new("QuickRemesh",'REMESH')
            mod.mode = 'SMOOTH'
            mod.octree_depth = QuickRemesh.remeshLevel
            mod.use_smooth_shade = True
            bpy.ops.object.convert(target='MESH')
            self.report({'INFO'}, "Finshed Remeshing at level %d" % (QuickRemesh.remeshLevel))

            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            mod = context.object.modifiers["QuickRemesh"]
            mod = context.object.modifiers.remove(mod)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:            
            context.window_manager.modal_handler_add(self)
            self.report({'INFO'}, "Current remesh level (adjust with scroll wheel) %d" % (QuickRemesh.remeshLevel))

            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(QuickRemesh)


def unregister():
    bpy.utils.unregister_class(QuickRemesh)


if __name__ == "__main__":
    register()
