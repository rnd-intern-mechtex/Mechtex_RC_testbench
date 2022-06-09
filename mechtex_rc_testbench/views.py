import tkinter as tk
from tkinter import ttk

class SetupPage(ttk.Frame):
    # !!! Add controller
    def __init__(self, container, controller):
        super().__init__(container)
        
        # required variables
        self.supply_port = tk.StringVar()
        self.arduino_port = tk.StringVar()
        self.numPoles = tk.IntVar()
        self.numReadings = tk.IntVar()
        self.maxV = tk.DoubleVar()
        self.maxI = tk.DoubleVar()
        self.maxT = tk.DoubleVar()
        self.maxN = tk.DoubleVar()
        self.source_filename = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.destination_filename = tk.StringVar()
        
        # configuring rows and columns for frames
        self.grid_rowconfigure([2, 4, 6, 8], weight=2)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(2, weight=2)
        # configuring rows and columns for spacers
        self.grid_rowconfigure([0, 15], weight=3)
        self.grid_columnconfigure([0, 4], weight=3)
        
        # creating frames
        self.param_frame = ttk.LabelFrame(self)
        self.ports_frame = ttk.LabelFrame(self, text='Select COM Ports')
        self.safety_frame = ttk.LabelFrame(self, text='Safety Parameters')
        self.file_frame = ttk.LabelFrame(self, text='Select Files')
        self.start_frame = ttk.Frame(self)
        
        # creating spacers
        self.spacer = [ttk.Label(self, text=' ') for i in range(2)]
        self.spacer[0].grid(row=0, column=0)
        self.spacer[1].grid(row=15, column=4)
        
        # -------------------------------------------------------------------------------
        # creating param_frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.param_frame.grid_rowconfigure([0], weight=1)
        self.param_frame.grid_columnconfigure([0, 1], weight=1)
        # creating inner frames
        self.param_inner_fr = [ttk.Frame(self.param_frame) for i in range(2)]
        ttk.Label(self.param_inner_fr[0], text='Number of Poles: ').grid(
            row=0, column=0, padx=2, pady=2
        )
        ttk.Label(self.param_inner_fr[1], text='Number of Readings: ').grid(
            row=0, column=0, padx=2, pady=2
        )
        self.numPoles_entry = ttk.Entry(self.param_inner_fr[0], width=15, textvariable=self.numPoles)
        self.numPoles_entry.grid(row=0, column=1, padx=2, pady=2)
        self.numReadings_entry = ttk.Entry(self.param_inner_fr[1], width=15, textvariable=self.numReadings)
        self.numReadings_entry.grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self.param_inner_fr[1], text='(for averaging)').grid(row=1, column=0)
        self.param_inner_fr[0].grid(row=0, column=0, padx=2, pady=2)
        self.param_inner_fr[1].grid(row=0, column=1, padx=2, pady=2)
        
        # -------------------------------------------------------------------------------
        # Creating Ports Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.ports_frame.grid_rowconfigure([0, 1, 2, 3], weight=1)
        self.ports_frame.grid_columnconfigure([0, 1], weight=1)
        
        ttk.Label(self.ports_frame, text='Power Supply').grid(row=1, column=0, padx=2, pady=2)
        ttk.Label(self.ports_frame, text='Arduino').grid(row=2, column=0, padx=2, pady=2)
        
        self.supply_port_menu = ttk.OptionMenu(self.ports_frame, self.supply_port)
        self.supply_port_menu.grid(row=1, column=1, padx=2, pady=2)
        self.arduino_port_menu = ttk.OptionMenu(self.ports_frame, self.arduino_port)
        self.arduino_port_menu.grid(row=2, column=1, padx=2, pady=2)
        
        self.refresh_button = ttk.Button(self.ports_frame, text='Refresh Ports')
        self.refresh_button.grid(row=3, column=1, pady=2, sticky=tk.E)
        
        # -------------------------------------------------------------------------------
        # Creating Safety Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.safety_frame.grid_rowconfigure([0, 1], weight=1)
        self.safety_frame.grid_columnconfigure([0, 1], weight=1)
        # creating inner frames
        self.safety_inner_fr = [ttk.Frame(self.safety_frame) for i in range(4)]
        ttk.Label(self.safety_inner_fr[0], text='Max Voltage (V): ').grid(
            row=0, column=0, padx=2, pady=2
        )
        ttk.Label(self.safety_inner_fr[1], text='Max Current (mA): ').grid(
            row=0, column=0, padx=2, pady=2
        )
        ttk.Label(self.safety_inner_fr[2], text='Max Thrust (gf): ').grid(
            row=0, column=0, padx=2, pady=2
        )
        ttk.Label(self.safety_inner_fr[3], text='Max Speed (rpm): ').grid(
            row=0, column=0, padx=2, pady=2
        )
        self.maxV_entry = ttk.Entry(self.safety_inner_fr[0], width=20, textvariable=self.maxV)
        self.maxV_entry.grid(row=0, column=1, padx=2, pady=2)
        self.maxI_entry = ttk.Entry(self.safety_inner_fr[1], width=20, textvariable=self.maxI)
        self.maxI_entry.grid(row=0, column=1, padx=2, pady=2)
        self.maxT_entry = ttk.Entry(self.safety_inner_fr[2], width=20, textvariable=self.maxT)
        self.maxT_entry.grid(row=0, column=1, padx=2, pady=2)
        self.maxN_entry = ttk.Entry(self.safety_inner_fr[3], width=20, textvariable=self.maxN)
        self.maxN_entry.grid(row=0, column=1, padx=2, pady=2)
        self.safety_inner_fr[0].grid(row=0, column=0, padx=2, pady=2)
        self.safety_inner_fr[1].grid(row=0, column=1, padx=2, pady=2)
        self.safety_inner_fr[2].grid(row=1, column=0, padx=2, pady=2)
        self.safety_inner_fr[3].grid(row=1, column=1, padx=2, pady=2)
        
        # -------------------------------------------------------------------------------
        # Creating File Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.file_frame.grid_rowconfigure(0, weight=1)
        self.file_frame.grid_columnconfigure([0, 1], weight=1)
        
        self.file_inner_fr = [ttk.Frame(self.file_frame) for i in range(2)]
        
        ttk.Label(self.file_inner_fr[0], text='Select Source File: ').grid(
            row=0, column=0, padx=2, pady=2
        )
        self.source_entry = ttk.Entry(
            self.file_inner_fr[0],
            width=45,
            textvariable=self.source_filename
        )
        self.source_entry.grid(row=1, column=0, padx=2, pady=2)
        self.source_button = ttk.Button(self.file_inner_fr[0], text='Browse')
        self.source_button.grid(row=1, column=1, padx=2, pady=2)
        
        ttk.Label(self.file_inner_fr[1], text='Select Destination Folder: ').grid(
            row=0, column=0, padx=2, pady=2
        )
        self.dest_folder_entry = ttk.Entry(
            self.file_inner_fr[1],
            width=45,
            textvariable=self.destination_folder
        )
        self.dest_folder_entry.grid(row=1, column=0, padx=2, pady=2)
        self.destination_button = ttk.Button(self.file_inner_fr[1], text='Browse')
        self.destination_button.grid(row=1, column=1, padx=2, pady=2)
        
        ttk.Label(self.file_inner_fr[1], text='Enter destination file name: ').grid(
            row=2, column=0, padx=2, pady=2
        )
        self.dest_filename_entry = ttk.Entry(
            self.file_inner_fr[1],
            width=45,
            textvariable=self.destination_filename
        )
        self.dest_filename_entry.grid(row=3, column=0, padx=2, pady=2)
        
        self.file_inner_fr[0].grid(row=0, column=0, padx=15, pady=2)
        self.file_inner_fr[1].grid(row=0, column=1, padx=15, pady=2)
        
        
        # -------------------------------------------------------------------------------
        # Creating Buttons Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.start_frame.grid_rowconfigure(0, weight=1)
        self.start_frame.grid_columnconfigure(0, weight=1)
        
        self.button_save = ttk.Button(self.start_frame, text='Save')
        self.button_save.grid(row=0, column=0, padx=2, pady=2)
        self.button_auto = ttk.Button(self.start_frame, text='Automated Testing')
        self.button_auto.grid(row=0, column=1, padx=2, pady=2)
        self.button_manual = ttk.Button(self.start_frame, text='Manual Testing')
        self.button_manual.grid(row=0, column=2, padx=2, pady=2)
        
        
        
        # -------------------------------------------------------------------------------
        # Placing all frames on grid
        # -------------------------------------------------------------------------------
        self.param_frame.grid(
            row=2,
            column=2,
            padx=2,
            pady=2,
            sticky=tk.NSEW
        )
        self.ports_frame.grid(
            row=4,
            column=2,
            padx=2,
            pady=2,
            sticky=tk.NSEW
        )
        self.safety_frame.grid(
            row=6,
            column=2,
            padx=2,
            pady=2,
            sticky=tk.NSEW
        )
        self.file_frame.grid(
            row=8,
            column=2,
            padx=2,
            pady=2,
            sticky=tk.NSEW
        )
        self.start_frame.grid(
            row=10,
            column=2,
            padx=2,
            pady=2,
            sticky=tk.E
        )
        
    def getData(self):
        data = {}
        data['num_poles'] = self.numPoles.get()
        data['num_readings'] = self.numReadings.get()
        data['supply_port'] = self.supply_port.get()
        data['arduino_port'] = self.arduino_port.get()
        data['max_voltage'] = self.maxV.get()
        data['max_current'] = self.maxI.get()
        data['max_thrust'] = self.maxT.get()
        data['max_rpm'] = self.maxN.get()
        data['source_file'] = self.source_filename.get()
        data['dest_file'] = self.destination_folder.get() + '/' + self.destination_filename.get() 
        
        return data


