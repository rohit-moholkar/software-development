"""A digital clock and date display application built with Python and Tkinter."""

import tkinter as tk
from datetime import datetime


class DigitalClock:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Digital Clock")
        self.window.geometry("420x300")
        self.window.resizable(False, False)
        self.window.configure(bg="#111827")

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        container = tk.Frame(self.window, bg="#111827")
        container.pack(expand=True, fill="both", padx=24, pady=24)

        title_label = tk.Label(
            container,
            text="DIGITAL CLOCK",
            bg="#111827",
            fg="#9ca3af",
            font=("Calibri", 16, "bold"),
        )
        title_label.pack(pady=(0, 20))

        self.time_label = tk.Label(
            container,
            text="",
            bg="#111827",
            fg="#f9fafb",
            font=("Calibri", 42, "bold"),
        )
        self.time_label.pack(pady=(0, 10))

        self.day_label = tk.Label(
            container,
            text="",
            bg="#111827",
            fg="#60a5fa",
            font=("Calibri", 22, "bold"),
        )
        self.day_label.pack(pady=(0, 8))

        self.date_label = tk.Label(
            container,
            text="",
            bg="#111827",
            fg="#d1d5db",
            font=("Calibri", 20),
        )
        self.date_label.pack()

    def update_clock(self):
        current_datetime = datetime.now()

        current_time = current_datetime.strftime("%I:%M:%S %p")
        current_day = current_datetime.strftime("%A")
        current_date = current_datetime.strftime("%d %B %Y")

        self.time_label.config(text=current_time)
        self.day_label.config(text=current_day)
        self.date_label.config(text=current_date)

        self.window.after(1000, self.update_clock)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    clock = DigitalClock()
    clock.run()