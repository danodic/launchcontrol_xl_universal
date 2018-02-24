import tkinter as tk
from tkinter import ttk

from window_main import MainWindow

root = tk.Tk()
#root.wm_title("pianopad")
#root.geometry("320x900")
app = MainWindow()

# Wait for the input thread to finish
app.mainloop()