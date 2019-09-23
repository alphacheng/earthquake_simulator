"""
Created on Thu FEb 01 19:01:14 2018

@author: jeevi

Description: This code provides a bode plot's magnitude of a 3 body system which includes a tuned mass damper to dampen
resonance.

"""
# include dependencies
import numpy as np
from matplotlib import pyplot as plt
import scipy.linalg as sp

# parameters of model

g = 8.77
m = 1.83
L = 0.2
N = 3
b = 0.08
E = 210 * (10 ** 9)
d = 0.001
I = (b * d * d * d) / 12
k = (24 * E * I) / (L ** 3)
mass_on_floor = int(input("Which floor should mass be on: "))
mab = 0.2
kspring = 90.8  

max_amp_on_floor = []
M = m * np.identity(4)
M[3][3] = mab
# creating the mass matrix

K = np.identity(4)
K[0] = [2, -1, 0, 0]
K[1] = [-1, 2, -1, 0]
K[2] = [0, -1, 1, 0]
K[3] = [0, 0, 0, 0]
K[mass_on_floor - 1][mass_on_floor - 1] += 1
K[3][mass_on_floor - 1] -= 1
K = k * K
K[mass_on_floor - 1][3] = -kspring
K[3][3] = kspring

G = np.identity(4, dtype=np.complex)
G[0] = [2j, -1j, 0, 0]
G[1] = [-1j, 2j, -1j, 0]
G[2] = [0, -1j, 1j, 0]
G[3] = [0, 0, 0, 0]
G[mass_on_floor - 1][mass_on_floor - 1] += 1j
G[3][mass_on_floor - 1] -= 1j

G[mass_on_floor - 1][3] = -1j
G[3][3] = 1j
G = g * G

vect = np.zeros((4, 1))
vect[0] = 1
vect[1] = 0
vect[2] = 0

V, D = (sp.eig(K, M))

V = np.real(np.sqrt(V))  ##

print("Natural angular frequencies are: ", V)  # natural frequencies in radians
for i in range(3):
    amplitude = []
    amplitude_log = []
    frequencies = np.linspace(0, 130, 1001)
    for f in frequencies:
        B = K + (f * G) - ((f ** 2) * M)

        B_inv = (np.linalg.inv(B))

        amplitude.append((np.absolute(B_inv.dot(vect)[i])))

    if (abs(max(amplitude))) > (abs(min(amplitude))):  # prints the largest magnitude of amplitude for each floor
        max_amp_on_floor.append(abs(max(amplitude)))

    else:
        max_amp_on_floor.append(abs(min(amplitude)))
    plt.plot(frequencies, amplitude)
    n = str(i + 1)
    plt.title("Floor number: " + n)
    plt.show()

print("Maximum amplitude is ", max(max_amp_on_floor))
print("This occurs on floor: ", max_amp_on_floor.index(max(max_amp_on_floor)) + 1)
