"""
Created on Thu FEb 01 19:01:14 2018

@author: jeevi

Description: This code provides a bode plot's magnitude of a 3 body system. This is a simulation of an earthquake on a three-storey building
"""

# include dependencies
import numpy as np
from matplotlib import pyplot as plt
import scipy.linalg as sp

# set up initial parameters of model

m = 1.83
L = 0.2
N = 3
b = 0.08
E = 210*(10**9)
d = 0.001
I = (b*d*d*d)/12
k = (24*E*I)/(L**3)

max_amp_on_floor = [] # this array will store the maximum resonant amplitude for each floor

# set up matrix equations

M = m*np.identity(3)
K = np.identity(3)
K[0] = [2, -1, 0]
K[1] = [-1, 2, -1]
K[2] = [0, -1, 1]
K = k*K

G = np.identity(3, dtype=np.complex)
G[0] = [2j, -1j, 0]
G[1] = [-1j, 2j, -1j]
G[2] = [0, -1j, 1j]
G = 15* G
M_inv = np.linalg.inv(M)

# this vector simulates only moving the ground floor
vect = np.zeros((3, 1))
vect[0] = 1

# V stores the square of the natural frequencies, D stores the eigenvectors (the relative amplitude between each floor)
V, D = (sp.eig(K, M))

V = np.real(np.sqrt(V)) # now V stores the natural frequencies

print("Natural angular frequencies are: ",V)

for i in range(3):
    amplitude = []
    phase = []
    amplitude_log = []
    frequencies = np.linspace(0, 130, 1001)
    for f in frequencies:
        B = K + (f*G)-((f**2)*M)
        B_inv = (np.linalg.inv(B))
        amplitude.append(np.absolute(B_inv.dot(vect)[i])[0])
        phase.append((np.angle(B_inv.dot(vect)[i])*180/np.pi)[0])
    print(amplitude)
    print(phase) # phase is in degrees



    if (abs(max(amplitude))) > (abs(min(amplitude))):   # prints the largest magnitude of amplitude for each floor
        max_amp_on_floor.append(abs(max(amplitude)))
    else:
        max_amp_on_floor.append(abs(min(amplitude)))
    plt.plot(frequencies, amplitude)
    n = str(i+1)
    plt.title("Floor number: " + n)
    plt.show()

print("Maximum amplitude is ", max(max_amp_on_floor))
print("This occurs on floor: ", max_amp_on_floor.index(max(max_amp_on_floor))+1)







