#(C) Copyright Artificial Brain 2021.
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


from quantumcat.circuit import QCircuit
from quantumcat.utils import providers, constants, helper
import math
import numpy as np

class RandInt:

    def __init__(self, output_type=constants.DECIMAL,provider=providers.DEFAULT_PROVIDER,
                simulator_name=constants.DEFAULT_SIMULATOR, api=None, device=None):
        super(RandInt, self).__init__()
        self.output_type = output_type
        self.provider = providers.DEFAULT_PROVIDER
        self.simulator=simulator_name
        self.api=api
        self.device = device
        self.qc = None

    def get_num_bits(self, upper_limit):
        return math.floor(math.log(upper_limit,2))+1

    def nth_bit(self,num, n):
        return num&(1<<n) != 0

    def make_output(self,a,b,bits):
        num_vals=b-a+1
        output=[]
        rep=(2**bits)//num_vals
        for i in range(a,b+1):
            output+=([i]*rep)
        if((2**bits)%num_vals!=0):
            for i in range (0,(2**bits)%num_vals):
                output+=[a]
                a+=1
        return output

    def get_binary_output(self, num_bits,decimal_output):
        outputs_binary = []
        output=np.array(decimal_output)
        for n in range(num_bits-1, -1, -1):
            func = lambda x: self.nth_bit(x, n)
            outputs_binary.append(func(output))
        outputs_binary = np.asarray(outputs_binary, dtype='int8')
        return outputs_binary

    def get_sop(self, binary_output, num_bits):
        inp = np.arange(1, 2**num_bits+1, 1, dtype='int32')
        SOP = []
        for i in range(num_bits):
            SOP.append(inp * binary_output[i])
        return SOP

    def make_circuit(self, num_qubits, sop):
        qc = QCircuit(num_qubits*3)
        #self.qc = qc
        for i in range(num_qubits):
            qc.h_gate(i)
            
        #qc.barrier()
        
        for i in range(num_qubits):
            qc.cx_gate(i, i+(num_qubits*2))
            qc.x_gate(i+(num_qubits*2))
        cnt=0 
        #qc.barrier()
        for o in sop:
            for i in range(len(o)):
                lst=[]
                if(o[i]!=0):
                    for j in range(num_qubits):
                        if(self.nth_bit(o[i]-1,j)==1):
                            lst.append(j)
                        else:
                            lst.append(j+(num_qubits*2))
                    qc.mct_gate(lst,cnt+num_qubits)
            cnt+=1
            #qc.barrier()
            
        for i in range(num_qubits):
            qc.measure(num_qubits+i)
        self.qc=qc   
        return qc

    def run_circuit(self):
        counts = self.qc.execute(provider=self.provider, repetitions=1,
                                 simulator_name=self.simulator, api=self.api, device=self.device)
        return counts

    def rand_range(self, lower_limit,upper_limit):
        bits=self.get_num_bits(upper_limit)
        output=self.make_output(lower_limit,upper_limit,bits)
        final_op=self.get_binary_output(bits,output)
        sop=self.get_sop(final_op,bits)
        self.qc=self.make_circuit(bits,sop)
        cnts=self.run_circuit()
        res=list(cnts.keys())[0][::-1]
        res = res[:-bits]
        return int(res,2)