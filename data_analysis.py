#!/usr/local/bin/python
from ctypes import *
import numpy

avlib = cdll.LoadLibrary( "libav.so" )
avlib.allan_deviation.restype = c_double



import datetime
import matplotlib.pyplot as plt
from statistics import mean
from operator import truediv #for diving lists
from matplotlib.legend_handler import HandlerLine2D #for using legend
import math


def B (X):
    return[x*7 for x in zip(X) ]
   


    
data_file=open('20_01_2017_10_39_14scope.txt' , 'r')


Time=[]
ch1=[] # the z axis of the fluxgate
ch1p=[]
ch2=[] # the y axis of the fluxgate
ch2p=[]
ch3=[] # the x axis of the fluxgate
ch3p=[]

i=0
#N=51815  #number of data points
N=i



gainx=1000
gainy=1000
gainz=500


for line in data_file:
    line_data=line.split(' ')        
    Time.append(line_data[0])
    ch1.append(float(line_data[1])*7/gainz)
    ch2.append(float(line_data[2])*7/gainy)
    ch3.append(float(line_data[3])*7/gainx)
    i+=1

    


Bz=[]
By=[]
Bx=[]



#Bz=B(ch1)
#By=B(ch2)
#Bx=B(ch3)


print ch1




Bzdev = (c_double*(len(ch1)/2-1))()
Bydev = (c_double*(len(ch2)/2-1))()
Bxdev = (c_double*(len(ch3)/2-1))()

CBZ = (c_double*len(ch1))(*ch1)
CBY = (c_double*len(ch2))(*ch2)
CBX = (c_double*len(ch3))(*ch3)



avlib.allan_deviation( CBZ, len(ch1), Bzdev )
avlib.allan_deviation( CBY, len(ch2), Bydev )
avlib.allan_deviation( CBX, len(ch3), Bxdev )



#Zdev = (c_double*(len(ch1)/2-1))()
#Ydev = (c_double*(len(ch2)/2-1))()
#Xdev = (c_double*(len(ch3)/2-1))()

#CZ = (c_double*len(ch1))(*ch1)
#CY = (c_double*len(ch2))(*ch2)
#CX = (c_double*len(ch3))(*ch3)


#avlib.allan_deviation( CZ, len(ch1), Zdev )
#avlib.allan_deviation( CY, len(ch2), Ydev )
#avlib.allan_deviation( CX, len(ch3), Xdev )


plt.figure()
plt.plot(Bzdev,'k')
plt.title(r'Allan Deviation of B$_{z}$')
plt.xlabel('Time (s)')
plt.ylabel(r'Allan deviation of B$_{z}$ ($\mu$ T)')
plt.xscale('log')
plt.yscale('log')

plt.figure()
plt.plot(Bydev,'k')
plt.title(r'Allan Deviation of B$_{y}$')
plt.xlabel('Time (s)')
plt.ylabel(r'Allan deviation of Bmeas$_{y}$ ($\mu$ T)')
plt.xscale('log')
plt.yscale('log')



plt.figure()
plt.plot(Bxdev,'k')
plt.title(r'Allan Deviation of B$_{x}$')
plt.xlabel('Time (s)')
plt.ylabel(r'Allan deviation of Bmeas$_{x}$ ($\mu$ T)')
plt.xscale('log')
plt.yscale('log')
