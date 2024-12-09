import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


# Function to update patient details
def show_patient_details(event):
    selected_index = patient_listbox.curselection()
    if selected_index:
        patient_data = patients[selected_index[0]]
        for widget in patient_details_frame.winfo_children():
            widget.destroy()  # Clear previous details
        for idx, (key, value) in enumerate(patient_data.items()):
            label = tk.Label(patient_details_frame, text=f"{key}: {value}", bg="#FFFFFF", font=("Arial", 14))
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)


# Dummy patient data
patients = [
    {"Name": "John Doe", "Email": "john.doe@mail.com", "Location": "Jakarta", "Status": "Hepatology", "Date": "2024-11-25"},
    {"Name": "Jane Smith", "Email": "jane.smith@mail.com", "Location": "Surabaya", "Status": "Dermatology", "Date": "2024-11-26"},
    {"Name": "Tom Harris", "Email": "tom.harris@mail.com", "Location": "Bandung", "Status": "Cardiology", "Date": "2024-11-27"},
]

# Main window
root = tk.Tk()
root.title("Clinic Box")
root.geometry("900x600")
root.configure(bg="#E8F5FE")

# Sidebar
sidebar = tk.Frame(root, bg="#0078D7", width=200)
sidebar.pack(side="left", fill="y")

sidebar_title = tk.Label(sidebar, text="Clinic Box", bg="#0078D7", fg="white", font=("Arial", 18, "bold"))
sidebar_title.pack(pady=20)

menu_items = [("Home", "🏠"), ("History", "🔄"), ("Profile", "👤")]
for item, icon in menu_items:
    menu_button = tk.Button(
        sidebar, text=f"{icon} {item}", bg="#0078D7", fg="white", font=("Arial", 14),
        bd=0, anchor="w", padx=20, relief="flat", activebackground="#005A9E"
    )
    menu_button.pack(fill="x", pady=5)

# Content Area
content = tk.Frame(root, bg="#E8F5FE")
content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Booking Section
title_label = tk.Label(content, text="Booking", bg="#E8F5FE", fg="black", font=("Arial", 24, "bold"))
title_label.pack(anchor="w", pady=10)

booking_frame = tk.Frame(content, bg="#FFFFFF", highlightbackground="#CCCCCC", highlightthickness=1)
booking_frame.pack(fill="x", padx=10, pady=10)

# Patient Listbox
patient_listbox = tk.Listbox(booking_frame, height=8, font=("Arial", 12), bg="#F7F7F7", bd=0, relief="flat")
patient_listbox.pack(fill="both", padx=10, pady=10)
for patient in patients:
    patient_listbox.insert(tk.END, f"{patient['Name']} - {patient['Status']}")

patient_listbox.bind("<<ListboxSelect>>", show_patient_details)

# Patient Details Section
patient_details_label = tk.Label(content, text="Patient Details", bg="#E8F5FE", font=("Arial", 16, "bold"))
patient_details_label.pack(anchor="w", pady=10)

patient_details_frame = tk.Frame(content, bg="#FFFFFF", highlightbackground="#CCCCCC", highlightthickness=1)
patient_details_frame.pack(fill="x", padx=10, pady=10)

# Default Placeholder Details
placeholder_label = tk.Label(patient_details_frame, text="Select a patient to view details", bg="#FFFFFF", font=("Arial", 14))
placeholder_label.pack(pady=20)

# Run the application
root.mainloop()
