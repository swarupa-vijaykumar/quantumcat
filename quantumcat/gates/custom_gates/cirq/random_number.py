# (C) Copyright Artificial Brain 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import cirq
import numpy as np
import math


class RandomNumber(cirq.Gate):
    
    def __init__(self,lower_limit,upper_limit):
        super(RandomNumber, self).__init__()
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.bits=math.floor(math.log(self.upper_limit,2))+1

    def _num_qubits_(self):
        return self.bits

    def zero_rows(self):
        lst=[]
        lst=list(range(0,self.lower_limit))
        lst.extend(list((range(self.upper_limit+1,2**self.bits))))
        return lst
    
    def make_matrix(self,lst):
        H=[[1,1],
          [1,-1]]
        H2=H
        for i in range(self.bits-1):
            H2=np.kron(H2,H)
        for i in lst:
            H2[i]=np.zeros(1)
        return H2

    def gs(self,x):
        Q, R = np.linalg.qr(x)
        return Q

    def _unitary_(self, dtype=None):
        lst=zero_rows(self)
        matrix=make_matrix(self,lst)
        return gs(matrix)

    def _circuit_diagram_info_(self, args):
        return ["Random number matrix"]*self.bits