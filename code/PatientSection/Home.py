import tkinter as tk
from tkinter import filedialog, PhotoImage
from PIL import Image, ImageTk

class PatientHome():
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("1360x768")

        # Add background image to window
        self.background_image = tk.PhotoImage(file='images/patient_home_dashboard.png')
        self.background = tk.Label(self.root, image=self.background_image)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        # Home Button and Icon
        self.home_btn = tk.Label(self.root, text="Home", bd=0, bg='#69C6F7', fg="white", font=("Poppins Semibold", 18))
        self.home_btn.place(x=72, y=125)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')
        home_label = tk.Label(self.root, image=self.home_icon, bd=0, bg='#69C6F7')
        home_label.place(x=30, y=130)

        # Booking Button and Icon
        self.booking_btn = tk.Label(self.root, text="Booking", bd=0, bg='#69C6F7', fg="white",
                                    font=("Poppins Semibold", 18))
        self.booking_btn.place(x=72, y=185)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')
        booking_label = tk.Label(self.root, image=self.booking_icon, bd=0, bg='#69C6F7')
        booking_label.place(x=30, y=190)

        # Welcome message for patient
        self.patient_name = tk.Label(text='Welcome, Patient', font=('Poppins', 25, "bold"), bg='white')
        self.patient_name.place(x=280, y=40)

        # Default profile picture
        self.default_profile = Image.open('images/Screenshot (16).png')
        self.default_profile = self.default_profile.resize((150, 150), Image.Resampling.LANCZOS)
        self.profile_pic = ImageTk.PhotoImage(self.default_profile)
        self.profile_label = tk.Label(self.root, image=self.profile_pic)
        self.profile_label.place(x=280, y=110)

        # **Change Profile Button** (to change profile picture)
        self.change_profile = Image.open("images/change_profile.png")
        self.change_profile = self.change_profile.resize((200, 50), Image.Resampling.LANCZOS)
        self.change_profile_icon = ImageTk.PhotoImage(self.change_profile)
        self.change_profile_button = tk.Label(self.root, image=self.change_profile_icon, cursor="hand2")
        self.change_profile_button.place(x=470, y=120)
        self.change_profile_button.bind("<Button-1>", self.change_profile_pic)  # Bind click event to change picture

        # **Remove Profile Button**
        self.remove = Image.open("images/delete picture.png")
        self.remove = self.remove.resize((200, 50), Image.Resampling.LANCZOS)
        self.remove_icon = ImageTk.PhotoImage(self.remove)
        self.remove_button = tk.Label(self.root, image=self.remove_icon, cursor="hand2")
        self.remove_button.place(x=470, y=190)
        self.remove_button.bind("<Button-1>", self.remove_profile_pic)  # Bind click event to remove picture

        # Display appointment information
        self.appointment = tk.Label(self.root, text='Appointment Time', font=('Poppins', 18, "bold"), bg='white')
        self.appointment.place(x=1000, y=100)
        self.date = tk.Label(self.root, text='Monday, 05 November 2030', font=('Poppins', 17), bg='white')
        self.date.place(x=970, y=160)
        self.time = tk.Label(self.root, text='Time: 14:00', font=('Poppins', 13), bg='white')
        self.time.place(x=970, y=200)

        # Patient info labels
        self.name = tk.Label(self.root, text="Full Name:", font=("Poppins", 14), bg='white')
        self.name.place(x=300, y=300)

        self.sex = tk.Label(self.root, text="Sex:", font=("Poppins", 14), bg='white')
        self.sex.place(x=300, y=350)

        self.dob = tk.Label(self.root, text="Date Of Birth:", font=("Poppins", 14), bg='white')
        self.dob.place(x=300, y=400)

        self.Address = tk.Label(self.root, text="Address:", font=("Poppins", 14), bg='white')
        self.Address.place(x=300, y=450)

        self.email = tk.Label(self.root, text="Email:", font=("Poppins", 14), bg='white')
        self.email.place(x=300, y=500)

        self.phone = tk.Label(self.root, text="Phone Number:", font=("Poppins", 14), bg='white')
        self.phone.place(x=300, y=550)

        self.emergency = tk.Label(self.root, text="Emergency Contact:", font=("Poppins", 14), bg='white')
        self.emergency.place(x=300, y=600)

        self.insurance = tk.Label(self.root, text="Insurance:", font=("Poppins", 14), bg='white')
        self.insurance.place(x=300, y=650)

        # Entry fields for user info (initially hidden)
        self.name2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.name2.place(x=400, y=300, width=300)
        self.name2.insert(0, "John Doe")

        self.sex2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.sex2.place(x=400, y=350, width=300)
        self.sex2.insert(0, "Male")

        self.dob2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.dob2.place(x=400, y=400, width=300)
        self.dob2.insert(0, "01/01/1990")

        self.address2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.address2.place(x=400, y=450, width=300)
        self.address2.insert(0, "123 Main St.")

        self.email2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.email2.place(x=400, y=500, width=300)
        self.email2.insert(0, "johndoe@example.com")

        self.phone2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.phone2.place(x=460, y=550, width=300)
        self.phone2.insert(0, "+1234567890")

        self.emergency2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.emergency2.place(x=500, y=600, width=300)
        self.emergency2.insert(0, "Jane Doe")

        self.insurance2 = tk.Entry(self.root, font=("Poppins", 14), state='disabled')
        self.insurance2.place(x=400, y=650, width=300)
        self.insurance2.insert(0, "ABC Insurance")

        # **Edit User Info Button** (to enable editing user information)
        self.edit = Image.open("images/edit.png")
        self.edit = self.edit.resize((40, 40), Image.Resampling.LANCZOS)
        self.edit_icon = ImageTk.PhotoImage(self.edit)
        self.edit_button = tk.Label(self.root, image=self.edit_icon, cursor="hand2")
        self.edit_button.place(x=750, y=280)
        self.edit_button.bind("<Button-1>", self.enable_edit)  # Bind the image to the edit function

        # Save button (to save edited info)
        self.save_button = tk.Button(self.root, text="Save Changes", font=("Poppins", 14), command=self.save_changes)
        self.save_button.place(x=400, y=600)
        self.save_button.place_forget()  # Initially hide it

        # Hide the Entry widgets initially
        self.name2.place_forget()
        self.sex2.place_forget()
        self.dob2.place_forget()
        self.address2.place_forget()
        self.email2.place_forget()
        self.phone2.place_forget()
        self.emergency2.place_forget()
        self.insurance2.place_forget()

        # Medical History Button
        self.medhistory = tk.Label(self.root, text='Medical History', font=('Poppins', 18, 'bold'), bg='white')
        self.medhistory.place(x=1020, y=370)
        self.medbutton = Image.open('images/view more.png')
        self.medbutton = self.medbutton.resize((150, 50), Image.Resampling.LANCZOS)
        self.medbutton_button = ImageTk.PhotoImage(self.medbutton)
        self.viewmore = tk.Label(self.root, image=self.medbutton_button, bg='white')
        self.viewmore.place(x=1040, y=420)

        # Start the application
        self.root.mainloop()

    # Function to change profile picture
    def change_profile_pic(self, event):
        # Open file dialog to select a new picture
        file_path = filedialog.askopenfilename(title='Select Image', filetypes=(('Image files', "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*.*")))

        if file_path:
            # Resize the selected image and update the profile
            new_image = Image.open(file_path)
            new_image = new_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.profile_pic = ImageTk.PhotoImage(new_image)
            self.profile_label.config(image=self.profile_pic)

    # Function to remove profile picture
    def remove_profile_pic(self, event):
        # Replace with default image
        self.profile_pic = ImageTk.PhotoImage(self.default_profile)
        self.profile_label.config(image=self.profile_pic)

    # Function to enable editing of user info
    def enable_edit(self, event):
        # Show the Entry widgets
        self.name2.place(x=460, y=300, width=300)
        self.sex2.place(x=460, y=350, width=300)
        self.dob2.place(x=460, y=400, width=300)
        self.address2.place(x=460, y=450, width=300)
        self.email2.place(x=460, y=500, width=300)
        self.phone2.place(x=460, y=550, width=300)
        self.emergency2.place(x=460, y=600, width=300)
        self.insurance2.place(x=460, y=650, width=300)

        # Enable the Entry widgets
        self.name2.config(state='normal')
        self.sex2.config(state='normal')
        self.dob2.config(state='normal')
        self.address2.config(state='normal')
        self.email2.config(state='normal')
        self.phone2.config(state='normal')
        self.emergency2.config(state='normal')
        self.insurance2.config(state='normal')

        # Show Save button
        self.save_button.place(x=600, y=280)

    def save_changes(self):
        # Save data and update the labels next to the entry boxes
        self.name.config(text=f"Full Name: {self.name2.get()}")
        self.sex.config(text=f"Sex: {self.sex2.get()}")
        self.dob.config(text=f"Date Of Birth: {self.dob2.get()}")
        self.Address.config(text=f"Address: {self.address2.get()}")
        self.email.config(text=f"Email: {self.email2.get()}")
        self.phone.config(text=f"Phone Number: {self.phone2.get()}")
        self.emergency.config(text=f"Emergency Contact: {self.emergency2.get()}")
        self.insurance.config(text=f"Insurance: {self.insurance2.get()}")

        # Disable editing of entry widgets
        self.name2.config(state='disabled')
        self.sex2.config(state='disabled')
        self.dob2.config(state='disabled')
        self.address2.config(state='disabled')
        self.email2.config(state='disabled')
        self.phone2.config(state='disabled')
        self.emergency2.config(state='disabled')
        self.insurance2.config(state='disabled')

        # Hide Entry widgets
        self.name2.place_forget()
        self.sex2.place_forget()
        self.dob2.place_forget()
        self.address2.place_forget()
        self.email2.place_forget()
        self.phone2.place_forget()
        self.emergency2.place_forget()
        self.insurance2.place_forget()

        # Hide Save button
        self.save_button.place_forget()

# Start the PatientHome window
PatientHome()
