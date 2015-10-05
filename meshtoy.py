import time
import logging

import numpy as np
import mcubes
from noise import pnoise3

import meshexport



# FORMAT = '%(levelname)s - %(threadName)s: %(message)s'
FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)


def LineSegmentFactory((x1, y1, z1), (x2, y2, z2), radius=1):
    a = np.array([x1, y1, z1])
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    # TODO
    return lambda x, y, z: x


FREQUENCY = 1.0
AMPLITUDE = 100.0


# Create the volume
def f(x, y, z):
    return x ** 2 + y ** 2 + z ** 2  # + AMPLITUDE * \
    #  pnoise3(x * FREQUENCY, y * FREQUENCY, z * FREQUENCY, octaves=2)


def main():
    logging.info("Example 2: Isosurface in Python function...")
    logging.info("(this might take a while...)")
    samples = 200
    bounds = 8
    t = time.time()
    # Extract the 16-isosurface
    vertices, triangles = mcubes.marching_cubes_func(
        (-0, -0, -0),
        (bounds, bounds, bounds),
        samples, samples, samples,
        f,  # Implicit function
        16)  # Isosurface value
    logging.info("mesh completed in %f seconds" % (time.time() - t))

    logging.debug("vertices: {} length: {}".format(type(vertices), len(vertices)))
    logging.debug(vertices)
    logging.debug("triangles: {} length: {}".format(type(triangles), len(triangles)))
    logging.debug(triangles)

    meshexport.export(vertices, triangles)
    # meshexport.preview(triangles, vertices)


def main2():
    logging.info("(this might take a while...)")
    samples = 50
    t = time.time()
    # from stl import mesh
    diameter = 10
    radius = diameter / 2
    half = radius / 2

    # X, Y, Z = np.mgrid[:diameter, :diameter, :diameter]
    # print "X"
    # print X
    # print "Y"
    # print Y
    # print "Z"
    # print Z
    # u = (X-50)**2 + (Y-50)**2 + (Z-50)**2 - 25**2 + pnoise3(X,Y,Z,octaves=3)*3
    # u = (X-radius)**2 + (Y-radius)**2 + (Z-radius)**2 - half**2 #+ pnoise3(X,Y,Z,octaves=3)*3
    # u = [[[(X)**2 + (Y)**2 + (Z)**2 - 25**2 + pnoise3(X,Y,Z,octaves=3)*3 for X in range(-100,100)] for Y in range(-100,100)] for Z in range(-100,100)]
    u = np.ndarray((200, 200, 200))
    for X in range(-100, 100):
        for Y in range(-100, 100):
            for Z in range(-100, 100):
                # print v
                u[X + 100, Y + 100, Z + 100] = ((X) ** 2 + (Y) ** 2 + (Z) ** 2) + pnoise3(X * 0.05, Y * 0.05, Z * 0.05,
                                                                                          octaves=3) * 30
    # print u
    # Extract the 0-isosurface

    logging.debug("u")
    logging.debug(u)
    vertices, triangles = mcubes.marching_cubes(u, 60)
    logging.info("mesh completed in %f seconds" % (time.time() - t))

    meshexport.export(vertices, triangles)
    # meshexport.preview(triangles, vertices)


def main3():
    logging.info("(this might take a while...)")
    t = time.time()
    # from stl import mesh
    samples = 50
    radius = samples / 2.0
    half = radius / 2.0

    array = np.ndarray((samples, samples, samples))
    for x in range(samples):
        for y in range(samples):
            for z in range(samples):
                noise = AMPLITUDE * pnoise3(x * FREQUENCY, y * FREQUENCY, z * FREQUENCY, octaves=2)
                array[x, y, z] = x ** 2 + y ** 2 + z ** 2 - half ** 2 + noise

    logging.debug("array")
    logging.debug(array)
    # Extract the 0-isosurface
    vertices, triangles = mcubes.marching_cubes(array, 0)
    logging.info("mesh completed in %f seconds" % (time.time() - t))

    meshexport.export(vertices, triangles)
    # meshexport.preview(triangles, vertices)


def octant_array(samples, isosurface, x_offset, y_offset, z_offset):
    """

    :param samples: the number of samples per dimension per octant,
     the full model would have samples**3 * 8 samples
    :param isosurface:
    :param x_offset: controls which octant
    :param y_offset:
    :param z_offset:
    :return: a numpy.ndarray
    """
    array = np.ndarray((samples, samples, samples))
    isosurface **= 2
    for x in range(samples):
        for y in range(samples):
            for z in range(samples):
                x2, y2, z2 = x + x_offset, y + y_offset, z + z_offset
                noise = AMPLITUDE * pnoise3(x2 * FREQUENCY, y2 * FREQUENCY, z2 * FREQUENCY, octaves=2)
                array[x, y, z] = x2 ** 2 + y2 ** 2 + z2 ** 2 - isosurface + noise
    return array

def octant(samples, isosurface, x_offset, y_offset, z_offset):
    array = octant_array(samples, isosurface, x_offset, y_offset, z_offset)
    logging.debug("array")
    logging.debug(array)
    # Extract the 0-isosurface
    return mcubes.marching_cubes(array, 0)


def main4():
    logging.info("(this might take a while...)")
    t = time.time()
    # from stl import mesh
    samples = 150
    diameter = samples
    radius = diameter / 2.0
    half = radius / 2.0

    vertices, triangles = None, None
    offset = -1.0 * radius

    args = [(0, 0, 0), (0, 0, offset), (0, offset, 0), (0, offset, offset),
            (offset, 0, 0), (offset, 0, offset), (offset, offset, 0), (offset, offset, offset)]
    for tuple in args:
        octant_verts, octant_tris = octant(samples, half, *tuple)
        # meshexport.export(octant_verts, octant_tris)
        vertices = octant_verts if vertices is None else np.concatenate([vertices, octant_verts])
        triangles = octant_tris if triangles is None else np.concatenate([triangles, octant_tris])

    logging.info("mesh completed in %f seconds" % (time.time() - t))

    meshexport.export(octant_verts, octant_tris, "combined", "combined")
    # meshexport.preview(triangles, vertices)


def octant_wrapper(args):
    return octant(*args)


def main5():
    logging.info("(this might take a while...)")
    from multiprocessing import Pool
    t = time.time()

    samples = 150
    diameter = samples
    radius = diameter / 2.0
    half = radius / 2.0

    vertices, triangles = None, None
    offset = -1.0 * radius
    args = [(samples, half, x * offset, y * offset, z * offset)
            for x in range(2)
            for y in range(2)
            for z in range(2)]
    pool = Pool(processes=4)
    output = pool.map(octant_wrapper, args)
    for octant_verts, octant_tris in output:
        # meshexport.export(octant_verts, octant_tris)
        vertices = octant_verts if vertices is None else np.concatenate([vertices, octant_verts])
        triangles = octant_tris if triangles is None else np.concatenate([triangles, octant_tris])

    logging.info("mesh completed in %f seconds" % (time.time() - t))

    meshexport.export(octant_verts, octant_tris, "combined", "combined")
    # meshexport.preview(triangles, vertices)


if __name__ == "__main__":
    main5()
