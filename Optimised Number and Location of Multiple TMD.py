"""
Created on Thu FEb 01 19:01:14 2018

@author: jeevi

This program optimises how many dampers should be placed and on what floor

"""
import numpy as np

# please edit these parameters to set an upper bound on how many dampers
max_damper_val = 10
# parameters of model
m = 1.83
L = 0.2
N = 3
b = 0.08
E = 210 * (10 ** 9)
d = 0.001
I = (b * d * d * d) / 12
k = (24 * E * I) / (L ** 3)
g = 8.77


def optimiser(n_dampers, mass_on_floor):
    max_amp_on_floor = []
    mab = 1 / n_dampers

    M = m * np.identity(n_dampers + 3)
    for i in range(3, n_dampers + 3):
        M[i][i] = 1
    # creating the mass matrix

    K = np.identity(n_dampers + 3)
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
    # creates the stiffness matrix of the system, depends on where the tuned mass damper is placed

    vect = np.zeros((n_dampers + 3, 1))
    vect[0] = 1

    for i in range(3):
        amplitude = []

        frequencies = np.linspace(0, 100, 1000)
        for f in frequencies:
            B = K + (f * G) - ((f ** 2) * M)
            B_inv = (np.linalg.inv(B))
            amplitude.append((np.absolute(B_inv.dot(vect)[i])))
            # creates the steady state output at frequencies ranging from 0 to 100 radians/second
        if (abs(max(amplitude))) > (abs(min(amplitude))):  # prints the largest magnitude of amplitude for each floor
            max_amp_on_floor.append(abs(max(amplitude)))
        else:
            max_amp_on_floor.append(abs(min(amplitude)))
    return max(max_amp_on_floor)


op_floor = 0
op_damper_number = 0
min_value = 100
for damper_number in range(1, max_damper_val, 1):
    for floor in range(1, 4, 1):
        x = optimiser(damper_number, floor)
        if x < min_value:
            min_value = x
            op_floor = floor
            op_damper_number = damper_number
print("Optimised System found")
print("Place the dampers on floor",op_floor)
print(op_damper_number, " is the number of dampers required")
print("Finished")
