# -*- coding: utf-8 -*-
"""
Created on Sun May 07 15:15:04 2017

@author: DChung
"""
from numpy import*
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.constants as const
import General_ODE as Solve


m = 10.
l = 1.
g = const.g
omega = 10*-1.
latitude = np.radians(30.)
omegaz = omega*sin(latitude)


# x = X[0], Y = X[1], Z = X[2], vx = X[3], vy = X[4], vz = X[5]

alpha = sqrt(g/l)

def Fx(t,X):
    return -alpha**2 * X[0] + 2*omegaz*X[4]

def Fy(t,X):
    return -alpha**2 * X[1] - 2*omegaz*X[3]

def Fz(t,X):
    return 0.
    

F_Foucault = [Fx, Fy, Fz]

# Set up Initial Condition
theta0 = np.radians(1.)
IC_Foucault = Solve.IC([l*sin(theta0), 0., 0.], [0., 0., 0.])

T = 2*pi *sqrt(l/g)
N = 100000
sol = Solve.IC_ODE(2, F_Foucault, 0., 100.*T, IC_Foucault, 'self_define', N = N)


set_speed = 10

x = sol[0][::set_speed]
y = sol[1][::set_speed]
z = sol[2][::set_speed]

fig = plt.figure()
ax = plt.axes(xlim = (min(x), max(x)), ylim=(min(y), max(y)))

star1, = ax.plot([], [], '-b')
starline1, = ax.plot([], [], '--or')

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