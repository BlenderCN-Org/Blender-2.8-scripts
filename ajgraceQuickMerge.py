# Merge, but deselect all for faster merging
# Author: Alex Grace

import bpy
import bmesh

bl_info = {
	"name": "Quick Merge",
	"author": "Alex Grace",
	"version": (0, 1),
	"blender": (2, 80, 0),
	"location": "Mesh > Edit Mode",
	"description": "Merges, then deselects all for faster next merge",
	"warning": "",
	"wiki_url": "",
	"category": "Mesh"}


def main(context):

	bpy.ops.mesh.merge(type='CENTER')
	bpy.ops.mesh.select_all(action='DESELECT')

class SimpleOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "mesh.quickmerge"
	bl_label = "Quick Merge"

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