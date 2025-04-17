# Copyright (c) [2025] [Yifu Ding]
import time
import tkinter as tk
from tkinter import PhotoImage, ttk
import common_data
from convert_config_list import config_list
from currency_cache import currency_cache

class ConvertComponent(tk.Frame):
    def __init__(self, parent, uuid, component_list):
        super().__init__(parent, highlightbackground="darkgrey", highlightthickness=2)
        self.config_uuid = uuid
        self.component_list = component_list
        self.create_ui()
        self.set_data()
        self.bind_hanlder()
        self.pack(fill="both", expand=True, padx=10, pady=10)

    def create_ui(self):
        self.currency_from_combo = ttk.Combobox(self, values=currency_cache.currency_list, state="readonly", width=5)
        self.currency_from_combo.grid(row=0, column=0, padx=5, pady=5)

        self.pay_period_combo = ttk.Combobox(self, values=common_data.PAY_PERIOD, state="readonly", width=5)
        self.pay_period_combo.grid(row=2, column=0, padx=5, pady=5)

        self.input_amount_str = tk.StringVar(value="0")
        self.entry = tk.Entry(self, textvariable=self.input_amount_str, width=8, justify=tk.RIGHT, validate="key")
        self.entry.grid(row=2, column=1, padx=5, pady=5)
        self.last_change_time = time.time()
        self.input_amount_saved = True;


        label2 = tk.Label(self, text="=>", anchor="center", justify=tk.CENTER, width=8)
        label2.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.currency_to_combo = ttk.Combobox(self, values=currency_cache.currency_list, state="readonly", width=5)
        self.currency_to_combo.grid(row=0, column=2, padx=5, pady=5)

        self.result_hourly_label = tk.Label(self, text=common_data.PAY_PERIOD[0], anchor="w", justify=tk.LEFT, width=8)
        self.result_hourly_label.grid(row=1, column=2, padx=5, pady=5, sticky="n")

        self.result_monthly_label = tk.Label(self, text=common_data.PAY_PERIOD[1], anchor="w", justify=tk.LEFT, width=8)
        self.result_monthly_label.grid(row=2, column=2, padx=5, pady=5, sticky="n")

        self.result_yearly_label = tk.Label(self, text=common_data.PAY_PERIOD[2], anchor="w", justify=tk.LEFT, width=8)
        self.result_yearly_label.grid(row=3, column=2, padx=5, pady=5, sticky="n")

        self.hourly_cnt_label = tk.Label(self, text="0", anchor="e", justify=tk.RIGHT, width=8)
        self.hourly_cnt_label.grid(row=1, column=3, padx=5, pady=5, sticky="n")

        self.monthly_cnt_label = tk.Label(self, text="0", anchor="e", justify=tk.RIGHT, width=8)
        self.monthly_cnt_label.grid(row=2, column=3, padx=5, pady=5, sticky="n")

        self.yearly_cnt_label = tk.Label(self, text="0", anchor="e", justify=tk.RIGHT, width=8)
        self.yearly_cnt_label.grid(row=3, column=3, padx=5, pady=5, sticky="n")

        self.remove_button = tk.Button(self, text="-", command=self.remove)
        self.remove_button.grid(row=2, column=4, padx=5, pady=5, sticky="n")

        # 配置列权重以便调整间距
        # self.columnconfigure(3, weight=1)  # 使第3列（间隔）可扩展

    def set_data(self):
        config_item = config_list.get_item(self.config_uuid)
        if config_item == None:
            return

        if config_item.from_currency != "" and config_item.from_currency in currency_cache.currency_list:
            self.currency_from_combo.current(currency_cache.currency_list.index(config_item.from_currency))
        if config_item.to_currency != "" and config_item.to_currency in currency_cache.currency_list:
            self.currency_to_combo.current(currency_cache.currency_list.index(config_item.to_currency))
        if config_item.from_paid_period_idx != -1:
            self.pay_period_combo.current(config_item.from_paid_period_idx)
        if config_item.from_amount != 0:
            self.input_amount_str.set(str(config_item.from_amount))
        self.calculate()

    def reset_data(self):
        self.unbind_hanlder()
        self.set_data()
        self.bind_hanlder()

    def bind_hanlder(self):
        self.currency_from_combo.bind("<<ComboboxSelected>>", self.on_from_combo_change)
        self.pay_period_combo.bind("<<ComboboxSelected>>", self.on_pay_period_combo_change)
        self.input_amount_str.trace_add("write", self.on_input_change)
        self.entry['validatecommand'] = (self.entry.register(self.validate_input), '%P')
        self.currency_to_combo.bind("<<ComboboxSelected>>", self.on_to_combo_change)

    def unbind_hanlder(self):
        # 解绑 Combobox 事件
        self.currency_from_combo.bind("<<ComboboxSelected>>", None)
        self.pay_period_combo.bind("<<ComboboxSelected>>", None)
        self.currency_to_combo.bind("<<ComboboxSelected>>", None)

        # 解绑 StringVar 跟踪器
        if self.input_amount_str.trace_info():
            self.input_amount_str.trace_remove("write", self.input_amount_str.trace_info()[0][1])

        # 解绑 Entry 的 validatecommand
        self.entry['validatecommand'] = None

    def on_from_combo_change(self, event):
        # print("on_from_combo_change", self.currency_from_combo.get())
        config_list.update(self.config_uuid, from_currency=self.currency_from_combo.get())
        self.calculate()

    def on_to_combo_change(self, event):
        # print("on_to_combo_change", self.currency_to_combo.get())
        config_list.update(self.config_uuid, to_currency=self.currency_to_combo.get())
        self.calculate()

    def on_pay_period_combo_change(self, event):
        # print("on_pay_period_combo_change", self.pay_period_combo.get())
        config_list.update(self.config_uuid, from_paid_period_idx=common_data.PAY_PERIOD.index(self.pay_period_combo.get()))
        self.calculate()

    def remove(self):
        config_list.remove(self.config_uuid)
        self.pack_forget()
        self.destroy()
        if self in self.component_list:
            self.component_list.remove(self)

    def validate_input(self, new_value):
        # Allow empty string or numeric input only
        # print(f"validate_input, new_value: {new_value}")
        return new_value == "" or new_value.isdigit()

    def on_input_change(self, *args):
        self.last_change_time = time.time()
        self.input_amount_saved = False

    def update_entry(self):
        if self.input_amount_saved:
            return;
        config_list.update(self.config_uuid, from_amount=int("0" if len(self.input_amount_str.get()) == 0 else self.input_amount_str.get()))
        self.calculate()
        self.input_amount_saved = True

    def calculate(self):
        # print(self.config_uuid, "calculated")
        if int(self.input_amount_str.get()) == 0:
            return
        rate = currency_cache.get_rates(self.currency_from_combo.get(), self.currency_to_combo.get())
        self.result_hourly_label.config(text="Hourly")
        self.result_monthly_label.config(text="Monthly")
        self.result_yearly_label.config(text="Yearly")
        self.hourly_cnt_label.config(text="0")
        self.monthly_cnt_label.config(text="0")
        self.yearly_cnt_label.config(text="0")
        if rate < 0:
            return
        tmp_result = float(self.input_amount_str.get()) * rate
        if self.pay_period_combo.get() == common_data.PAY_PERIOD[3]:
            self.result_hourly_label.config(text="")
            self.result_monthly_label.config(text="")
            self.result_yearly_label.config(text="")
            self.hourly_cnt_label.config(text="")
            self.monthly_cnt_label.config(text="{:,}".format(int(tmp_result)))
            self.yearly_cnt_label.config(text="")
        else:
            pay_period = self.pay_period_combo.get()
            if pay_period == common_data.PAY_PERIOD[0]:
                self.hourly_cnt_label.config(text="{:,}".format(int(tmp_result)))
                self.monthly_cnt_label.config(text="{:,}".format(int(tmp_result * 160)))
                self.yearly_cnt_label.config(text="{:,}".format(int(tmp_result * 1920)))
            elif pay_period == common_data.PAY_PERIOD[1]:
                self.hourly_cnt_label.config(text="{:,}".format(int(tmp_result / 160)))
                self.monthly_cnt_label.config(text="{:,}".format(int(tmp_result)))
                self.yearly_cnt_label.config(text="{:,}".format(int(tmp_result * 12)))
            elif pay_period == common_data.PAY_PERIOD[2]:
                self.hourly_cnt_label.config(text="{:,}".format(int(tmp_result / 1920)))
                self.monthly_cnt_label.config(text="{:,}".format(int(tmp_result / 12)))
                self.yearly_cnt_label.config(text="{:,}".format(int(tmp_result)))
