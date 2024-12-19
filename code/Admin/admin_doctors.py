import tkinter as tk
from tkinter import messagebox,ttk, filedialog
from PIL import Image, ImageTk
import os
import re
import shutil
from connection import connect_to_db

class AdminDoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None
        self.branch_no = None

        self.table = None
        self.specialty_data = None
        self.doctor_id = None
        self.doctor_name = None

        self.show_pass_img = tk.PhotoImage(file='images/show_pass.png')
        self.hide_pass_img = tk.PhotoImage(file='images/hide_pass.png')
        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((100, 100)))
        self.delete_pic = ImageTk.PhotoImage(Image.open("images/delete_icon.png"))

        self.filter_field = 'd.DoctorId'
        self.sort_order = 'ASC'

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
    
    def navigate_home(self):
        self.master.admin_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_dashboard)
    
    def navigate_patient(self):
        self.master.admin_patient_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_patient_page)
    
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
        self.doctor_btn = tk.Button(self, text="Doctor", bd=0,bg=self.master.bg_color1, fg="white", 
                                    font=("Poppins Semibold", 18))
        self.doctor_btn.place(x=0, y=183,  width=213, height=52)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg=self.master.bg_color1)  
        doctor_label.place(x=23, y=196)

        # patient
        self.patient_btn = tk.Button(self, text="Patient", bd=0,bg='#5FBBF5', fg="white", 
                                    font=("Poppins Semibold", 18), command=self.navigate_patient)
        self.patient_btn.place(x=0, y=243, width=213, height=52)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg='#5FBBF5')  
        patient_label.place(x=23, y=255)

        # booking
        self.booking_btn = tk.Button(self, text=" Booking", bd=0,bg='#5BB7F4', fg="white", 
                                    font=("Poppins Semibold", 18),command=self.navigate_booking)
        self.booking_btn.place(x=0, y=300, width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#5BB7F4')  
        booking_label.place(x=23, y=311)

    def create_widgets(self):
        # background
        self.background_photo = tk.PhotoImage(file='images/admin_default.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()

        # title
        title_label = tk.Label(self, text="Doctors", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=248, y=20)

        self.get_user_info()

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select(event):
            selected_option = combo.get()
            if selected_option == 'DoctorId': selected_option = 'd.DoctorId' 
            elif selected_option == 'Spec.Name': selected_option = 's.SpecialtyName' 

            self.filter_field = selected_option  
            self.create_table()

        options = ["DoctorId", "Name", "Spec.Name", "TotalBookings", "ThisMonthsBookings"]
        combo = ttk.Combobox(self, values=options, font=("Poppins", 12), state='readonly')
        combo.set("Filter")
        combo.place(x=1214, y=112, width=135, height=42)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.sort_img = tk.PhotoImage(file='images/sort_ascending.png')  
        sort_icon = tk.Label(self, image=self.sort_img)
        sort_icon.place(x=1182, y=124)

        def toggle_sort():
            if self.sort_order == 'ASC':
                self.sort_order = 'DESC'
                self.sort_img = tk.PhotoImage(file='images/sort_descending.png')
            else:
                self.sort_order = 'ASC'
                self.sort_img = tk.PhotoImage(file='images/sort_ascending.png')
            sort_icon.config(image=self.sort_img)
            self.create_table() 

        sort_icon.bind("<Button-1>", lambda e: toggle_sort()) 

        # specialty panel
        self.specialty_panel = tk.Frame(self, bg='white',bd=1,relief='groove')
        self.specialty_panel.place(x=1170, y=180, width=165, height=215)

        self.specialty_label = tk.Label(self.specialty_panel, text="Specialty", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg='white')
        self.specialty_label.place(x=10, y=11)

        splist = self.get_specialty_list()

        if len(splist) >= 4:
            for i in range(3):  
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  
        else:
            for i in range(len(splist)): 
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  

        
        spview_more_btn = tk.Button(self.specialty_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0, command=self.open_specialties)
        spview_more_btn.place(x=30, y=161, width=110, height=32)


        # schedule panel
        self.schedule_panel = tk.Frame(self, bg=self.master.disabled_color,bd=1,relief='groove')
        self.schedule_panel.place(x=1170, y=180 + 215 + 10, width=165, height=165)

        self.schedule_label = tk.Label(self.schedule_panel, text="Schedule", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg=self.master.disabled_color)
        self.schedule_label.place(x=10, y=11)

        
        self.scview_more_btn = tk.Button(self.schedule_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11),state=tk.DISABLED)
        self.scview_more_btn.place(x=30, y=120, width=110, height=32)

        # add btn
        add_btn = tk.Button(self, text='Add', bg='white', fg=self.master.green_font, 
                            font=('Poppins Medium', 14), bd=0, command=self.add_doctor)
        add_btn.place(x=1180, y=590, width=135, height=35)

        # edit btn
        edit_btn = tk.Button(self, text='Edit', bg='white', fg=self.master.yellow_font, 
                             font=('Poppins Medium', 14), bd=0, command=self.edit_doctor)
        edit_btn.place(x=1180, y=641, width=135, height=35)

        # delete btn
        delete_btn = tk.Button(self, text='Delete', bg='white', fg=self.master.red_font, 
                               font=('Poppins Medium', 14), bd=0, command=self.delete_doctor)
        delete_btn.place(x=1180, y=692, width=135, height=35)

        self.create_table()

    def update_specialty_panel(self):
        for widget in self.specialty_panel.winfo_children():
            widget.destroy()

        self.specialty_label = tk.Label(self.specialty_panel, text="Specialty", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg='white')
        self.specialty_label.place(x=10, y=11)

        splist = self.get_specialty_list()

        if len(splist) >= 4:
            for i in range(3):  
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  
        else:
            for i in range(len(splist)): 
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  

        spview_more_btn = tk.Button(self.specialty_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0, command=self.open_specialties)
        spview_more_btn.place(x=30, y=161, width=110, height=32)

    def populate_specialty_combobox(self):
        try:
            conn = connect_to_db() 
            cursor = conn.cursor()
            cursor.execute("SELECT SpecialtyId, SpecialtyName FROM Specialty")
            specialties = cursor.fetchall()

            specialty_names = [specialty[1] for specialty in specialties]
            self.specialty_combobox['values'] = specialty_names
            self.specialty_id_map = {specialty[1]: specialty[0] for specialty in specialties}

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch specialties: {e}")
        finally:
            if conn:
                conn.close()

    def edit_doctor(self):
        if not self.doctor_id:
            messagebox.showerror("Error", "Please select a doctor first!")
            return
        
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
                save_dir = "profile_pictures/doctors"
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

        conn = connect_to_db()
        cursor = conn.cursor()
        # UserId, 
        query = """
            SELECT 
                u.Email, u.Password, u.FirstName, u.LastName, u.Gender, u.PhoneNumber, u.City, u.AddressDetail,
                d.SpecialtyId, d.ProfilePicture, d.Description
            FROM User u JOIN Doctor d ON u.UserId = d.DoctorId WHERE u.UserId = %s
        """
        cursor.execute(query, (self.doctor_id,))
        doctor_data = cursor.fetchone()
        conn.close()

        if not doctor_data:
            messagebox.showerror("Error", "Doctor not found!")
            return

        email, password, first_name, last_name, gender, phone, city, address, \
        spid, profile_picture_path, description = (
            doctor_data[0], doctor_data[1], doctor_data[2], doctor_data[3], doctor_data[4],
            doctor_data[5], doctor_data[6], doctor_data[7], doctor_data[8],
            doctor_data[9], doctor_data[10]
        )

        # Gender mapping
        gender_str = "Male" if gender == 0 else "Female"

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Doctor")
        edit_window.geometry("1011x699")
        edit_window.configure(bg="white")

        # Title
        title_label = tk.Label(edit_window, text="Edit Doctor", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
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

        # Specialty
        specialty_label = tk.Label(edit_window, text="Specialty", font=("Poppins Semibold",16), fg=self.master.font_color1, bg='white')
        specialty_label.place(x=735, y=228)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.specialty_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=18, state="readonly", style="Custom.TCombobox")
        self.populate_specialty_combobox()
        self.specialty_combobox.place(x=735, y=271)

        spname = "Select"
        for name, id_ in self.specialty_id_map.items():
            if id_ == spid:
                spname = name
                break
        self.specialty_combobox.set(spname)

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

        self.pict_label = tk.Label(edit_window, bg='white', image=self.default_pic, width=100, height=100)
        self.pict_label.place(x=890, y=365)
        self.pict_label.image = self.default_pic

        upload_button = tk.Button(
            edit_window, text="Upload", font=("Poppins", 12), bg='grey', fg='white',
            bd=0, command=upload_profile_picture
        )
        upload_button.place(x=718, y=403, width=110, height=35)

        if profile_picture_path:
            img = Image.open(profile_picture_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            profile_pic_img = ImageTk.PhotoImage(img)
            self.pict_label.config(image=profile_pic_img)
            self.pict_label.image = profile_pic_img
        
        def delete_profile_picture(event=None):
            if hasattr(self, "uploaded_file_path") and self.uploaded_file_path:
                if os.path.exists(self.uploaded_file_path):
                    os.remove(self.uploaded_file_path)
                self.uploaded_file_path = None 
                self.pict_label.config(image=self.default_pic)  
                self.pict_label.image = self.default_pic
                messagebox.showinfo("Info", "Profile picture reset to default.")

        delete_button = tk.Label(edit_window,image=self.delete_pic, fg='white',bd=0, cursor='hand2')
        delete_button.bind("<Button-1>", lambda event: delete_profile_picture(event))
        delete_button.image = self.delete_pic
        delete_button.place(x=846, y=415)

        # Address
        address_label = tk.Label(edit_window, text="Address Details", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        address_label.place(x=31, y=489)
        self.address_entry = tk.Entry(edit_window, font=('Poppins', 14), width=36, bd=1, relief="solid", bg='white')
        self.address_entry.insert(0, address)
        self.address_entry.place(x=31, y=532)

        # Description
        desc_label = tk.Label(edit_window, text="Description", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        desc_label.place(x=489, y=489)
        self.desc_entry = tk.Entry(edit_window, font=('Poppins', 14), width=40, bd=1, relief="solid", bg='white')
        self.desc_entry.insert(0, description)
        self.desc_entry.place(x=489, y=532)

        def update_doctor():
            updated_email = self.email_entry.get().strip()
            updated_first_name = self.fname_entry.get().strip()
            updated_last_name = self.lname_entry.get().strip()
            updated_password = self.password_entry.get().strip()
            updated_conf_password = self.confirm_password_entry.get().strip()
            updated_phone = self.phone_entry.get().strip()
            updated_specialty_name = self.specialty_combobox.get().strip()
            updated_specialty_id = self.specialty_id_map.get(updated_specialty_name)
            updated_gender_val = self.gender_combobox.get().strip()
            updated_city = self.city_entry.get().strip()
            updated_address = self.address_entry.get().strip()
            updated_description = self.desc_entry.get().strip()
            updated_profile_picture_path = getattr(self, "uploaded_file_path", None)

            updated_gender = 0 if updated_gender_val == "Male" else 1

            if not self.doctor_id:
                messagebox.showerror("Error", "Please select a doctor first!")

            if not updated_email or not updated_password or not updated_conf_password or not updated_first_name \
                or not updated_last_name or not updated_phone or not updated_specialty_id or not updated_city \
                or not updated_address or updated_gender is None or not updated_description:
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
                                        updated_gender, updated_phone, updated_city, updated_address, self.doctor_id))

                # Update Doctor table
                query2 = """
                    UPDATE Doctor
                    SET SpecialtyId = %s, ProfilePicture = %s, Description = %s
                    WHERE DoctorId = %s
                """
                cursor.execute(query2, (updated_specialty_id, updated_profile_picture_path,
                                        updated_description, self.doctor_id))

                conn.commit()
                messagebox.showinfo("Success", "Doctor updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update doctor: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                edit_window.destroy()

        # Save Button
        save_button = tk.Button(edit_window, text="Save", bg=self.master.bg_color1, 
                                fg='white', font=("Poppins", 16), bd=0, command=update_doctor)
        save_button.place(x=826, y=623, width=110, height=45)

    def delete_doctor(self):
        if not self.doctor_id:
            messagebox.showerror("Error", "Please select a doctor first!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the doctor '{self.doctor_id}'?"
        )

        if confirm:
            try:
                conn = connect_to_db()
                if not conn:
                    messagebox.showerror("Error", "Database connection failed.")
                    return

                with conn.cursor() as cursor:
                    query = "UPDATE `User` SET IsDeleted = 1 WHERE UserId = %s;"
                    cursor.execute(query, (self.doctor_id,))
                    conn.commit()

                    query = """UPDATE Booking SET AppointmentStatus = 'Cancelled' WHERE DoctorId = %s 
                        AND AppointmentStatus = 'Pending';"""
                    cursor.execute(query, (self.doctor_id,))
                    conn.commit()
                                        
                    messagebox.showinfo("Success", f"Doctor '{self.doctor_id}' has been deleted.") 

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()

    def add_doctor(self):   
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
                save_dir = "profile_pictures/doctors"
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
        add_window.title("Add New Doctor")
        add_window.geometry("1011x699")
        add_window.configure(bg="white")

        # Title
        title_label = tk.Label(add_window, text="Add Doctor", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
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

        # Specialty
        specialty_label = tk.Label(add_window, text="Specialty", font=("Poppins Semibold",16), fg=self.master.font_color1, bg='white')
        specialty_label.place(x=735, y=228)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.specialty_combobox = ttk.Combobox(add_window, font=('Poppins', 14), width=18, state="readonly", style="Custom.TCombobox")
        self.populate_specialty_combobox()
        self.specialty_combobox.place(x=735, y=271)
        self.specialty_combobox.set("Select")

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

        self.pict_label = tk.Label(add_window, bg='white', image=self.default_pic, width=100, height=100)
        self.pict_label.place(x=890, y=365)
        self.pict_label.image = self.default_pic

        upload_button = tk.Button(
            add_window, text="Upload", font=("Poppins", 12), bg='grey', fg='white',
            bd=0, command=upload_profile_picture
        )
        upload_button.place(x=718, y=403, width=110, height=35)

        def delete_profile_picture(event=None):
            if hasattr(self, "uploaded_file_path") and self.uploaded_file_path:
                if os.path.exists(self.uploaded_file_path):
                    os.remove(self.uploaded_file_path)
                self.uploaded_file_path = None 
                self.pict_label.config(image=self.default_pic)  
                self.pict_label.image = self.default_pic
                messagebox.showinfo("Info", "Profile picture reset to default.")

        delete_button = tk.Label(add_window,image=self.delete_pic, fg='white',bd=0, cursor='hand2')
        delete_button.bind("<Button-1>", lambda event: delete_profile_picture(event))
        delete_button.image = self.delete_pic
        delete_button.place(x=846, y=415)

        # Address
        address_label = tk.Label(add_window, text="Address Details", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        address_label.place(x=31, y=489)
        self.address_entry = tk.Entry(add_window, font=('Poppins', 14), width=36, bd=1, relief="solid", bg='white')
        self.address_entry.place(x=31, y=532)

        # Description
        desc_label = tk.Label(add_window, text="Description", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        desc_label.place(x=489, y=489)
        self.desc_entry = tk.Entry(add_window, font=('Poppins', 14), width=40, bd=1, relief="solid", bg='white')
        self.desc_entry.place(x=489, y=532)

        # Save Button
        def save_doctor():
            email = self.email_entry.get().strip()
            first_name = self.fname_entry.get().strip()
            last_name = self.lname_entry.get().strip()
            
            password = self.password_entry.get().strip()
            phone = self.phone_entry.get().strip()
            specialty_name = self.specialty_combobox.get().strip()
            specialty_id = self.specialty_id_map.get(specialty_name)

            conf_password = self.confirm_password_entry.get().strip()
            gender_val = self.gender_combobox.get().strip()
            city = self.city_entry.get().strip()
            profile_picture_path = getattr(self, "uploaded_file_path", None)

            address = self.address_entry.get().strip()
            description = self.desc_entry.get().strip()

            if gender_val == 'Male': gender = 0
            elif gender_val == 'Female': gender = 1
            else: 
                messagebox.showerror("Error", "Invalid gender!")
                return

            if not email or not password or not conf_password or not first_name \
                or not last_name or not phone or not specialty_id or not city or not address \
                or gender is None or not description:
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
                conn = connect_to_db()
                cursor = conn.cursor()

                cursor.execute("SELECT DoctorId FROM Doctor ORDER BY DoctorId DESC LIMIT 1")
                last_doctor_id = cursor.fetchone()
                if last_doctor_id:
                    last_id = last_doctor_id[0]
                    numeric_part = int(last_id[3:])  
                    new_numeric_part = numeric_part + 1
                else:
                    new_numeric_part = 1

                new_doctor_id = f'DOC{str(new_numeric_part).zfill(7)}'

                query1 = """
                    INSERT INTO User (UserId, Email, Password, FirstName, LastName, 
                    Gender, PhoneNumber, RoleName, City, AddressDetail, IsDeleted)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query1, (new_doctor_id, email, password, first_name, last_name,
                                        gender, phone, "Doctor", city, address, 0))
                conn.commit()

                query2 = """
                    INSERT INTO Doctor (DoctorId, SpecialtyId, ProfilePicture,  
                    Description, BranchNo)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query2, (new_doctor_id, specialty_id, profile_picture_path,
                                        description, self.branch_no))
                conn.commit()

                messagebox.showinfo("Success", "Doctor added successfully!")

            except Exception as e:
                print(f"Error occurred: {e}")
                messagebox.showerror("Error", f"Failed to add doctor: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                add_window.destroy()

        save_button = tk.Button(add_window, text="Save", bg=self.master.bg_color1, fg='white', font=("Poppins", 16), bd=0, command=save_doctor)
        save_button.place(x=826, y=623, width=110, height=45)

    def get_specialty_list(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT SpecialtyName FROM Specialty"
                cursor.execute(query1)
                result = cursor.fetchall()
                return result  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
        
    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = f"""
                    SELECT 
                        d.DoctorId,
                        s.SpecialtyName AS Specialty,
                        u.Email,
                        CONCAT(u.FirstName, ' ', u.LastName) AS Name,
                        CASE u.Gender 
                            WHEN 0 THEN 'Male'
                            ELSE 'Female'
                        END AS Gender,
                        u.PhoneNumber,
                        u.City,
                        u.AddressDetail AS Address,
                        COUNT(b.BookingId) AS TotalBookings,
                        SUM(
                            CASE 
                                WHEN MONTH(b.AppointmentDate) = MONTH(CURRENT_DATE) 
                                    AND YEAR(b.AppointmentDate) = YEAR(CURRENT_DATE)
                                THEN 1 
                                ELSE 0 
                            END
                        ) AS ThisMonthsBookings
                    FROM 
                        Doctor d
                    LEFT JOIN 
                        Specialty s ON d.SpecialtyID = s.SpecialtyID
                    LEFT JOIN 
                        `User` u ON d.DoctorId = u.UserId
                    LEFT JOIN 
                        Booking b ON d.DoctorId = b.DoctorId
                    WHERE d.BranchNo = %s AND u.IsDeleted = 0
                    GROUP BY 
                        d.DoctorId, s.SpecialtyName, u.Email, u.FirstName, u.LastName,
                        u.Gender, u.PhoneNumber, u.City, u.AddressDetail
                    ORDER BY 
                        {self.filter_field} {self.sort_order};                
                """
                cursor.execute(query1, (self.branch_no,))
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

        columns = ['DoctorId','Specialty','Email','Name','Gender','Phone Number',
                   'City','Address','Total Bookings',"This Month's Bookings"]  
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
        self.table.bind("<<TreeviewSelect>>", lambda event: self.update_schedule_panel(event))

    def update_schedule_panel(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item[0])
            self.doctor_id = item['values'][0]
            self.schedule = self.get_doctor_schedule(self.doctor_id)
            self.doctor_name = item['values'][3]

            for widget in self.schedule_panel.winfo_children():
                widget.destroy()  

            self.schedule_panel.config(bg='white')
            self.schedule_label = tk.Label(self.schedule_panel, text="Schedule", 
                                           font=("Poppins Semibold", 15), fg=self.master.font_color2, bg='white')
            self.schedule_label.place(x=6, y=11)

            if self.schedule:
                for i, entry in enumerate(self.schedule[:3]):  
                    text, id = entry
                    label = tk.Label(self.schedule_panel, text=f"• {text}", font=("Poppins", 11), bg="white", anchor="w")
                    label.place(x=6, y=49 + i * 25)
            else:
                label = tk.Label(self.schedule_panel, text="No schedule", font=("Poppins", 11), bg="white", anchor="w")
                label.place(x=6, y=49)
            
            self.scview_more_btn = tk.Button(self.schedule_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11), command=self.open_schedule,bd=0)
            self.scview_more_btn.place(x=30, y=125, width=110, height=26)

    def get_doctor_schedule(self, doctor_id):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        CONCAT(LEFT(DayOfWeek, 3), ': ', 
                        TIME_FORMAT(StartHour, '%H:%i'), '-', 
                        TIME_FORMAT(EndHour, '%H:%i')) AS Schedule,
                        ScheduleId
                    FROM DoctorSchedule
                    WHERE DoctorId = %s
                    ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 
                    'Thursday', 'Friday', 'Saturday', 'Sunday'),
                    StartHour, EndHour;
                """
                cursor.execute(query, (doctor_id,))
                result = cursor.fetchall()
                return [(row[0], row[1]) for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_specialty_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        SpecialtyId,
                        SpecialtyName, 
                        SpecialtyDescription
                    FROM Specialty
                """
                cursor.execute(query)
                result = cursor.fetchall()
                self.specialty_data = [(row[0], row[1], row[2]) for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.specialty_data = []
        finally:
            if conn:
                conn.close()

    def open_specialties(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Specialty")
        child_window.geometry("533x676")  

        # specialty label
        sptitle_label = tk.Label(child_window, text="Specialties",font=("Poppins Semibold", 32), 
                                 fg='black', bg='white')
        sptitle_label.place(x=142, y=18)

        # scrollpane specialties
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
        self.get_specialty_data()

        for i, (id, name, desc) in enumerate(self.specialty_data):
            # row container
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=name, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                    command=lambda id=id, child_window=child_window: self.edit_specialty(id,child_window))
            edit_button.grid(row=0, column=1, padx=(10, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda id=id, name=name, child_window=child_window: self.delete_specialty(id,name,child_window))
            delete_button.grid(row=0, column=2, padx=(5, 0), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text=desc, font=("Poppins", 12), 
                                fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w")

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=self.add_specialty)
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=211, y=615, width=116, height=40)

        child_window.resizable(False, False)

    def add_specialty(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Specialty")
        add_window.geometry("500x400")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Specialty Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spname_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        spname_entry.pack(pady=5)

        tk.Label(add_window, text="Specialty Description:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spdesc_entry = tk.Text(add_window, font=("Poppins", 12), width=30, height=5, bd=2, relief="solid")
        spdesc_entry.pack(pady=5)

        def save_specialty():
            spname = spname_entry.get().strip()
            spdesc = spdesc_entry.get("1.0", tk.END).strip()

            if not spname or not spdesc:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT SpecialtyID FROM Specialty ORDER BY SpecialtyID DESC LIMIT 1")
                    last_sp_id = cursor.fetchone()

                    if last_sp_id:
                        last_id = last_sp_id[0]  
                        numeric_part = int(last_id[2:])  
                        new_numeric_part = numeric_part + 1
                    else:
                        new_numeric_part = 1
                    
                    new_sp_id = f"SP{str(new_numeric_part).zfill(7)}"

                    query = """
                        INSERT INTO Specialty (SpecialtyId, SpecialtyName, SpecialtyDescription)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (new_sp_id,spname, spdesc))
                    conn.commit()
                    messagebox.showinfo("Success", "New specialty added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add specialty: {e}")
            finally:
                if conn:
                    conn.close()
                add_window.destroy() 
                self.open_specialties()  
                self.update_specialty_panel()

        save_button = tk.Button(add_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_specialty)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def edit_specialty(self, specialty_id, spwindow):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Specialty")
        edit_window.geometry("500x400")
        edit_window.configure(bg="white")

        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = "SELECT SpecialtyName, SpecialtyDescription FROM Specialty WHERE SpecialtyId = %s"
                cursor.execute(query, (specialty_id,))
                specialty = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch specialty: {e}")
            return
        finally:
            if conn:
                conn.close()

        if not specialty:
            messagebox.showerror("Error", "Specialty not found!")
            return

        current_name, current_description = specialty

        tk.Label(edit_window, text="Specialty Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spname_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        spname_entry.pack(pady=5)
        spname_entry.insert(0, current_name)  

        tk.Label(edit_window, text="Specialty Description:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spdesc_entry = tk.Text(edit_window, font=("Poppins", 12), width=30, height=5, bd=2, relief="solid")
        spdesc_entry.pack(pady=5)
        spdesc_entry.insert("1.0", current_description)  

        def save_changes():
            new_name = spname_entry.get().strip()
            new_description = spdesc_entry.get("1.0", tk.END).strip()

            if not new_name or not new_description:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    query = """
                        UPDATE Specialty
                        SET SpecialtyName = %s, SpecialtyDescription = %s
                        WHERE SpecialtyID = %s
                    """
                    cursor.execute(query, (new_name, new_description, specialty_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Specialty updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update specialty: {e}")
            finally:
                if conn:
                    conn.close()
                    
                edit_window.destroy()
                spwindow.destroy()  # Ensure old child_window is properly closed
                self.open_specialties() 
                self.update_specialty_panel()

        save_button = tk.Button(edit_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_changes)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def delete_specialty(self, specialty_id, specialty_name, spwindow):
        try:
            conn = connect_to_db()
            if not conn:
                messagebox.showerror("Error", "Database connection failed.")
                return

            with conn.cursor() as cursor:
                query = "SELECT COUNT(DoctorId) FROM Doctor WHERE SpecialtyId = %s"
                cursor.execute(query, (specialty_id,))
                amt = cursor.fetchone()[0]  

                if amt > 0:
                    messagebox.showerror(
                        "Error",
                        f"Cannot delete '{specialty_name}' because there are {amt} doctor(s) with this specialty."
                    )
                    return

                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete the specialty '{specialty_name}'?"
                )
                if confirm:
                    query = "DELETE FROM Specialty WHERE SpecialtyId = %s"
                    cursor.execute(query, (specialty_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Specialty '{specialty_name}' has been deleted.")
                    spwindow.destroy()
                    self.open_specialties()  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete specialty: {e}")
        finally:
            if conn:
                conn.close()
            self.update_specialty_panel()

    def is_valid_time(self, time_str):
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False  

            hour, minute = map(int, parts)  
            return 0 <= hour < 24 and 0 <= minute < 60  
        except (ValueError, TypeError):
            return False 
    
    def open_schedule(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Schedule")
        child_window.geometry("533x676")  

        # schedule label
        sctitle_label = tk.Label(child_window, text=f"Dr.{self.doctor_name.split()[0]} Schedule",
                                 font=("Poppins Semibold", 24), 
                                 fg='black', bg='white',wraplength=500)
        sctitle_label.place(x=30, y=18)

        # scrollpane schedule
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

        for i, entry in enumerate(self.schedule):
            schedule_text, schedule_id = entry
            day_abbrev, time_range = schedule_text.split(": ", 1)
            days_full = {
                "Mon": "Monday",
                "Tue": "Tuesday",
                "Wed": "Wednesday",
                "Thu": "Thursday",
                "Fri": "Friday",
                "Sat": "Saturday",
                "Sun": "Sunday"
            }
            day_full = days_full.get(day_abbrev, "Unknown Day")

            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=day_full, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                   command=lambda schedule_id=schedule_id, child_window=child_window: self.edit_schedule(schedule_id, child_window))
            edit_button.grid(row=0, column=1, padx=(0, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda schedule_id=schedule_id, child_window=child_window: self.delete_schedule(schedule_id, child_window))
            delete_button.grid(row=0, column=2, padx=(0, 5), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text=time_range,
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w",padx=(5, 10), pady=(0, 10))
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=self.add_schedule)
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=206, y=615, width=116, height=40)

        child_window.resizable(False, False)

    def add_schedule(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Schedule")
        add_window.geometry("500x400")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Day of the Week:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        day_entry = ttk.Combobox(add_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                font=("Poppins", 12), state="readonly", width=28)
        day_entry.pack(pady=5)

        tk.Label(add_window, text="Start Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        start_time_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        start_time_entry.pack(pady=5)

        tk.Label(add_window, text="End Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        end_time_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        end_time_entry.pack(pady=5)

        def save_schedule():
            day = day_entry.get().strip()
            start_time = start_time_entry.get().strip()
            end_time = end_time_entry.get().strip()

            if not day or not start_time or not end_time:
                messagebox.showerror("Error", "All fields are required!")
                add_window.destroy()
                return
            if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM format.")
                add_window.destroy()
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ScheduleId FROM DoctorSchedule ORDER BY ScheduleId DESC LIMIT 1")
                    last_id = cursor.fetchone()

                    if last_id:
                        last = last_id[0]  
                        numeric_part = int(last[3:])  
                        new_numeric_part = numeric_part + 1
                    else:
                        new_numeric_part = 1
                    
                    new_id = f"SCH{str(new_numeric_part).zfill(7)}"

                    query = """
                        INSERT INTO DoctorSchedule (ScheduleId, DoctorId, DayOfWeek, StartHour, EndHour)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (new_id,self.doctor_id, day, start_time, end_time))
                    conn.commit()
                    messagebox.showinfo("Success", "New schedule added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add schedule: {e}")
            finally:
                if conn:
                    conn.close()
                add_window.destroy()
                self.schedule = self.get_doctor_schedule(self.doctor_id)
                self.open_schedule()  
                self.update_schedule_panel() 

        save_button = tk.Button(add_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_schedule)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def edit_schedule(self, schedule_id, schedule_window):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Schedule")
        edit_window.geometry("500x400")
        edit_window.configure(bg="white")

        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT DayOfWeek, TIME_FORMAT(StartHour, '%H:%i'), TIME_FORMAT(EndHour, '%H:%i')
                    FROM DoctorSchedule
                    WHERE ScheduleId = %s
                """
                cursor.execute(query, (schedule_id,))
                schedule = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch schedule: {e}")
            return
        finally:
            if conn:
                conn.close()

        if not schedule:
            messagebox.showerror("Error", "Schedule not found!")
            return

        current_day, current_start, current_end = schedule

        tk.Label(edit_window, text="Day of the Week:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        day_entry = ttk.Combobox(edit_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                font=("Poppins", 12), state="readonly", width=28)
        day_entry.pack(pady=5)
        day_entry.set(current_day)

        tk.Label(edit_window, text="Start Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        start_time_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        start_time_entry.pack(pady=5)
        start_time_entry.insert(0, current_start)

        tk.Label(edit_window, text="End Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        end_time_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        end_time_entry.pack(pady=5)
        end_time_entry.insert(0, current_end)

        def save_changes():
            new_day = day_entry.get().strip()
            new_start_time = start_time_entry.get().strip()
            new_end_time = end_time_entry.get().strip()

            if not new_day or not new_start_time or not new_end_time:
                messagebox.showerror("Error", "All fields are required!")
                edit_window.destroy()
                return
            if not self.is_valid_time(new_start_time) or not self.is_valid_time(new_end_time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM format.")
                edit_window.destroy()
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    query = """
                        UPDATE DoctorSchedule
                        SET DayOfWeek = %s, StartHour = %s, EndHour = %s
                        WHERE ScheduleId = %s
                    """
                    cursor.execute(query, (new_day, new_start_time, new_end_time, schedule_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update schedule: {e}")
            finally:
                if conn:
                    conn.close()
                    
                edit_window.destroy()
                schedule_window.destroy()  
                self.schedule = self.get_doctor_schedule(self.doctor_id)
                self.open_schedule()  
                self.update_schedule_panel() 

        save_button = tk.Button(edit_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_changes)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def delete_schedule(self, schedule_id, schedule_window):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this schedule?"
                )
                if confirm:
                    query = "DELETE FROM DoctorSchedule WHERE ScheduleId = %s"
                    cursor.execute(query, (schedule_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule deleted successfully!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting: {e}")
        finally:
            if conn:
                conn.close()
            schedule_window.destroy()  
            self.schedule = self.get_doctor_schedule(self.doctor_id)
            self.open_schedule() 
            self.update_schedule_panel() 

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  # Scroll up
            canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            canvas.yview_scroll(1, "units")

    
    