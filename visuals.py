import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt

# from qiskit import *
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, execute, assemble, transpile
from qiskit.visualization import plot_histogram, plot_bloch_vector
from qiskit.visualization import plot_state_qsphere, plot_state_city, plot_bloch_multivector
from qiskit.visualization import array_to_latex
import qiskit.quantum_info as qi
from qiskit_ibm_runtime import QiskitRuntimeService

#import IonQ-specific
from qiskit_ionq import IonQProvider

#import appropriate circuit constructions
from pipeline.ionq_circuit_constructor import construct_ionq_circuit
from pipeline.qiskit_circuit_constructor import construct_qiskit_circuit
from pipeline.ibm_circuit_constructor import construct_ibm_circuit
from pipeline.run_experiments import get_fidelities, run_simulation


def display_result(job_id, alice_bit = 0, show = True, backend = "qiskit", shots = 1024):
    '''
    This function retrieves and displays the results of the experiment: Counts, Probabilities, and their histogram.

    Parameters:
    --------------
    job_id - ID of experiment (job) for which to retrieve information. If run on IBM, pass actual job, not job ID.
    backend - String of backend used: IBMQ computer utilized or 'ionq' or 'qiskit-ionq'. 
                    Default is 'ibmq_manila', but should use return from `run_experiment_ibm` when running on IBM. 
                    Overwritten for backend = 'ionq' or 'qiskit-ionq'.
    alice_bit - Value of the bit sent (0 or 1). Int, default is 0.
    shots - Number of samples. Int, default value is 1024. 

    Returns:
    --------------
    bob_prob - Probability of Bob measuring Alice bit.
    eve_prob - Probability of Eve measuring Alice bit.
    ancilla_prob - Probability of the ancilla being correct bit.
    counts - The 3-digit value counts for the experiment.
    
    '''

    if backend == 'ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        ionq = provider.get_backend("ionq_qpu", gateset="native")
        job = ionq.retrieve(job_id)
            
    elif backend == 'qiskit-ionq':
        provider = IonQProvider("RmK0yNkCDPmoxCH12uQ4U67lpu9kFgik")
        ionq = provider.get_backend("ionq_qpu")
        job = ionq.retrieve(job_id)

    else: #gateset == 'qiskit' or 'ibm'
        provider = IBMQ.load_account()
        backend = provider.get_backend(backend)
        job = backend.retrieve_job(job_id)

    counts = job.result().get_counts()

    #if show:
    print ("Counts:", counts)

    prob_bob = 0
    prob_eve = 0
    prob_ancilla = 0
    for key in counts.keys():
        if int(list(key)[-1]) == alice_bit:
            prob_bob += counts[key]/shots
        if int(list(key)[-2]) == alice_bit:
            prob_eve += counts[key]/shots
        if int(list(key)[-3]) == alice_bit:
            prob_ancilla += counts[key]/shots
    print("The probability of Bob measuring the correct bit is ", prob_bob, "\n",
            "The probability of Eve eavesdropping the correct bit is", prob_eve, "\n",
            "The probability of ancilla being the correct bit is", prob_ancilla)
    if show:
        display(plot_histogram(counts))
    
    return prob_bob, prob_eve, prob_ancilla, counts




def plot_fidelities(job_ids = [], basis = 'X', gateset = 'qiskit', backend = 'ibmq_manila', alice_bit = 0, shots = 1024, show = True):
    '''
    This function retrieves and displays the fidelities resulting from the experiment for Alice, Bob, and the Ancilla. 
    It returns ts, and the probabilities to plot against simulation and/or theory results.

    Parameters:
    --------------
    job_ids - List of IDs (str) of experiments (jobs) for which to retrieve information. 
    backend - String of backend used: IBMQ computer utilized or 'ionq' or 'qiskit-ionq'. 
                    Default is 'ibmq_manila', but should use return from `run_experiment_ibm` when running on IBM. 
                    Overwritten for backend = 'ionq' or 'qiskit-ionq'.
    alice_bit - Value of the bit sent (0 or 1). Int, default is 0.
    shots - Number of samples. Int, default value is 1024. 
    show - Boolean: display plot. Default is True.

    Returns:
    --------------
    QPU_B - Fidelities for Bob's measured qubit.
    QPU_E - Fidelities for Eve's measured qubit.
    QPU_A - Fidelities for Ancilla.
    ts - The theta_2 values used (x-axis values for plotting).
    
    '''
    #get angles tested
    ts = np.linspace(-np.pi/2, np.pi/2, 20)
    QPU_B = []
    QPU_E = []
    QPU_A = []

    for idx in range(len(job_ids)):
        #get fidelities/probabilities for each angle in ts
        qpu_prob_bob, qpu_prob_eve, qpu_prob_ancilla = get_fidelities(job_id = job_ids[idx], 
                                                                        gateset = gateset,
                                                                        backend = backend,
                                                                        bitval = alice_bit,
                                                                        shots = shots)
        #add probabilities to appropriate list
        QPU_B.append(qpu_prob_bob)
        QPU_E.append(qpu_prob_eve)
        QPU_A.append(qpu_prob_ancilla)
        
    #convert lists to arrays for plotting
    QPU_B = np.array(QPU_B)
    QPU_E = np.array(QPU_E)
    QPU_A = np.array(QPU_A)

    if show:
        #plot fidelites if show is true
        plt.figure(figsize=(15,8))
        plt.rcParams.update({'font.size': 12})

        plt.plot(ts, QPU_B, label = "Bob's fidelity (IonQ QPU)", marker='o',color='blue')
        plt.plot(ts, QPU_E, label = "Eve's fidelity (IonQ QPU)", marker='o',color='red')
        plt.plot(ts, QPU_A, label = "Ancilla fidelity (IonQ QPU)", marker='o',color='green')

        plt.yticks(np.arange(0,1.1, step = .1))
        plt.xticks(np.arange(-np.pi/2, 5*np.pi/8, step = np.pi/8))
        plt.legend(title = "Message bit =" + str(alice_bit) + str(basis) + "basis")

        plt.xlabel('theta_2')
        plt.show()
    
    return QPU_B, QPU_E, QPU_A, ts



