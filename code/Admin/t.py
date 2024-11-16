import tkinter as tk

# Function to handle mouse wheel scrolling
def on_mouse_wheel(event, canvas):
    if event.delta > 0:  # Scroll up
        canvas.yview_scroll(-1, "units")
    else:  # Scroll down
        canvas.yview_scroll(1, "units")

# Create main window
root = tk.Tk()
root.title("Scrollable Panes with Mousewheel")

# Create a frame for the first scrollable pane
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=10)

# Add canvas and scrollbar for the first pane
canvas1 = tk.Canvas(frame1, width=200, height=300)
scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
canvas1.config(yscrollcommand=scrollbar1.set)
scrollbar1.pack(side="right", fill="y")
canvas1.pack(side="left", fill="both", expand=True)

# Add content to the first canvas
content1 = tk.Frame(canvas1)
canvas1.create_window((0, 0), window=content1, anchor="nw")

for i in range(20):
    tk.Label(content1, text=f"Pane 1 - Item {i+1}").pack()

# Update scrollregion for the first canvas
content1.update_idletasks()
canvas1.config(scrollregion=canvas1.bbox("all"))

# Bind mouse wheel event to the first canvas
canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: on_mouse_wheel(event, canvas))

# Create a frame for the second scrollable pane
frame2 = tk.Frame(root)
frame2.pack(side=tk.LEFT, padx=10)

# Add canvas and scrollbar for the second pane
canvas2 = tk.Canvas(frame2, width=200, height=300)
scrollbar2 = tk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)
canvas2.config(yscrollcommand=scrollbar2.set)
scrollbar2.pack(side="right", fill="y")
canvas2.pack(side="left", fill="both", expand=True)

# Add content to the second canvas
content2 = tk.Frame(canvas2)
canvas2.create_window((0, 0), window=content2, anchor="nw")

for i in range(20):
    tk.Label(content2, text=f"Pane 2 - Item {i+1}").pack()

# Update scrollregion for the second canvas
content2.update_idletasks()
canvas2.config(scrollregion=canvas2.bbox("all"))

# Bind mouse wheel event to the second canvas
canvas2.bind("<MouseWheel>", lambda event, canvas=canvas2: on_mouse_wheel(event, canvas))

# Create a frame for the third scrollable pane
frame3 = tk.Frame(root)
frame3.pack(side=tk.LEFT, padx=10)

# Add canvas and scrollbar for the third pane
canvas3 = tk.Canvas(frame3, width=200, height=300)
scrollbar3 = tk.Scrollbar(frame3, orient="vertical", command=canvas3.yview)
canvas3.config(yscrollcommand=scrollbar3.set)
scrollbar3.pack(side="right", fill="y")
canvas3.pack(side="left", fill="both", expand=True)

# Add content to the third canvas
content3 = tk.Frame(canvas3)
canvas3.create_window((0, 0), window=content3, anchor="nw")

for i in range(20):
    tk.Label(content3, text=f"Pane 3 - Item {i+1}").pack()

# Update scrollregion for the third canvas
content3.update_idletasks()
canvas3.config(scrollregion=canvas3.bbox("all"))

# Bind mouse wheel event to the third canvas
canvas3.bind("<MouseWheel>", lambda event, canvas=canvas3: on_mouse_wheel(event, canvas))

# Run the Tkinter event loop
root.mainloop()
