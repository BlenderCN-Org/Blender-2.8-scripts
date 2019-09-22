# Convert selection to edges, or to edge loops if already in edge mode
# Used to save a key for hotkey availability
# Author: Alex Grace

import bpy
import bmesh

bl_info = {
    "name": "Convert To Edges Or Loops",
    "author": "Alex Grace",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh > Edit Mode",
    "description": "Convert selection to edges, or select edge loops if already in edge mode",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}


def main(context):
    if bpy.context.scene.tool_settings.mesh_select_mode[1] == False:
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
    else:
        bpy.ops.mesh.loop_multi_select(ring=False)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.to_edges_or_loops"
    bl_label = "Convert to Edges or Loops"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()