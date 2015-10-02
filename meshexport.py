import os
import time

import numpy as np

import mcubes


def export(vertices, triangles, object_name="MyShape", file_name="my_shape"):
    t = time.time()
    print "exporting dae..."
    # get untaken file_name
    full_path = file_name + ".dae"
    iterator = 2
    while (os.path.isfile(full_path)):
        full_path = file_name + str(iterator) + ".dae"
        iterator += 1

    mcubes.export_mesh(vertices, triangles, full_path, object_name)
    print "Done. Result saved in '%s' in %f seconds." % (full_path, time.time() - t)


def export_ply(vertices, triangles, filename):
    from stl import mesh
    data = np.zeros(len(triangles), dtype=mesh.Mesh.dtype)
    for v in vertices:
        data['vectors']


def preview(vertices, triangles):
    try:
        print "Plotting mesh..."
        from mayavi import mlab
        mlab.triangular_mesh(
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            triangles)
        print "Done."
        mlab.show()
    except ImportError:
        print "Could not import mayavi. Interactive demo not available."
