'''
Created on Jul 28, 2011
@author: KJordy
'''
import pyvisa


class E3631a():
    '''
    vsource = E3631a(gpib=6,setMaxLimit=True)
    
    This class provides access to the E3631A voltage sources.
    Each E3631a has three sources referred to by their string name:
        P6V
        P25V
        N25V
    Raw SCIP commands can be written with "E3631A.write()"
    
    Example Usage:
        vsource = E3631a(gpib=6,setMaxLimit=True)
        vsource.setVoltage('P6V', 5)
        vsource.setVoltage('P25V', 1.8)
        print vsourve.getVoltage('P25V')
    '''
    def __init__(self,gpib=0,setMaxLimit=True):
        '''
        vsource = E3631a(gpib=6,setMaxLimit=True)
        Inputs:
            gpib: (int) gpib address
            reset: (bool) reset on intialization
        '''
        try:
            gpib = 'GPIB::'+str(int(gpib))
        except ValueError:
            pass
        resource_manager = pyvisa.ResourceManager()
        # Instrument.__init__(self,gpib)
        self.instrument = resource_manager.open_resource(gpib)
        
        if setMaxLimit:
            self.setCurrLimit('P6V','max')
            self.setCurrLimit('P25V','max')
            self.setCurrLimit('N25V','max')

    def setVoltage(self,source,voltage):
        '''
        vsrc.setVoltage('P6V',1.8)
        
        Set DC voltage level for source.
        Inputs:
            source: (str)(P6V, P25V, N25V)
            voltage: (float)
        '''
        #Source = P6V, P25V, N25V
        self.instrument.write('INST:SEL ' + source)
        self.instrument.write('CURR MAX')
        #self.instrument.write('MEAS:CURR' + source) # Measure the output current
        self.instrument.write('VOLT ' + str(voltage))
    
    def getVoltage(self,source):
        self.instrument.write('INST:SEL ' + source)
        return float(self.instrument.query('MEAS:VOLT:DC? '))
    
    def getCurrent(self,source):
        self.instrument.write('INST:SEL ' + source)
        return float(self.instrument.query('MEAS:CURR:DC?'))
    
    def setCurrLimit(self,source,limit):
        self.instrument.write('INST:SEL ' + source)
        self.instrument.write('CURR ' + str(limit))

    def outputEnable(self):
        self.instrument.write('OUTP ON')

    def outputDisable(self):
        self.instrument.write('OUTP OFF')
