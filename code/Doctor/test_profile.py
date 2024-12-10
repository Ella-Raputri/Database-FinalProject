import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to change profile picture
def change_picture():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((100, 100))
        profile_pic = ImageTk.PhotoImage(img)
        profile_pic_label.config(image=profile_pic)
        profile_pic_label.image = profile_pic  # Keep a reference to avoid garbage collection

# Function to delete profile picture
def delete_picture():
    profile_pic_label.config(image=default_pic)
    profile_pic_label.image = default_pic

# Main window
root = tk.Tk()
root.title("Profile Settings")
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

title_label = tk.Label(content, text="Settings", bg="#E8F5FE", fg="black", font=("Arial", 24, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

# Profile Picture Section
profile_pic_frame = tk.Frame(content, bg="#E8F5FE")
profile_pic_frame.grid(row=1, column=0, sticky="w", padx=10, pady=10)

default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((100, 100)))  # Replace with your image path
profile_pic_label = tk.Label(profile_pic_frame, image=default_pic, bg="#E8F5FE")
profile_pic_label.image = default_pic
profile_pic_label.pack()

change_pic_btn = tk.Button(profile_pic_frame, text="Change Picture", bg="#0078D7", fg="white", font=("Arial", 12),
                           command=change_picture)
change_pic_btn.pack(pady=5)

delete_pic_btn = tk.Button(profile_pic_frame, text="Delete Picture", bg="#E8F5FE", font=("Arial", 12),
                           command=delete_picture)
delete_pic_btn.pack(pady=5)

# Input Fields
fields = [
    ("First Name", ""), ("Last Name", ""), ("Phone Number", ""),
    ("Date of Birth", ""), ("City", ""), ("Address Details", "")
]

for idx, (label_text, _) in enumerate(fields):
    label = tk.Label(content, text=label_text, bg="#E8F5FE", font=("Arial", 14))
    label.grid(row=idx + 2, column=0, sticky="w", padx=10, pady=5)
    entry = ttk.Entry(content, width=30)
    entry.grid(row=idx + 2, column=1, sticky="w", padx=10, pady=5)

# Specialties and Description
specialties_label = tk.Label(content, text="Specialties", bg="#E8F5FE", font=("Arial", 14))
specialties_label.grid(row=8, column=0, sticky="nw", padx=10, pady=10)
specialties_text = tk.Text(content, height=2, width=40)
specialties_text.grid(row=8, column=1, sticky="w", padx=10, pady=10)

description_label = tk.Label(content, text="Description", bg="#E8F5FE", font=("Arial", 14))
description_label.grid(row=9, column=0, sticky="nw", padx=10, pady=10)
description_text = tk.Text(content, height=5, width=40)
description_text.grid(row=9, column=1, sticky="w", padx=10, pady=10)

# Doctor's Name and Email (Top Right)
doctor_info = tk.Frame(content, bg="#E8F5FE")
doctor_info.grid(row=0, column=1, sticky="e", padx=20)

doctor_name_label = tk.Label(doctor_info, text="Name", bg="#E8F5FE", font=("Arial", 14, "bold"))
doctor_name_label.pack(anchor="e")
doctor_email_label = tk.Label(doctor_info, text="Email: raaa@mail.com", bg="#E8F5FE", font=("Arial", 12))
doctor_email_label.pack(anchor="e")

# Run the application
root.mainloop()


def change_picture(self):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((100, 100))
        self.profile_pic = ImageTk.PhotoImage(img)
        self.profile_pic_label.config(image=self.profile_pic)
        self.profile_pic_label.image = self.profile_pic  # Keep reference

def delete_picture(self):
    self.profile_pic_label.config(image=self.default_pic)
    self.profile_pic_label.image = self.default_pic

