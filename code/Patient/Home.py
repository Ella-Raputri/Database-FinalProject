import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import mysql.connector

class PatientHome:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill='both', expand=True)

        # Setup database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="BinusSQL2005",  # Update with your MySQL password
            database="ClinicSystemDB"
        )
        self.cursor = self.db_connection.cursor()

        # Fetch patient data from the database
        self.retrieve_patient_info()

        # Background image
        self.background_image = Image.open('images/patient_home_dashboard (3).png')
        self.background_image = self.background_image.resize((1200, 768), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.background_image)
        self.bg_label = tk.Label(self.frame, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1, x=-120)

        # Welcome message for the patient
        self.patient_name = tk.Label(self.frame, text='Welcome, Patient', font=('Poppins', 25, "bold"), bg='white')
        self.patient_name.place(x=100, y=40)

        # Default profile picture
        self.default_profile = Image.open('images/Screenshot (16).png')
        self.default_profile = self.default_profile.resize((150, 150), Image.Resampling.LANCZOS)
        self.profile_pic = ImageTk.PhotoImage(self.default_profile)
        self.profile_label = tk.Label(self.frame, image=self.profile_pic)
        self.profile_label.place(x=100, y=110)

        # Change Profile Button
        self.change_profile = Image.open("images/change_profile.png")
        self.change_profile = self.change_profile.resize((200, 50), Image.Resampling.LANCZOS)
        self.change_profile_icon = ImageTk.PhotoImage(self.change_profile)
        self.change_profile_button = tk.Label(self.frame, image=self.change_profile_icon, cursor="hand2")
        self.change_profile_button.place(x=280, y=120)
        self.change_profile_button.bind("<Button-1>", self.change_profile_pic)

        # Remove Profile Button
        self.remove = Image.open("images/delete picture.png")
        self.remove = self.remove.resize((200, 50), Image.Resampling.LANCZOS)
        self.remove_icon = ImageTk.PhotoImage(self.remove)
        self.remove_button = tk.Label(self.frame, image=self.remove_icon, cursor="hand2")
        self.remove_button.place(x=280, y=190)
        self.remove_button.bind("<Button-1>", self.remove_profile_pic)

        # Display appointment information
        self.appointment = tk.Label(self.frame, text='Appointment Time', font=('Poppins', 18, "bold"), bg='white')
        self.appointment.place(x=730, y=100)
        self.date = tk.Label(self.frame, text='Monday, 05 November 2030', font=('Poppins', 15), bg='white')
        self.date.place(x=720, y=160)
        self.time = tk.Label(self.frame, text='Time: 14:00', font=('Poppins', 11), bg='white')
        self.time.place(x=720, y=200)

        # Patient info labels
        self.name = self.create_label(self.frame, "Full Name:", 110, 300)
        self.sex = self.create_label(self.frame, "Sex:", 110, 350)
        self.dob = self.create_label(self.frame, "Date Of Birth:", 110, 400)
        self.address = self.create_label(self.frame, "Address:", 110, 450)
        self.email = self.create_label(self.frame, "Email:", 110, 500)
        self.phone = self.create_label(self.frame, "Phone Number:", 110, 550)
        self.emergency = self.create_label(self.frame, "Emergency Contact:", 110, 600)
        self.insurance = self.create_label(self.frame, "Insurance:", 110, 650)

        # Entry fields for user info (initially hidden)
        self.name2 = self.create_entry(self.frame, "John Doe", 400, 300)
        self.sex2 = self.create_entry(self.frame, "Male", 400, 350)
        self.dob2 = self.create_entry(self.frame, "01/01/1990", 400, 400)
        self.address2 = self.create_entry(self.frame, "123 Main St.", 400, 450)
        self.email2 = self.create_entry(self.frame, "johndoe@example.com", 400, 500)
        self.phone2 = self.create_entry(self.frame, "+1234567890", 460, 550)
        self.emergency2 = self.create_entry(self.frame, "Jane Doe", 500, 600)
        self.insurance2 = self.create_entry(self.frame, "ABC Insurance", 400, 650)

        # Edit button
        self.edit_button = self.create_button(self.frame, "edit.png", self.enable_edit, 500, 280)

        # Save button (now created correctly as a tk.Button)
        self.save_button = tk.Button(self.frame, text="Save Changes", font=("Poppins", 14), command=self.save_changes)
        self.save_button.place(x=-100, y=280)
        self.save_button.place_forget()  # Initially hide it

        # Medical History Button
        self.medhistory = tk.Label(self.frame, text='Medical History', font=('Poppins', 18, 'bold'), bg='white')
        self.medhistory.place(x=750, y=360)
        self.viewmore = Image.open('images/view more.png')
        self.viewmore = self.viewmore.resize((150,60), Image.Resampling.LANCZOS)
        self.viewmorebutton = ImageTk.PhotoImage(self.viewmore)
        self.viewmorebutton1 = tk.Label(self.frame, image=self.viewmorebutton, cursor='hand2')
        self.viewmorebutton1.place(x=765, y=410)

    def create_label(self, parent, text, x, y):
        label = tk.Label(parent, text=text, font=("Poppins", 14), bg='white')
        label.place(x=x, y=y)
        return label

    def create_entry(self, parent, text, x, y):
        entry = tk.Entry(parent, font=("Poppins", 14), state='disabled', bg='white', highlightthickness=0, bd=0)
        entry.place(x=x, y=y, width=300)
        entry.insert(0, text)
        entry.place_forget()  # Make it initially invisible
        return entry

    def create_button(self, parent, img_path, command, x, y):
        if img_path:
            img = Image.open(f"images/{img_path}")
            img = img.resize((40, 40), Image.Resampling.LANCZOS)
            button_icon = ImageTk.PhotoImage(img)
            button = tk.Label(parent, image=button_icon, cursor="hand2")
            button.place(x=x, y=y)
            button.image = button_icon
            if command:
                button.bind("<Button-1>", command)
        else:
            button = tk.Button(parent, text=img_path, command=command, font=("Poppins", 14))
            button.place(x=x, y=y)
        return button

    def change_profile_pic(self, event):
        file_path = filedialog.askopenfilename(title='Select Image', filetypes=(('Image files', "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*.*")))

        if file_path:
            new_image = Image.open(file_path)
            new_image = new_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.profile_pic = ImageTk.PhotoImage(new_image)
            self.profile_label.config(image=self.profile_pic)

    def remove_profile_pic(self, event):
        self.profile_pic = ImageTk.PhotoImage(self.default_profile)
        self.profile_label.config(image=self.profile_pic)

    def enable_edit(self, event):
        # Show the Entry widgets and make them editable
        self.name2.place(x=300, y=300, width=300)
        self.sex2.place(x=300, y=350, width=300)
        self.dob2.place(x=300, y=400, width=300)
        self.address2.place(x=300, y=450, width=300)
        self.email2.place(x=300, y=500, width=300)
        self.phone2.place(x=300, y=550, width=300)
        self.emergency2.place(x=300, y=600, width=300)
        self.insurance2.place(x=300, y=650, width=300)

        # Enable the Entry widgets for editing
        self.name2.config(state='normal')
        self.sex2.config(state='normal')
        self.dob2.config(state='normal')
        self.address2.config(state='normal')
        self.email2.config(state='normal')
        self.phone2.config(state='normal')
        self.emergency2.config(state='normal')
        self.insurance2.config(state='normal')

        # Show the Save button
        self.save_button.place(x=600, y=280)

    def save_changes(self):
        updated_name = self.name2.get()
        name_parts = updated_name.split()  # Split the name into first and last name

        # Avoid index error in case the user only inputs a single name
        if len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = ""
        else:
            first_name = name_parts[0]
            last_name = name_parts[1]

        updated_email = self.email2.get()
        updated_phone = self.phone2.get()

        # Update the database with the new information
        query = """
            UPDATE `User` 
            SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s 
            WHERE UserId = %s
        """
        values = (first_name, last_name, updated_email, updated_phone, 'P001')  # Assuming UserId is 'P001'

        self.cursor.execute(query, values)
        self.db_connection.commit()

        # Update the labels with the new values
        self.name.config(text=f"Full Name: {updated_name}")
        self.email.config(text=f"Email: {updated_email}")
        self.phone.config(text=f"Phone Number: {updated_phone}")

        # Hide the Entry widgets
        self.name2.place_forget()
        self.sex2.place_forget()
        self.dob2.place_forget()
        self.address2.place_forget()
        self.email2.place_forget()
        self.phone2.place_forget()
        self.emergency2.place_forget()
        self.insurance2.place_forget()

        # Show the labels again (now updated)
        self.name.place(x=110, y=300)
        self.sex.place(x=110, y=350)
        self.dob.place(x=110, y=400)
        self.address.place(x=110, y=450)
        self.email.place(x=110, y=500)
        self.phone.place(x=110, y=550)
        self.emergency.place(x=110, y=600)
        self.insurance.place(x=110, y=650)

        # Hide Save button
        self.save_button.place_forget()

    def retrieve_patient_info(self):
        # Fetch patient info from the database
        self.cursor.execute("SELECT FirstName, LastName, Email, PhoneNumber FROM `User` WHERE UserId = 'P001'")
        result = self.cursor.fetchone()

        if result:
            first_name, last_name, email, phone = result
            self.name.config(text=f"Full Name: {first_name} {last_name}")
            self.email.config(text=f"Email: {email}")
            self.phone.config(text=f"Phone Number: {phone}")
            self.sex.config(text=f"Sex: {sex}")
            self.dob.config(text=f"Date of Birth: {dob}")
            self.address.config(text=f"Address: {address}")
            self.emergency.config(text=f"Emergency Contact: {emergency}")
            self.insurance.config(text=f"Insurance: {insurance}")