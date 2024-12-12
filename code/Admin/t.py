import tkinter as tk

class HoverWindowDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hover Popup Example")
        self.geometry("400x300")
        
        # Create a label
        self.label = tk.Label(self, text="Hover over me!", font=("Poppins", 16), bg="white", fg="black")
        self.label.pack(pady=100)
        
        # Bind hover events
        self.label.bind("<Enter>", self.show_tooltip)
        self.label.bind("<Leave>", self.hide_tooltip)
        
        # Tooltip window (hidden by default)
        self.tooltip_window = None

    def show_tooltip(self, event):
        # Create a Toplevel window as a tooltip
        if not self.tooltip_window:
            self.tooltip_window = tk.Toplevel(self)
            self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
            self.tooltip_window.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tk.Label(self.tooltip_window, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus mollis aliquam ex, in mattis ipsum blandit nec. Donec maximus lectus vel augue iaculis tempus. Cras facilisis tristique libero, quis imperdiet enim accumsan sit amet. Sed in commodo ", bg="yellow", font=("Poppins", 12)).pack()

    def hide_tooltip(self, event):
        # Destroy the tooltip window when the cursor leaves
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Run the application
if __name__ == "__main__":
    app = HoverWindowDemo()
    app.mainloop()
