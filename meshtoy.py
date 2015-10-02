import time
import math
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


FREQUENCY = 0.3
AMPLITUDE = 10.0


# Create the volume
def f(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 + AMPLITUDE * \
                                      pnoise3(x * FREQUENCY, y * FREQUENCY, z * FREQUENCY, octaves=2)


def main():
    logging.info("Example 2: Isosurface in Python function...")
    logging.info("(this might take a while...)")
    samples = 100
    bounds = math.sqrt(samples) + 1.0
    t = time.time()
    # Extract the 16-isosurface
    vertices, triangles = mcubes.marching_cubes_func(
        (-bounds, -bounds, -bounds),
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
    t = time.time()
    # from stl import mesh
    diameter = 10
    radius = diameter / 2
    half = radius / 2

    X, Y, Z = np.mgrid[:diameter, :diameter, :diameter]
    print "X"
    print X
    print "Y"
    print Y
    print "Z"
    print Z
    # u = (X-50)**2 + (Y-50)**2 + (Z-50)**2 - 25**2 + pnoise3(X,Y,Z,octaves=3)*3
    u = (X - radius) ** 2 + (Y - radius) ** 2 + (Z - radius) ** 2 - half ** 2  # + pnoise3(X,Y,Z,octaves=3)*3
    print "u"
    print u
    # Extract the 0-isosurface
    vertices, triangles = mcubes.marching_cubes(u, 0)
    print "mesh completed in %f seconds" % (time.time() - t)

    # meshexport.export(vertices, triangles)
    # meshexport.preview(triangles, vertices)


if __name__ == "__main__":
    main()
