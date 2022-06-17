import tkinter as tk
from tkinter import END, ttk


class FloatEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(
            validate='key',
            validatecommand=(self.register(self._validate), '%P'),
            invalidcommand=(self.register(self._on_invalid), )
        )
    
    def _validate(self, proposed_value):
        if proposed_value == '':
            return True
        try:
            float(proposed_value)
            return True
        except ValueError:
            return False
    
    def _on_invalid(self):
        self.delete(tk.END)

class IntEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(
            validate='key',
            validatecommand=(self.register(self._validate), '%P'),
            invalidcommand=(self.register(self._on_invalid), )
        )
    
    def _validate(self, proposed_value):
        if proposed_value == '':
            return True
        try:
            int(proposed_value)
            return True
        except ValueError:
            return False
    
    def _on_invalid(self):
        self.delete(tk.END)