# -*- coding: utf-8 -*-
"""
Created on Tue May 02 12:16:09 2017

@author: DChung
"""
from numpy import*
import numpy as np
import General_ODE as Sol
import scipy.constants as const
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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

T = 2*V0[2]/g0 * 10

N = 10000
sol = Sol.IC_ODE(2, F, 0., T, IC_Coriolis, 'self_define', N)



set_speed = 10

x = sol[0][::set_speed]
y = sol[1][::set_speed]
z = sol[2][::set_speed]

fig = plt.figure()
ax = plt.axes(xlim = (min(x), max(x)), ylim=(min(y), max(y)))

star1, = ax.plot([], [], '-b')
starline1, = ax.plot([], [], '--ob')

ax.set_xlim( min(x), max(x) )
ax.set_ylim( min(y), max(y) )

# initialization function: plot the background of each frame (2D)
def init():

    star1.set_data([], [])
    starline1.set_data([], [])
    
    return star1, starline1, 

# Animate 2d
def animate(i):

    X = x[:i]
    Y = y[:i]

    star1.set_data(X, Y)
    starline1.set_data([0, x[i]], [0, y[i]])

    return star1, starline1,



anim = animation.FuncAnimation(fig, animate, init_func=init,
                            frames = N//set_speed, interval= 10, blit=True)

plt.show()