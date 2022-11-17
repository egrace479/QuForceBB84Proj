import numpy as np

# from qiskit import *
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute, assemble
from qiskit.visualization import plot_histogram, plot_bloch_vector
from qiskit.visualization import plot_state_qsphere, plot_state_city, plot_bloch_multivector
from qiskit.visualization import array_to_latex
import qiskit.quantum_info as qi


def qiskit_alice_prepares(qc, bitval, basis):
    '''
    This function prepares the qubit to send in qiskit.

    Parameters:
    --------------
    qc - Quantum circuit.
    bitval - Value of the bit to send ('0' or '1')
    basis - Basis with which to encode the bitvalue ('X' or 'Y').

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''

    if basis == 'X' and bitval == 1: # initial state is |->
        qc.x(0)
        qc.h(0)
        return qc

    if basis == 'X' and bitval == 0: # initial state is |+>
        qc.h(0)
        return qc

    if basis == 'Y' and bitval == 1: # initial state |-i>
        qc.rx(np.pi/2, 0)
        return qc

    if basis == 'Y' and bitval == 0: # initial state |+i>
        qc.rx(-np.pi/2, 0)
        return qc



def qiskit_measurement_prep(qc, basis):
    '''
    This function prepares the circuit (in qiskit) to measure in desired measurement basis.

    Parameters:
    --------------
    qc - Quantum circuit.
    basis - Basis in which to measure the qubit ('X' or 'Y').

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''
    
    if basis == 'X':
        qc.h(0)
        qc.h(1)
        qc.h(2)
        
    if basis == 'Y':
        qc.rx(np.pi/2, 0)
        qc.rx(np.pi/2, 1)
        qc.rx(np.pi/2, 2)

    return qc

def qiskit_clone(qc, theta_2):
    '''
    This function constructs the cloning circuit in qiskit.

    Parameters:
    --------------
    qc - Quantum circuit.
    theta_2 - [-pi/2, pi/2]. 

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''
        
    #Eve Prep
    #
    qc.ry(np.pi/2, 1)   
    qc.cnot(1,2)  #cnot(control, target)   
    qc.ry(2*theta_2, 2)
    qc.cnot(2,1)
    qc.ry(2*theta_2, 1)
    
    #Eve Clone
    #  
    qc.cnot(0,1)
    qc.cnot(0,2)
    qc.cnot(1,0)
    qc.cnot(2,0)
    
    return qc

def construct_qiskit_circuit(qc, theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X'):
    '''
    This function constructs the full circuit in Qiskit Gates.

    Parameters:
    --------------
    qc - Quantum circuit.
    theta_2 - [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.


    Returns:
    --------------
    qc - Quantum circuit.
    
    '''

    qiskit_alice_prepares(qc, bitval, basis_send)
    qc.barrier()
    
    # Eve clones the flying qubit
    qiskit_clone(qc, theta_2)
    
    qc.barrier()
    # Bob and Eve prepare to measure
    qiskit_measurement_prep(qc, bitval, basis_measure)
    
    qc.barrier()
    
    # Bob and Eve measure
    qc.measure(0,0)
    qc.measure(1,1)
    qc.measure(2,2)

    return qc