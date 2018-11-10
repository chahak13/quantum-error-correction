from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import circuit_drawer
from qiskit.extensions.simulator import *
import math
import random
from copy import deepcopy

def bitFlipError(stateVector = [], error_probability = 0.2):
    '''
        Quantum circuit to detect single bit flip errors.

        Note: Add compatibility of user given arbitrary state vector in the first qubit.
    '''
    q = QuantumRegister(3, name = 'q')
    c = ClassicalRegister(3, name = 'c')

    qc = QuantumCircuit(q, c, name='bit_flip_circuit')

    # Brings the 3 qubit system to the state (a*|000> + b*|111>). a=b=1/sqrt(2)
    if stateVector == []:
        qc.h(q[0])
    else:
        desired_vector = stateVector
        qc.initialize(desired_vector, [q[0]])
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    # Random bit flip error with a probability of 0.2
    ind = random.randint(0, 2)
    if random.random() <= error_probability:
        print("Bit number {} flipped due to noise".format(ind+1))
        qc.x(q[ind])

    ancilla = QuantumRegister(2, name = 'a')
    classical_ancilla = ClassicalRegister(2, name = 'ca')
    qc.add(ancilla)
    qc.add(classical_ancilla)

    qc.cx(q[0], ancilla[0])
    qc.cx(q[1], ancilla[0])
    qc.cx(q[0], ancilla[1])
    qc.cx(q[2], ancilla[1])

    qc.measure(ancilla, classical_ancilla)

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Finding bit flip error: ", result_sim)
    print(result_sim.get_counts(qc))

    error_bit = list(result_sim.get_counts().keys())[0].split()[0]
    if error_bit == '11':
        print("Bit-flip error in the first bit")
        qc.x(q[0])
    elif error_bit == '01':
        print("Bit-flip error in second bit")
        qc.x(q[1])
    elif error_bit == '10':
        print("Bit-flip error in third bit")
        qc.x(q[2])
    else:
        print("No bit-flip error in the code.")

    return q, c, qc


def phaseFlipError(stateVector=[], error_probability=0.2):
    '''
        Quantum circuit to detect single bit flip errors.

        Note: Add compatibility of user given arbitrary state vector in the first qubit.
    '''
    q = QuantumRegister(3, name='q')
    c = ClassicalRegister(3, name='c')

    qc = QuantumCircuit(q, c, name='phase_flip_circuit')

    # Brings the 3 qubit system to the state (a*|000> + b*|111>). a=b=1/sqrt(2)
    if stateVector == []:
        qc.h(q[0])
    else:
        desired_vector = stateVector
        qc.initialize(desired_vector, [q[0]])

    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])

    for qubit in q:
        qc.h(qubit)

    # Random phase flip error with a probability p
    ind = random.randint(0, 2)
    if random.random() <= error_probability:
        print("Phase of bit number {} flipped due to noise".format(ind+1))
        qc.h(q[ind])
    else:
        print("No phase error")
    # qc.h(q[1])
    print("Received noisy qubits. Correcting them.")

    for qubit in q:
        qc.h(qubit)

    qc.cx(q[0], q[2])
    qc.cx(q[0], q[1])


    qc.ccx(q[1], q[2], q[0])
    # qc.measure(q[0], c[0])
    # qc.measure(q[1], c[1])
    # qc.measure(q[2], c[2])

    # backend_sim = Aer.get_backend('qasm_simulator')
    # job_sim = execute(qc, backend_sim)
    # result_sim = job_sim.result()

    # print("Finding phase flip error: ", result_sim)
    # print(result_sim.get_counts(qc))

    # if len(result_sim.get_counts()) != 1:
    #     error_bit = list(result_sim.get_counts().keys())[1][:2]
    #     print(error_bit)
    #     if error_bit == '11':
    #         print("Phase-flip error in the first bit")
    #         qc.x(q[0])
    #     elif error_bit == '01':
    #         print("Phase-flip error in second bit")
    #         qc.h(q[1])
    #     elif error_bit == '10':
    #         print("Phase-flip error in third bit")
    #         qc.h(q[2])
    #     else:
    #         print("No phase-flip error in the code.")
    # else:
    #     print("No phase-flip error in the code.")

    return q, c, qc


def shorsCode(stateVector = [], error_probability=0.8):
    '''
        Quantum circuit that detects and corrects any one bit error. Based on Shor's code.

        Qubits 0, 3, 6 are the main three qubits that the user sends.
        Qubits 1, 2, 4, 5, 7, 8 are auxiliary qubits that are used by the circuit.

        |----------|---------------|
        |   Main   |    Auxiliary  |
        |    0     |      1,2      |
        |    3     |      4,5      |
        |    6     |      7,8      |
        |----------|---------------|

    '''

    q = QuantumRegister(9)
    c = ClassicalRegister(9)

    qc = QuantumCircuit(q, c, name='Shor_code')

    if stateVector == []:
        qc.h(q[0])
    else:
        desired_vector = stateVector
        qc.initialize(desired_vector, [q[0]])

    qc.cx(q[0], q[3])
    qc.cx(q[0], q[6])

    qc.h(q[0])
    qc.h(q[3])
    qc.h(q[6])

    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])

    qc.cx(q[3], q[4])
    qc.cx(q[3], q[5])

    qc.cx(q[6], q[7])
    qc.cx(q[6], q[8])


    # Random errors here
    ind = random.choice([0, 3, 6])
    if random.random() <= error_probability:
        if random.random() <= 0.5:
            print("Phase of bit number {} flipped due to noise".format(ind+1))
            qc.h(q[ind])
        else:
            print("Bit number {} flipped due to noise".format(ind+1))
            qc.x(q[ind])
    else:
        print("No error")
    print("Received noisy qubits. Correcting them.")

    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])

    qc.cx(q[3], q[4])
    qc.cx(q[3], q[5])

    qc.cx(q[6], q[7])
    qc.cx(q[6], q[8])

    qc.ccx(q[1], q[2], q[0])
    qc.ccx(q[4], q[5], q[3])
    qc.ccx(q[7], q[8], q[6])

    qc.h(q[0])
    qc.h(q[3])
    qc.h(q[6])

    qc.cx(q[0], q[3])
    qc.cx(q[0], q[6])

    qc.ccx(q[3], q[6], q[0])

    return q, c, qc
