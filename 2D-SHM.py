# -*- coding: utf-8 -*-
"""
Created on Sun Jan 07 16:00:54 2018

@author: DChung
"""

from numpy import*
import numpy as np
import ODE.General_ODE as Solve
from matplotlib import pyplot as plt
from matplotlib import animation



R = 1.
m = 1.
omega = 3.


""" Solve  """
IC = Solve.IC([R, 0], [0, R*omega])


def Fx(t, X):
    return -m* omega**2 *R *np.cos(omega*t)

def Fy(t, X):
    return -m* omega**2 *R *np.sin(omega*t)


sol = Solve.IC_ODE(2, [Fx, Fy], 0., 100., IC, 'self_define')

x = sol[0]
y = sol[1]
t = Solve.IC_ODE(2, [Fx, Fy], 0., 100., IC, 'time')

"""" Animation """

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(min(x), max(x)), ylim=(min(y), max(y)))
#plt.axes().set_aspect('equal')
line, = ax.plot([], [], lw=2)
line1, = ax.plot([], [], 'o--')
line2, = ax.plot([], [], 'o-')
line3, = ax.plot([], [], 'o--')
line4, = ax.plot([], [], '-', color = 'gray')
# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line1.set_data([], [])    
    line2.set_data([], []) 
    line3.set_data([], [])
    line4.set_data([], [])
    return line, line1, line2, line3, line4, 

    
def animate(i):
    X = x[:i]
    Y = y[:i]
    line.set_data(X, Y)
    line1.set_data([0, X[i-1]],[0, Y[i-1]])
    line2.set_data([0, X[i-1]],[0, 0])
    line3.set_data([X[i-1], X[i-1]],[0, Y[i-1]])
    
    Y1 = np.linspace(min(y), max(y), 1000)
    X1 = np.cos(m* omega**2 *Y1 - omega*t[i])
    line4.set_data(X1, Y1)
    return line, line1,line2, line3, line4, 


plt.grid()
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=5000, interval=10, blit=True)

plt.show()
