import time

import numpy as np
import mcubes
from noise import pnoise3

import meshexport


def LineSegmentFactory((x1, y1, z1), (x2, y2, z2), radius=1):
    a = np.array([x1, y1, z1])
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    #TODO
    return lambda x, y, z: x


# Create the volume
def f(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 + pnoise3(x, y, z, octaves=2)


def main():
    print "Example 2: Isosurface in Python function..."
    print "(this might take a while...)"

    t = time.time()
    # Extract the 16-isosurface
    vertices, triangles = mcubes.marching_cubes_func(
        (-10, -10, -10), (10, 10, 10),  # Bounds
        100, 100, 100,                  # Number of samples in each dimension
        f,                              # Implicit function
        16)                             # Isosurface value
    print "mesh completed in %f seconds" % (time.time() - t)

    meshexport.export(vertices, triangles)
    meshexport.preview(triangles, vertices)

def main2():
    t = time.time()
    #from stl import mesh
    X, Y, Z = np.mgrid[:5, :5, :5]
    print X
    print Y
    print Z
    u = (X-50)**2 + (Y-50)**2 + (Z-50)**2 - 25**2 #+ pnoise3(X,Y,Z,octaves=3)*3
    print u

    # Extract the 0-isosurface
    vertices, triangles = mcubes.marching_cubes(u, 0)
    print "mesh completed in %f seconds" % (time.time() - t)

    meshexport.export(vertices, triangles)
    meshexport.preview(triangles, vertices)


if __name__ == "__main__":
    main2()