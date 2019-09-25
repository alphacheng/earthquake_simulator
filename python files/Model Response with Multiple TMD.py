"""
Created on Thu FEb 01 19:01:14 2018

@author: jeevi

This simulates the previous model with multiple dampers

"""
import numpy as np
from matplotlib import pyplot as plt
import scipy.linalg as sp

m = 1.83  # parameters of model
L = 0.2
N = 3
b = 0.08
E = 210 * (10 ** 9)
d = 0.001
I = (b * d * d * d) / 12
k = (24 * E * I) / (L ** 3)
g = 8.77
mab = 0.3  # 5% of the building's mass is the extra mass for the absorber
# parameters of the damper
while True:
    n_dampers = int(input("How many dampers do you want to add: "))
    mass_on_floor = int(input("What floor should the masses be added to: "))
    max_amp_on_floor = []
    mab = 1 / n_dampers
    M = m * np.identity(n_dampers + 3)
    for i in range(3, n_dampers + 3):
        M[i][i] = 1
    # creating the mass matrix
    K = np.zeros((n_dampers + 3, n_dampers + 3))
    K[0][0:3] = [2, -1, 0]
    K[1][0:3] = [-1, 2, -1]
    K[2][0:3] = [0, -1, 1]
    K[3][0:3] = [0, 0, 0]
    K[mass_on_floor - 1][mass_on_floor - 1] += n_dampers

    for i in range(3, n_dampers + 3):
        K[i][mass_on_floor - 1] -= 1
    K = k * K
    for i in range(3, n_dampers + 3):
        kspring = (i ** 2) * mab * (100 / n_dampers)

        K[mass_on_floor - 1][i] = -kspring
        K[i][i] = kspring

    # creates stiffness matrix
    G = np.zeros((n_dampers + 3, n_dampers + 3), dtype=np.complex)
    G[0][0:3] = [2j, -1j, 0]
    G[1][0:3] = [-1j, 2j, -1j]
    G[2][0:3] = [0, -1j, 1j]
    G[3][0:3] = [0, 0, 0]
    G[mass_on_floor - 1][mass_on_floor - 1] += 1j
    G[mass_on_floor - 1][mass_on_floor - 1] *= n_dampers
    for i in range(3, n_dampers + 3):
        G[i][mass_on_floor - 1] -= 1j
        G[mass_on_floor - 1][i] = -1j
        G[i][i] = 1j
    G = g * G
    # creates damping matrix
    vect = np.zeros((n_dampers + 3, 1))
    vect[0] = 1
    # this is equivalent to a forcing function which provides a unit harmonic input on floor 1
    V, D = (sp.eig(K, M))
    V = np.real(np.sqrt(V))  ##
    print("Natural angular frequencies are: ", V)  # natural frequencies in radians (without damping)
    for i in range(3):  # iterate for each floor
        amplitude = []
        frequencies = np.linspace(0, 130, 1001)
        for f in frequencies:
            B = K + (f * G) - ((f ** 2) * M)
            B_inv = (np.linalg.inv(B))
            amplitude.append((np.absolute(B_inv.dot(vect)[i])))  # this provides the y vector for each floor
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
