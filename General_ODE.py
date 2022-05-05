# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:41:16 2017

@author: DChung
"""

from numpy import*
import numpy as np
import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d.axes3d as p3
import scipy.special as sp
import scipy.optimize as opt

"""Initial Value ODE"""
"""Construct Initial Condition Array like: [x0,y0,vx0,vy0,ax0,ay0]"""
def IC(*Initial_Condition):
    Total_Initial_Condition = []
    
    for i in range(0,len(Initial_Condition)):
        Total_Initial_Condition += Initial_Condition[i]
    
    return Total_Initial_Condition


"""Solve with RK algorithm"""    
def IC_ODE(order, F, t0, tN, IC, kind, N = 10000.):
    t = linspace(t0,tN,N+1)
    eps = (tN-t0)/N
    Parameters = len(F)
    
    #Solution Matrix: [[x0,...,xN],[y0,...,yN],[vx0,...vxN],[vy0,...,vyN]]
    
    Solutions = zeros((order*Parameters,int(N)+1))
    
    #Initialize
    for i in range(0,shape(Solutions)[0]):
        Solutions[i][0] = IC[i]
    
    #K Matrix
    K = zeros((4,order*Parameters))
    
    #Start recurrence 
    for i in range(1,len(t)): #Fill Solution Matrix Recurrence
        #Start K recurrece
        for j in range(0,4): #K1 -> K2 -> K3 -> K4
            for k in range(0,shape(K)[1]): #Kx1 -> Ky1 -> ... -> Kvx1 -> Kvy1 ... 
                # K1 recurrence (j=0)
                if j == 0:
                    if k < (order-1)*Parameters:
                        K[j][k] = (Solutions[k + Parameters][i-1])*eps
                    else:
                        K[j][k] = F[k-(order-1)*Parameters](t[i-1],\
                        transpose(Solutions)[i-1])*eps
                
                # K2 & K3 recurrence (j=1,2) 
                elif j ==  1 or j == 2:
                    if k < (order-1)*Parameters:
                        K[j][k] = (Solutions[k+Parameters][i-1] + 0.5*K[j-1][k+Parameters])*eps
                    else:
                        K[j][k] = (F[k-(order-1)*Parameters](t[i-1] + 0.5*eps,\
                        transpose(Solutions)[i-1] + 0.5*K[j-1]))*eps
                
                # K4 recurrence (j=3)
                elif j == 3:
                    if k < (order-1)*Parameters: 
                        K[j][k] = (Solutions[k+Parameters][i-1] + K[j-1][k+Parameters])*eps
                    else:
                        K[j][k] = (F[k-(order-1)*Parameters](t[i-1] + eps,
                        transpose(Solutions)[i-1] + K[j-1]))*eps
        
        #Filling the Solution matrix
        for l in range(0,shape(Solutions)[0]):
            Solutions[l][i] = Solutions[l][i-1] +\
            (transpose(K)[l][0] + 2.*transpose(K)[l][1] + 2.*transpose(K)[l][2] + transpose(K)[l][3])/6.
#============================== Do not change anything obove this line!!! =================================
    # Plot the Result
    if kind == '3d' or kind == '3D':
        plt.figure()
        plt.axes(projection='3d')
        plt.plot(Solutions[0],Solutions[1],Solutions[2])
        
    elif kind[:-3] == '2d': #Side view
        if kind[3:] == 'xy' or kind[3:] == 'yx':
            plt.plot(Solutions[0],Solutions[1])
        
        elif kind[3:] == 'yz' or kind[3:] == 'zy':
            plt.plot(Solutions[1],Solutions[2])
        
        elif kind[3:] == 'xz' or kind[3:] == 'zx':
            plt.plot(Solutions[0],Solutions[2])    
    
    elif kind[:-1] == 'x' and int(kind[-1:]) <= len(F):
        plt.plot(t,Solutions[int(kind[-1:])-1])
    
    elif kind[:-1] == 'v':
        plt.plot(t,Solutions[int(kind[-1:])-1 + len(F)])
    
    # elif kind[:-2] == 'PhaseSpace':
    #     plt.plot(Solutions[int(kind[-1:])-1],Solutions[int(kind[-1:])-1+len(Forces)])
    
    elif kind == 'polar':
        plt.plot(Solutions[0]*cos(Solutions[1]),Solutions[0]*sin(Solutions[1]))
    
    elif kind == 'self_define':
        return Solutions
    
    elif kind == 'time':
        return t



"""Shooting Method for Boundary Condition ODE"""
# Consider 2 coupled 3rd order ODE
# x''' = fx(t, x, x', x'', y, y', y'')
# y''' = fy(t, x, x', x'', y, y', y'')

# x[t0] = x0, x'[tN] = x'N, x''[t0] = x''0
# y[tN] = yN, y'[t0] = y'0, y''[tN] = y''N

# left = [[x0, None, x''0], [None, y'0, None]]
# right = [[None, x'N, None], [yN, None, y''N]]

# trial_IC = [x0, y0_try, x'0_try, y'0, x''0, y''0_try]


def BC_ODE(order, F, t0, tN, left, right, kind):    
    parameters = len(F)
    
    known_IC = []
    UIP = []  # Unknown Initial Value Position in IC space
    count = 0
    for i in range(0, order):
        for j in range(0, parameters):
            count += 1
            
            if left[j][i] != None:
                known_IC.append(left[j][i])
            
            else:
                UIP.append(count - 1)
    
    known_FC = []
    KFP = []  # Known Final Value Position in IC space
    count2 = 0
    for i in range(0, order):
       for j in range(0, parameters):
           count2 += 1
           
           if right[j][i] != None:
               known_FC.append(right[j][i])
               KFP.append(count2 - 1)
    
    known_FC = np.array(known_FC)
    
    
    def Trial(Try_List):
        initial = []
        for i in range(0, len(known_IC)):
            initial.append(known_IC[i])
        
        for i in range(0, len(UIP)):
            initial.insert(UIP[i], Try_List[i])
        
        trial = IC_ODE(order, F, t0, tN, initial, 'self_define', 10000.)
        
        thetas = []
        for i in range(0, len(UIP)):
            thetas.append(trial[KFP[i]][10000])
        
        thetas = np.array(thetas) - known_FC
        return thetas
    
    
    Guess = np.ones((1, len(UIP)))
    Second_IC = opt.root(Trial, Guess[0]).x
    
    
    #Insert the correct ICs into known_IC
    for i in range(0, len(UIP)):
       known_IC.insert(UIP[i], Second_IC[i])
    
    print (known_IC )
    return IC_ODE(order, F, t0, tN, known_IC, kind)
    


"""Find Eigenstate of a 2nd order coupled system"""
def Find_Eigen(F, show_result = False):
    parameters = len(F)
    X0 = np.zeros((1, parameters))
    X0 = list(X0[0])
    
    
    # Fill the target matrix 
    target = np.zeros((parameters, parameters)) # Find Eigen values of the target matrix
    
    for i in range(0, parameters):
        X0[i] = 1.
        
        for j in range(0, parameters):
            target[i][j] = F[j](0., X0)
        
        X0 = zeros((1, parameters))
        X0 = list(X0[0])
    
    target = np.transpose(-target)
    
    
    # Find Eigen values of the target matrix
    result = sp.linalg.eig(target)
    
    
    # Print a  more friendly form
    Eigen_Value = result[0]
    Eigen_Vector = result[1]
    
    if show_result == True:
        for i in range (0, parameters):
            print ('Eigenvalue:', Eigen_Value[i], ',', 'Eigenvector:', Eigen_Vector[i])
    
    
    # Return a list of Eigen vectors
    Eig_vec_list = []
    for i in range(0, parameters):
        Eig_vec_list.append(list(Eigen_Vector[i]))
    
    
    return Eig_vec_list




