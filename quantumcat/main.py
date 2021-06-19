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

from quantumcat.circuit import QCircuit
from quantumcat.utils import providers, constants
from quantumcat.algorithms import GroversAlgorithm
from quantumcat.applications.generator import RandomNumber
from qiskit import IBMQ

circuit = QCircuit(2)
circuit.u3_gate(45, 45, 45, 0)
circuit.cx_gate(0, 1)
# circuit.x_gate(0)

# circuit.z_gate(0)
# circuit.ccx_gate(0, 1, 2)
# circuit.s_gate(0)
# circuit.sdg_gate(1)
# circuit.swap_gate(0, 2)
# circuit.iswap_gate(1, 2)
# circuit.sx_gate(0)
# circuit.sxd_gate(1)
# circuit.t_gate(0)
# circuit.td_gate(1)
# circuit.i_gate(1)
# circuit.cy_gate(0, 1)
# circuit.cz_gate(0, 1)
# circuit.cswap_gate(0, 1, 2)
# circuit.rx_gate(30, 0)
# circuit.ry_gate(30, 0)
# circuit.cphase_gate(30, 0, 1)
# circuit.ryy_gate(30, 0, 1)
# circuit.rz_gate(30, 0)
# circuit.rxx_gate(30, 0, 1)
# circuit.p_gate(30, 0)
# circuit.rzz_gate(30, 0, 1)
# circuit.u1_gate(30, 1)
# circuit.ch_gate(0, 1)
# circuit.crx_gate(30, 0, 1)
# circuit.cry_gate(40, 0, 1)
# circuit.crz_gate(60, 0, 1)
# circuit.csx_gate(0, 1)
# circuit.cu1_gate(30, 0, 1)
# circuit.dcx_gate(0, 1)
# circuit.rc3x_gate(0, 1, 2, 3)
# circuit.rccx_gate(0, 1, 2)
# circuit.rzx_gate(30, 0, 1)

# gates having multiple angles
# circuit.u3_gate(30, 40, 2, 0)
# circuit.u2_gate(30, 20, 0)
# circuit.u_gate(40, 60, 3, 1)
# circuit.cu_gate(30, 60, 20, 60, 0, 1)
# circuit.cu3_gate(30, 60, 30, 0, 1)
# circuit.r_gate(30, 60, 0)


    input_arr = [0, 0, 0, 1, 0, 1, 1, 1, 0]

    grovers_algorithm_unknown_solution = GroversAlgorithm(clause_list=clause_list_light_board, input_arr=input_arr,
                                                          flip_output=True, solution_known='N')

    grovers_algorithm_known_solution = GroversAlgorithm(solution_known='Y', search_keyword=101)

    results = grovers_algorithm_unknown_solution.execute(repetitions=10, provider=providers.IBM_PROVIDER)

    # grovers_algorithm_unknown_solution.draw_grovers_circuit()

    print(results)


def random_number_demo():
    random_number = RandomNumber(length=4, output_type=constants.DECIMAL)\
        .execute(api=constants.IBM_API, device=constants.IBM_DEVICE_NAME)
    print(random_number)


def run_on_real_device():
    circuit = QCircuit(1)
    circuit.x_gate(0)
    circuit.measure_all()
    # circuit.draw_circuit(provider=providers.GOOGLE_PROVIDER)
    print(circuit.execute(provider=providers.IBM_PROVIDER, repetitions=10,
                          api=constants.IBM_API, device=constants.IBM_DEVICE_NAME))


if __name__ == '__main__':
    random_number_demo()
