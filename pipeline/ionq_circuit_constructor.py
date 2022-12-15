import numpy as np

# from qiskit import *
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit

from qiskit_ionq import IonQProvider
# import gates
from qiskit_ionq import GPIGate, GPI2Gate, MSGate
from qiskit import Aer, execute, assemble



def ionq_alice_prepares(qc, bitval, basis):
    '''
    This function prepares the qubit to send in IonQ Native Gates.

    Parameters:
    --------------
    qc - Quantum circuit.
    bitval - Int value of the bit to send (0 or 1).
    basis - Basis with which to encode the bitvalue ('X' or 'Y').

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''

    if basis == 'X' and bitval == 1: # initial state is |->
        #qc.x(0)
        #qc.h(0)
        qc.append(GPIGate(0), [0])
        qc.append(GPI2Gate(1/4), [0])
        qc.append(GPIGate(0), [0])
        return qc
    if basis == 'X' and bitval == 0: # initial state is |+>
        #qc.h(0)
        qc.append(GPI2Gate(1/4), [0])
        qc.append(GPIGate(0), [0])
        return qc
    if basis == 'Y' and bitval == 1: # initial state |-i>
        #qc.rx(np.pi/2, 0)
        qc.append(GPI2Gate(1/4), [0])
        qc.append(GPIGate(-1/8), [0])
        return qc
    if basis == 'Y' and bitval == 0: # initial state |+i>
        #qc.rx(-np.pi/2, 0)
        qc.append(GPI2Gate(1/4), [0])
        qc.append(GPIGate(1/8), [0])
        return qc



def ionq_measurement_prep(qc, basis):
    '''
    This function prepares the circuit (in IonQ Native Gates) to measure in desired measurement basis.

    Parameters:
    --------------
    qc - Quantum circuit.
    basis - Basis in which to measure the qubit ('X' or 'Y').

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''
    
    if basis == 'X':
        #qc.h(0)
        qc.append(GPI2Gate(1/4), [0])
        qc.append(GPIGate(0), [0])
        #qc.h(1)
        qc.append(GPI2Gate(1/4), [1])
        qc.append(GPIGate(0), [1])
        #qc.h(2)
        qc.append(GPI2Gate(1/4), [2])
        qc.append(GPIGate(0), [2])
        
    if basis == 'Y':
        #qc.rx(np.pi/2, 0)
        qc.append(GPI2Gate(0), [0])
        #qc.rx(np.pi/2, 1)
        qc.append(GPI2Gate(0), [1])
        #qc.rx(np.pi/2, 2)
        qc.append(GPI2Gate(0), [2])
    '''    
    if basis == 'Y':
        #qc.rx(np.pi/2, 0)
        qc.append(GPIGate(1/8), [0])
        qc.append(GPI2Gate(-.25), [0])
        
        #qc.rx(np.pi/2, 1)
        qc.append(GPIGate(1/8), [1])
        qc.append(GPI2Gate(-.25), [1])
        
        #qc.rx(np.pi/2, 2)
        qc.append(GPIGate(1/8), [2])
        qc.append(GPI2Gate(-.25), [2])
        '''

    return qc

def ionq_clone(qc, theta_2):
    '''
    This function constructs the cloning circuit in IonQ Native Gates.

    Parameters:
    --------------
    qc - Quantum circuit.
    theta_2 - float in [-pi/2, pi/2]. 

    Returns:
    --------------
    qc - Quantum circuit.
    
    '''
        
    #Eve Prep

    qc.append(GPIGate(1/4), [1])
    
    qc.append(MSGate(0,0), [1,2])
    
    qc.append(GPIGate(5/8), [1])
    #AltB
    #qc.append(GPIGate(-1/8), [1])
    #AltE
    # qc.append(GPIGate(3/8), [1])
    
    qc.append(GPIGate((3*np.pi/4 - theta_2)/(2*np.pi)), [2])
    #AltB
    #qc.append(GPIGate((-np.pi/4 - theta_2)/(2 * np.pi)), [2])
    #AltE
    #qc.append(GPIGate((np.pi/4 - theta_2)/(2 * np.pi)), [2])
    
    qc.append(MSGate(0,0), [2,1])
    
    qc.append(GPI2Gate(3/4), [2])
    #AltBE
    #qc.append(GPI2Gate(-1/4),[2])
     
    
    qc.append(GPIGate(1/8),[1])
    qc.append(GPIGate(0), [1])
    qc.append(GPI2Gate(1/4), [1])
    qc.append(GPIGate(theta_2/(2*np.pi)), [1])
    qc.append(GPI2Gate(1/4), [1])
    qc.append(GPIGate(1/8), [1])
    
    #Eve Clone
    
    qc.append(GPI2Gate(1/4), [0])
    
    qc.append(MSGate(0,0), [0,1])
    
    qc.append(MSGate(0,0), [0,2])
    
    qc.append(GPI2Gate(1/4), [0])
    
    qc.append(GPIGate(3/8), [2])
    qc.append(GPIGate(3/8), [1])
    #AltB
    #qc.append(GPIGate(-1/8), [2])
    #qc.append(GPIGate(-1/8), [1])
    #AltE
    #qc.append(GPIGate(1/8), [2])
    #qc.append(GPIGate(1/8), [1])
    
    qc.append(MSGate(0,0), [1,0])
    
    qc.append(GPI2Gate(3/4), [1])
    #AltBE
    #qc.append(GPI2Gate(-1/4), [1])
    
    qc.append(MSGate(0,0), [2,0])
    
    qc.append(GPI2Gate(3/4), [2])
    #AltBE
    #qc.append(GPI2Gate(-1/4), [2])

    
    return qc


def construct_ionq_circuit(qc, theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X'):
    '''
    This function constructs the full circuit in IonQ Native Gates.

    Parameters:
    --------------
    qc - Quantum circuit.
    theta_2 - Float in [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Int, default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.


    Returns:
    --------------
    qc - Quantum circuit.
    
    '''

    ionq_alice_prepares(qc, bitval, basis_send)
    qc.barrier()
    
    # Eve clones the flying qubit
    ionq_clone(qc, theta_2)
    
    qc.barrier()
    # Bob and Eve prepare to measure
    ionq_measurement_prep(qc, bitval, basis_measure)
    
    qc.barrier()
    
    # Bob and Eve measure
    qc.measure(0,0)
    qc.measure(1,1)
    qc.measure(2,2)

    return qc