# Select linked faces by auto smooth angle
# Author: Alex Grace

import bpy
import bmesh

bl_info = {
	"name": "Select Linked Smooth",
	"author": "Alex Grace",
	"version": (0, 1),
	"blender": (2, 80, 0),
	"location": "Mesh",
	"description": "Select Linked flat faces by auto smooth angle",
	"warning": "",
	"wiki_url": "",
	"category": "Mesh"}


def main(context):
	sharpAngle = bpy.context.object.data.auto_smooth_angle
	bpy.ops.mesh.faces_select_linked_flat(sharpness=sharpAngle)


class SimpleOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "mesh.selectlinkedsmooth"
	bl_label = "Select Linked Smooth"

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