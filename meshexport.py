import os
import time

import numpy as np

import mcubes
import logging

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.INFO)

def export(vertices, triangles, object_name="MyShape", file_name="my_shape"):
    t = time.time()
    logging.info("exporting dae...")
    # get untaken file_name
    full_path = file_name + ".dae"
    iterator = 2
    while (os.path.isfile(full_path)):
        full_path = file_name + str(iterator) + ".dae"
        iterator += 1

    mcubes.export_mesh(vertices, triangles, full_path, object_name)
    logging.info("Done in %f seconds. Result saved in '%s'" % (time.time() - t, full_path))


def export_ply(vertices, triangles, filename):
    from stl import mesh
    data = np.zeros(len(triangles), dtype=mesh.Mesh.dtype)
    for v in vertices:
        data['vectors']


def preview(vertices, triangles):
    try:
        logging.info("Plotting mesh for preview...")
        from mayavi import mlab
        mlab.triangular_mesh(
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            triangles)
        print "Done."
        mlab.show()
    except ImportError:
        logging.error("Could not import mayavi. Interactive demo not available.")
