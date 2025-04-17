# Copyright (c) [2025] [Yifu Ding]
# This file is not used
import time
import tkinter as tk

class NumericInput:
    def __init__(self, parent, monitor_callback):
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.on_input_change)

        self.entry = tk.Entry(parent, textvariable=self.input_var, validate="key")
        self.entry['validatecommand'] = (self.entry.register(self.validate_input), '%P')
        self.entry.pack(padx=10, pady=5)

        self.last_change_time = time.time()
        self.value_to_print = None
        self.monitor_callback = monitor_callback

    def validate_input(self, new_value):
        # Allow empty string or numeric input only
        return new_value == "" or new_value.isdigit()

    def on_input_change(self, *args):
        self.last_change_time = time.time()
        self.value_to_print = self.input_var.get()
        self.monitor_callback(self)
