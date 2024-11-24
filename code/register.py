import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime
from tkinter import messagebox
from connection import connect_to_db
import mysql.connector

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.show_pass_img = tk.PhotoImage(file='images/show_pass.png')
        self.hide_pass_img = tk.PhotoImage(file='images/hide_pass.png')
        self.create_widgets()
    

    def create_widgets(self):
        def show_hide_password():
            if self.password_entry['show'] == '*':
                self.password_entry.config(show='')
                show_hide_btn.config(image=self.hide_pass_img)
            else:
                self.password_entry.config(show='*')
                show_hide_btn.config(image=self.show_pass_img)
        
        def show_hide_confirm_password():
            if self.confirm_password_entry['show'] == '*':
                self.confirm_password_entry.config(show='')
                confirm_show_hide_btn.config(image=self.hide_pass_img)
            else:
                self.confirm_password_entry.config(show='*')
                confirm_show_hide_btn.config(image=self.show_pass_img)

        # background
        self.background_photo = tk.PhotoImage(file='images/signup_bg.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        title_label = tk.Label(self, text="Register", font=("Poppins", 40, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=111, y=85)

        # instruction
        instruction_label = tk.Label(self, text="Please fill in the required information.",
                                     font=("Poppins", 16), fg=self.master.font_color1, 
                                     bg='white')
        instruction_label.place(x=111, y=163)
        
        # email field
        email_label = tk.Label(self, text="Email",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        email_label.place(x=111, y=232)

        self.email_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.email_entry.place(x=111, y=273)


        # password field
        password_label = tk.Label(self, text="Password",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        password_label.place(x=111, y=359)

        self.password_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white', show='*')
        self.password_entry.place(x=111, y=401)

        show_hide_btn = tk.Button(self, image=self.show_pass_img, 
                            bd=0, command=show_hide_password, bg='white')
        show_hide_btn.place(x=565, y=412)


        # confirm password field
        confirm_password_label = tk.Label(self, text="Confirm Password",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        confirm_password_label.place(x=111, y=494)

        self.confirm_password_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white', show='*')
        self.confirm_password_entry.place(x=111, y=532)

        confirm_show_hide_btn = tk.Button(self, image=self.show_pass_img, 
                            bd=0, command=show_hide_confirm_password, bg='white')
        confirm_show_hide_btn.place(x=565, y=544)


        # login label
        login_label = tk.Label(self, text="Already have an account?",
                                     font=("Poppins", 16), fg=self.master.font_color1, 
                                     bg='white', justify='center')
        login_label.place(x=136, y=645)

        # here label
        here_label = tk.Label(self, text="Login here",
                                     font=("Poppins", 16, 'underline'), fg=self.master.font_color1, 
                                     bg='white', justify='center', cursor="hand2")
        here_label.place(x=415, y=645)
        here_label.bind("<Button-1>", self.click_label_login)


        # fname field
        fname_label = tk.Label(self, text="First Name",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        fname_label.place(x=679, y=102)

        self.fname_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.fname_entry.place(x=679, y=145)


        # lname field
        lname_label = tk.Label(self, text="Last Name",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        lname_label.place(x=978, y=102)

        self.lname_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.lname_entry.place(x=978, y=145)

        # phone field
        phone_label = tk.Label(self, text="Phone Number",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        phone_label.place(x=679, y=230)

        self.phone_entry = tk.Entry(self, font=('Poppins',16), width=28,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.phone_entry.place(x=679, y=273)


        # gender option
        gender_label = tk.Label(self, text="Gender", font=("Poppins Semibold", 18),
                        fg=self.master.font_color1, bg='white')
        gender_label.place(x=1080, y=230)

        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 16))
        self.gender_combobox = ttk.Combobox(self, font=('Poppins', 16), width=10,
                                            state="readonly",style="Custom.TCombobox")  
        self.gender_combobox['values'] = ("Male", "Female")  
        self.gender_combobox.place(x=1080, y=273)
        self.gender_combobox.set("Select")


        # dob field
        dob_label = tk.Label(self, text="Date of Birth",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        dob_label.place(x=679, y=358)

        self.dob_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.dob_entry.place(x=679, y=401)


        # city field
        city_label = tk.Label(self, text="City",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        city_label.place(x=978, y=358)

        self.city_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.city_entry.place(x=978, y=401)

        # address field
        address_label = tk.Label(self, text="Address Details",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        address_label.place(x=679, y=494)

        self.address_entry = tk.Entry(self, font=('Poppins',16), width=42,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=0, bg='white')
        self.address_entry.place(x=679, y=532)


        # submit btn
        submit_btn = tk.Button(self, text='Submit', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins Semibold', 18), bd=0, command=self.register_user)
        submit_btn.place(x=1120, y=635, width=128, height=49)
    

    def register_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        conf_password = self.confirm_password_entry.get().strip()
        fname = self.fname_entry.get().strip()
        lname = self.lname_entry.get().strip()
        phone_num = self.phone_entry.get().strip()
        gender_val = self.gender_combobox.get()
        dob = self.dob_entry.get().strip()
        city = self.city_entry.get().strip()
        address = self.address_entry.get().strip()        
        
        if not email or not password or not conf_password or not fname \
            or not lname or not phone_num or not dob or not city or not address:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        if password != conf_password:
            messagebox.showerror("Error", "Please reconfirm your password!")
            return
        if not re.match(r'^\d+$', phone_num):
            messagebox.showerror("Error", "Invalid phone number format!")
            return
        
        gender = None
        if gender_val == 'Male': gender = 0
        elif gender_val == 'Female': gender = 1
        else: 
            messagebox.showerror("Error", "Invalid gender!")
            return

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()  
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT PatientID FROM Patient ORDER BY PatientID DESC LIMIT 1")
            last_patient_id = cursor.fetchone()

            if last_patient_id:
                last_id = last_patient_id[0]  
                numeric_part = int(last_id[3:])  
                new_numeric_part = numeric_part + 1
            else:
                new_numeric_part = 1
            
            new_patient_id = f"PAT{str(new_numeric_part).zfill(7)}"  
            print(f"New: {new_patient_id}")

            # insert to user
            query = """INSERT INTO User (UserId, Email, Password, FirstName, LastName, Gender,
                    PhoneNumber, RoleName, City, AddressDetail)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (new_patient_id, email, password, fname, lname, gender, phone_num, 
                                   'Patient', city, address))
            conn.commit()

            # insert to patient
            patient_query = """INSERT INTO Patient (PatientID, DateOfBirth, ProfilePicture)
                            VALUES (%s, %s, %s)"""
            cursor.execute(patient_query, (new_patient_id, dob_date, None))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.master.show_frame(self.master.admin_dashboard)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error inserting data: {err}")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()


    def click_label_login(self, event):
        self.master.show_frame(self.master.login_page)