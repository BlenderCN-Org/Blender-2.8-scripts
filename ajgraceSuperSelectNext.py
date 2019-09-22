# Provide Modo like next edge selection
# Author: Alex Grace

import bpy
import bmesh

bl_info = {
    "name": "Super Select Next",
    "author": "Alex Grace",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Mesh > Edit Mode",
    "description": "Selects along edge loop. Less prone to fail cases",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh"}


def main(context):
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)

    if len(bm.select_history) < 2:
        return

    edgeA = bm.select_history[len(bm.select_history)-2]
    edgeB = bm.select_history[len(bm.select_history)-1]

    currVert = edgeB.verts[0]
    edgeBVector = edgeB.verts[0].co-edgeB.verts[1].co

    if currVert in edgeA.verts:
        currVert = edgeB.verts[1]
        edgeBVector = -edgeBVector

    connectedEdges = currVert.link_edges
    largestDot = -1;
    bestEdge = None;

    for edge in connectedEdges:
        newVector = edge.verts[0].co-edge.verts[1].co

        if currVert == edge.verts[0]:
            newVector = -newVector

        dot = newVector.normalized().dot(edgeBVector.normalized())

        if dot > largestDot:
            bestEdge = edge;
            largestDot = dot;

    if bestEdge is not None and bestEdge.hide is False:
        bm.select_history.add(bestEdge)
        bestEdge.select = True

    bmesh.update_edit_mesh(me)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.super_select_next"
    bl_label = "Super Select Next"

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