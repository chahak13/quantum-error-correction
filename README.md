# quantum-error-correction

This repository consists of implementations of Quantum Error Correction circuits that were implemented as a part of a course project. It uses the Qiskit package provided by IBM for Python to simulate the quantum circuits. Circuits for 1 qubit Bit Flip, Phase Flip and Shors code have been implemented.

## To install Qiskit

`pip install qiskit`

## Testing

To run the codes and test the circuits, simply provide a command line argument from `bitflip`, `phaseflip` or `shors` while running the `test.py`. The circuits implement random noise of its own too with a default error probability of `0.8` which can be changed by providing it as a command line argument. The user can also use the command line option `desiredState` to provide the amplitudes of `0` and `1` in the desired state. The default is a `0` state.

```shell
usage: test.py [-h] --error {bitflip,phaseflip,shors}
               [--error_probability ERROR_PROBABILITY]
               [--desiredState DESIREDSTATE DESIREDSTATE]

optional arguments:
  -h, --help            show this help message and exit
  --error {bitflip,phaseflip,shors}
                        The type of error correction that is to be simulated.
  --error_probability ERROR_PROBABILITY
                        The probability of there being an error in the qubits
                        while transmission.
  --desiredState DESIREDSTATE DESIREDSTATE
                        Amplitudes of the states 0 and 1 in the form of a
                        list.
```

Example: `python test.py --error bitflip --desiredState 1 0`