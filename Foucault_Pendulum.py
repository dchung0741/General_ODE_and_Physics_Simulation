# -*- coding: utf-8 -*-
"""
Created on Sun May 07 15:15:04 2017

@author: DChung
"""
from numpy import*
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import General_ODE as Solve
import Animate as Ani

m = 10.
l = 1.
g = const.g
omega = 10.**2
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
sol = Solve.IC_ODE(2, F_Foucault, 0., 100.*T, IC_Foucault, 'self_define', 100000.)


a = Ani.animate()
a.setX(sol[0])
a.setY(sol[1])
#a.setZ(sol[2])
a.setSpeed(100)
a.show2d()
