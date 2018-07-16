#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Mariusz
#
# Created:     04-05-2016
# Copyright:   (JP)
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#_______Wykresy bez sumy___________#
import cmath
import pylab
from math import sin, cos, exp, pi, sqrt, fabs
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

e0 = 8.854 * 10**(-12)
u0 = 1.257 * 10**(-6)
n0 = 376.7
c0 = 299792458

#------------------------------
#-----Przenikalnosc teflonu----
et = 19 * 10 **(-12)
ut = 1.257* 10 **(-6)

#------------------------------

dz = dx = dy = 0.05
dt = 0.01*dx/c0  #tak ma byc z warunku stabilnosci, im mniejsza liczba, tym wolniej rosnie do nieskonczonosci, ale tez dlugo leci.

Nz = 100
Nx = Ny = 100

#---------------Macierze przenikalnosci--------------

CH=np. zeros((Nx, Ny, Nz))                       #dt/(dx*u0)  # tak bylo w pdf
CE=np. zeros((Nx, Ny, Nz))                       #dt/(dx*e0)

for i in range(Nz):
    for j in range (Nx):
        for k in range(Ny):
                CE[j,k,i]=dt/(dx*e0)
                CH[j,k,i]=dt/(dx*u0)


#--------Umieszczenie teflonu wewnatrz falowodu------
a=65

for i in range(a, Nz):
    for j in range (Ny):
        for k in range(Nx):
                CE[k,j,i]=(dt/(dx*et))
                CH[k,j,i]=(dt/(dx*ut))

#--------Macierze pol-----------------------------
Hx = np.zeros((Nx, Ny, Nz))
Hy = np.zeros((Nx, Ny, Nz))
Hz = np.zeros((Nx, Ny, Nz))

Ex = np.zeros((Nx, Ny, Nz))
Ey = np.zeros((Nx, Ny, Nz))
Ez = np.zeros((Nx, Ny, Nz))


# Macierze dla Hy rzutowane na XZ
Hxz = np.zeros((Nx,Nz))




for j in range (1000):
#-----------------------------------------------------POLE H--------------------------------------------------------
    for xi in range(1, Nx-1):
        for yi in range(1, Ny-1):
            for zi in range(1, Nz-1):
                Hx[xi,yi,zi] = Hx[xi,yi,zi] + CH[xi,yi,zi]*((Ey[xi,yi,zi+1]-Ey[xi,yi,zi])/dz-(Ez[xi,yi+1,zi]-Ez[xi,yi,zi])/dy)
                Hy[xi,yi,zi] = Hy[xi,yi,zi] + CH[xi,yi,zi]*((Ez[xi+1,yi,zi]-Ez[xi,yi,zi])/dx-(Ex[xi,yi,zi+1]-Ex[xi,yi,zi])/dz)
                Hz[xi,yi,zi] = Hz[xi,yi,zi] + CH[xi,yi,zi]*((Ex[xi,yi+1,zi]-Ex[xi,yi,zi])/dy-(Ey[xi+1,yi,zi]-Ey[xi,yi,zi])/dx)
#-------------------------------------------------------------------------------------------------------------------


    # Tworzenie macierzy Hy0 dla kazdego punktu XZ I para
    for xii in range (1, Nx):
        for zii in range(1, Nz):
            Hxz[xii,zii]=Hy[xii, Ny/2-5, zii]


#-----------------------------------------------------POLE E--------------------------------------------------------
    for xi in range(1, Nx-1):
        for yi in range(1, Ny-1):
            for zi in range(1, Nz-1):
                Ex[xi,yi,zi] = Ex[xi,yi,zi] + CE[xi,yi,zi]*((Hz[xi,yi,zi]-Hz[xi,yi-1,zi])/dy-(Hy[xi,yi,zi]-Hy[xi,yi,zi-1])/dz)
                Ey[xi,yi,zi] = Ey[xi,yi,zi] + CE[xi,yi,zi]*((Hx[xi,yi,zi]-Hx[xi,yi,zi-1])/dz-(Hz[xi,yi,zi]-Hz[xi-1,yi,zi])/dx)
                Ez[xi,yi,zi] = Ez[xi,yi,zi] + CE[xi,yi,zi]*((Hy[xi,yi,zi]-Hy[xi-1,yi,zi])/dx-(Hx[xi,yi,zi]-Hx[xi,yi-1,zi])/dy)
#-------------------------------------------------------------------------------------------------------------------

    # Generowanie fali E w kierunku X
    if j < 350:
        Ez[Nx/2, Ny/2, Nz/2]=Ez[Nx/2, Ny/2, Nz/2]+np.sin(270*10**9*2*pi*j*dt)
#-------------------------------------------------------------------------------------------------------------------


#-----------Tworzenie wykresow--------------------------------------------------------------------------------------
    a = plt.subplot(111, projection='3d')
    plt.title('t= %e [s] \n Pole Hy na XZ'%(j*dt))
    Y, Z = np.meshgrid(range(Ny-2), range(Nz))
    a.plot_surface(Y, Z, Hxz[Y, Z],  rstride=1, cstride=1,
    cmap=plt.cm.gist_heat_r, linewidth=0, antialiased=False)


    plt.savefig("%s.png"%(j))
