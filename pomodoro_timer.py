#Libraries needed
import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
import os

#tomato_path = os.path.abspath("Work_Projects/Software_Developer/Python Projects/Pomodoro Timer GUI/tomato.png")

class PomodoroTimer():

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file="/Users/sachaguimarey/Documents/Work_Projects/Software_Developer/Python Projects/Pomodoro Timer GUI/tomato.png"))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Building the visual side of the timer.
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))
        
        self.tab = ttk.Notebook(self.root)
        self.tab.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tab, width=600, height=110)
        self.tab2 = ttk.Frame(self.tab, width=600, height=110)
        self.tab3 = ttk.Frame(self.tab, width=600, height=110)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=20)

        self.tab.add(self.tab1, text="Pomodoro")
        self.tab.add(self.tab2, text="Short Break")
        self.tab.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=("Ubuntu", 16))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3)

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()



    #Adding functionality
    def start_timer_thread(self):
        if not self.running:
            self.tab.select(0)
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tab.index(self.tab.select()) + 1

        if timer_id == 1:
            full_seconds = 60 * 25
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(0.9)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tab.select(2)
                    self.start_timer()
                else:
                    self.tab.select(1)
                self.start_timer()

        elif timer_id == 2:
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(0.9)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tab.select(0)
                self.start_timer()

        elif timer_id == 3:
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(0.9)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tab.select(0)
                self.start_timer()
        else:
            print("Invalid timer ID")

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.running = False

    def skip_clock(self):
        current_tab = self.tab.index(self.tab.select())

        if current_tab == 0:
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text="15:00")

        self.skipped = True
        self.stopped = True

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


PomodoroTimer()