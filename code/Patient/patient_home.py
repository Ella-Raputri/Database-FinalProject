import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db
import os, shutil,re

class PatientHome(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email_val = None

        self.fname_val = None
        self.lname_val = None
        self.gender_val = None
        self.phone_val = None
        self.city_val = None
        self.address_val = None
        self.dob_val = None

        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((150, 150)))
        self.profile_pic = self.default_pic
        self.propic_path = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg=self.master.bg_color1, fg="white", 
                                  font=("Poppins Semibold", 18))
        self.home_btn.place(x=0, y=119, width=226, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg=self.master.bg_color1)  
        home_label.place(x=27, y=130)

        # booking
        self.booking_btn = tk.Button(self, text="    Booking", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18),
                                    command=self.navigate_booking)
        self.booking_btn.place(x=0, y=186,  width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/pat_booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#64C1F6')  
        booking_label.place(x=23, y=195)

        # history
        self.history_btn = tk.Button(self, text="  History", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_history)
        self.history_btn.place(x=0, y=246, width=213, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg='#5FBBF5')  
        history_label.place(x=26, y=257)

    def navigate_history(self):
        print('historyy')
        # self.master.doctor_history.set_user_id(self.user_id)
        # self.master.show_frame(self.master.doctor_history)
    
    def navigate_booking(self):
        print('booking')
        # self.master.doctor_profile.set_user_id(self.user_id)
        # self.master.show_frame(self.master.doctor_profile)

    def get_user_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """SELECT Email, FirstName, LastName, Gender, PhoneNumber, City, AddressDetail
                FROM User WHERE UserId = %s"""
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.email_val, self.fname_val, self.lname_val, self.gender_val, self.phone_val, self.city_val, self.address_val= result
                else:
                    messagebox.showerror("Error", "Invalid user.")
                    return
                
                query2 = "SELECT ProfilePicture, DATE_FORMAT(DateOfBirth, '%Y-%m-%d') AS formatted_dob FROM Patient WHERE PatientId = %s;"
                cursor.execute(query2, (self.user_id,))
                result2 = cursor.fetchone()
                if result2:  
                    self.propic_path, self.dob_val = result2

                    if(self.propic_path == None): 
                        self.profile_pic = self.default_pic
                    else: 
                        self.profile_pic = ImageTk.PhotoImage(Image.open(self.propic_path).resize((150, 150)))
                else:
                    messagebox.showerror("Error", "Invalid patient.")
                    return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def create_widgets(self):        
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/patient_home_dashboard.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        # title
        self.title_label = tk.Label(self, text=f"Welcome, {self.fname_val}", font=("Poppins", 32, "bold"), fg='black', bg='white')
        self.title_label.place(x=261, y=28)

        # name login
        self.name_label = tk.Label(self, text=f'{self.fname_val} {self.lname_val}', font=("Poppins", 16), fg=self.master.font_color3, bg='white')
        self.name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        self.email_label = tk.Label(self, text=f"Email: {self.email_val}", font=("Poppins", 12), fg=self.master.font_color3, bg='white')
        self.email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # Default profile picture
        self.profile_label = tk.Label(self, image=self.profile_pic, bg='white')
        self.profile_label.place(x=284, y=121)

        # Change Profile Button
        self.change_profile = Image.open("images/change_profile.png")
        self.change_profile = self.change_profile.resize((195, 53), Image.Resampling.LANCZOS)
        self.change_profile_icon = ImageTk.PhotoImage(self.change_profile)
        self.change_profile_button = tk.Label(self, image=self.change_profile_icon, cursor="hand2",bd=0, highlightthickness=0)
        self.change_profile_button.place(x=455, y=137)
        self.change_profile_button.bind("<Button-1>", self.change_profile_pic)

        # Remove Profile Button
        self.remove = Image.open("images/delete_picture.png")
        self.remove = self.remove.resize((195, 53), Image.Resampling.LANCZOS)
        self.remove_icon = ImageTk.PhotoImage(self.remove)
        self.remove_button = tk.Label(self, image=self.remove_icon, cursor="hand2",bd=0, highlightthickness=0)
        self.remove_button.place(x=455, y=207)
        self.remove_button.bind("<Button-1>", self.remove_profile_pic)

        # next appointment
        self.get_appointment_info()        

        self.appointment = tk.Label(self, text='Next Appointment', font=('Poppins', 20, "bold"), bg='white')
        self.appointment.place(x=964, y=134)
        self.date = tk.Label(self, text=self.formatted_date, font=('Poppins',16), bg='white',fg=self.master.font_color2)
        self.date.place(x=964, y=182)
        self.time = tk.Label(self, text=f'Time: {self.next_hour}', font=('Poppins', 14), bg='white',fg=self.master.font_color2)
        self.time.place(x=964, y=220)

        if(self.gender_val == 0): self.gender = 'Male'
        else: self.gender = 'Female'

        # Patient info labels
        self.name = self.create_label(self, f"Full Name: {self.fname_val} {self.lname_val}", 289, 330)
        self.sex = self.create_label(self, f"Sex: {self.gender}", 289, 380)
        self.dob = self.create_label(self, f"Date Of Birth: {self.dob_val}", 289, 430)
        self.email = self.create_label(self, f"Email: {self.email_val}", 289, 480)
        self.phone = self.create_label(self, f"Phone Number: {self.phone_val}", 289, 530)
        self.city = self.create_label(self, f"City: {self.city_val}", 289, 580)
        self.address = self.create_label(self, f"Address: {self.address_val}", 289, 630)

        # Entry fields
        self.name2 = self.create_entry(self, "John Doe", 362, 330)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.sex2 = ttk.Combobox(self, font=('Poppins', 14), width=15, state="readonly", style="Custom.TCombobox")
        self.sex2['values'] = ("Male", "Female")
        self.sex2.place(x=335, y=380)
        self.sex2.place_forget()

        self.dob2 = self.create_entry(self, "01/01/1990", 422, 430)
        self.email2 = self.create_entry(self, "johndoe@example.com", 351, 480)
        self.phone2 = self.create_entry(self, "+1234567890", 447, 530)
        self.city2 = self.create_entry(self, "Jane Doe", 347, 580)
        self.address2 = self.create_entry(self, "123 Main St.", 365, 630)

        # Edit button
        self.edit_button = self.create_button(self, "edit.png", self.enable_edit, 785, 280)

        # Save button
        self.save_button = tk.Button(self, text="Save", font=("Poppins", 14), relief='flat',
                                     fg='white',bg=self.master.bg_color1,command=self.save_changes)
        self.save_button.place(x=770, y=280, width=70, height=40)
        self.save_button.place_forget()

        # medical history
        self.medhistory = tk.Label(self, text='Medical History', font=('Poppins', 20, 'bold'), bg='white')
        self.medhistory.place(x=964, y=332)
        self.create_medhist_scroll()
    
    def get_appointment_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """
                SELECT 
                    DATE_FORMAT(AppointmentDate, '%Y-%m-%d') AS Date, 
                    DATE_FORMAT(AppointmentHour, '%H:%i') AS Hour
                from BranchBookings 
                WHERE AppointmentDate >= CURDATE() and PatientId = %s
                ORDER BY AppointmentDate, AppointmentHour ASC LIMIT 1;"""
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    next_date, self.next_hour = result
                    date_object = datetime.strptime(next_date, '%Y-%m-%d')
                    self.formatted_date = date_object.strftime('%A, %d %b %Y')
                else:
                    self.formatted_date = 'No upcoming appointment'
                    self.next_hour = '-'

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_medhistory(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                    CONCAT(d.DiseaseName, ': ', 
                            CASE m.Status 
                                WHEN 0 THEN 'Ongoing'
                                ELSE 'Recovered'
                            END
                        ) AS MedHistory
                    FROM MedicalHistory m JOIN Disease d 
                    ON m.DiseaseId = d.DiseaseId
                    WHERE m.PatientId = %s
                    ORDER BY m.Status ASC;
                """
                cursor.execute(query, (self.user_id,))
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def create_medhist_scroll(self):
        history = self.get_medhistory()
        frame1 = tk.Frame(self)
        frame1.place(x=969, y=392)

        canvas1 = tk.Canvas(frame1, width=310, height=305, bg='white',bd=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white',bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        for i, disease in enumerate(history):           
            label = tk.Label(content1, text=disease, justify='left',
                            font=("Poppins", 14), wraplength=310, fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10))

            separator = tk.Frame(content1, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

    def enable_edit(self, event=None):
        self.name.config(text="Full Name: ")
        self.sex.config(text="Sex: ")
        self.dob.config(text="Date Of Birth: ")
        self.address.config(text="Address: ")
        self.email.config(text="Email: ")
        self.phone.config(text="Phone Number: ")
        self.city.config(text="City: ")

        self.name2.place(x=406, y=330, width=300)
        self.sex2.place(x=337, y=380, width=150)
        self.dob2.place(x=435, y=430, width=300)
        self.email2.place(x=359, y=480, width=300)
        self.phone2.place(x=457, y=530, width=300)
        self.city2.place(x=347, y=580, width=300)
        self.address2.place(x=387, y=630, width=300)

        self.name2.config(state='normal')
        self.name2.insert(0, f'{self.fname_val} {self.lname_val}')
        self.sex2.config(state='readonly')
        self.sex2.set(self.gender)
        self.dob2.config(state='normal')
        self.dob2.insert(0, self.dob_val)

        self.address2.config(state='normal')
        self.address2.insert(0, self.address_val)
        self.email2.config(state='normal')
        self.email2.insert(0, self.email_val)

        self.phone2.config(state='normal')
        self.phone2.insert(0, self.phone_val)
        self.city2.config(state='normal')
        self.city2.insert(0, self.city_val)

        self.edit_button.place_forget()
        self.save_button.place(x=770, y=280, width=60, height=35)
    
    def save_changes(self):
        try:
            updated_name = self.name2.get().strip()
            updated_sex = self.sex2.get().strip()
            updated_dob = self.dob2.get().strip()
            updated_address = self.address2.get().strip()
            updated_email = self.email2.get().strip()
            updated_phone = self.phone2.get().strip()
            updated_city = self.city2.get().strip()

            name_parts = updated_name.split(maxsplit=1)
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            if updated_sex == 'Male': sex_value = 0
            else: sex_value = 1

            if not updated_email or not first_name or not last_name or not updated_phone or not \
                updated_dob or not updated_city or not updated_address or updated_sex is None:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', updated_email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            if not re.match(r'^\d+$', updated_phone):
                messagebox.showerror("Error", "Invalid phone number format!")
                return
            
            try:
                dob_date = datetime.strptime(updated_dob, '%Y-%m-%d').date()  
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
                return

            conn = connect_to_db()
            cursor = conn.cursor()
            check_email_query = "SELECT COUNT(*) FROM `User` WHERE Email = %s AND UserId != %s"
            cursor.execute(check_email_query, (updated_email, self.user_id))
            email_exists = cursor.fetchone()[0] > 0

            if email_exists:
                messagebox.showerror("Error", "The email is already in use by another user.")
                return
            
            query1 = """
                UPDATE `User`
                SET Email = %s, FirstName = %s, LastName = %s, Gender = %s, 
                    PhoneNumber = %s, City = %s, AddressDetail = %s
                WHERE UserId = %s
            """
            values = (updated_email, first_name, last_name, sex_value,
                updated_phone, updated_city, updated_address, self.user_id)

            cursor.execute(query1, values)
            conn.commit()

            query2 = "UPDATE Patient SET DateOfBirth = %s WHERE PatientId = %s"
            cursor.execute(query2, (dob_date, self.user_id))
            conn.commit()
            messagebox.showinfo("Success", "Changes saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

        self.name.config(text=f"Full Name: {updated_name}")
        self.fname_val = first_name
        self.lname_val = last_name

        self.sex.config(text=f"Sex: {updated_sex}")
        self.gender = updated_sex
        self.dob.config(text=f"Date Of Birth: {updated_dob}")
        self.dob_val = updated_dob
        self.address.config(text=f"Address: {updated_address}")
        self.address_val = updated_address

        self.email.config(text=f"Email: {updated_email}")
        self.email_val = updated_email
        self.phone.config(text=f"Phone Number: {updated_phone}")
        self.phone_val = updated_phone
        self.city.config(text=f"City: {updated_city}")
        self.city_val = updated_city

        self.title_label.config(text=f"Welcome, {self.fname_val}")
        self.name_label.config(text=f'{self.fname_val} {self.lname_val}')
        self.email_label.config(text=f"Email: {self.email_val}")

        for entry in [self.name2, self.sex2, self.dob2, self.address2, 
                      self.email2, self.phone2, self.city2]:
            entry.place_forget()
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)

        self.save_button.place_forget()
        self.edit_button.place(x=785, y=280)
    
    def change_profile_pic(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            save_dir = "profile_pictures/patients"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            file_name = os.path.basename(file_path)
            save_path = os.path.join(save_dir, file_name)
            shutil.copy(file_path, save_path)
            self.propic_path = save_path  

            img = Image.open(save_path)
            img = img.resize((150,150), Image.Resampling.LANCZOS)  
            self.profile_pic = ImageTk.PhotoImage(img)
            self.profile_label.config(image=self.profile_pic)
            self.profile_label.image = self.profile_pic
            self.update_pic_database(self.propic_path)

    def remove_profile_pic(self, event=None):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to reset this photo to default?"
        )
        if confirm:
            if self.propic_path and os.path.exists(self.propic_path):
                os.remove(self.propic_path)
                self.propic_path = None

            self.profile_label.config(image=self.default_pic)
            self.profile_label.image = self.default_pic
            self.profile_pic = self.default_pic
            self.update_pic_database(None)

    def update_pic_database(self, file_path):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                if file_path:
                    cursor.execute(
                        "UPDATE Patient SET ProfilePicture = %s WHERE PatientId = %s",
                        (file_path, self.user_id),
                    )
                else:
                    cursor.execute(
                        "UPDATE Patient SET ProfilePicture = NULL WHERE PatientId = %s",
                        (self.user_id,),
                    )

            conn.commit()
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def create_label(self, parent, text, x, y):
        label = tk.Label(parent, text=text, font=("Poppins", 16), bg='white',bd=0, highlightthickness=0)
        label.place(x=x, y=y)
        return label

    def create_entry(self, parent, text, x, y):
        entry = tk.Entry(parent, font=("Poppins", 16), state='disabled', bg='white', highlightthickness=0, bd=0)
        entry.place(x=x, y=y, width=300)
        entry.insert(0, text)
        entry.place_forget()  
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
