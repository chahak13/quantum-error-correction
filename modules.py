from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import circuit_drawer
import math

def bitFlipError(stateVector = []):
    '''
        Quantum circuit to detect single bit flip errors.

        Note: Add compatibility of user given arbitrary state vector in the first qubit.
    '''
    q = QuantumRegister(3, name = 'q')
    c = ClassicalRegister(3, name = 'c')

    qc = QuantumCircuit(q, c, name='bit_flip_circuit')

    # Brings the 3 qubit system to the state (a*|000> + b*|111>). a=b=1/sqrt(2)
    qc.h(q[0])
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])

    # Random bit flip error section.
    qc.x(q[2])

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

    print("Simulation: ", result_sim)
    print(result_sim.get_counts(qc))

    error_bit = list(result_sim.get_counts().keys())[0].split()[0]
    if error_bit == '11':
        print("Bit-flip error in the first bit")
        
    elif error_bit == '01':
        print("Bit-flip error in second bit")
    elif error_bit == '10':
        print("Bit-flip error in third bit")
    else:
        print("No bit-flip error in the code.")

    return q, c, qc
