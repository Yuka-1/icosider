bl_info = {
    "name": "Icos",
    "author": "SMeShariki",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from math import sqrt

# -----------------------------------------------------------------------------
# Settings

scale = 1
subdiv = 0
name = 'Icos'

# -----------------------------------------------------------------------------
# Functions

middle_point_cache = {}


def vertex(x, y, z):
    length = sqrt(x ** 2 + y ** 2 + z ** 2)

    return [(i * scale) / length for i in (x, y, z)]


def middle_point(point_1, point_2):
    smaller_index = min(point_1, point_2)
    greater_index = max(point_1, point_2)

    key = '{0}-{1}'.format(smaller_index, greater_index)

    if key in middle_point_cache:
        return middle_point_cache[key]

    vert_1 = verts[point_1]
    vert_2 = verts[point_2]
    middle = [sum(i) / 2 for i in zip(vert_1, vert_2)]

    verts.append(vertex(*middle))

    index = len(verts) - 1
    middle_point_cache[key] = index

    return index


# -----------------------------------------------------------------------------
# Make the base icosahedron

PHI = (1 + sqrt(5)) / 2

verts = [
    vertex(-1, PHI, 0),
    vertex(1, PHI, 0),
    vertex(-1, -PHI, 0),
    vertex(1, -PHI, 0),

    vertex(0, -1, PHI),
    vertex(0, 1, PHI),
    vertex(0, -1, -PHI),
    vertex(0, 1, -PHI),

    vertex(PHI, 0, -1),
    vertex(PHI, 0, 1),
    vertex(-PHI, 0, -1),
    vertex(-PHI, 0, 1),
]

faces = [
    [0, 11, 5],
    [0, 5, 1],
    [0, 1, 7],
    [0, 7, 10],
    [0, 10, 11],

    [1, 5, 9],
    [5, 11, 4],
    [11, 10, 2],
    [10, 7, 6],
    [7, 1, 8],

    [3, 9, 4],
    [3, 4, 2],
    [3, 2, 6],
    [3, 6, 8],
    [3, 8, 9],

    [4, 9, 5],
    [2, 4, 11],
    [6, 2, 10],
    [8, 6, 7],
    [9, 8, 1],
]

# -----------------------------------------------------------------------------
# Subdivisions

for i in range(subdiv):
    faces_subdiv = []

    for tri in faces:
        v1 = middle_point(tri[0], tri[1])
        v2 = middle_point(tri[1], tri[2])
        v3 = middle_point(tri[2], tri[0])

        faces_subdiv.append([tri[0], v1, v3])
        faces_subdiv.append([tri[1], v2, v1])
        faces_subdiv.append([tri[2], v3, v2])
        faces_subdiv.append([v1, v2, v3])

    faces = faces_subdiv

# -----------------------------------------------------------------------------
# Add Object to Scene

mesh = bpy.data.meshes.new(name)
mesh.from_pydata(verts, [], faces)

obj = bpy.data.objects.new(name, mesh)
bpy.context.scene.collection.objects.link(obj)

obj = bpy.context.window.scene.objects[0]
bpy.context.view_layer.objects.active = obj

# -----------------------------------------------------------------------------
# Smoothing

for face in mesh.polygons:
    face.use_smooth = True