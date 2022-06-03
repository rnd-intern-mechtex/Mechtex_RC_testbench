import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from serial.tools.list_ports import comports
from . import views as v
from . import models as m


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()
        self.title('Mechtex RC Testbench')
        
        self.port_list = []
        
        container = ttk.Frame(self)
        container.pack(fill='both', side='top', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)        
        self.frames = {}
        
        # -------------------------------------------------------------------------------
        # Creating all the views
        # -------------------------------------------------------------------------------
        self.frames["setup"] = v.SetupPage(container, self)
        self.frames["manual"] = v.ManualPage(container, self)
        self.frames["auto"] = v.AutomatedPage(container, self)
        
        # -------------------------------------------------------------------------------
        # Configuring all setup view functionalities
        # -------------------------------------------------------------------------------
        self.setup__on_refresh()    # refresh comports on start
        self.frames["setup"].refresh_button.config(command=self.setup__on_refresh)
        self.frames["setup"].source_button.config(command=self.setup__on_browse_src)
        self.frames["setup"].destination_button.config(command=self.setup__on_browse_dest)
        self.frames["setup"].button_save.config(command=self.setup__on_save)
        self.frames["setup"].button_auto.config(
            state=tk.DISABLED,
            command=self.setup__on_auto
        )
        self.frames["setup"].button_manual.config(
            state=tk.DISABLED,
            command=self.setup__on_manual
        )
        
        # -------------------------------------------------------------------------------
        # Configuring all manual view functionalities
        # -------------------------------------------------------------------------------
        self.current_slider_voltage = tk.DoubleVar()
        self.current_slider_pwm = tk.DoubleVar()
        self.current_entry_voltage = tk.DoubleVar()
        self.current_entry_pwm = tk.DoubleVar()
        self.old_voltage = 0.0
        self.old_pwm = 1000
        self.current_slider_voltage.set(0)
        self.current_slider_pwm.set(1000)
        for widget in self.frames["manual"].pwm_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        for widget in self.frames["manual"].voltage_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        self.frames["manual"].stop_button.config(
            command=self.manual__on_stop,
            state=tk.DISABLED
        )
        self.frames["manual"].back_button.config(command=self.manual__on_back)
        self.frames["manual"].start_button.config(command=self.manual__on_start)
        self.frames["manual"].voltage_slider.config(
            variable=self.current_slider_voltage,
            command=self.manual__v_slider_changed
        )
        self.frames["manual"].pwm_slider.config(
            variable=self.current_slider_pwm,
            command=self.manual__p_slider_changed
        )
        # Binding functions with events
        self.frames["manual"].voltage_entry.config(textvariable=self.current_entry_voltage)
        self.frames["manual"].pwm_entry.config(textvariable=self.current_entry_pwm)
        self.frames["manual"].voltage_button.bind('<Return>', self.manual__on_volt_set)
        self.frames["manual"].voltage_button.bind('<Button-1>', self.manual__on_volt_set)
        self.frames["manual"].pwm_button.bind('<Return>', self.manual__on_pwm_set)
        self.frames["manual"].pwm_button.bind('<Button-1>', self.manual__on_pwm_set)
        self.frames["manual"].voltage_entry.bind('<Return>', self.manual__on_volt_set)
        self.frames["manual"].pwm_entry.bind('<Return>', self.manual__on_pwm_set)
        
        # -------------------------------------------------------------------------------
        # Configuring all auto view functionalities
        # -------------------------------------------------------------------------------
        self.frames["auto"].stop_button.config(
            command=self.auto__on_stop,
            state=tk.DISABLED
        )
        self.frames["auto"].start_button.config(command=self.auto__on_start)
        self.frames["auto"].back_button.config(command=self.auto__on_back)
        
        # -------------------------------------------------------------------------------
        # Adding all frames to the grid and finally displaying Setup Frame
        # -------------------------------------------------------------------------------
        self.deiconify()
        self.frames["setup"].grid(row=0, column=0, sticky=tk.NSEW)
        self.frames["manual"].grid(row=0, column=0, sticky=tk.NSEW)
        self.frames["auto"].grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame("setup")
        
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    # -------------------------------------------------------------------------------
    # Functions for setup view widgets
    # -------------------------------------------------------------------------------
    def setup__on_refresh(self):
        self.port_list = [port.device for port in comports()]
        self.frames["setup"].supply_port.set('')
        self.frames["setup"].arduino_port.set('')
        self.frames["setup"].supply_port_menu['menu'].delete(0, 'end')
        self.frames["setup"].arduino_port_menu['menu'].delete(0, 'end')
        for choice in self.port_list:
            self.frames["setup"].supply_port_menu['menu'].add_command(
                label=choice,
                command=tk._setit(self.frames["setup"].supply_port, choice)
            )
            self.frames["setup"].arduino_port_menu['menu'].add_command(
                label=choice,
                command=tk._setit(self.frames["setup"].arduino_port, choice)
            )
        pass
        
    
    def setup__on_browse_src(self):
        self.frames["setup"].source_filename.set(fd.askopenfilename())
    
    def setup__on_browse_dest(self):
        self.frames["setup"].destination_folder.set(fd.askdirectory())

    def setup__on_save(self):
        # check if all com ports are different
        self.data = self.frames["setup"].getData()
        print(self.data)
        self.frames["setup"].button_auto.config(state=tk.NORMAL)
        self.frames["setup"].button_manual.config(state=tk.NORMAL)
    
    def setup__on_manual(self):
        self.show_frame("manual")
        self.frames["setup"].button_auto.config(state=tk.DISABLED)
        self.frames["setup"].button_manual.config(state=tk.DISABLED)
    
    def setup__on_auto(self):
        self.show_frame("auto")
        self.frames["setup"].button_auto.config(state=tk.DISABLED)
        self.frames["setup"].button_manual.config(state=tk.DISABLED)
    
    # -------------------------------------------------------------------------------
    # Functions for manual view widgets
    # -------------------------------------------------------------------------------
    def manual__on_start(self):
        
        # Open power supply port
        self.supply = m.PowerSupply(self.data['supply_port'])
        # Set OVP, current limit
        self.supply.setVoltage(0)
        self.supply.turnOutputON()
        self.arduino = m.Arduino(self.data['arduino_port'], self.data['num_readings'])
        self.arduino.send_pwm(1000)
        
        # Update GUI
        self.frames["manual"].back_button.config(state=tk.DISABLED)
        for widget in self.frames["manual"].pwm_frame.winfo_children():
            widget.config(state=tk.NORMAL)
        for widget in self.frames["manual"].voltage_frame.winfo_children():
            widget.config(state=tk.NORMAL)
        self.frames["manual"].stop_button.config(state=tk.NORMAL)
        self.frames["manual"].start_button.config(state=tk.DISABLED)
    
    def manual__on_stop(self):
        self.current_entry_voltage.set(0)
        self.current_slider_voltage.set(0)
        self.current_entry_pwm.set(1000)
        self.current_slider_pwm.set(1000)
        self.supply.setVoltage(0)
        self.supply.close()
        self.arduino.send_pwm(1000)
        self.arduino.close()
        self.frames["manual"].back_button.config(state=tk.NORMAL)
        self.frames["manual"].stop_button.config(state=tk.DISABLED)
        self.frames["manual"].start_button.config(state=tk.NORMAL)
        for widget in self.frames["manual"].pwm_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        for widget in self.frames["manual"].voltage_frame.winfo_children():
            widget.config(state=tk.DISABLED)
    
    def manual__on_back(self):
        self.show_frame("setup")
    
    def manual__v_slider_changed(self, event):
        value = self.current_slider_voltage.get()
        new_value = (value // 2.5) * 2.5
        if value > self.old_voltage:
            new_value += 2.5
        self.old_voltage = new_value
        self.current_slider_voltage.set(new_value)
        self.current_entry_voltage.set(new_value)
        self.supply.setVoltage(new_value)
        self.frames["manual"].voltage_slider.focus()
    
    def manual__p_slider_changed(self, event):
        value  = self.current_slider_pwm.get()
        new_value = (value // 50) * 50
        if value > self.old_pwm:
            new_value += 50
        self.old_pwm = new_value
        self.current_slider_pwm.set(new_value)
        self.current_entry_pwm.set(new_value)
        # !!! Send PWM to Arduino here !!!
        self.arduino.send_pwm(new_value)
        self.frames["manual"].pwm_slider.focus()
    
    def manual__on_pwm_set(self, event):
        value = self.current_entry_pwm.get()
        if value < 1000 or value > 2000:
            # ignore
            self.current_entry_pwm.set(self.current_slider_pwm.get())
            return
        self.current_slider_pwm.set(value)
        self.old_pwm = value
        # !!! Send PWM to Arduino Here !!!
        self.arduino.send_pwm(value)
    
    def manual__on_volt_set(self, event):
        value = self.current_entry_voltage.get()
        if value < 0 or value > 80:
            # ignore
            self.current_entry_voltage.set(self.current_slider_voltage.get())
            return
        self.current_slider_voltage.set(value)
        self.old_voltage = value
        self.supply.setVoltage(value)
        
        
    # -------------------------------------------------------------------------------
    # Functions for auto widgets
    # -------------------------------------------------------------------------------
    
    def auto__on_start(self):
        self.frames["auto"].stop_button.config(state=tk.NORMAL)
        self.frames["auto"].start_button.config(state=tk.DISABLED)
        self.frames["auto"].back_button.config(state=tk.DISABLED)
    
    def auto__on_stop(self):
        self.frames["auto"].back_button.config(state=tk.NORMAL)
        self.frames["auto"].stop_button.config(state=tk.DISABLED)
        self.frames["auto"].start_button.config(state=tk.NORMAL)
    
    def auto__on_back(self):
        self.show_frame("setup")