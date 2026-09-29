"""Read-only Blender audit. Call audit(objects) with an explicit object scope."""
import bpy


def audit(objects):
    graph = bpy.context.evaluated_depsgraph_get()
    rows = []
    for obj in objects:
        row = {"name": obj.name, "type": obj.type, "dimensions": list(obj.dimensions)}
        if obj.type == 'MESH':
            evaluated = obj.evaluated_get(graph)
            mesh = evaluated.to_mesh()
            try:
                mesh.calc_loop_triangles()
                row.update(vertices=len(mesh.vertices), triangles=len(mesh.loop_triangles),
                           base_vertices=len(obj.data.vertices),
                           materials=len(obj.material_slots),
                           modifiers=[m.type for m in obj.modifiers])
            finally:
                evaluated.to_mesh_clear()
        rows.append(row)
    return {"blender": bpy.app.version_string, "objects": rows,
            "triangles": sum(r.get("triangles", 0) for r in rows)}
