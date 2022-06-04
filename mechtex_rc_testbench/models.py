import serial
import time

class Model:
    pass

class PowerSupply(serial.Serial):
    def __init__(self, comPort):
        super().__init__(comPort)
        self.baudrate = 9600
        self.parity = 'N'
        self.bytesize = 8
        self.stopbits = 1
        
        self.rst()
        time.sleep(0.05)
    
    def rst(self):
        self.write(b'*RST')
        time.sleep(0.05)

    def getID(self):
        self.write(b'*IDN?')
        return self._getResponse()
    
    def checkMode(self):
        self.write(b'SYST:LOCK:OWN?')
        return self._getResponse()
    
    # Output control commands
    def turnOutputON(self):
        self.write(b'OUTP ON')
        time.sleep(0.05)

    def turnOutputOFF(self):
        self.write(b'OUTP OFF')
        time.sleep(0.05)
    
    def checkOutput(self):
        self.write(b'OUTP?')
        return self._getResponse()

    # Setting and getting OVP
    def setOVP(self, value):
        setCommand = f'SOUR:VOLT:PROT {value}'
        self.write(bytes(setCommand, encoding='ascii'))
        time.sleep(0.05)
    
    def getOVP(self):
        self.write(b'SOUR:VOLT:PROT?')
        return self._getResponse()
    
    # voltage commands
    def setVoltage(self, value):
        setCommand = f'VOLT {value}'
        self.write(bytes(setCommand, encoding='ASCII'))
        time.sleep(0.05)

    def getVoltage(self):
        # returns only the set voltage, not actual voltage
        self.write(b'VOLT?')
        return self._getResponse()
    
    def getActualVoltage(self):
        # returns the actual voltage
        self.write(b'MEAS:VOLT?')
        return self._getResponse()
    
    # current commands
    def setCurrentLimit(self, value):
        setCommand = f'CURR {value}'
        self.write(bytes(setCommand, encoding='ASCII'))
        time.sleep(0.05)
    
    def getCurrentLimit(self):
        self.write(b'CURR?')
        return self._getResponse()
    
    def getActualCurrent(self):
        self.write(b'MEAS:CURR?')
        return self._getResponse()
    
    # Private methods
    def _getResponse(self):
        received_message = b''
        time.sleep(0.05)
        while self.inWaiting():
            received_message += self.read()
        return received_message.decode('ASCII')



class Arduino(serial.Serial):
    def __init__(self, comPort, avgValue):
        super().__init__(comPort)
        self.baudrate = 9600
        self.stopbits = 1
        self.bytesize = 8
        self.parity = 'N'
        self.averaging_value = avgValue
        time.sleep(3)
        
        self.rpm = None
        self.pwm = None
        self.thrust = None
        
        self.send_avgValue()
    
    def send_avgValue(self):
        self.write(bytes(f'A{self.averaging_value}\n', encoding='ASCII'))
    
    def send_pwm(self, pwm_value):
        self.write(bytes(f'P{pwm_value}\n', encoding='ASCII'))
    
    def getSensorValues(self):
        self.reset_input_buffer()
        while self.read() != bytes('\n', encoding='ascii'):
            pass
        sensor_value = self.readline().decode('utf-8')
        if sensor_value[0] == 'P':
            self.pwm = sensor_value[1:-2]
            self.thrust = self.readline()[1:-2]
            self.rpm = self.readline()[1:-2]
        elif sensor_value[0] == 'T':
            self.thrust = sensor_value[1:-2]
            self.rpm = self.readline()[1:-2]
            self.pwm = self.readline()[1:-2]
        elif sensor_value[0] == 'R':
            self.rpm = sensor_value[1:-2]
            self.pwm = self.readline()[1:-2]
            self.thrust = self.readline()[1:-2]


# supply = PowerSupply('COM11')
# supply.setVoltage(10.00)
# supply.setCurrentLimit(5.00)
# time.sleep(3)
# print(supply.getCurrentLimit())
# print(supply.getActualCurrent())