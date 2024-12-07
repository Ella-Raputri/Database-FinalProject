import tkinter as tk


class History:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill='both', expand=True)

        label = tk.Label(self.frame, text="History Section")
        label.pack()
