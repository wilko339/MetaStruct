cimport cython
import numpy as np
from cython.parallel import prange

DTYPE = np.float32

cdef float clip(float a, float min_value, float max_value) nogil:
    return min(max(a, min_value), max_value)

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
def compute(float[:, :, ::1] array, float a, float b):

    cdef Py_ssize_t x_max = array.shape[0]
    cdef Py_ssize_t y_max = array.shape[1]
    cdef Py_ssize_t z_max = array.shape[2]

    result = np.zeros((x_max, y_max, z_max), dtype=DTYPE)
    cdef float [:, :, ::1] result_view = result

    cdef float tmp

    cdef Py_ssize_t x, y, z

    for x in prange(x_max, nogil=True):
        for y in range(y_max):
            for z in range(z_max):
                tmp = clip(array[x, y, z], a, b)
                result_view[x, y, z] = tmp

    return result