class ManualPage(ttk.LabelFrame):
    # !!! Add controller
    def __init__(self, container, controller):
        super().__init__(container)
        self.grid_rowconfigure([2, 3], weight=1)
        self.grid_columnconfigure([2, 6], weight=1)
        
        # -------------------------------------------------------------------------------
        # Creating all Manual Frames
        # -------------------------------------------------------------------------------
        self.start_frame = ttk.Frame(self)
        self.pwm_frame = ttk.LabelFrame(self, text='PWM Control')
        self.voltage_frame = ttk.LabelFrame(self, text='Voltage Control')
        self.dashboard = ttk.LabelFrame(self, text='Dashboard')
        # Add info frame???

        # -------------------------------------------------------------------------------
        # Creating PWM Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.pwm_frame.grid_rowconfigure([0, 1], weight=1)
        self.pwm_frame.grid_columnconfigure([0, 1], weight=1)
        self.pwm_slider = ttk.Scale(
            self.pwm_frame,
            length=300,
            from_=1000,
            to=2000,
            value=1000,
            orient='horizontal'
        )
        self.pwm_slider.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=tk.NS)
        self.pwm_entry = ttk.Entry(self.pwm_frame, width=10)
        self.pwm_entry.grid(row=1, column=0, padx=2, pady=2, sticky=tk.E)
        self.pwm_button = ttk.Button(self.pwm_frame, text='Set')
        self.pwm_button.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
        
        # -------------------------------------------------------------------------------
        # Creating Voltage Frame
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.voltage_frame.grid_rowconfigure([0, 1], weight=1)
        self.voltage_frame.grid_columnconfigure([0, 1], weight=1)
        self.voltage_slider = ttk.Scale(
            self.voltage_frame,
            length=300,
            from_=0,
            to=80,
            value=0,
            orient='horizontal'
        )
        self.voltage_slider.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=tk.NS)
        self.voltage_entry = ttk.Entry(self.voltage_frame, width=10)
        self.voltage_entry.grid(row=1, column=0, padx=2, pady=2, sticky=tk.E)
        self.voltage_button = ttk.Button(self.voltage_frame, text='Set')
        self.voltage_button.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
        
        # -------------------------------------------------------------------------------
        # Creating dashboard
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.dashboard.grid_rowconfigure([2, 4, 6, 8, 10, 12], weight=1)
        self.dashboard.grid_columnconfigure([2, 4], weight=1)
        
        ttk.Label(self.dashboard, text='Voltage: ').grid(
            row=2, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='PWM: ').grid(
            row=4, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Current: ').grid(
            row=6, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Thrust: ').grid(
            row=8, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='RPM: ').grid(
            row=10, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Power: ').grid(
            row=12, column=2, padx=2, pady=2
        )
        self.dashboard_values = []
        self.dash_voltage = ttk.Label(self.dashboard, text='')
        self.dash_voltage.grid(row=2, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_voltage)
        self.dash_pwm = ttk.Label(self.dashboard, text='')
        self.dash_pwm.grid(row=4, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_pwm)
        self.dash_current = ttk.Label(self.dashboard, text='')
        self.dash_current.grid(row=6, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_current)
        self.dash_thrust = ttk.Label(self.dashboard, text='')
        self.dash_thrust.grid(row=8, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_thrust)
        self.dash_rpm = ttk.Label(self.dashboard, text='')
        self.dash_rpm.grid(row=10, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_rpm)
        self.dash_power = ttk.Label(self.dashboard, text = '')
        self.dash_power.grid(row=12, column=4, padx=2, pady=2)
        
        
        # -------------------------------------------------------------------------------
        # Creating buttons
        # -------------------------------------------------------------------------------
        self.start_button = ttk.Button(self.start_frame, text='START')
        self.start_button.grid(row=0, column=2, padx=2, pady=2, ipadx=5, ipady=5)
        self.stop_button = ttk.Button(self.start_frame, text='STOP')
        self.stop_button.grid(row=0, column=4, padx=2, pady=2, ipadx=5, ipady=5)
        self.back_button = ttk.Button(self.start_frame, text='BACK TO SETUP')
        self.back_button.grid(row=0, column=6, padx=2, pady=2, ipadx=5, ipady=5)
        
        # -------------------------------------------------------------------------------
        # Adding all manual frames to grid
        # -------------------------------------------------------------------------------
        self.start_frame.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW)
        self.pwm_frame.grid(row=2, column=2, sticky=tk.NSEW)
        self.voltage_frame.grid(row=3, column=2, sticky=tk.NSEW)
        self.dashboard.grid(row=2, column=6, rowspan=2, sticky=tk.NSEW)


