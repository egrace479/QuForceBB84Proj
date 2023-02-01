import numpy as np

# from qiskit import *
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, execute, assemble, transpile
from qiskit.visualization import plot_histogram, plot_bloch_vector
from qiskit.visualization import plot_state_qsphere, plot_state_city, plot_bloch_multivector
from qiskit.visualization import array_to_latex
import qiskit.quantum_info as qi
from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_ionq import IonQProvider
from qiskit import Aer, execute, assemble

#import appropriate circuit constructions
from .ionq_circuit_constructor import construct_ionq_circuit
from .qiskit_circuit_constructor import construct_qiskit_circuit
from .ibm_circuit_constructor import construct_ibm_circuit


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
    theta_2 - Float in [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Int, default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq', 'ibm', and 'qiskit-ionq' 
                for running simple Qiskit gateset on IonQ.
    shots - Number of samples used for statistics. Int, efault value is 1024. 

    Returns:
    --------------
    qc - Quantum circuit.

    '''

    qc = QuantumCircuit(3,3)
    
    if (gateset == 'qiskit') or (gateset == 'qiskit-ionq'):
        #run with qiskit_circuit
        construct_qiskit_circuit(qc, theta_2, bitval, basis_send, basis_measure)

    if gateset == 'ionq':
        #run with ionq_circuit
        construct_ionq_circuit(qc, theta_2, bitval, basis_send, basis_measure)
    
    if gateset == 'ibm':
        #run with ibm_circuit
        construct_ibm_circuit(qc, theta_2, bitval, basis_send, basis_measure)

    return qc


def run_experiment(theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X', gateset = 'qiskit', backend = 'ibmq_manila', shots = 1024):
    '''
    This function runs the experiment with qiskit, IonQ Native Gates, or IBM Basis Gates.

    Parameters:
    --------------
    theta_2 - Float in [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Int, default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq', 'ibm', and 'qiskit-ionq' 
                for running simple Qiskit gateset on IonQ.
    backend - String of IBM computer to run on: eg, 'ibm_nairobi', 'ibm_oslo', or 'ibmq_manila'. Default set to 'ibmq_manila'.
    shots - Number of samples used for statistics. Int, default value is 1024. 

    Returns:
    --------------
    qc - Quantum circuit.
    job_id - ID to identify job (running on QPU).


    
    '''
    qc = get_circuit(theta_2, bitval, basis_send, basis_measure, gateset)
        
 
    #Set up to run on hardware, not simulators
    if gateset == 'ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        ionq = provider.get_backend("ionq_qpu", gateset="native")
        job = ionq.run(qc, backend = ionq, shots = shots)
        #probs = job.get_probabilities()
    
    elif gateset == 'qiskit-ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        ionq = provider.get_backend("ionq_qpu")
        job = ionq.run(qc, backend = ionq, shots = shots)

    elif gateset == 'ibm':
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='HUB')
        backend = provider.get_backend(backend)
        job = execute(qc, shots = shots)
        
    else: #if gateset == 'qiskit' (our default)
        qc_1 = transpile(qc, basis_gates = ['cx', 'rz', 'id', 'sx', 'x'])
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='HUB')
        backend = provider.get_backend(backend)
        job = execute(qc_1, shots = shots)
    
    job_id = job.job_id()
    
    #bob_fidelity, eve_fidelity, ancilla_fidelity = fidelities(out000, out001, out010, out011, out100, out101, out110, out111, bitval, shots)
    
    return qc, job_id #, bob_fidelity, eve_fidelity, ancilla_fidelity



def run_simulation(theta_2 = np.pi/8, bitval = 0, basis_send = 'X', basis_measure = 'X', gateset = 'qiskit', shots = 1024):
    '''
    This function runs the experiment on the simulator with qiskit, IonQ Native Gates, or IBM Basis Gates.

    Parameters:
    --------------
    theta_2 - Float in [-pi/2, pi/2]. Default value is pi/8, which gives symmetric clone.
    bitval - Value of the bit to send (0 or 1). Int, default is 0.
    basis_send - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    basis_measure - Basis in which to measure the qubit ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq', 'ibm', and 'qiskit-ionq' 
                for running simple Qiskit gateset on IonQ.
    shots - Number of samples used for statistics. Int, default value is 1024. 

    Returns:
    --------------
    qc - Quantum circuit.
    job_id - ID to identify job (running on QPU).


    
    '''
    qc = get_circuit(theta_2, bitval, basis_send, basis_measure, gateset)
    
    #shots = 1024 # number of samples used for statistics
    if gateset == 'ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        native_simulator = provider.get_backend("ionq_simulator", gateset="native")
        job = native_simulator.run(qc, shots = shots)
        #probs = job.get_probabilities()
    
    elif gateset == 'qiskit-ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        native_simulator = provider.get_backend("ionq_simulator")
        job = native_simulator.run(qc, shots = shots)

    else: #if gateset == 'qiskit' (our default) or 'ibm'
        sim = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend = sim, shots = shots)
        
    bob_fidelity, eve_fidelity, ancilla_fidelity = get_sim_fidelities(job, bitval, shots)

    return qc, bob_fidelity, eve_fidelity, ancilla_fidelity



def get_fidelities(job_id, gateset = 'qiskit', bitval = 0, shots = 1024):
    '''
    This function averages the fidelity of the clones and ancilla over experiment (job).

    Parameters:
    --------------
    job_id - ID of experiment (job) for which to retrieve information.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq', 'ibm', and 'qiskit-ionq' 
                for running simple Qiskit gateset on IonQ.
    bitval - Value of the bit sent (0 or 1). Int, default is 0.
    shots - Number of samples. Int, default value is 1024. 

    Returns:
    --------------
    bob_fidelity - Fidelity of copy sent to intended recipient (Bob).
    eve_fidelity - Fidelity of copy kept by eavesdropper (Eve).
    ancilla_fidelity - Fidelity of the ancilla.
    
    '''

    if gateset == 'ionq':
            provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
            ionq = provider.get_backend("ionq_qpu", gateset="native")
            job = ionq.retrieve(job_id)
            
    elif gateset == 'qiskit-ionq':
            provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
            ionq = provider.get_backend("ionq_qpu")
            job = ionq.retrieve(job_id)

   # elif gateset == 'ibm':
   #         job = execute(qc, shots = shots)
        
   # else: #if gateset == 'qiskit' (our default)
   #         sim = Aer.get_backend('qasm_simulator')
   #         job = execute(qc, backend = sim, shots = shots)



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
    
    if bitval == 1:
        bob_fidelity = (out001 + out011 + out101 + out111)/shots
        eve_fidelity = (out010 + out011 + out110 + out111)/shots
        ancilla_fidelity = (out100 + out101 + out110 + out111)/shots
        
    if bitval == 0:
        bob_fidelity = (out010 + out000 + out110 + out100)/shots
        eve_fidelity = (out001 + out000 + out101 + out100)/shots
        ancilla_fidelity = (out000 + out001 + out010 + out011)/shots
        
    return bob_fidelity, eve_fidelity, ancilla_fidelity 

def get_sim_fidelities(job, bitval, shots):
    '''
    This function averages the fidelity of the clones and ancilla over simulated experiment (job).

    Parameters:
    --------------
    job - Simulation (job) for which to retrieve information.
    bitval -
    shots - Number of samples. Int, default 1024.

    Returns:
    --------------
    bob_fidelity - Fidelity of copy sent to intended recipient (Bob).
    eve_fidelity - Fidelity of copy kept by eavesdropper (Eve).
    ancilla_fidelity - Fidelity of the ancilla.
    
    '''

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
    
    if bitval == 1:
        bob_fidelity = (out001 + out011 + out101 + out111)/shots
        eve_fidelity = (out010 + out011 + out110 + out111)/shots
        ancilla_fidelity = (out100 + out101 + out110 + out111)/shots
        
    if bitval == 0:
        bob_fidelity = (out010 + out000 + out110 + out100)/shots
        eve_fidelity = (out001 + out000 + out101 + out100)/shots
        ancilla_fidelity = (out000 + out001 + out010 + out011)/shots
        
    return bob_fidelity, eve_fidelity, ancilla_fidelity 

