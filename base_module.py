import os
import time
import numpy
#from __future__ import print_function 
datetime = time.strftime('%d_%m_%Y_%H_%M_%S')


voltagescale = "2000E-3"
voltagescale2 = "2000E-3"
voltagescalech3 = "2000E-3"
filename = datetime+"scope"


class Instrument:
    
    """ Instrument base class"""

    def __init__(self,device):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

    def write(self,command):
        os.write(self.FILE,command)

    def read(self,length=4000):
        return os.read(self.FILE, length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def printName(self):
        self.name=self.getName()
        print(self.name)

    def sendReset(self):
        self.write("*RST")


####################### Scope Settings ########################

class TekScope(Instrument):
    
    """ Tektronix DPO 2014 class"""

    def scope_settings(self):
        #print("Scope configured for degaussing sequence")
        self.write("TRIG:A:MOD AUTO")
        #self.write("ACQ:STATE RUN")
        self.write("HOR:DEL:MOD OFF")
	#time_scale = float(data_time)/10
	#time_scale_str = str(time_scale)
        #self.write("HOR:SCA "+time_scale_str)
        self.write("HOR:SCA 1")
        self.write("HOR:RECO 100000")
        self.write("HOR:POS 0")
        #self.write("TRIG:A:EDGE:SOU LINE")
	self.write("CH1:SCALe "+voltagescale) 
        self.write("CH2:SCALe "+voltagescale2)
	self.write("CH3:SCALe "+voltagescalech3)

        
    def scope_run(self):
        self.write("ACQ:STATE RUN")
        self.write("DATA:WIDTH 2") # Set data width to 2 for better resolution
        #time.sleep(data_time)
        time.sleep(11)
        self.write("ACQ:STATE STOP") # Stop data acquisition
     

    def read_data( self ):
        self.write( "CURV?" )
        rawdata = self.read(250000)
        return numpy.frombuffer( rawdata, 'i2' )[7:-1]
  
    
    def get_data( self,source ):

        """method to scale data """
       
        
        self.write("DATA:SOURCE " + source)
        self.write("DATA:ENCD SRI") # Set data format to binary, zero is center-frame and big endian
        self.write("WFMI:NR_PT 125000")
        self.write("WFMOUTPRE:RECORDLENGTH?")
        self.write("DATA:START 1")
        self.write("DATA:STOP 125000")
        data = self.read_data()

        print("Got data for "+ source)
        self.write("WFMO:YMUlt?")
        ymult = float(self.read(200))
        self.write("WFMO:YOFF?")
        yoff=float(self.read(200))
        self.write("WFMO:YZERO?")
        yzero = float(self.read(200))
        print("For "+source,ymult,yoff,yzero)
        data = ((data - yoff) * ymult) + yzero
        return data


    """ reading scope"""

    def data_array(self):
         
        self.write("SELECT?")
        self.wfms=self.read(200)
        print(self.wfms)

        # parse into array of characters
        self.wfms = self.wfms.strip().split(";")

        if self.wfms[0]=="1":
            self.ch1data = self.get_data("CH1")

        if self.wfms[1]=="1":
            self.ch2data = self.get_data("CH2")

        if self.wfms[2]=="1":
            self.ch3data = self.get_data("CH3")
      

    def time_scale(self):
         #get the time scale

        self.write("HORIZONTAL:MAIN:SCALE?")
        self.timescale = float(self.read(20))

        # Get the timescale offset
        self.write("HORIZONTAL:MAIN:POSITION?")
        self.timeoffset = float(self.read(20))

        # Get the length of the horizontal record
        self.write("HORIZONTAL:RECORDLENGTH?")
        self.time_size = int(self.read(30))

        self.time = numpy.arange(0,self.timescale*10,self.timescale*10/self.time_size)
        print(self.time)
        self.write("ACQ:STATE RUN")

    def save_data(self):
        print "Ch1:"
        print self.ch1data[10:30]
        print "___________________"
        print "ch2:"
        print self.ch2data[10:30]
        with open(filename+'.txt','w') as thefile:
            for item1,item2,item3,item4 in zip(self.time,self.ch1data,self.ch2data,self.ch3data):
                print>>thefile,item1,item2,item3,item4
                #print '{:07.4f} {:-07.4f} {:-07.4f} {:07.4f}'.format(item1,item2,item3,item4)
                

