from braket.circuits import circuit,Circuit
import numpy


@circuit.subroutine(register=True)
def Unitary(matrix,bits, dtype=None):
    return numpy.array(matrix, dtype=dtype)
