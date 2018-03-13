#!/usr/bin/python


import base_module as bm
import numpy
import time

print('\nInitializing the device:\n')

scope= bm.TekScope("/dev/usbtmc0")

scope.printName()

#print("How long do you want to take data (s) (Maximum of 1000 seconds)?")

#data_time = input("\nEnter your desired number of seconds: ")
#answer = int(data_time)


print("Set the settings on the scope")
scope.scope_settings()


print ("Wait until the scope gets all the data points")
scope.scope_run()



print("\nSaving data:")

#scope_data.adjusting()
scope.data_array()
scope.time_scale()
scope.save_data()
#print(" ")
