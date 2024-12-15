import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, time
from connection import connect_to_db

class AdminBookingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.name = None
        self.email = None
        self.branch_no = None

        self.filter_field = 'BookingId'
        self.sort_order = 'ASC'
        self.booking_id = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def navigate_home(self):
        self.master.admin_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_dashboard)
    
    def navigate_patient(self):
        self.master.admin_patient_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_patient_page)
    
    def navigate_doctor(self):
        self.master.admin_doctor_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_doctor_page)
    
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
                                   font=("Poppins Semibold", 18),command=self.navigate_doctor)
        self.doctor_btn.place(x=0, y=183, width=213, height=52)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg='#64C1F6')  
        doctor_label.place(x=23, y=196)

        # patient
        self.patient_btn = tk.Button(self, text="Patient", bd=0,bg='#5FBBF5', fg="white", 
                                    font=("Poppins Semibold", 18),command=self.navigate_patient)
        self.patient_btn.place(x=0, y=243, width=213, height=52)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg='#5FBBF5')  
        patient_label.place(x=23, y=255)

        # booking
        self.booking_btn = tk.Button(self, text=" Booking", bd=0,bg=self.master.bg_color1, 
                                     fg="white", font=("Poppins Semibold", 18))
        self.booking_btn.place(x=0, y=300, width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg=self.master.bg_color1)  
        booking_label.place(x=23, y=311)

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

    def create_widgets(self):
        self.get_user_info()

        # background
        self.background_photo = tk.PhotoImage(file='images/admin_default.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
 
        # title
        title_label = tk.Label(self, text="Bookings", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=248, y=20)

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select(event):
            selected_option = combo.get()
            if selected_option == 'Status': selected_option = 'AppointmentStatus'
            # print(f"Selected: {selected_option}")
            
            self.filter_field = selected_option  
            self.create_table()

        options = ["BookingId", "Date & Hour", "Status"]
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

        # add btn
        add_btn = tk.Button(self, text='Add', bg='white',fg=self.master.green_font, 
                            font=('Poppins Medium', 14), bd=0, command=self.add_booking)
        add_btn.place(x=1180, y=590, width=135, height=35)

        # edit btn
        edit_btn = tk.Button(self, text='Edit', bg='white',fg=self.master.yellow_font, 
                             font=('Poppins Medium', 14), bd=0,command=self.edit_booking)
        edit_btn.place(x=1180, y=641, width=135, height=35)

        # delete btn
        delete_btn = tk.Button(self, text='Delete', bg='white',fg=self.master.red_font, 
                               font=('Poppins Medium', 14), bd=0, command=self.delete_booking)
        delete_btn.place(x=1180, y=692, width=135, height=35)

        self.create_table()

    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                if self.filter_field == 'Date & Hour':
                    query1 = f"""
                        SELECT 
                            BookingId, PatientName, DoctorName, AppointmentDate, AppointmentHour,
                            AppointmentStatus, CheckUpType, ReasonOfVisit
                        FROM BranchBookings WHERE BranchNo = %s
                        ORDER BY AppointmentDate {self.sort_order}, STR_TO_DATE(AppointmentHour, '%H:%i') {self.sort_order};                
                    """
                else:
                    query1 = f"""
                        SELECT 
                            BookingId, PatientName, DoctorName, AppointmentDate, AppointmentHour,
                            AppointmentStatus, CheckUpType, ReasonOfVisit
                        FROM BranchBookings WHERE BranchNo = %s
                        ORDER BY {self.filter_field} {self.sort_order};                
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

        columns = ['BookingId','Patient Name','Doctor Name','Appointment Date','Appointment Hour',
                   'Appointment Status','Check Up Type','Reason Of Visit']  
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=220, anchor=tk.CENTER)

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
        self.table.bind("<<TreeviewSelect>>", lambda event: self.update_booking(event))
    
    def update_booking(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item[0])
            self.booking_id = item['values'][0]

    def populate_doctor_combobox(self):
        try:
            conn = connect_to_db() 
            cursor = conn.cursor()
            query = """
                SELECT 
                    d.DoctorId AS Id,  
                    CONCAT(u.FirstName, ' ', u.LastName, ' (', d.DoctorId, ')') AS Name 
                FROM Doctor d
                INNER JOIN User u ON u.UserId = d.DoctorId
                WHERE d.BranchNo = %s AND u.IsDeleted = 0
                ORDER BY Id ASC"""
            
            cursor.execute(query, (self.branch_no,))
            doctors = cursor.fetchall()

            doctor_names = [d[1] for d in doctors]
            self.doctor_combobox['values'] = doctor_names
            self.doctor_id_map = {d[1]: d[0] for d in doctors}

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch specialties: {e}")
        finally:
            if conn:
                conn.close()

    def populate_patient_combobox(self):
        try:
            conn = connect_to_db() 
            cursor = conn.cursor()
            query = """
                SELECT UserId,  CONCAT(FirstName, ' ', LastName, ' (', UserId, ')') AS Name 
                FROM User WHERE RoleName = 'Patient' AND IsDeleted = 0
                ORDER BY UserId ASC"""
            
            cursor.execute(query)
            patients = cursor.fetchall()

            patient_names = [d[1] for d in patients]
            self.patient_combobox['values'] = patient_names
            self.patient_id_map = {d[1]: d[0] for d in patients}

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch patients: {e}")
        finally:
            if conn:
                conn.close()

    def populate_schedule_combobox(self, event=None):
        try:
            conn = connect_to_db()
            doctor_id = self.doctor_id_map.get(self.doctor_combobox.get().strip())
            if not doctor_id:
                self.schedule_combobox['values'] = []  
                return
                        
            cursor = conn.cursor()
            query = """
                SELECT CONCAT(DayOfWeek, ' ', TIME_FORMAT(StartHour, '%H:%i'), '-', TIME_FORMAT(EndHour, '%H:%i')) AS Schedule
                FROM DoctorSchedule
                WHERE DoctorId = %s
                ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
            """
            cursor.execute(query, (doctor_id,))
            schedules = cursor.fetchall()

            schedule_values = [s[0] for s in schedules]
            self.schedule_combobox['values'] = schedule_values

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch doctor schedules: {e}")
        finally:
            if conn:
                conn.close()

    def add_booking(self):  
        add_window = tk.Toplevel(self)
        add_window.title("Add New Booking")
        add_window.geometry("970x579")
        add_window.configure(bg="white")

        # Title
        title_label = tk.Label(add_window, text="Add Booking", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=31, y=16)

        # Doctor Name
        dname_label = tk.Label(add_window, text="Doctor Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        dname_label.place(x=31, y=103)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.doctor_combobox = ttk.Combobox(add_window, font=('Poppins', 14), width=34, state="readonly", style="Custom.TCombobox")
        self.populate_doctor_combobox()
        self.doctor_combobox.place(x=31, y=144)
        self.doctor_combobox.set("Select") 
        self.doctor_combobox.bind("<<ComboboxSelected>>", self.populate_schedule_combobox)

        # Patient Name
        pname_label = tk.Label(add_window, text="Patient Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        pname_label.place(x=486, y=103)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.patient_combobox = ttk.Combobox(add_window, font=('Poppins', 14), width=34, state="readonly", style="Custom.TCombobox")
        self.populate_patient_combobox()
        self.patient_combobox.place(x=486, y=144)
        self.patient_combobox.set("Select") 

        # schedule choice
        schedule_label = tk.Label(add_window, text="Schedule", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        schedule_label.place(x=31, y=228)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.schedule_combobox = ttk.Combobox(add_window, font=('Poppins', 14), width=18, state="readonly", style="Custom.TCombobox")
        self.populate_schedule_combobox()
        self.schedule_combobox.place(x=31, y=272)
        self.schedule_combobox.set("Select")    

        # Date
        date_label = tk.Label(add_window, text="Date (YYYY-MM-DD)", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        date_label.place(x=307, y=228)
        self.date_entry = tk.Entry(add_window, font=('Poppins', 14), width=18, bd=1, relief="solid", bg='white')
        self.date_entry.place(x=307, y=272)

        # Hour
        hour_label = tk.Label(add_window, text="Hour (HH:MM)", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        hour_label.place(x=581, y=228)
        self.hour_entry = tk.Entry(add_window, font=('Poppins', 14), width=16, bd=1, relief="solid", bg='white')
        self.hour_entry.place(x=581, y=272)

        # check up type
        checktype_label = tk.Label(add_window, text="Check Up Type", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        checktype_label.place(x=31, y=358)
        self.checktype_entry = tk.Entry(add_window, font=('Poppins', 14), width=20, bd=1, relief="solid", bg='white')
        self.checktype_entry.place(x=31, y=401)

        # reason of visit
        reason_label = tk.Label(add_window, text="Reason of Visit", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        reason_label.place(x=295, y=358)
        self.reason_entry = tk.Entry(add_window, font=('Poppins', 14), width=50, bd=1, relief="solid", bg='white')
        self.reason_entry.place(x=295, y=401)   

        def save_booking():
            doctor_str = self.doctor_combobox.get().strip()
            doctor_id = self.doctor_id_map.get(doctor_str)            

            patient_str = self.patient_combobox.get().strip()
            patient_id = self.patient_id_map.get(patient_str) 

            schedule = self.schedule_combobox.get().strip()

            if not schedule or schedule == 'Select':
                messagebox.showerror("Error", "No schedule selected.")
            if not doctor_str or doctor_str == 'Select':
                messagebox.showerror("Error", "No doctor selected.")
            if not patient_str or patient_str == 'Select':
                messagebox.showerror("Error", "No patient selected.")

            parts = schedule.split()
            if len(parts) < 2:
                messagebox.showerror("Error", "Invalid schedule format. Expected 'DayOfWeek StartHour-EndHour'.")

            day_of_week = parts[0]  
            range_hour = parts[1]  
            time_parts = range_hour.split('-')
            if len(time_parts) != 2:
                messagebox.showerror("Error", "Invalid time range format. Expected 'StartHour-EndHour'.")

            start_hour = time_parts[0]
            end_hour = time_parts[1]
            if not (start_hour.count(':') == 1 and end_hour.count(':') == 1):
                messagebox.showerror("Error", "Time format should be 'HH:mm'.")
            
            dates = self.date_entry.get().strip()
            hour = self.hour_entry.get().strip()
            check_up_type = self.checktype_entry.get().strip()
            reason = self.reason_entry.get().strip()

            try:
                date_date = datetime.strptime(dates, '%Y-%m-%d').date()  
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
                return   

            if not dates or not hour or not check_up_type or not reason:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not self.validate_date_and_hour(dates, hour, day_of_week, start_hour, end_hour):
                messagebox.showerror("Error", "Date or hour is not valid!")
                return
            
            try:
                query = """
                SELECT COUNT(BookingId) FROM Booking WHERE DoctorId = %s AND AppointmentDate = %s 
                AND AppointmentHour BETWEEN %s AND %s;
                """
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute(query, (doctor_id, dates, start_hour, end_hour))
                    result = cursor.fetchone()
                    bookings_count = result[0] if result else 0

                start_time_obj = datetime.strptime(start_hour, "%H:%M")
                end_time_obj = datetime.strptime(end_hour, "%H:%M")
                time_difference = end_time_obj - start_time_obj
                hours = time_difference.total_seconds() / 3600

                if bookings_count >= hours*4:
                    messagebox.showwarning("Booking Limit Exceeded", "This doctor is already full at this time.")
                    return
            except Exception as e:
                messagebox.showwarning("Error", f"An error occurred while checking the bookings: {e}")
                return

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
                cursor.execute(query1, (new_booking_id, patient_id, doctor_id, date_date, hour, 
                                        "Pending", check_up_type, reason))
                conn.commit()

                messagebox.showinfo("Success", "Booking added successfully!")

            except Exception as e:
                print(f"Error occurred: {e}")
                messagebox.showerror("Error", f"Failed to add booking: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                add_window.destroy()

        # Save Button
        save_button = tk.Button(add_window, text="Save", bg=self.master.bg_color1, fg='white', font=("Poppins", 16), bd=0, command=save_booking)
        save_button.place(x=816, y=492, width=110, height=45)

    def edit_booking(self):  
        if not self.booking_id:
            messagebox.showerror("Error", "Please select a booking first.")
            return
        
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                PatientId, DoctorId, AppointmentDate, TIME_FORMAT(AppointmentHour, '%H:%i'), 
                AppointmentStatus, CheckUpType, ReasonOfVisit
            FROM Booking WHERE BookingId = %s
        """
        cursor.execute(query, (self.booking_id,))
        booking_data = cursor.fetchone()
        conn.close()

        if not booking_data:
            messagebox.showerror("Error", "Booking not found!")
            return

        patient_id, doctor_id, appointDate, appointHour, appointStatus, check_type, reason = (
            booking_data[0], booking_data[1], booking_data[2], booking_data[3], booking_data[4],
            booking_data[5], booking_data[6]
        )

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Booking")
        edit_window.geometry("970x579")
        edit_window.configure(bg="white")

        # Title
        title_label = tk.Label(edit_window, text="Edit Booking", font=("Poppins", 32, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=31, y=16)

        # Doctor Name
        dname_label = tk.Label(edit_window, text="Doctor Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        dname_label.place(x=31, y=103)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.doctor_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=34, state="disabled", style="Custom.TCombobox")
        self.populate_doctor_combobox()
        self.doctor_combobox.place(x=31, y=144)
        reversed_doctor_map = {v: k for k, v in self.doctor_id_map.items()}
        self.doctor_combobox.set(reversed_doctor_map.get(doctor_id)) 

        # Patient Name
        pname_label = tk.Label(edit_window, text="Patient Name", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        pname_label.place(x=486, y=103)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.patient_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=34, state="disabled", style="Custom.TCombobox")
        self.populate_patient_combobox()
        self.patient_combobox.place(x=486, y=144)
        reversed_patient_map = {v: k for k, v in self.patient_id_map.items()}
        self.patient_combobox.set(reversed_patient_map.get(patient_id)) 

        # schedule choice
        schedule_label = tk.Label(edit_window, text="Schedule", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        schedule_label.place(x=31, y=228)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.schedule_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=18, state="readonly", style="Custom.TCombobox")
        self.populate_schedule_combobox()
        self.schedule_combobox.place(x=31, y=272)
        self.schedule_combobox.set(self.find_doctor_schedule(appointDate, appointHour, doctor_id))    

        # Date
        date_label = tk.Label(edit_window, text="Date (YYYY-MM-DD)", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        date_label.place(x=300, y=228)
        self.date_entry = tk.Entry(edit_window, font=('Poppins', 14), width=12, bd=1, relief="solid", bg='white')
        self.date_entry.insert(0, appointDate)
        self.date_entry.place(x=300, y=272)

        # Hour
        hour_label = tk.Label(edit_window, text="Hour (HH:MM)", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        hour_label.place(x=540, y=228)
        self.hour_entry = tk.Entry(edit_window, font=('Poppins', 14), width=10, bd=1, relief="solid", bg='white')
        self.hour_entry.insert(0, appointHour)
        self.hour_entry.place(x=540, y=272)

        # status
        status_label = tk.Label(edit_window, text="Status", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        status_label.place(x=700, y=228)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.status_combobox = ttk.Combobox(edit_window, font=('Poppins', 14), width=12, state="readonly", style="Custom.TCombobox")
        self.status_combobox['values'] = ("Pending", "Completed", "Cancelled")
        self.status_combobox.place(x=700, y=272)
        self.status_combobox.set(appointStatus) 

        # check up type
        checktype_label = tk.Label(edit_window, text="Check Up Type", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        checktype_label.place(x=31, y=358)
        self.checktype_entry = tk.Entry(edit_window, font=('Poppins', 14), width=20, bd=1, relief="solid", bg='white')
        self.checktype_entry.insert(0, check_type)
        self.checktype_entry.place(x=31, y=401)

        # reason of visit
        reason_label = tk.Label(edit_window, text="Reason of Visit", font=("Poppins Semibold", 16), fg=self.master.font_color1, bg='white')
        reason_label.place(x=295, y=358)
        self.reason_entry = tk.Entry(edit_window, font=('Poppins', 14), width=50, bd=1, relief="solid", bg='white')
        self.reason_entry.insert(0, reason)
        self.reason_entry.place(x=295, y=401)   

        def save_booking():
            schedule = self.schedule_combobox.get().strip()

            if not schedule or schedule == 'Select':
                messagebox.showerror("Error", "No schedule selected.")

            parts = schedule.split()
            if len(parts) < 2:
                messagebox.showerror("Error", "Invalid schedule format. Expected 'DayOfWeek StartHour-EndHour'.")

            day_of_week = parts[0]  
            range_hour = parts[1]  
            time_parts = range_hour.split('-')
            if len(time_parts) != 2:
                messagebox.showerror("Error", "Invalid time range format. Expected 'StartHour-EndHour'.")

            start_hour = time_parts[0]
            end_hour = time_parts[1]
            if not (start_hour.count(':') == 1 and end_hour.count(':') == 1):
                messagebox.showerror("Error", "Time format should be 'HH:mm'.")
                return
            
            dates = self.date_entry.get().strip()
            hour = self.hour_entry.get().strip()
            new_status = self.status_combobox.get().strip()
            check_up_type = self.checktype_entry.get().strip()
            reason = self.reason_entry.get().strip()

            try:
                date_date = datetime.strptime(dates, '%Y-%m-%d').date()  
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD.")
                return   

            if not dates or not hour or not check_up_type or not reason or not new_status:
                messagebox.showerror("Error", "All fields are required!")
                return
            if not self.validate_date_and_hour(dates, hour, day_of_week, start_hour, end_hour):
                messagebox.showerror("Error", "Date or hour is not valid!")
                return
            
            try:
                query = """
                SELECT COUNT(BookingId) FROM Booking WHERE DoctorId = %s AND AppointmentDate = %s 
                AND AppointmentHour BETWEEN %s AND %s;
                """
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute(query, (doctor_id, dates, start_hour, end_hour))
                    result = cursor.fetchone()
                    bookings_count = result[0] if result else 0

                start_time_obj = datetime.strptime(start_hour, "%H:%M")
                end_time_obj = datetime.strptime(end_hour, "%H:%M")
                time_difference = end_time_obj - start_time_obj
                hours = time_difference.total_seconds() / 3600

                if bookings_count >= hours*4:
                    messagebox.showwarning("Booking Limit Exceeded", "This doctor is already full at this time.")
                    return
            except Exception as e:
                messagebox.showwarning("Error", f"An error occurred while checking the bookings: {e}")
                return

            try:
                conn = connect_to_db()
                cursor = conn.cursor()

                query = """
                    UPDATE Booking 
                    SET AppointmentDate = %s, AppointmentHour = %s, AppointmentStatus = %s, 
                    CheckUpType = %s, ReasonOfVisit = %s
                    WHERE BookingId = %s
                """
                
                cursor.execute(query, (date_date, hour, new_status, check_up_type, 
                                       reason, self.booking_id))
                conn.commit()

                messagebox.showinfo("Success", "Booking updated successfully!")

            except Exception as e:
                print(f"Error occurred: {e}")
                messagebox.showerror("Error", f"Failed to add booking: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()
                edit_window.destroy()

        # Save Button
        save_button = tk.Button(edit_window, text="Save", bg=self.master.bg_color1, fg='white', font=("Poppins", 16), bd=0, command=save_booking)
        save_button.place(x=816, y=492, width=110, height=45)
    
    def delete_booking(self):
        if not self.booking_id:
            messagebox.showerror("Error", "Please select a booking first!")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the booking '{self.booking_id}'?"
        )

        if confirm:
            try:
                conn = connect_to_db()
                if not conn:
                    messagebox.showerror("Error", "Database connection failed.")
                    return

                with conn.cursor() as cursor:
                    query = "DELETE FROM Booking WHERE BookingId = %s;"
                    cursor.execute(query, (self.booking_id,))
                    conn.commit()
                                        
                    messagebox.showinfo("Success", f"Booking '{self.booking_id}' has been deleted.") 

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete booking: {e}")
            finally:
                if conn:
                    conn.close()
                self.create_table()

    def find_doctor_schedule(self, appointment_date, appointment_hour, doctor_id):        
        day_of_week = appointment_date.strftime("%A")

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            query = """
                SELECT DayOfWeek, TIME_FORMAT(StartHour, '%H:%i'), TIME_FORMAT(EndHour, '%H:%i')
                FROM DoctorSchedule
                WHERE DoctorId = %s
            """
            cursor.execute(query, (doctor_id,))
            schedules = cursor.fetchall()

            for schedule in schedules:
                schedule_day = schedule[0]
                start_hour = schedule[1]
                end_hour = schedule[2]

                if schedule_day == day_of_week:
                    if start_hour <= appointment_hour <= end_hour:
                        return f"{schedule_day} {start_hour}-{end_hour}"
            return None

        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            if conn:
                conn.close()
    
    def validate_date_and_hour(self, dates, hour, day_of_week, start_hour, end_hour):
        try:
            input_date = datetime.strptime(dates, "%Y-%m-%d").date()
            today = date.today()
            if input_date < today:
                messagebox.showerror("Error", "The selected date must be in the future.")
                raise ValueError("The selected date must be in the future.")

            input_day_of_week = input_date.strftime("%A")  
            if input_day_of_week != day_of_week:
                messagebox.showerror("Error", f"The selected date does not match the day of the week: {day_of_week}.")
                raise ValueError(f"The selected date does not match the day of the week: {day_of_week}.")

            input_hour = datetime.strptime(hour, "%H:%M").time()
            start_time = datetime.strptime(start_hour, "%H:%M").time()
            end_time = datetime.strptime(end_hour, "%H:%M").time()

            if not (start_time <= input_hour <= end_time):
                messagebox.showerror("Error", f"The selected hour must be between {start_hour} and {end_hour}.")
                raise ValueError(f"The selected hour must be between {start_hour} and {end_hour}.")

            return True

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return False     