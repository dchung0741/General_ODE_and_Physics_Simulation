# -*- coding: utf-8 -*-
"""
Created on Tue May 02 12:16:09 2017

@author: DChung
"""
from numpy import*
import numpy as np
import pyAnimate as Ani
import General_ODE as Sol
import scipy.constants as const

#Constants
g0 = const.g
g = [0., 0., -g0]

Lambda = np.radians(30.) #Latitude

omega = 10
Omega = [omega*cos(Lambda), 0, omega*sin(Lambda)]

g_x_omega = np.cross(g, Omega)

# Initial Conditions
x0 = 0.
y0 = 0.
z0 = 0.
R0 = [x0, y0, z0]

v0 = 10.
alpha = np.radians(30.)
V0 = [v0*cos(alpha), 0., v0*sin(alpha)]
V0_x_omega = np.cross(V0, Omega)

IC_Coriolis = Sol.IC(R0, V0)

#Define forces
# x = X[0], y = X[1], Z = X[2]
# vy = X[3], vy = X[4], vz = X[5]

def Fx(t,X):
    return g[0] + 2*t * g_x_omega[0] + 2 * V0_x_omega[0]

def Fy(t,X):
    return g[1] + 2*t * g_x_omega[1] + 2 * V0_x_omega[1]

def Fz(t,X):
    return g[2] + 2*t * g_x_omega[2] + 2 * V0_x_omega[2]

F = [Fx, Fy, Fz]

T = 2*V0[2]/g0


sol = Sol.IC_ODE(2, F, 0., T, IC_Coriolis, 'self_define')
#Sol.BC_ODE(2, F, 0., T, [[0., None],[0., None],[0., None]],[[V0[0]*T, None],[0., None],[0.,None]], 'self_define')

#ani = Ani.animate()
#ani.setX(sol[0])
#ani.setY(sol[1])
#ani.setZ(sol[3])
#ani.setSpeed(5)
#ani.show2d()
p1 = Ani.dataSet(sol[0], sol[1], sol[2])
f1 = Ani.figure(p1)
Animate(p1)