def plot_sim_fidelities(basis = 'X', gateset = 'qiskit', alice_bit = 0, shots = 1024, show = True):
    '''
    This function runs, retrieves, and displays the fidelities resulting from the simulated experiment for Alice, Bob, and the Ancilla.
    It returns ts, and the probabilities to plot against experimental and/or theory results.

    Parameters:
    --------------
    basis - Basis with which to encode the bitvalue ('X' or 'Y'). Default is 'X'.
    gateset - Set of Gates with which to run experiment. Default 'qiskit', also takes 'ionq', 'ibm', and 'qiskit-ionq' 
                for running simple Qiskit gateset on IonQ. 'qiskit' uses qiskit transpile to basis gates.
    alice_bit - Value of the bit sent (0 or 1). Int, default is 0.
    shots - Number of samples. Int, default value is 1024. 
    show - Boolean: display plot. Default is True.

    Returns:
    --------------
    B - Fidelities for Bob's measured qubit.
    E - Fidelities for Eve's measured qubit.
    A - Fidelities for Ancilla.
    ts - The theta_2 values used (x-axis values for plotting).
    
    '''    
    ts = np.linspace(-np.pi/2, np.pi/2, 20)
    B = []
    E = []
    A = []
    for j in range(len(ts)):
        #run simulation for test angles
        qc, prob_bob, prob_eve, prob_ancilla, = run_simulation(theta_2 = ts[j], 
                                                                bitval = alice_bit, 
                                                                basis_send = basis, 
                                                                basis_measure = basis, 
                                                                gateset = gateset, 
                                                                shots = shots)
        #add probabilities to appropriate lists
        B.append(prob_bob)
        E.append(prob_eve)
        A.append(prob_ancilla)
    
    #convert lists to arrays for plotting
    B = np.array(B)
    E = np.array(E)
    A = np.array(A)

    if show:
        #plot if show is True
        plt.figure(figsize=(10,8))
        plt.plot(ts, B, label = "Bob's fidelity")
        plt.plot(ts, E, label = "Eve's fidelity")
        plt.plot(ts, A, label = "Ancilla fidelity")
        plt.yticks(np.arange(0,1.1, step = .1))
        plt.xticks(np.arange(-np.pi/2, 5*np.pi/8, step = np.pi/8))
        plt.legend(title = "Message bit =" + str(alice_bit) + str(basis) + "basis")
        plt.show()
    
    return B, E, A, ts

def plot_all_fidelities(basis, alice_bit, QPU_B, QPU_E, QPU_A, ts, B, E, A, hardware = 'IBM'):
    '''
    This function plots the fidelities resulting from the experiment and simulations for Alice, Bob, and the Ancilla. 
    It uses the returned values of plot_fidelities and plot_sim_fidelities.

    Parameters:
    --------------
    alice_bit - Value of the bit sent (0 or 1). Int, default is 0.
    QPU_B - QPU fidelities for Bob's measured qubit.
    QPU_E - QPU fidelities for Eve's measured qubit.
    QPU_A - QPU fidelities for Ancilla.
    ts - The theta_2 values used (x-axis values for plotting).
    B - Simulateion fidelities for Bob's measured qubit.
    E - Simulateion fidelities for Eve's measured qubit.
    A - Simulateion fidelities for Ancilla.

    Returns:
    --------------
    displays plot of fidelities
    
    '''

    plt.figure(figsize=(15,8))
    plt.rcParams.update({'font.size': 12})

    plt.plot(ts, QPU_B, label = "Bob's fidelity (" + hardware + "QPU)", marker='o',color='blue')
    plt.plot(ts, QPU_E, label = "Eve's fidelity (" + hardware + "QPU)", marker='o',color='red')
    plt.plot(ts, QPU_A, label = "Ancilla fidelity (" + hardware + "QPU)", marker='o',color='green')

    plt.plot(ts, B, label = "Bob's fidelity (" + hardware + "Simulation)", linestyle='--',color='blue')
    plt.plot(ts, E, label = "Eve's fidelity (" + hardware + "Simulation)", linestyle='--',color='red')
    plt.plot(ts, A, label = "Ancilla fidelity (" + hardware + "Simulation)", linestyle='--',color='green')

    plt.yticks(np.arange(0,1.1, step = .1))
    plt.xticks(np.arange(-np.pi/2, 5*np.pi/8, step = np.pi/8))
    #plt.legend(title = "Message bit =" + alice_bit + basis + "basis")
    plt.title("Fidelity Comparisons for " + str(hardware) + ": Message bit =" + str(alice_bit) + str(basis) + "basis", fontsize = 18)

    plt.ylabel('Fidelity')
    plt.xlabel('theta_2')
    plt.show()

    return

