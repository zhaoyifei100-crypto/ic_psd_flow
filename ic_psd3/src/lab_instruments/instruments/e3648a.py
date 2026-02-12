'''
Created on 20250117
@author: yfzhao
'''


#from visa import Instrument
import pyvisa



class E3648a():
    '''
    vsource = E3646a(gpib=6,setMaxLimit=True)
    
    This class provides access to the E3646A voltage sources.
    Each E3646a has three sources referred to by their string name:
        OUTP1
        OUTP2        
    Raw SCIP commands can be written with "E3646A.write()"
    
    Example Usage:
        vsource = E3646a(gpib=6,setMaxLimit=True)
        vsource.setVoltage('OUTP1', 5)
        vsource.setVoltage('OUTP2', 1.8)
        print vsourve.getVoltage('OUTP2')
    '''
    def __init__(self,gpib=0,setMaxLimit=True):
        '''
        vsource = E3646a(gpib=6,setMaxLimit=True)
        Inputs:
            gpib: (int) gpib address
            reset: (bool) reset on intialization
        '''
        try:
            gpib = 'GPIB::'+str(int(gpib))
        except ValueError:
            pass
        resource_manager = pyvisa.ResourceManager()
        #Instrument.__init__(self,gpib)
        self.instrument=resource_manager.open_resource(gpib)
        
        if setMaxLimit:
            self.setCurrLimit('OUTP1','max')
            self.setCurrLimit('OUTP2','max')

    def setVoltage(self,source,voltage):
        '''
        vsrc.setVoltage('P6V',1.8)
        
        Set DC voltage level for source.
        Inputs:
            source: (str)(OUT1, OUT2)
            voltage: (float)
        '''
        #Source = P6V, P25V, N25V
        self.instrument.write('INST:SEL ' + source)
        self.instrument.write('CURR MAX')
        self.instrument.write('VOLT ' + str(voltage))
    
    def getVoltage(self,source):
        self.instrument.write('INST:SEL ' + source)
        return float(self.instrument.query('MEAS:VOLT:DC? '))
    
    def getCurrent(self,source):
        self.instrument.write('INST:SEL ' + source)
        return float(self.instrument.query('MEAS:CURR:DC? '))
    
    def setCurrLimit(self,source,limit):
        self.instrument.write('INST:SEL ' + source)
        self.instrument.write('CURR ' + str(limit))
        
    def outputEnable(self):
        self.instrument.write('OUTP ON')

    def outputDisable(self):
        self.instrument.write('OUTP OFF')
        
        
        
