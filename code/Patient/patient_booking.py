import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db
import os, shutil,re

class PatientBooking(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None

        self.branch_options = []
        self.specialty_options = []
        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((135, 135)))
        self.info_icon = ImageTk.PhotoImage(Image.open("images/info_icon.png"))
        self.doctors_list = []
        self.loaded_images = {}

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                  font=("Poppins Semibold", 18),
                                    command=self.navigate_home)
        self.home_btn.place(x=0, y=119, width=226, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=27, y=130)

        # booking
        self.booking_btn = tk.Button(self, text="    Booking", bd=0,bg=self.master.bg_color1, fg="white", 
                                    font=("Poppins Semibold", 18))
        self.booking_btn.place(x=0, y=186,  width=226, height=52)
        self.booking_icon = tk.PhotoImage(file='images/pat_booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg=self.master.bg_color1)  
        booking_label.place(x=23, y=195)

        # history
        self.history_btn = tk.Button(self, text="  History", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_history)
        self.history_btn.place(x=0, y=246, width=226, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg='#5FBBF5')  
        history_label.place(x=26, y=257)

    def navigate_history(self):
        self.master.patient_history.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_history)
    
    def navigate_home(self):
        self.master.patient_home.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_home)

    def get_user_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT Email, FirstName, LastName FROM User WHERE UserId = %s"
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.email, fname, lname = result
                    self.name = f'{fname} {lname}'
                else:
                    messagebox.showerror("Error", "Invalid user.")
                    return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def populate_branch(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT BranchNo, BranchName FROM ClinicBranch"
                cursor.execute(query1)
                result = cursor.fetchall()
                self.branch_options = [row[1] for row in result] 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def populate_specialty(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT SpecialtyId, SpecialtyName FROM Specialty"
                cursor.execute(query1)
                result = cursor.fetchall()
                self.specialty_options = [row[1] for row in result] 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def create_widgets(self):        
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/patient_main_background.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        # title
        self.title_label = tk.Label(self, text="Search and Book Doctor", font=("Poppins", 32, "bold"), fg='black', bg='white')
        self.title_label.place(x=500, y=28)

        # name login
        self.name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg='white')
        self.name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        self.email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg='white')
        self.email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # Branch selection
        self.populate_branch()
        self.branch_options.insert(0,'All')
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 16))
        self.branch_combobox = ttk.Combobox(self, font=('Poppins', 16), width=23, state="readonly", style="Custom.TCombobox")
        self.branch_combobox['values'] = self.branch_options
        self.branch_combobox.set('All')
        self.branch_combobox.place(x=339, y=172)

        branch_label = tk.Label(self, text="Select Branch:", font=("Poppins", 18), bg='white')
        branch_label.place(x=339, y=122)

        # Specialty selection
        self.populate_specialty()
        self.specialty_options.insert(0,'All')
        self.sp_combobox = ttk.Combobox(self, font=('Poppins', 16), width=30, state="readonly", style="Custom.TCombobox")
        self.sp_combobox['values'] = self.specialty_options
        self.sp_combobox.set('All')
        self.sp_combobox.place(x=678, y=172)
        specialty_label = tk.Label(self, text="Select Specialty:", font=("Poppins", 18), bg='white')
        specialty_label.place(x=678, y=122)

        # Search button
        search_button = tk.Button(self, text="Search",fg='white',bg=self.master.bg_color1,font=("Poppins", 18), 
                                  command=self.filter_profiles)
        search_button.place(x=1109, y=170, width=126, height=46)
        
        self.frame1 = tk.Frame(self, bd=0, highlightthickness=1, highlightbackground=self.master.font_color2)
        self.frame1.place(x=306, y=240)
        self.filter_profiles()
    
    def get_profile_picture(self, image_path):
        if image_path is None:
            return self.default_pic  
        
        if image_path not in self.loaded_images:
            try:
                img = Image.open(image_path)
                img_resized = img.resize((135, 135))  
                self.loaded_images[image_path] = ImageTk.PhotoImage(img_resized)  
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                self.loaded_images[image_path] = self.default_pic 
        
        return self.loaded_images[image_path]
    
    def create_canvas_booking(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()

        if not self.doctors_list:
            empty_label = tk.Label(self.frame, text="No doctor available.", font=("Poppins", 16), bg='white')
            empty_label.place(x=44, y=32)
            return

        canvas1 = tk.Canvas(self.frame1, width=960, height=470, bg='white', bd=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(self.frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white', bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        for i, entry in enumerate(self.doctors_list):
            entry_frame = tk.Frame(content1, bg='white', pady=10)
            entry_frame.pack(fill="x", padx=5, pady=5)

            profile_pic = self.get_profile_picture(entry[1])

            propic_label = tk.Label(entry_frame, image=profile_pic, bd=0, highlightthickness=0, bg='white')
            propic_label.image = profile_pic
            propic_label.pack(side="left", padx=40)

            details_frame = tk.Frame(entry_frame, bg='white')
            details_frame.pack(side="left", fill="x", expand=True)

            name_label = tk.Label(details_frame, text=f"Name: Dr. {entry[5]} {entry[6]}", font=("Poppins", 12), bg='white')
            name_label.pack(anchor="w",padx=(10, 0))

            branch_label = tk.Label(details_frame, text=f"Branch: {entry[7]}", font=("Poppins", 12), bg='white')
            branch_label.pack(anchor="w",padx=(10, 0))

            specialty_label = tk.Label(details_frame, text=f"Specialty: {entry[3]}", font=("Poppins", 12), bg='white')
            specialty_label.pack(anchor="w",padx=(10, 0))

            book_button = tk.Button(details_frame, text="Book Now", font=("Poppins Semibold", 12),
                                 bg=self.master.bg_color1, fg="white", relief="flat", 
                                 command=lambda doctor_id=entry[0]: self.insert_booking(doctor_id))
            book_button.pack(anchor="w", pady=(10, 10), padx=(10, 0))

            info_button = tk.Label(entry_frame, image=self.info_icon, bd=0, highlightthickness=0, bg='white')
            info_button.bind("<Button-1>", lambda event,desc=entry[4]: self.show_description(desc))
            info_button.pack(side="left", padx=5)

            desc_frame = tk.Frame(entry_frame, bg='white', bd=1, relief="solid", pady=5, padx=5)
            desc_frame.pack(side="right", fill="both", expand=False, padx=(20, 0))

            desc_text = tk.Text(desc_frame, wrap="word", font=("Poppins", 10), bg='white', bd=0, height=4, width=40)
            desc_text.insert("1.0", entry[2])
            desc_text.config(state="disabled")  
            desc_text.pack(side="left", fill="both", expand=True)

            desc_scrollbar = tk.Scrollbar(desc_frame, orient="vertical", command=desc_text.yview)
            desc_text.config(yscrollcommand=desc_scrollbar.set)
            desc_scrollbar.pack(side="right", fill="y")

            separator = tk.Frame(content1, bg=self.master.separator_color, height=1)
            separator.pack(fill="x", pady=(10, 0))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

    def show_description(self, description):
        messagebox.showinfo("Specialty Description", description)

    def filter_profiles(self):
        selected_branch = self.branch_combobox.get()
        selected_specialty = self.sp_combobox.get()

        query = """
        SELECT d.DoctorId, d.ProfilePicture, d.Description, s.SpecialtyName, s.SpecialtyDescription,
        u.FirstName, u.LastName, cb.BranchName
        FROM Doctor d
        JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
        JOIN `User` u ON d.DoctorId = u.UserId
        JOIN ClinicBranch cb ON d.BranchNo = cb.BranchNo
        WHERE u.IsDeleted = 0
        """

        conditions = []
        parameters = []

        if selected_branch != "All":
            conditions.append("cb.BranchName = %s")
            parameters.append(selected_branch)

        if selected_specialty != "All":
            conditions.append("s.SpecialtyName = %s")
            parameters.append(selected_specialty)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                cursor.execute(query, tuple(parameters))
                results = cursor.fetchall()

            self.doctors_list = results
            self.create_canvas_booking()  

        except Exception as e:
            print(f"Error fetching doctor profiles: {e}")

    def get_doctor_schedule(self, doctor_id):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        CONCAT(DayOfWeek, ': ', 
                        TIME_FORMAT(StartHour, '%H:%i'), '-', 
                        TIME_FORMAT(EndHour, '%H:%i')) AS Schedule
                    FROM DoctorSchedule
                    WHERE DoctorId = %s
                    ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                    StartHour, EndHour;
                """
                cursor.execute(query, (doctor_id,))
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def insert_booking(self, doctor_id):
        booking_window = tk.Toplevel(self)
        booking_window.title("Booking Appointment")
        booking_window.geometry("400x700")  
        booking_window.configure(bg='white')

        schedule_label = tk.Label(booking_window, text="Select Schedule:", font=("Poppins", 14), bg='white')
        schedule_label.pack(pady=10)

        schedules = self.get_doctor_schedule(doctor_id)
        schedule_combobox = ttk.Combobox(booking_window, font=("Poppins", 12), state="readonly")
        schedule_combobox['values'] = schedules
        schedule_combobox.set('Select Time') 
        schedule_combobox.pack(pady=10)

        appointment_date_label = tk.Label(booking_window, text="Appointment Date (YYYY-MM-DD):", font=("Poppins", 14), bg='white')
        appointment_date_label.pack(pady=5)

        appointment_date_entry = tk.Entry(booking_window, font=("Poppins", 12),bd=1, relief="solid", bg='white')
        appointment_date_entry.pack(pady=5)

        appointment_hour_label = tk.Label(booking_window, text="Appointment Hour (HH:MM):", font=("Poppins", 14),bg='white')
        appointment_hour_label.pack(pady=5)

        appointment_hour_entry = tk.Entry(booking_window, font=("Poppins", 12),bd=1, relief="solid", bg='white')
        appointment_hour_entry.pack(pady=5)

        # Checkup Type
        checkup_type_label = tk.Label(booking_window, text="Checkup Type:", font=("Poppins", 14),bg='white')
        checkup_type_label.pack(pady=5)
        checkup_entry = tk.Entry(booking_window, font=("Poppins", 12),bd=1, relief="solid", bg='white')
        checkup_entry.pack(pady=5)

        # Reason of Visit
        reason_label = tk.Label(booking_window, text="Reason for Visit:", font=("Poppins", 14),bg='white')
        reason_label.pack(pady=5)
        reason_textarea = tk.Text(booking_window, font=("Poppins", 12), bd=1, relief="solid", bg='white', height=5, width=30)
        reason_textarea.pack(pady=5)

        # Submit Button
        def submit_booking():
            schedule = schedule_combobox.get().strip()
            appointment_date = appointment_date_entry.get().strip()
            appointment_hour = appointment_hour_entry.get().strip()
            checkup_type = checkup_entry.get().strip()
            reason = reason_textarea.get("1.0", "end").strip()

            if schedule == 'Select Time' or not appointment_date \
            or not appointment_hour or not checkup_type or not reason:
                messagebox.showwarning("Input Error", "Please fill all fields.")
                return
            
            try:
                valid_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
                today_date = datetime.today().date()
                if valid_date < today_date:
                    messagebox.showwarning("Date Error", "The appointment date cannot be in the past.")
                    return

            except ValueError:
                messagebox.showwarning("Date Error", "Please enter a valid date in the format YYYY-MM-DD.")
                return
            
            try:
                valid_time = datetime.strptime(appointment_hour, '%H:%M').time()
            except ValueError:
                messagebox.showwarning("Time Error", "Please enter a valid time in the format HH:MM.")
                return
            
            day_of_week = valid_date.strftime('%A')  
            try:
                schedule_day, schedule_time_range = schedule.split(': ')
                schedule_day = schedule_day.strip()
                start_time_str, end_time_str = schedule_time_range.split('-')
                
                schedule_start_time = datetime.strptime(start_time_str, '%H:%M').time()
                schedule_end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if day_of_week != schedule_day:
                    messagebox.showwarning("Schedule Error", f"Invalid day of week. Please choose another schedule.")
                    return
                
                if (valid_time < schedule_start_time or valid_time > schedule_end_time):
                    messagebox.showwarning("Time Slot Error", f"Please choose a time between {schedule_start_time} and {schedule_end_time}.")
                    return
            except Exception as e:
                print("Schedule Error: ", e)
                messagebox.showwarning("Schedule Error", "There was an error parsing the schedule.")
                return

            start_time_obj = datetime.strptime(start_time_str, "%H:%M")
            end_time_obj = datetime.strptime(end_time_str, "%H:%M")
            time_difference = end_time_obj - start_time_obj
            hours = time_difference.total_seconds() / 3600

            try:
                query = """
                SELECT COUNT(BookingId) FROM Booking WHERE DoctorId = %s AND AppointmentDate = %s 
                AND AppointmentHour BETWEEN %s AND %s;
                """
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute(query, (doctor_id, appointment_date, schedule_start_time, schedule_end_time))
                    result = cursor.fetchone()
                    bookings_count = result[0] if result else 0

                if bookings_count >= hours*4:
                    messagebox.showwarning("Booking Limit Exceeded", "This doctor is already full at this time.")
                    return
            except Exception as e:
                messagebox.showwarning("Error", f"An error occurred while checking the bookings: {e}")
                return

            try:
                self.insert_booking_db(doctor_id, appointment_date, appointment_hour, checkup_type, reason)
                booking_window.destroy()  
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while booking the appointment: {e}")
        
        submit_button = tk.Button(booking_window, text="Book Now", font=("Poppins", 14), width=10, height = 1,
                                  bg=self.master.bg_color1, fg="white", command=submit_booking)
        submit_button.pack(pady=20)

    def insert_booking_db(self, doctor_id, appointment_date, appointment_hour, checkup_type, reason):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT BookingId FROM Booking ORDER BY BookingId DESC LIMIT 1")
            last_booking_id = cursor.fetchone()
            if last_booking_id:
                last_id = last_booking_id[0]
                numeric_part = int(last_id[3:])  
                new_numeric_part = numeric_part + 1
            else:
                new_numeric_part = 1

            new_booking_id = f'BOK{str(new_numeric_part).zfill(7)}'

            query1 = """
                INSERT INTO Booking (BookingId, PatientId, DoctorId, AppointmentDate, 
                AppointmentHour, AppointmentStatus, CheckUpType, ReasonOfVisit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query1, (new_booking_id, self.user_id, doctor_id, appointment_date, appointment_hour, 
                                    "Pending", checkup_type, reason))
            conn.commit()
            messagebox.showinfo("Success", "Booking added successfully!")

        except Exception as e:
            print(f"Error inserting appointment: {e}")
            messagebox.showerror("Error", f"Failed to add booking: {e}")

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  
            canvas.yview_scroll(-1, "units")
        else:  
            canvas.yview_scroll(1, "units")
