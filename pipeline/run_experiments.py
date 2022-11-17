import numpy as np

# from qiskit import *
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute, assemble
from qiskit.visualization import plot_histogram, plot_bloch_vector
from qiskit.visualization import plot_state_qsphere, plot_state_city, plot_bloch_multivector
from qiskit.visualization import array_to_latex
import qiskit.quantum_info as qi

from qiskit_ionq import IonQProvider
from qiskit import Aer, execute, assemble

#import appropriate circuit constructions
from ionq_circuit_constructor import construct_ionq_circuit
from qiskit_circuit_constructor import construct_qiskit_circuit
from ibm_circuit_constructor import construct_ibm_circuit


def fidelities(out000, out001, out010, out011, out100, out101, out110, out111, bitval, shots):
    '''
    This function averages the fidelity of the clones and ancilla over experiment.

    Parameters:
    --------------
    outijk -
    bitval -
    shots - Number of samples.

    Returns:
    --------------
    bob_fidelity - Fidelity of copy sent to intended recipient (Bob).
    eve_fidelity - Fidelity of copy kept by eavesdropper (Eve).
    ancilla_fidelity - Fidelity of the ancilla.
    
    '''
    
    if bitval == 1:
        bob_fidelity = (out001 + out011 + out101 + out111)/shots
        eve_fidelity = (out010 + out011 + out110 + out111)/shots
        ancilla_fidelity = (out100 + out101 + out110 + out111)/shots
        
    if bitval == 0:
        bob_fidelity = (out010 + out000 + out110 + out100)/shots
        eve_fidelity = (out001 + out000 + out101 + out100)/shots
        ancilla_fidelity = (out000 + out001 + out010 + out011)/shots
        
    return bob_fidelity, eve_fidelity, ancilla_fidelity 

def get_circuit(theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X', gateset = 'qiskit'):
    '''
    This function gets the circuit to run with qiskit, IonQ Native Gates, or IBM Basis Gates.

    Parameters:
    --------------
    theta_2 - [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq' and 'ibm'.
    shots - Number of samples used for statistics. Default value is 1024. 

    Returns:
    --------------
    qc - Quantum circuit.
        
    '''

    qc = QuantumCircuit(3,3)
    
    if gateset == 'qiskit':
        #run with qiskit_circuit
        construct_qiskit_circuit(qc, theta_2, bitval, basis_send, basis_measure)

    if gateset == 'ionq':
        #run with ionq_circuit
        construct_ionq_circuit(qc, theta_2, bitval, basis_send, basis_measure)
    
    if gateset == 'ibm':
        #run with ibm_circuit
        construct_ibm_circuit(qc, theta_2, bitval, basis_send, basis_measure)

    return qc


def run_experiment(qc, theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X', gateset = 'qiskit', shots = 1024):
    '''
    This function runs the experiment with qiskit, IonQ Native Gates, or IBM Basis Gates.

    Parameters:
    --------------
    theta_2 - [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq' and 'ibm'.
    shots - Number of samples used for statistics. Default value is 1024. 

    Returns:
    --------------
    qc - Quantum circuit.
    bob_fidelity - Fidelity of copy sent to intended recipient (Bob).
    eve_fidelity - Fidelity of copy kept by eavesdropper (Eve).
    ancilla_fidelity - Fidelity of the ancilla.
    
    '''
    qc = get_circuit(theta_2, bitval, basis_send, basis_measure, gateset)
    
    #shots = 1024 # number of samples used for statistics
    if gateset == 'ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        native_simulator = provider.get_backend("ionq_simulator", gateset="native")
        job = native_simulator.run(qc)

    if gateset == 'ibm':

    #if gateset == 'qiskit' (our default)
    job = #appropriate simulator/etc.
    probs = job.get_probabilities()
    
    out000 = job.result().get_counts().get("000")
    out001 = job.result().get_counts().get("001")
    out010 = job.result().get_counts().get("010")
    out011 = job.result().get_counts().get("011")
    out100 = job.result().get_counts().get("100")
    out101 = job.result().get_counts().get("101")
    out110 = job.result().get_counts().get("110")
    out111 = job.result().get_counts().get("111")

    if out000 == None:
        out000 = 0
    if out001 == None:
        out001 = 0
    if out010 == None:
        out010 = 0
    if out011 == None:
        out011 = 0
        
    if out100 == None:
        out100 = 0
    if out101 == None:
        out101 = 0
    if out110 == None:
        out110 = 0
    if out111 == None:
        out111 = 0
        
    #print(f"out000 = {out000}; out001 = {out001}; out010 = {out010}; out011={out011}")
    #print(f"out100 = {out100}; out101 = {out101}; out110 = {out110}; out111={out111}")
    
    bob_fidelity, eve_fidelity, ancilla_fidelity = fidelities(out000, out001, out010, out011, out100, out101, out110, out111, bitval, shots)
    
    return qc, bob_fidelity, eve_fidelity, ancilla_fidelity