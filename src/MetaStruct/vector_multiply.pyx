cimport cython
import numpy as np
from cython.parallel import prange

DTYPE = np.float32

cdef float multiply(float a, float b, float c, float d, float e, float f) nogil:
    return a*b + c*d + e*f

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
def compute_3_1(float[:, :, ::1] a, float b, float[:, :, ::1] c, float d, float[:, :, ::1] e, float f):

    cdef Py_ssize_t x_max = a.shape[0]
    cdef Py_ssize_t y_max = a.shape[1]
    cdef Py_ssize_t z_max = a.shape[2]

    result = np.zeros((x_max, y_max, z_max), dtype=DTYPE)
    cdef float [:, :, ::1] result_view = result

    cdef float tmp

    cdef Py_ssize_t x, y, z

    for x in prange(x_max, nogil=True):
        for y in range(y_max):
            for z in range(z_max):
                tmp = multiply(a[x, y, z], b, c[x, y, z], d, e[x, y, z], f)
                result_view[x, y, z] = tmp

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_3_3(float[:, :, ::1] a, float[:, :, ::1] b, float[:, :, ::1] c, float[:, :, ::1] d, float[:, :, ::1] e, float[:, :, ::1] f):


    cdef Py_ssize_t x_max = a.shape[0]
    cdef Py_ssize_t y_max = a.shape[1]
    cdef Py_ssize_t z_max = a.shape[2]

    result = np.zeros((x_max, y_max, z_max), dtype=DTYPE)
    cdef float [:, :, ::1] result_view = result

    cdef float tmp

    cdef Py_ssize_t x, y, z

    for x in prange(x_max, nogil=True):
        for y in range(y_max):
            for z in range(z_max):
                tmp = multiply(a[x, y, z], b[x, y, z], c[x, y, z], d[x, y, z], e[x, y, z], f[x, y, z])
                result_view[x, y, z] = tmp

    return result
