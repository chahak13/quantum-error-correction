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

    qc = QuantumCircuit(q, c, name='bit_flip_circuit')

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
    # ind = random.randint(0, 2)
    # if random.random() <= error_probability:
    #     print("Phase of bit number {} flipped due to noise".format(ind+1))
        # qc.h(q[ind])
    qc.h(q[0])
    print("Received noisy qubits. Correcting them.")

    for qubit in q:
        qc.h(qubit)

    qc.cx(q[0], q[2])
    qc.cx(q[0], q[1])


    # qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])
    qc.measure(q[2], c[2])

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Finding bit flip error: ", result_sim)
    print(result_sim.get_counts(qc))

    if len(result_sim.get_counts()) != 1:
        error_bit = list(result_sim.get_counts().keys())[1][:2]
        print(error_bit)
        if error_bit == '11':
            print("Phase-flip error in the first bit")
            qc.x(q[0])
        elif error_bit == '01':
            print("Phase-flip error in second bit")
            qc.h(q[1])
        elif error_bit == '10':
            print("Phase-flip error in third bit")
            qc.h(q[2])
        else:
            print("No phase-flip error in the code.")
    else:
        print("No phase-flip error in the code.")

    return q, c, qc
