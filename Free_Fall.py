#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 22:03:27 2017

@author: daniel
"""

from numpy import*
import numpy as np
import scipy.constants as const
import ODE.General_ODE as Solve
import matplotlib.pyplot as plt

k = 1.
m = 1.
g = const.g

H = 10.
vt = np.sqrt(m * g / k)
IC = Solve.IC([H], [0.])

T = (m / (k*vt)) * np.arccosh(np.exp(H*k/m))

def F(t, X):
    return (k/m) * (X[1])**2 - g

Solve.IC_ODE(2, [F], 0., T, IC, 'v1')

def z(t):
    return H - (m/k) * np.log(np.cosh(k * vt * t/m))

def vz(t):
    return -vt * np.tanh((k*vt/m)*t)

t= np.linspace(0., T, 10)

Z = []
VZ = []
for i in range(0, len(t)):
    Z.append(z(t[i]))
    VZ.append(vz(t[i]))

plt.axhline(y = -vt, color = 'red')
plt.plot(t, VZ, 'o')
plt.grid()