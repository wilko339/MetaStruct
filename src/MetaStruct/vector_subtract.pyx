cimport cython
import numpy as np
from cython.parallel import prange

DTYPE = np.float32

cdef float subtract(float a, float b) nogil:
    return a-b

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
def compute_3_1(float[:, :, :] a, float b):

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
                tmp = subtract(a[x, y, z], b)
                result_view[x, y, z] = tmp

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_3_3(float[:, :, :] a, float[:, :, :] b):


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
                tmp = subtract(a[x, y, z], b[x, y, z])
                result_view[x, y, z] = tmp

    return result
