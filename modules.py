from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import circuit_drawer

def bitFlipError(stateVector = []):
    '''
        Quantum circuit to detect single bit flip errors.

        Note: Add compatibility of user given arbitrary state vector in the first qubit.
    '''
    q = QuantumRegister(3)
    c = QuantumRegister(3)

    qc = QuantumCircuit(q, c)

    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])

    return qc

