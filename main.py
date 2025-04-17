# Copyright (c) [2025] [Yifu Ding]
import json
import tkinter as tk
import threading
import time
from tkinter import PhotoImage, ttk
import numeric_input
from convert_component import ConvertComponent
from convert_config_list import config_list
from PIL import Image, ImageTk
from currency_cache import currency_cache
from tkinter import messagebox

class NumericEntryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Calculator")
        # self.root.wm_iconbitmap("res/dollor.png")
        self.stay_on_top = True
        self.root.wm_attributes("-topmost", self.stay_on_top)
        # self.root.geometry("1000x800")
        self.root.minsize(460, 400)
        self.root.maxsize(460, 800) 
    
        self.image_pinned = ImageTk.PhotoImage(Image.open("res/pinned.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.image_not_pinned = ImageTk.PhotoImage(Image.open("res/not_pinned.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.button_bar = tk.Frame(self.root, bd=2)
        self.button_bar.pack(side=tk.TOP, fill=tk.X)
        self.pin_button_label = tk.Label(self.button_bar, image=self.image_pinned if self.stay_on_top else self.image_not_pinned)
        self.pin_button_label.pack(side=tk.RIGHT)
        self.pin_button_label.bind("<Button-1>", self.toggle_pin)

        self.refresh_image = ImageTk.PhotoImage(Image.open("res/refresh.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.refresh_button_label = tk.Label(self.button_bar, image=self.refresh_image)
        self.refresh_button_label.pack(side=tk.RIGHT)
        self.refresh_button_label.bind("<Button-1>", self.refresh_rates)
        
        scale = tk.Scale(self.button_bar,
                 from_=30,
                 to=100,
                 orient=tk.HORIZONTAL,
                 length=150,
                 showvalue=False,
                 resolution=1,
                 command=self.slider_changed)
        scale.pack(side=tk.RIGHT)
        scale.set(70)
        self.root.attributes("-alpha", 0.7)

        # 创建 Canvas 和 Frame
        self.canvas = tk.Canvas(self.root, takefocus=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # 创建竖向滚动条
        scrollbar = ttk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set, scrollregion=self.canvas.bbox("all"))
        # self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # 预设的最大高度
        self.max_height = 550
        self.numeric_inputs = []
        self.monitoring = True

        # Start the monitoring thread
        threading.Thread(target=self.monitor_inputs, daemon=True).start()

        # Add initial input box
        # self.add_numeric_input()

        self.convert_components = []
        self.init_convert_components();

        add_button = tk.Button(root, text="+", command=self.add_convert_component)
        add_button.pack(pady=10)
        self.root.geometry("")

    def slider_changed(self, value):
        self.root.attributes("-alpha", float(value)/100)

    def toggle_pin(self, event):
        self.stay_on_top = (not self.stay_on_top)
        self.pin_button_label.config(image=self.image_pinned if self.stay_on_top else self.image_not_pinned)
        self.root.wm_attributes("-topmost", self.stay_on_top)

    def refresh_rates(self, event):
        print("refresh button pressed")
        currency_cache.initialize_rates()
        for component_item in self.convert_components:
            component_item.reset_data()

    def init_convert_components(self):
        if config_list.is_empty():
            self.add_convert_component()
        else:
            for item in config_list.config_list:
                self.convert_components.append(ConvertComponent(self.frame, item.uuid, self.convert_components))
            self.update_canvas()

    def add_convert_component(self):
        # new_convert_component = convert_component.ConvertComponent(self.root, "a")
        self.convert_components.append(ConvertComponent(self.frame, config_list.add(), self.convert_components))
        self.update_canvas()

    def update_canvas(self):
        """更新 Canvas 高度和滚动区域."""
        self.frame.update_idletasks()  # 确保 Frame 布局更新
        total_height = self.frame.winfo_reqheight()  # 获取 Frame 总高度

        if total_height < self.max_height:
            self.canvas.configure(height=total_height, scrollregion=self.canvas.bbox("all"))
        else:
            self.canvas.configure(height=self.max_height, scrollregion=self.canvas.bbox("all"))
        # self.root.geometry("")

    def on_mousewheel(self, event):
        print("rolling...")
        # if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
        self.canvas.yview_scroll(int(-1 * (event.delta / 1)), "units")
        pass
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    # def add_numeric_input(self):
    #     new_numeric_input = numeric_input.NumericInput(self.root, self.update_monitor_list)
    #     self.numeric_inputs.append(new_numeric_input)

    # def update_monitor_list(self, new_numeric_input):
    #     # This method is called whenever an input changes
    #     pass

    def monitor_inputs(self):
        while self.monitoring:
            time.sleep(1)
            current_time = time.time()
            for component_item in self.convert_components:
                if current_time - component_item.last_change_time >= 1:
                    component_item.update_entry()
            # for numeric_input in self.numeric_inputs:
            #     if current_time - numeric_input.last_change_time >= 1 and numeric_input.value_to_print:
            #         print(f"Input value: {numeric_input.value_to_print}")
            #         numeric_input.value_to_print = None  # Reset after printing

    def on_closing(self):
        self.monitoring = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    if not currency_cache.initialize_rates():
        root.withdraw()
        messagebox.showerror("Error", "Can not get rates, existing.")
        root.destroy()
    else:
        app = NumericEntryApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
