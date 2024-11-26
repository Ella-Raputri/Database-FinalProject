import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os
import re
import shutil
from connection import connect_to_db

class AdminPatientPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.name = None
        self.email = None
        self.branch_no = None

        self.patient_id = None
        self.show_pass_img = tk.PhotoImage(file='images/show_pass.png')
        self.hide_pass_img = tk.PhotoImage(file='images/hide_pass.png')

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def get_user_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT Email, FirstName, LastName FROM User WHERE UserId = %s"
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.email, firstname, lastname = result
                    self.name = f"{firstname} {lastname}"
                else:
                    messagebox.showerror("Error", "Invalid user.")
                    return

                query2 = "SELECT BranchNo FROM Admin WHERE AdminId = %s"
                cursor.execute(query2, (self.user_id,))
                result2 = cursor.fetchone()

                if result2: 
                    self.branch_no = result2[0]
                else:
                    messagebox.showerror("Error", "Admin details not found.")
                    return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    
    def navigate_doctor(self):
        self.master.admin_doctor_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_doctor_page)
    
    def navigate_home(self):
        self.master.admin_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_dashboard)
    
    def navigate_booking(self):
        self.master.admin_booking_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_booking_page)
    
    def create_navbar(self):
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                  font=("Poppins Semibold", 18), command=self.navigate_home)
        self.home_btn.place(x=0, y=120, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=23, y=130)

        # doctor
        self.doctor_btn = tk.Button(self, text="Doctor", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18), command=self.navigate_doctor)
        self.doctor_btn.place(x=0, y=183, width=213, height=52)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg='#64C1F6')  
        doctor_label.place(x=23, y=196)

        # patient
        self.patient_btn = tk.Button(self, text="Patient", bd=0,bg=self.master.bg_color1, fg="white", 
                                     font=("Poppins Semibold", 18))
        self.patient_btn.place(x=0, y=243, width=213, height=52)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg=self.master.bg_color1)  
        patient_label.place(x=23, y=255)

        # booking
        self.booking_btn = tk.Button(self, text="Booking", bd=0,bg='#5BB7F4', fg="white", 
                                     font=("Poppins Semibold", 18),command=self.navigate_booking)
        self.booking_btn.place(x=0, y=300, width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#5BB7F4')  
        booking_label.place(x=23, y=311)

    def create_widgets(self):
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/admin_default.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()

        # title
        title_label = tk.Label(self, text="Patients", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=248, y=20)

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select():
            selected_option = combo.get()
            print(f"Selected: {selected_option}")

        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        combo = ttk.Combobox(self, values=options, font=("Poppins", 16),state='readonly')
        combo.set("Filter")  
        combo.place(x=1220, y=112, width=114, height=42)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.filter_img = tk.PhotoImage(file='images/filter_icon.png')
        filter_icon = tk.Label(self, image=self.filter_img)  
        filter_icon.place(x=1182, y=124) 

        # medical panel
        self.medical_panel = tk.Frame(self, bg=self.master.disabled_color,bd=1,relief='groove')
        self.medical_panel.place(x=1170, y=185 + 180 + 10, width=165, height=195)

        self.medical_label = tk.Label(self.medical_panel, text="Med. History", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg=self.master.disabled_color)
        self.medical_label.place(x=10, y=11)
        
        mdview_more_btn = tk.Button(self.medical_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12),state=tk.DISABLED, bd=0, command=self.open_medical)
        mdview_more_btn.place(x=30, y=140, width=110, height=32)

        # add btn
        add_btn = tk.Button(self, text='Add', bg='white',fg=self.master.green_font, 
                            font=('Poppins Medium', 14), bd=0, command=self.add_patient)
        add_btn.place(x=1180, y=590, width=135, height=35)

        # edit btn
        edit_btn = tk.Button(self, text='Edit', bg='white',fg=self.master.yellow_font, 
                             font=('Poppins Medium', 14), bd=0, command=self.edit_patient)
        edit_btn.place(x=1180, y=641, width=135, height=35)

        # delete btn
        delete_btn = tk.Button(self, text='Delete', bg='white',fg=self.master.red_font, 
                               font=('Poppins Medium', 14), bd=0, command=self.delete_patient)
        delete_btn.place(x=1180, y=692, width=135, height=35)

        self.create_table()
    
    def add_patient(self):  
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

        def upload_profile_picture():
            file_path = filedialog.askopenfilename(
                title="Select Profile Picture",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                save_dir = "profile_pictures"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                file_name = os.path.basename(file_path)
                save_path = os.path.join(save_dir, file_name)
                shutil.copy(file_path, save_path)
                self.uploaded_file_path = save_path  

                img = Image.open(save_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  
                self.profile_pic_img = ImageTk.PhotoImage(img)
                self.pict_label.config(image=self.profile_pic_img)
                self.pict_label.image = self.profile_pic_img

                messagebox.showinfo("Success", f"Profile picture uploaded successfully to {save_path}")
            else:
                self.uploaded_file_path = None

        add_window = tk.Toplevel(self)
        add_window.title("Add New Patient")
        add_window.geometry("1011x699")
        add_window.configure(bg="white")

        # Title
        title_label = tk.Label(add_window, text="Add Patient", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=31, y=16)

        # Email
        email_label = tk.Label(add_window, text="Email", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        email_label.place(x=31, y=103)
        self.email_entry = tk.Entry(add_window, font=('Poppins', 14), width=28, bd=1, relief="solid", bg='white')
        self.email_entry.place(x=31, y=144)

        # First Name
        fname_label = tk.Label(add_window, text="First Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        fname_label.place(x=390, y=103)
        self.fname_entry = tk.Entry(add_window, font=('Poppins', 14), width=22, bd=1, relief="solid", bg='white')
        self.fname_entry.place(x=390, y=144)

        # Last Name
        lname_label = tk.Label(add_window, text="Last Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        lname_label.place(x=675, y=103)
        self.lname_entry = tk.Entry(add_window, font=('Poppins', 14), width=24, bd=1, relief="solid", bg='white')
        self.lname_entry.place(x=675, y=144)
        
        # Password
        password_label = tk.Label(add_window, text="Password",font=("Poppins Semibold", 16), 
                               fg=self.master.font_color1, bg='white')
        password_label.place(x=31, y=230)

        self.password_entry = tk.Entry(add_window, font=('Poppins',14), width=28,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=1, bg='white', show='*')
        self.password_entry.place(x=31, y=272)

        show_hide_btn = tk.Button(add_window, image=self.show_pass_img, 
                            bd=0, command=show_hide_password, bg='white')
        show_hide_btn.place(x=322, y=282)

        # Phone Number
        phone_label = tk.Label(add_window, text="Phone Number", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        phone_label.place(x=390, y=228)
        self.phone_entry = tk.Entry(add_window, font=('Poppins', 14), width=27, bd=1, relief="solid", bg='white')
        self.phone_entry.place(x=390, y=271)

        # DOB
        dob_label = tk.Label(add_window, text="Date of Birth", font=("Poppins Semibold",16), fg=self.master.font_color1, bg='white')
        dob_label.place(x=735, y=228)
        self.dob_entry = tk.Entry(add_window, font=('Poppins', 14), width=18, bd=1, relief="solid", bg='white')
        self.dob_entry.place(x=735, y=271)

        # Confirm Password
        confirm_password_label = tk.Label(add_window, text="Confirm Password",font=("Poppins Semibold", 16), 
                               fg=self.master.font_color1, bg='white')
        confirm_password_label.place(x=31, y=365)

        self.confirm_password_entry = tk.Entry(add_window, font=('Poppins',14), width=28,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=1, bg='white', show='*')
        self.confirm_password_entry.place(x=31, y=403)

        confirm_show_hide_btn = tk.Button(add_window, image=self.show_pass_img, 
                            bd=0, command=show_hide_confirm_password, bg='white')
        confirm_show_hide_btn.place(x=322, y=415)

        # City
        city_label = tk.Label(add_window, text="City", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        city_label.place(x=390, y=365)
        self.city_entry = tk.Entry(add_window, font=('Poppins', 14), width=13, bd=1, relief="solid", bg='white')
        self.city_entry.place(x=390, y=403)

        # Gender
        gender_label = tk.Label(add_window, text="Gender", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        gender_label.place(x=572, y=365)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.gender_combobox = ttk.Combobox(add_window, font=('Poppins', 14), width=8, state="readonly", style="Custom.TCombobox")
        self.gender_combobox['values'] = ("Male", "Female")
        self.gender_combobox.place(x=572, y=403)
        self.gender_combobox.set("Select")    

        # Profile
        profile_label = tk.Label(add_window, text="Profile Picture", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        profile_label.place(x=715, y=365)

        self.pict_label = tk.Label(add_window, bg='white', width=100, height=100)
        self.pict_label.place(x=890, y=365)

        upload_button = tk.Button(
            add_window, text="Upload", font=("Poppins", 12), bg='grey', fg='white',
            bd=0, command=upload_profile_picture
        )
        upload_button.place(x=715, y=403, width=130, height=43)

        # Address
        address_label = tk.Label(add_window, text="Address Details", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        address_label.place(x=31, y=489)
        self.address_entry = tk.Entry(add_window, font=('Poppins', 14), width=36, bd=1, relief="solid", bg='white')
        self.address_entry.place(x=31, y=532)

        # Save Button
        def save_doctor():
            email = self.email_entry.get().strip()
            first_name = self.fname_entry.get().strip()
            last_name = self.lname_entry.get().strip()
            
            password = self.password_entry.get().strip()
            phone = self.phone_entry.get().strip()
            dob = self.dob_entry.get().strip()

            conf_password = self.confirm_password_entry.get().strip()
            gender_val = self.gender_combobox.get().strip()
            city = self.city_entry.get().strip()
            profile_picture_path = getattr(self, "uploaded_file_path", None)
            profile_picture_path = profile_picture_path or ""

            address = self.address_entry.get().strip()

            if gender_val == 'Male': gender = 0
            elif gender_val == 'Female': gender = 1
            else: 
                messagebox.showerror("Error", "Invalid gender!")
                return

            if not email or not password or not conf_password or not first_name \
                or not last_name or not phone or not city or not address \
                or gender is None:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            if password != conf_password:
                messagebox.showerror("Error", "Please reconfirm your password!")
                return
            if not re.match(r'^\d+$', phone):
                messagebox.showerror("Error", "Invalid phone number format!")
                return

            try:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()  
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
                return

            try:
                conn = connect_to_db()
                cursor = conn.cursor()

                cursor.execute("SELECT PatientId FROM Patient ORDER BY PatientId DESC LIMIT 1")
                last_patient_id = cursor.fetchone()
                if last_patient_id:
                    last_id = last_patient_id[0]
                    numeric_part = int(last_id[3:])  
                    new_numeric_part = numeric_part + 1
                else:
                    new_numeric_part = 1

                new_patient_id = f'PAT{str(new_numeric_part).zfill(7)}'

                query1 = """
                    INSERT INTO User (UserId, Email, Password, FirstName, LastName, 
                    Gender, PhoneNumber, RoleName, City, AddressDetail, IsDeleted)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query1, (new_patient_id, email, password, first_name, last_name,
                                        gender, phone, "Patient", city, address, 0))
                conn.commit()

                query2 = """
                    INSERT INTO Patient (PatientId, DateOfBirth, ProfilePicture, IsDeleted)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query2, (new_patient_id, dob_date, profile_picture_path, 0))
                conn.commit()

                messagebox.showinfo("Success", "Patient added successfully!")

            except Exception as e:
                print(f"Error occurred: {e}")
                messagebox.showerror("Error", f"Failed to add patient: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                add_window.destroy()

        save_button = tk.Button(add_window, text="Save", bg=self.master.bg_color1, fg='white', font=("Poppins", 16), bd=0, command=save_doctor)
        save_button.place(x=826, y=623, width=110, height=45)

    def edit_patient(self):
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

        def upload_profile_picture():
            file_path = filedialog.askopenfilename(
                title="Select Profile Picture",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                save_dir = "profile_pictures"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                file_name = os.path.basename(file_path)
                save_path = os.path.join(save_dir, file_name)
                shutil.copy(file_path, save_path)
                self.uploaded_file_path = save_path  

                img = Image.open(save_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  
                self.profile_pic_img = ImageTk.PhotoImage(img)
                self.pict_label.config(image=self.profile_pic_img)
                self.pict_label.image = self.profile_pic_img

                messagebox.showinfo("Success", f"Profile picture uploaded successfully to {save_path}")
            else:
                self.uploaded_file_path = None
        
        if not self.patient_id:
            messagebox.showerror("Error", "Please select a patient first!")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                u.Email, u.Password, u.FirstName, u.LastName, u.Gender, u.PhoneNumber, u.City, u.AddressDetail,
                p.DateOfBirth, p.ProfilePicture
            FROM User u JOIN Patient p ON u.UserId = p.PatientId WHERE u.UserId = %s
        """
        cursor.execute(query, (self.patient_id,))
        patient_data = cursor.fetchone()
        conn.close()

        if not patient_data:
            messagebox.showerror("Error", "Patient not found!")
            return

        email, password, first_name, last_name, gender, phone, city, address, \
        date_of_birth, profile_picture_path = (
            patient_data[0], patient_data[1], patient_data[2], patient_data[3], patient_data[4],
            patient_data[5], patient_data[6], patient_data[7], patient_data[8], patient_data[9]
        )
        gender_str = "Male" if gender == 0 else "Female"

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Patient")
        edit_window.geometry("1011x699")
        edit_window.configure(bg="white")

        # Title
        title_label = tk.Label(edit_window, text="Edit Patient", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=31, y=16)

        # Email
        email_label = tk.Label(edit_window, text="Email", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        email_label.place(x=31, y=103)
        self.email_entry = tk.Entry(edit_window, font=('Poppins', 14), width=28, bd=1, relief="solid", bg='white')
        self.email_entry.insert(0, email)
        self.email_entry.place(x=31, y=144)

        # First Name
        fname_label = tk.Label(edit_window, text="First Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        fname_label.place(x=390, y=103)
        self.fname_entry = tk.Entry(edit_window, font=('Poppins', 14), width=22, bd=1, relief="solid", bg='white')
        self.fname_entry.insert(0, first_name)
        self.fname_entry.place(x=390, y=144)

        # Last Name
        lname_label = tk.Label(edit_window, text="Last Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        lname_label.place(x=675, y=103)
        self.lname_entry = tk.Entry(edit_window, font=('Poppins', 14), width=24, bd=1, relief="solid", bg='white')
        self.lname_entry.insert(0, last_name)
        self.lname_entry.place(x=675, y=144)
        
        # Password
        password_label = tk.Label(edit_window, text="Password",font=("Poppins Semibold", 16), 
                               fg=self.master.font_color1, bg='white')
        password_label.place(x=31, y=230)

        self.password_entry = tk.Entry(edit_window, font=('Poppins',14), width=28,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=1, bg='white', show='*')
        self.password_entry.insert(0, password)
        self.password_entry.place(x=31, y=272)

        show_hide_btn = tk.Button(edit_window, image=self.show_pass_img, 
                            bd=0, command=show_hide_password, bg='white')
        show_hide_btn.place(x=322, y=282)

        # Phone Number
        phone_label = tk.Label(edit_window, text="Phone Number", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        phone_label.place(x=390, y=228)
        self.phone_entry = tk.Entry(edit_window, font=('Poppins', 14), width=27, bd=1, relief="solid", bg='white')
        self.phone_entry.insert(0, phone)
        self.phone_entry.place(x=390, y=271)

        # DOB
        dob_label = tk.Label(edit_window, text="Date of Birth", font=("Poppins Semibold",16), fg=self.master.font_color1, bg='white')
        dob_label.place(x=735, y=228)
        self.dob_entry = tk.Entry(edit_window, font=('Poppins', 14), width=18, bd=1, relief="solid", bg='white')
        self.dob_entry.insert(0, date_of_birth)
        self.dob_entry.place(x=735, y=271)

        # Confirm Password
        confirm_password_label = tk.Label(edit_window, text="Confirm Password",font=("Poppins Semibold", 16), 
                               fg=self.master.font_color1, bg='white')
        confirm_password_label.place(x=31, y=365)

        self.confirm_password_entry = tk.Entry(edit_window, font=('Poppins',14), width=28,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=1,
                        bd=1, bg='white', show='*')
        self.confirm_password_entry.insert(0, password)
        self.confirm_password_entry.place(x=31, y=403)

        confirm_show_hide_btn = tk.Button(edit_window, image=self.show_pass_img, 
                            bd=0, command=show_hide_confirm_password, bg='white')
        confirm_show_hide_btn.place(x=322, y=415)

        # City
        city_label = tk.Label(edit_window, text="City", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        city_label.place(x=390, y=365)
        self.city_entry = tk.Entry(edit_window, font=('Poppins', 14), width=13, bd=1, relief="solid", bg='white')
        self.city_entry.insert(0, city)
        self.city_entry.place(x=390, y=403)

        # Gender
        gender_label = tk.Label(edit_window, text="Gender", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        gender_label.place(x=572, y=365)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.gender_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=8, state="readonly", style="Custom.TCombobox")
        self.gender_combobox['values'] = ("Male", "Female")
        self.gender_combobox.place(x=572, y=403)
        self.gender_combobox.set(gender_str)    

        # Profile
        profile_label = tk.Label(edit_window, text="Profile Picture", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        profile_label.place(x=715, y=365)

        self.pict_label = tk.Label(edit_window, bg='white', width=100, height=100)
        self.pict_label.place(x=890, y=365)

        upload_button = tk.Button(
            edit_window, text="Upload", font=("Poppins", 12), bg='grey', fg='white',
            bd=0, command=upload_profile_picture
        )
        upload_button.place(x=715, y=403, width=130, height=43)

        if profile_picture_path:
            img = Image.open(profile_picture_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            profile_pic_img = ImageTk.PhotoImage(img)
            self.pict_label.config(image=profile_pic_img)
            self.pict_label.image = profile_pic_img

        # Address
        address_label = tk.Label(edit_window, text="Address Details", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        address_label.place(x=31, y=489)
        self.address_entry = tk.Entry(edit_window, font=('Poppins', 14), width=36, bd=1, relief="solid", bg='white')
        self.address_entry.insert(0, address)
        self.address_entry.place(x=31, y=532)

        # Save Button
        def update_patient():
            updated_email = self.email_entry.get().strip()
            updated_first_name = self.fname_entry.get().strip()
            updated_last_name = self.lname_entry.get().strip()
            updated_password = self.password_entry.get().strip()
            updated_conf_password = self.confirm_password_entry.get().strip()
            updated_phone = self.phone_entry.get().strip()
            updated_dob = self.dob_entry.get().strip()
            updated_gender_val = self.gender_combobox.get().strip()
            updated_city = self.city_entry.get().strip()
            updated_address = self.address_entry.get().strip()
            updated_profile_picture_path = getattr(self, "uploaded_file_path", None)
            updated_profile_picture_path = updated_profile_picture_path or ""

            updated_gender = 0 if updated_gender_val == "Male" else 1            

            if not updated_email or not updated_password or not updated_conf_password or not updated_first_name \
                or not updated_last_name or not updated_phone or not updated_dob or not updated_city \
                or not updated_address or not updated_gender:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', updated_email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            if updated_password != updated_conf_password:
                messagebox.showerror("Error", "Please reconfirm your password!")
                return
            if not re.match(r'^\d+$', updated_phone):
                messagebox.showerror("Error", "Invalid phone number format!")
                return
            try:
                updated_dob_date = datetime.strptime(updated_dob, '%Y-%m-%d').date()  
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
                return

            try:
                conn = connect_to_db()
                cursor = conn.cursor()

                # Update User table
                query1 = """
                    UPDATE User
                    SET Email = %s, Password = %s, FirstName = %s, LastName = %s,
                        Gender = %s, PhoneNumber = %s, City = %s, AddressDetail = %s
                    WHERE UserId = %s
                """
                cursor.execute(query1, (updated_email, updated_password, updated_first_name, updated_last_name,
                                        updated_gender, updated_phone, updated_city, updated_address, self.patient_id))

                # Update Doctor table
                query2 = """
                    UPDATE Patient
                    SET DateOfBirth = %s, ProfilePicture = %s
                    WHERE PatientId = %s
                """
                cursor.execute(query2, (updated_dob_date, updated_profile_picture_path,self.patient_id))

                conn.commit()
                messagebox.showinfo("Success", "Patient updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                edit_window.destroy()

        # Save Button
        save_button = tk.Button(edit_window, text="Save", bg=self.master.bg_color1, 
                                fg='white', font=("Poppins", 16), bd=0, command=update_patient)
        save_button.place(x=826, y=623, width=110, height=45)

    def delete_patient(self):
        if not self.patient_id:
            messagebox.showerror("Error", "Please select a patient first!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the patient '{self.patient_id}'?"
        )

        if confirm:
            try:
                conn = connect_to_db()
                if not conn:
                    messagebox.showerror("Error", "Database connection failed.")
                    return

                with conn.cursor() as cursor:
                    query = "UPDATE `User` SET IsDeleted = 1 WHERE UserId = %s;"
                    cursor.execute(query, (self.patient_id,))
                    conn.commit()

                    query = "UPDATE Patient SET IsDeleted = 1 WHERE PatientId = %s;"
                    cursor.execute(query, (self.patient_id,))
                    conn.commit()

                    query = """UPDATE Booking SET AppointmentStatus = 'Cancelled' WHERE PatientId = %s 
                        AND AppointmentStatus = 'Pending';"""
                    cursor.execute(query, (self.patient_id,))
                    conn.commit()
                                        
                    messagebox.showinfo("Success", f"Patient '{self.patient_id}' has been deleted.") 

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()


    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """
                    SELECT 
                        p.PatientId,
                        p.DateOfBirth,
                        u.Email,
                        CONCAT(u.FirstName, ' ', u.LastName) AS Name,
                        CASE u.Gender 
                            WHEN 0 THEN 'Male'
                            ELSE 'Female'
                        END AS Gender,
                        u.PhoneNumber,
                        u.City,
                        u.AddressDetail AS Address,
                        COUNT(b.BookingId) AS TotalBookings
                    FROM 
                        Patient p
                    LEFT JOIN 
                        `User` u ON p.PatientId = u.UserId
                    LEFT JOIN 
                        Booking b ON p.PatientId = b.PatientId
                    WHERE 
                        p.IsDeleted = 0 
                    GROUP BY 
                        p.PatientId, u.Email, u.FirstName, u.LastName,
                        u.Gender, u.PhoneNumber, u.City, u.AddressDetail
                    ORDER BY 
                        p.PatientId;                
                """
                cursor.execute(query1)
                result = cursor.fetchall()
                return result  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def create_table(self):
        self.data = self.get_table_data()
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Semibold", 14))
        style.configure("Treeview", rowheight=40, font=("Poppins", 12))

        table_frame = tk.Frame(self)
        table_frame.place(x=248, y=114, width=900, height=610)

        columns = ['PatientId','Date of Birth','Email','Name','Gender','Phone Number',
                   'City','Address','Total Bookings']  
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=200, anchor=tk.CENTER)

        for i, row in enumerate(self.data):
            tags = "odd_row" if i % 2 == 0 else "even_row"
            self.table.insert("", tk.END, values=row, tags=(tags,))
        
        self.table.tag_configure("odd_row", background="#f2f7fd", font=("Poppins", 12))
        self.table.tag_configure("even_row", background="white", font=("Poppins", 12))

        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<<TreeviewSelect>>", lambda event: self.update_medical_panel(event))

    def update_medical_panel(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item[0])
            self.patient_id = item['values'][0]
            self.history = self.get_medhistory()
            self.patient_name = item['values'][3]

            for widget in self.medical_panel.winfo_children():
                widget.destroy()  

            self.medical_panel.config(bg='white')
            self.medical_label = tk.Label(self.medical_panel, text="Med. History", 
                                           font=("Poppins Semibold", 15), fg=self.master.font_color2, bg='white')
            self.medical_label.place(x=6, y=11)

            if self.history:
                for i, entry in enumerate(self.history[:3]):  
                    label = tk.Label(self.medical_panel, text=f"• {entry}", font=("Poppins", 10), bg="white", anchor="w")
                    label.place(x=6, y=49 + i * 25)
            else:
                label = tk.Label(self.medical_panel, text="No history", font=("Poppins", 10), bg="white", anchor="w")
                label.place(x=6, y=49)
            
            self.mdview_more_btn = tk.Button(self.medical_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11), command=self.open_medical,bd=0)
            self.mdview_more_btn.place(x=30, y=135, width=110, height=26)

    def get_medhistory(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                    CONCAT(DiseaseName, ': ', 
                            CASE Status 
                                WHEN 0 THEN 'Ongoing'
                                ELSE 'Recovered'
                            END
                        ) AS MedHistory
                    FROM MedicalHistory
                    WHERE PatientId = %s
                    ORDER BY Status ASC;
                """
                cursor.execute(query, (self.patient_id,))
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def open_medical(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Medical History")
        child_window.geometry("533x676")  

        # medical label
        mhtitle_label = tk.Label(child_window, text=f"{self.patient_name.split()[0]} Medical History",font=("Poppins Semibold", 24), 
                                 fg='black', bg='white')
        mhtitle_label.place(x=25, y=18)

        # scrollpane 
        frame1 = tk.Frame(child_window, bd=1, highlightthickness=1)
        frame1.place(x=26, y=100)

        canvas1 = tk.Canvas(frame1, width=470, height=486, bg='white')
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white')
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        self.delete_photo = tk.PhotoImage(file='images/delete_icon.png')
        self.edit_photo = tk.PhotoImage(file='images/edit_icon.png')

        for i, entry in enumerate(self.history):
            disease = entry.split(':')[0].strip()
            status = entry.split()[-1].strip()
    
            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=disease, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                   command=lambda disease=disease, status=status, 
                                   child_window=child_window: self.edit_medhist(disease, status, child_window))
            edit_button.grid(row=0, column=1, padx=(0, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda disease=disease, child_window=child_window: 
                                    self.delete_medhist(disease, child_window))
            delete_button.grid(row=0, column=2, padx=(0, 5), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text=status,
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w",padx=(5, 10), pady=(0, 10))
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=self.add_medhist)
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=206, y=615, width=116, height=40)

        child_window.resizable(False, False)

    def add_medhist(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Medical History")
        add_window.geometry("500x400")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Disease Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        disease_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        disease_entry.pack(pady=5)

        tk.Label(add_window, text="Status:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        status_entry = ttk.Combobox(add_window, values=["Ongoing","Recovered"], 
                                font=("Poppins", 12), state="readonly", width=28)
        status_entry.pack(pady=5)

        def save_medhist():
            disease = disease_entry.get().strip()
            status_val = status_entry.get().strip()

            if status_val == "Ongoing": status = 0
            elif status_val == "Recovered": status = 1 
            else: status = None

            print(disease, status)

            if not disease or status is None:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    check_query = """
                        SELECT COUNT(*)
                        FROM MedicalHistory
                        WHERE PatientId = %s AND DiseaseName = %s
                    """
                    cursor.execute(check_query, (self.patient_id, disease))
                    exists = cursor.fetchone()[0]

                    if exists:
                        messagebox.showerror("Error", "This medical history already exists!")
                        return

                    query = """
                        INSERT INTO MedicalHistory (PatientId, DiseaseName, Status)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (self.patient_id, disease, status))
                    conn.commit()
                    messagebox.showinfo("Success", "New medical history added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add medical history: {e}")
            finally:
                if conn:
                    conn.close()
                add_window.destroy()
                self.history = self.get_medhistory()
                self.open_medical()  
                self.update_medical_panel() 

        save_button = tk.Button(add_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_medhist)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def edit_medhist(self, curr_disease, curr_status, mhwindow):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Schedule")
        edit_window.geometry("500x400")
        edit_window.configure(bg="white")

        tk.Label(edit_window, text="Disease Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        disease_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        disease_entry.pack(pady=5)
        disease_entry.insert(0, curr_disease)

        tk.Label(edit_window, text="Status:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        status_entry = ttk.Combobox(edit_window, values=["Ongoing", "Recovered"], 
                                font=("Poppins", 12), state="readonly", width=28)
        status_entry.pack(pady=5)
        status_entry.set(curr_status)
        
        def save_changes():
            new_disease = disease_entry.get().strip()
            new_status_val = status_entry.get().strip()

            if new_status_val == "Ongoing": new_status = 0
            elif new_status_val == "Recovered": new_status = 1 
            else: new_status = None

            if not new_disease or new_status is None:
                messagebox.showerror("Error", "All fields are required!")
                edit_window.destroy()
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    if new_disease != curr_disease:
                        check_query = """
                            SELECT COUNT(*)
                            FROM MedicalHistory
                            WHERE PatientId = %s AND DiseaseName = %s
                        """
                        cursor.execute(check_query, (self.patient_id, new_disease))
                        exists = cursor.fetchone()[0]

                        if exists:
                            messagebox.showerror("Error", "This disease name already exists for the patient!")
                            return

                    # Update the record
                    update_query = """
                        UPDATE MedicalHistory
                        SET DiseaseName = %s, Status = %s
                        WHERE PatientId = %s AND DiseaseName = %s
                    """
                    cursor.execute(update_query, (new_disease, new_status, self.patient_id, curr_disease))
                    conn.commit()
                    messagebox.showinfo("Success", "Medical history updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update schedule: {e}")
            finally:
                if conn:
                    conn.close()
                    
                edit_window.destroy()
                mhwindow.destroy()  
                self.history = self.get_medhistory()
                self.open_medical()  
                self.update_medical_panel() 

        save_button = tk.Button(edit_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_changes)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def delete_medhist(self, disease, mhwindow):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this medical history?"
                )
                if confirm:
                    query = "DELETE FROM MedicalHistory WHERE PatientId = %s AND DiseaseName = %s"
                    cursor.execute(query, (self.patient_id, disease))
                    conn.commit()
                    messagebox.showinfo("Success", "Medical history deleted successfully!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting: {e}")
        finally:
            if conn:
                conn.close()
            mhwindow.destroy()  
            self.history = self.get_medhistory()
            self.open_medical() 
            self.update_medical_panel()

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  # Scroll up
            canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            canvas.yview_scroll(1, "units")
    
    