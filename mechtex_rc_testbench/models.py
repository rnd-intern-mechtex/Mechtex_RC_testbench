import csv
import os
import serial
import time

class Model:
    def __init__(self, src_file, dest_file, supply, arduino):
        self.source_file = src_file
        self.dest_file = dest_file
        self.arduino = arduino
        self.supply = supply
        
        self.db = {}
        self.db["time(s)"] = None  # ???
        self.db["voltage(V)"] = None
        self.db["pwm"] = None
        self.db["current(A)"] = None
        self.db["rpm"] = None
        self.db["thrust(gf)"] = None
        self.db["power(W)"] = None
        self.db["efficiency"] = None    # ???

        self.old_db = {}
        self.old_db['voltage(V)'] = None
        self.old_db['current(A)'] = None
        self.old_db['power(W)'] = None
        
        self.auto_delay = None
        self.auto_pwm = None

        # list for plotting graphs
        self.time_list = []
        self.current_list = []
        self.power_list = []
        self.thrust_list = []
        self.rpm_list = []
    
    def update_efficiency(self):
        if self.db["thrust(gf)"] is None or self.db["power(W)"] is None:
            self.db['efficiency'] = '-'
            return
        try:
            self.db["efficiency"] = self.db["thrust(gf)"] / self.db["power(W)"]
        except ZeroDivisionError:
            self.db["efficiency"] = '-'
        
    def update_arduino_values(self):
        if self.arduino.isOpen():
            self.arduino.reset_input_buffer()
        self.db['pwm'] = self.arduino.getPwm()
        self.db['thrust(gf)'] = self.arduino.getThrust()
        self.db['rpm'] = self.arduino.getRpm()
        
    def update_supply_values(self):
        if self.supply.isOpen():
            self.supply.reset_input_buffer()
        self.voltage = self.supply.getActualVoltage()
        self.current = self.supply.getActualCurrent()
        self.power = self.supply.getPower()
    
    def append_graph_lists(self):
        self.time_list.append(self.db['time(s)'])
        self.power_list.append(self.db['power(W)'])
        self.current_list.append(self.db['current(A)'])
        self.rpm_list.append(self.db['rpm'])
        self.thrust_list.append(self.db['thrust(gf)'])

        if len(self.time_list) == 50:
            self.time_list = self.time_list[1:]
            self.current_list = self.current_list[1:]
            self.power_list = self.power_list[1:]
            self.thrust_list = self.thrust_list[1:]
            self.rpm_list = self.rpm_list[1:]

    def update_db(self):
        self.update_arduino_values()
        if self.db['pwm'] == 'fail' or self.db['thrust(gf)'] == 'fail' or self.db['rpm'] == 'fail':
            return 'arduino'
        self.update_supply_values()
        if self.voltage == 'fail' or self.current == 'fail' or self.power == 'fail':
            return 'supply'
        try:
            self.db['voltage(V)'] = float(self.voltage[:-3])
            self.old_db['voltage(V)'] = self.db['voltage(V)']
        except ValueError:
            self.db['voltage(V)'] = self.old_db['voltage(V)']
        try:
            self.db['current(A)'] = float(self.current[:-3])
            self.old_db['current(A)'] = self.db['current(A)']
        except ValueError:
            self.db['current(A)'] = self.old_db['current(A)']
        try:
            self.db['power(W)'] = float(self.power[:-3])
            self.old_db['power(W)'] = self.db['power(W)']
        except ValueError:
            self.db['power(W)'] = self.old_db['power(W)']

        self.update_efficiency()
        self.append_graph_lists()
        return False
        
    
    def append_dest_file(self):
        
        newfile = not os.path.exists(self.dest_file)
        with open(self.dest_file, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.db.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(self.db)
    
    def read_input_file(self):
        self.auto_pwm = []
        self.auto_delay = []
        with open(self.source_file, 'r') as fh:
            csvreader = csv.DictReader(fh)
            for col in csvreader:
                self.auto_pwm.append(col['PWM'])
                self.auto_delay.append(col['Delay'])

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
        if self.isOpen():
            try:
                self.write(b'MEAS:VOLT?')
                return self._getResponse()
            except serial.SerialException as e:
                if e.errno == 13:
                    return 'fail'
    
    # current commands
    def setCurrentLimit(self, value):
        setCommand = f'CURR {value}'
        self.write(bytes(setCommand, encoding='ASCII'))
        time.sleep(0.05)
    
    def getCurrentLimit(self):
        self.write(b'CURR?')
        return self._getResponse()
    
    def getActualCurrent(self):
        if self.isOpen():
            try:
                self.write(b'MEAS:CURR?')
                return self._getResponse()
            except serial.SerialException as e:
                if e.errno == 13:
                    return 'fail'
            
    def getPower(self):
        if self.isOpen():
            try:
                self.write(b'MEAS:POW?')
                return self._getResponse()
            except serial.SerialException as e:
                if e.errno == 13:
                    return'fail'
    
    # Private methods
    def _getResponse(self):
        received_message = b''
        time.sleep(0.05)
        while self.inWaiting():
            received_message += self.read()
        return received_message.decode('ASCII')



class Arduino(serial.Serial):
    def __init__(self, comPort):
        super().__init__(comPort)
        self.baudrate = 9600
        self.stopbits = 1
        self.bytesize = 8
        self.parity = 'N'
        
    
    def send_avgValue(self, value):
        try:
            self.write(bytes(f'A{value}\n', encoding='ASCII'))
            return False
        except serial.SerialException as e:
            if e.errno == 13:
                return 'arduino'
    
    def send_pwm(self, pwm_value):
        try:
            self.write(bytes(f'P{pwm_value}\n', encoding='ASCII'))
            return False
        except serial.SerialException as e:
            if e.errno == 13:
                return 'arduino'
    
    def getPwm(self):
        if self.isOpen():
            try:
                self.write(b'X\n')
                response = self.readline().decode('utf-8')
                if response[0] == 'P':
                    return int(response[1:-1])
            except serial.SerialException as e:
                if e.errno == 13:
                    return 'fail'
            
    def getThrust(self):
        if self.isOpen():
            try:
                self.write(b'T\n')
                response = self.readline().decode('utf-8')
                if response[0] == 'T':
                    return float(response[1:-1])
            except serial.SerialException as e:
                if e.errno == 13:
                    return 'fail'

    def getRpm(self):
        if self.isOpen():
            try:
                self.write(b'R\n')
                response = self.readline().decode('utf-8')
                if response[0] == 'R':
                    return int(response[1:-1])
            except serial.SerialException as e:
                if e.errno == 13:
                    return 'fail'