class AutomatedPage(ttk.LabelFrame):
    
    def __init__(self, container, controller):
        super().__init__(container)
        
        self.required_voltage = tk.DoubleVar()
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure([2, 4], weight=1)
        
        # -------------------------------------------------------------------------------
        # Creating all auto frames
        # -------------------------------------------------------------------------------
        self.start_frame = ttk.Frame(self)
        self.msg_frame = ttk.LabelFrame(self, text='Info')
        self.dashboard = ttk.LabelFrame(self, text='Dashboard')
        
        # -------------------------------------------------------------------------------
        # Creating buttons
        # -------------------------------------------------------------------------------
        self.voltage_label = ttk.Label(self.start_frame, text='Enter voltage: ')
        self.voltage_label.grid(row=0, column=2, padx=2, pady=2, ipadx=2, ipady=2)
        self.voltage_entry = ttk.Entry(self.start_frame, width=20, textvariable=self.required_voltage)
        self.voltage_entry.grid(row=0, column=3, padx=2, pady=2)
        self.start_button = ttk.Button(self.start_frame, text='START')
        self.start_button.grid(row=0, column=4, padx=2, pady=2, ipadx=5, ipady=5)
        self.stop_button = ttk.Button(self.start_frame, text='STOP')
        self.stop_button.grid(row=0, column=6, padx=2, pady=2, ipadx=5, ipady=5)
        self.back_button = ttk.Button(self.start_frame, text='BACK TO SETUP')
        self.back_button.grid(row=0, column=8, padx=2, pady=2, ipadx=5, ipady=5)
        
        # -------------------------------------------------------------------------------
        # Creating message frame
        # -------------------------------------------------------------------------------
        self.msg_frame.grid_rowconfigure([0, 1], weight=1)
        self.msg_frame.grid_columnconfigure(0, weight=1)
        
        self.pwm_label = ttk.Label(self.msg_frame, text='')
        self.pwm_label.grid(row=0, column=0, padx=2, pady=2)
        self.delay_label = ttk.Label(self.msg_frame, text='')
        self.delay_label.grid(row=1, column=0, padx=2, pady=2)
        # -------------------------------------------------------------------------------
        # Creating dashboard
        # -------------------------------------------------------------------------------
        # configuring rows and columns
        self.dashboard.grid_rowconfigure([2, 4, 6, 8, 10, 12], weight=1)
        self.dashboard.grid_columnconfigure([2, 4], weight=1)
        
        ttk.Label(self.dashboard, text='Voltage: ').grid(
            row=2, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='PWM: ').grid(
            row=4, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Current: ').grid(
            row=6, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Thrust: ').grid(
            row=8, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='RPM: ').grid(
            row=10, column=2, padx=2, pady=2
        )
        ttk.Label(self.dashboard, text='Power: ').grid(
            row=12, column=2, padx=2, pady=2
        )
        self.dashboard_values = []
        self.dash_voltage = ttk.Label(self.dashboard, text='')
        self.dash_voltage.grid(row=2, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_voltage)
        self.dash_pwm = ttk.Label(self.dashboard, text='')
        self.dash_pwm.grid(row=4, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_pwm)
        self.dash_current = ttk.Label(self.dashboard, text='')
        self.dash_current.grid(row=6, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_current)
        self.dash_thrust = ttk.Label(self.dashboard, text='')
        self.dash_thrust.grid(row=8, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_thrust)
        self.dash_rpm = ttk.Label(self.dashboard, text='')
        self.dash_rpm.grid(row=10, column=4, padx=2, pady=2)
        self.dashboard_values.append(self.dash_rpm)
        self.dash_power = ttk.Label(self.dashboard, text = '')
        self.dash_power.grid(row=12, column=4, padx=2, pady=2)
        
        # -------------------------------------------------------------------------------
        # Adding all auto frames to grid
        # -------------------------------------------------------------------------------
        self.start_frame.grid(row=0, column=2, sticky=tk.NSEW)
        self.msg_frame.grid(row=1, column=2, sticky=tk.NSEW)
        self.dashboard.grid(row=1, column=4, sticky=tk.NSEW)
        

class GraphFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
    
        


# if __name__ == '__main__':
    # root = tk.Tk()
    # frame = ManualPage(root)
    # frame.pack(
        # fill='both',
        # expand=True
    # )
    # root.mainloop()