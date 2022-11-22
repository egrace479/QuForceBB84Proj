# Asymmetric Cloning to Eavesdrop on BB84 Protocol

Elizabeth Campolongo, Brian Pigott, Hardik Routrat continuing our QuForce project.

The BB84 protocol is known to be a secure method of quantum key distribution, even in the case when an eavesdropper has unlimited resources at their disposal. However, the security of the protocol is only obtained below the level of noise that occurs in the quantum channel. The purpose of this project is twofold:

Develop an optimal strategy for an eavesdropper who is using asymmetric cloning; that is, develop and implement a strategy that gives the eavesdropper maximum information about the channel while minimizing the disturbance to the signal.

Consider the Quantum Bit Error Rate (QBER) in a lossy quantum channel with the presence of the eavesdropping strategy developed in (1) and implement error-correcting algorithms to derive a secure key. 

As an extension of this inital endeavor, we are further exploring the significance of the underlying hardware and noise on our base fidelity rates through implementation on IonQ using Native Gates directly. We hope to also check IBM's quantum computer using Basis Gates (pending access/funding).



# QuForce Innovation Fellows Project Description:
   
   This project was selected for 1st Place on Demo Day in August 2022, slides available on this repo, recording of Demo Day and more information on QuForce available at: https://thequantuminsider.com/2022/08/22/quforce-emerging-as-worlds-leading-community-for-post-quantum-cryptography-experts-academics-enthusiasts/.

## Experimental validation of information gain vs disturbance trade-offs for asymmetric cloning eavesdropping on BB84

### MENTOR: 
Alex Khan

### WHO’S WORKING ON THE PROJECT: 
Elizabeth Campolongo, Brian Pigott, Hardik Routray

### PROGRAMMING LANGUAGE: 
Python

### PROBLEM:  
The BB84 protocol is known to be a secure method of quantum key distribution, even in the case when an eavesdropper has unlimited resources at their disposal. However, the security of the protocol is only obtained below the level of noise that occurs in the quantum channel. The purpose of this project is twofold:

Develop an optimal strategy for an eavesdropper who is using asymmetric cloning; that is, develop and implement a strategy that gives the eavesdropper maximum information about the channel while minimizing the disturbance to the signal.

Consider the Quantum Bit Error Rate (QBER) in a lossy quantum channel with the presence of the eavesdropping strategy developed in (1) and implement error-correcting algorithms to derive a secure key. 

### STRATEGY & PLAN: 
This problem has two parts, both of which are important.

Theoretical Compnonent: What is the optimal strategy from a theoretical point of view? There is research about the optimal strategy in the symmetric case (see Ref 4, for instance) and it is known that with enough resources this is the best strategy. In case the eavesdropper has limited resources, there may be an advantage to an asymmetric approach. 

Experimental Component: The experimental component will involve use of an 11-qubit quantum computer developed by IonQ. We will need to develop our approach to execute these experiments and gather and interpret results.

### Timeline:
April 4 - May 2: learn about project content, develop code for BB84 protocol (in Qiskit), understand symmetric and asymmetric cloning, implement a noisy BB84 quantum channel and error-correcting algorithms in Qiskit 

May 2 - June 6: begin to implement asymmetric cloning in BB84, run on simulator, determine theoretical limit of information gain vs. disturbance for eavesdropper, study QBER and secure key rates as a function of various parameters (N transferred bits, n checked bits, Eve’s cloning strategies)

June 6 - July 11: testing on IonQ devices, experiments and data collection

July 11 - August 8: data analysis, preparation of presentation

### SUCCESS METRICS: 
Gold: Successful implementation on IonQ, including asymmetric cloning and simulation of noisy quantum channel. Theoretical predictions are a good match against experimental results.

Silver: Implementation on IonQ with a noisy channel is successful. Theoretical predictions regarding asymmetric cloning can be made. Implementation of asymmetric cloning on IonQ device is incomplete or unsuccessful OR there is a mismatch between the theoretical predictions and the experimental outcome.

Bronze: Implementation on IonQ with a noisy channel is unsuccessful OR theoretical predictions for asymmetric cloning are incomplete OR there is no implementation for the cloning on the IonQ device.

Participation Medal: We tried but nothing worked out; we learned a lot.

### Reading material:
Brus, Cinchetti, D’Ariano, and Macchiavello, Phase-covariant quantum cloning, Phys. Rev. A (2000) https://arxiv.org/abs/quant-ph/9909046

Lamoureux, and Cerf, Asymmetric phase-covariant d-dimensional cloning, Quantum Information and Computation (2005) https://arxiv.org/abs/quant-ph/0410054

Fan, Matsumoto, Wang, and Wadati, Quantum cloning machines for equatorial qubits, Phys. Rev. A (2001) https://arxiv.org/abs/quant-ph/0101101

Fuchs, Gisin, Griffiths, Niu, and Peres, Optimal eavesdropping in quantum cryptography. I. Information bound and optimal strategy, Phys. Rev. A (1997) https://arxiv.org/abs/quant-ph/9701039

Xu, Ma, Zhang, Lo, and Pan, Secure quantum key distribution with realistic devices, Reviews of Modern Physics (2020)  https://arxiv.org/abs/1903.09051 

Scarani, Bechmann-Pasquinucci, Cerf, Dusek, Lutkenhaus, Peev, The security of practical quantum key distribution, Reviews of Modern Physics (2009) https://arxiv.org/abs/0802.4155

Xiao, Yao, Zhou, and Wang, Distrubtion of quantum Fisher information in asymmetric cloning machines, Scientific Reports (2014) https://arxiv.org/abs/1409.2199

Schaffner, Cryptography in the bounded-quantum-storage model, Thesis (2007) https://arxiv.org/abs/0709.0289

Renner, Security of quantum key distribution, Thesis (2005) https://arxiv.org/abs/quant-ph/0512258 

Benletaief, Rezig, and Bouallegue, Reconciliation for Practical Quantum Key Distribution with BB84 Protocol, 2011 11th Mediterranean Microwave Symposium (MMS)R (2011) https://arxiv.org/abs/2002.07778

Rezakhani, Siadatnejad, and Ghaderi, Separability in asymmetric phase-covariant cloning, Phys. Lett. A (2004) https://arxiv.org/abs/quant-ph/0312024

