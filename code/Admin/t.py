import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Scrollable Table")
root.geometry("800x400")

# Create a frame to hold the table and scrollbars
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

# Create a Treeview widget
columns = [f"Column {i+1}" for i in range(8)]  # Example with 8 columns
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

# Define headings and column widths
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100, anchor=tk.CENTER)

# Add example data to the table
for i in range(50):  # Example with 50 rows
    row = [f"Row {i+1} Col {j+1}" for j in range(8)]
    table.insert("", tk.END, values=row)

# Create vertical scrollbar
v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Create horizontal scrollbar
h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=table.xview)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

# Attach scrollbars to the table
table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

# Pack the table into the frame
table.pack(fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()
