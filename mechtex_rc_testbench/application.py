from threading import Thread
from time import perf_counter, sleep
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from serial.tools.list_ports import comports
from mechtex_rc_testbench.views import AutomatedPage, ManualPage, SetupPage
from mechtex_rc_testbench.models import Arduino, Model, PowerSupply

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()     # hides app until proper init
        self.title('Mechtex RC Testbench')
        
        self.port_list = []
        self._handle = None
        self._auto_handle = None

        # -------------------------------------------------------------------------------
        # Creating the main frame
        # -------------------------------------------------------------------------------
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', side='top', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)        
        
        # -------------------------------------------------------------------------------
        # CREATING ALL VIEWS
        # -------------------------------------------------------------------------------
        self.frames = {}
        self.frames['setup'] = SetupPage(self.container, self)
        self.frames['manual'] = ManualPage(self.container, self)
        self.frames['auto'] = AutomatedPage(self.container, self)

        # -------------------------------------------------------------------------------
        # SETUP VIEW WIDGETS CONFIGURATION
        # -------------------------------------------------------------------------------
        
        self.setup__on_refresh()
        self.frames['setup'].refresh_button.config(command=self.setup__on_refresh)
        self.frames['setup'].source_button.config(command=self.setup__on_browse_src)
        self.frames['setup'].destination_button.config(command=self.setup__on_browse_dest)
        self.frames['setup'].button_save.config(command=self.setup__on_save)
        self.frames['setup'].button_auto.config(command=self.setup__on_auto)
        self.frames['setup'].button_manual.config(command=self.setup__on_manual)

        # -------------------------------------------------------------------------------
        # MANUAL VIEW WIDGETS CONFIGURATION
        # -------------------------------------------------------------------------------
        self.slider_voltage = tk.DoubleVar()
        self.slider_pwm = tk.DoubleVar()
        self.entry_voltage = tk.DoubleVar()
        self.entry_pwm = tk.DoubleVar()

        self.frames['manual'].start_button.config(command=self.manual__on_start)
        self.frames['manual'].stop_button.config(command=self.manual__on_stop)
        self.frames['manual'].back_button.config(command=self.manual__on_back)

        self.frames['manual'].voltage_slider.config(
            variable=self.slider_voltage,
            command=self.manual__v_slider_changed
        )
        self.frames['manual'].pwm_slider.config(
            variable=self.slider_pwm,
            command=self.manual__p_slider_changed
        )
        self.frames['manual'].voltage_entry.config(textvariable=self.entry_voltage)
        self.frames['manual'].voltage_entry.bind('<Return>', self.manual__on_v_set)
        self.frames['manual'].pwm_entry.config(textvariable=self.entry_pwm)
        self.frames['manual'].pwm_entry.bind('<Return>', self.manual__on_p_set)
        self.frames['manual'].voltage_button.bind('<Return>', self.manual__on_v_set)
        self.frames['manual'].voltage_button.bind('<Button-1>', self.manual__on_v_set)
        self.frames['manual'].pwm_button.bind('<Return>', self.manual__on_p_set)
        self.frames['manual'].pwm_button.bind('<Button-1>', self.manual__on_p_set)

        self.manual__init()

        # -------------------------------------------------------------------------------
        # AUTO VIEW WIDGETS CONFIGURATION
        # -------------------------------------------------------------------------------

        self.frames['auto'].start_button.config(command=self.auto__on_start)
        self.frames['auto'].stop_button.config(command=self.auto__on_stop)
        self.frames['auto'].back_button.config(command=self.auto__on_back)

        self.auto__init()

        # -------------------------------------------------------------------------------
        # Adding all frames to the grid and finally displaying Setup Frame
        # -------------------------------------------------------------------------------
        self.frames['setup'].grid(row=0, column=0, sticky=tk.NSEW)
        self.frames['manual'].grid(row=0, column=0, sticky=tk.NSEW)
        self.frames['auto'].grid(row=0, column=0, sticky=tk.NSEW)
        self.current_frame = 'setup'
        self.show_frame(self.current_frame)
        self.deiconify()

    # -------------------------------------------------------------------------------
    # METHODS
    # -------------------------------------------------------------------------------
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Setup
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

    def setup__on_browse_src(self):
        self.frames["setup"].source_filename.set(fd.askopenfilename())
    
    def setup__on_browse_dest(self):
        self.frames["setup"].destination_folder.set(fd.askdirectory())

    def setup__on_save(self):
        # check if all com ports are different
        self.data = self.frames["setup"].getData()
        self.frames["setup"].button_auto.config(state=tk.NORMAL)
        self.frames["setup"].button_manual.config(state=tk.NORMAL)
    
    def setup__on_manual(self):
        self.current_frame = "manual"
        self.show_frame(self.current_frame)
        self.frames["setup"].button_auto.config(state=tk.DISABLED)
        self.frames["setup"].button_manual.config(state=tk.DISABLED)
    
    def setup__on_auto(self):
        self.current_frame = "auto"
        self.show_frame(self.current_frame)
        self.frames["setup"].button_auto.config(state=tk.DISABLED)
        self.frames["setup"].button_manual.config(state=tk.DISABLED)


    # Manual
    def manual__init(self):
        self.old_voltage = 0
        self.old_pwm = 1000
        self.slider_pwm.set(1000)
        self.slider_voltage.set(0)
        self.entry_pwm.set(1000)
        self.entry_voltage.set(0)
        self.frames['manual'].pwm_slider.config(value=1000)
        self.frames['manual'].voltage_slider.config(value=0)

        self.frames['manual'].start_button.config(state=tk.NORMAL)
        self.frames['manual'].back_button.config(state=tk.NORMAL)
        for widget in self.frames['manual'].pwm_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        for widget in self.frames['manual'].voltage_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        self.frames['manual'].stop_button.config(state=tk.DISABLED)
        for val in self.frames["manual"].dashboard_values:
            val.config(text = '-')
    
    def manual__on_start(self):
        
        # Open power supply port, set OVP, current limit
        # turn output ON
        self.supply = PowerSupply(self.data['supply_port'])
        self.supply.setOVP(self.data['max_voltage'])
        self.supply.setCurrentLimit("{0:.3f}".format(self.data["max_current"]/1000))
        self.supply.setVoltage(0)
        self.supply.turnOutputON()
        # Open arduino port
        self.arduino = Arduino(self.data['arduino_port'], self.data['num_readings'])
        self.arduino.send_pwm(1000)
        self.model = Model(self.data['source_file'], self.data['dest_file'], self.supply, self.arduino)

        # Update GUI
        self.frames["manual"].back_button.config(state=tk.DISABLED)
        for widget in self.frames["manual"].pwm_frame.winfo_children():
            widget.config(state=tk.NORMAL)
        for widget in self.frames["manual"].voltage_frame.winfo_children():
            widget.config(state=tk.NORMAL)
        self.frames["manual"].stop_button.config(state=tk.NORMAL)
        self.frames["manual"].start_button.config(state=tk.DISABLED)

        self.start_time = perf_counter()
        self._handle = self.after(1, self.update_GUI)
    
    def manual__on_stop(self):
        self.supply.setVoltage(0)
        self.arduino.send_pwm(1000)
        self.cancel_update()
        self.supply.close()
        self.arduino.close()

        self.manual__init()
    
    def manual__on_back(self):
        self.current_frame = 'setup'
        self.show_frame(self.current_frame)
    
    def manual__v_slider_changed(self, event):
        value = self.slider_voltage.get()
        new_value = (value // 2.5) * 2.5
        if value > self.old_voltage:
            new_value += 2.5
        self.old_voltage = new_value
        self.slider_voltage.set(new_value)
        self.entry_voltage.set(new_value)
        self.supply.setVoltage(new_value)
        self.frames["manual"].voltage_slider.focus()
    
    def manual__p_slider_changed(self, event):
        value  = self.slider_pwm.get()
        new_value = (value // 50) * 50
        if value > self.old_pwm:
            new_value += 50
        self.old_pwm = new_value
        self.slider_pwm.set(new_value)
        self.entry_pwm.set(new_value)
        # !!! Send PWM to Arduino here !!!
        self.arduino.send_pwm(new_value)
        self.frames["manual"].pwm_slider.focus()
    
    def manual__on_p_set(self, event):
        value = self.entry_pwm.get()
        if value < 1000 or value > 2000:
            # ignore
            self.entry_pwm.set(self.slider_pwm.get())
            return
        self.slider_pwm.set(value)
        self.old_pwm = value
        # !!! Send PWM to Arduino Here !!!
        self.arduino.send_pwm(value)
    
    def manual__on_v_set(self, event):
        value = self.entry_voltage.get()
        if value < 0 or value > 80:
            # ignore
            self.entry_voltage.set(self.slider_voltage.get())
            return
        self.slider_voltage.set(value)
        self.old_voltage = value
        self.supply.setVoltage(value)
    
    # Automated
    
    def auto__init(self):
        self.frames["auto"].start_button.config(state=tk.NORMAL)
        self.frames["auto"].back_button.config(state=tk.NORMAL)
        self.frames["auto"].stop_button.config(state=tk.DISABLED)
        
        for val in self.frames["auto"].dashboard_values:
            val.config(text = '-')
    
    def auto__on_start(self):
        # Open power supply ports
        self.supply = PowerSupply(self.data['supply_port'])
        self.supply.setOVP(self.data['max_voltage'])
        self.supply.setCurrentLimit("{0:.3f}".format(self.data["max_current"]/1000))
        self.supply.setVoltage(self.frames['auto'].required_voltage.get())
        self.supply.turnOutputON()
        # Open arduino port
        self.arduino = Arduino(self.data['arduino_port'], self.data['num_readings'])
        self.arduino.send_pwm(1000)
        self.model = Model(self.data['source_file'], self.data['dest_file'], self.supply, self.arduino)
        
        self.frames["auto"].stop_button.config(state=tk.NORMAL)
        self.frames["auto"].start_button.config(state=tk.DISABLED)
        self.frames["auto"].back_button.config(state=tk.DISABLED)
        
        self.model.read_input_file()
        
        self.start_time = perf_counter()
        self._handle = self.after(1, self.update_GUI)
        self._auto_handle = True
        self.auto_thread = Thread(target=self.auto__loop)
        self.auto_thread.start()

    def auto__on_stop(self):
        self._auto_handle = None
        self.cancel_update()
        self.supply.setVoltage(0)
        self.arduino.send_pwm(1000)
        self.supply.close()
        self.arduino.close()
        self.frames[self.current_frame].pwm_label.config(text='')
        self.frames[self.current_frame].delay_label.config(text='')
        self.auto__init()
    
    def auto__on_back(self):
        self.current_frame = 'setup'
        self.show_frame(self.current_frame)
    
    def auto__loop(self):
        for i in range(len(self.model.auto_pwm)):
            if self._auto_handle is not None:
                if i==0:
                    self.frames[self.current_frame].delay_label.config(text='STARTING ...')
                    sleep(8)
                print('Entered autoloop')
                self.arduino.send_pwm(self.model.auto_pwm[i])
                pwm_text = f'PWM value {self.model.auto_pwm[i]} sent'
                delay_text = f'Waiting for {self.model.auto_delay[i]}s'
                self.frames[self.current_frame].pwm_label.config(text=pwm_text)
                self.frames[self.current_frame].delay_label.config(text=delay_text)
                sleep(int(self.model.auto_delay[i]))
            else:
                return

    # Common functions
    def update_GUI(self):
        if self._handle is not None:
            self.update_thread = Thread(target=self.update_db)
            self.update_thread.start()
            self._handle = self.after(200, self.update_GUI)
        return
    
    def cancel_update(self):
        if self._handle is not None:
            self.after_cancel(self._handle)
            self._handle = None

    def update_db(self):
        # !!! Format time to 3 decimal places !!!
        self.model.db["time(s)"] = perf_counter() - self.start_time
        self.model.update_db()
        
        self.frames[self.current_frame].dash_voltage.config(text=self.model.voltage)
        self.frames[self.current_frame].dash_current.config(text=self.model.current)
        self.frames[self.current_frame].dash_pwm.config(text=self.model.db['pwm'])
        self.frames[self.current_frame].dash_rpm.config(text=self.model.db['rpm'])
        self.frames[self.current_frame].dash_thrust.config(text=self.model.db['thrust(gf)'])
        self.frames[self.current_frame].dash_power.config(text=self.model.power)
        #append to file
        self.model.append_dest_file()