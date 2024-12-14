import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db

class DoctorDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None
        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((100, 100)))
        self.cancel_pic = ImageTk.PhotoImage(Image.open("images/cancel_icon.png"))
        self.complete_pic = ImageTk.PhotoImage(Image.open("images/completed_icon.png"))

        # patient
        self.profile_pic = self.default_pic
        self.current_patient_index = 0
        self.patients = []
        self.pat_amt = 0

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg=self.master.bg_color1, fg="white", 
                                  font=("Poppins Semibold", 18))
        self.home_btn.place(x=0, y=119, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg=self.master.bg_color1)  
        home_label.place(x=25, y=130)

        # history
        self.history_btn = tk.Button(self, text="History", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18),
                                    command=self.navigate_history)
        self.history_btn.place(x=0, y=186,  width=213, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg='#64C1F6')  
        history_label.place(x=23, y=198)

        # profile
        self.profile_btn = tk.Button(self, text="Profile", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_profile)
        self.profile_btn.place(x=0, y=246, width=213, height=52)
        self.profile_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        profile_label = tk.Label(self, image=self.profile_icon, bd=0, bg='#5FBBF5')  
        profile_label.place(x=23, y=257)

    def navigate_history(self):
        self.master.doctor_history.set_user_id(self.user_id)
        self.master.show_frame(self.master.doctor_history)
    
    def navigate_profile(self):
        self.master.doctor_profile.set_user_id(self.user_id)
        self.master.show_frame(self.master.doctor_profile)

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

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def get_patient_amt(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """
                SELECT 
                    COUNT(BookingId) FROM BranchBookings 
                WHERE DoctorId = %s AND AppointmentDate = CURDATE();"""
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.pat_amt = result[0]
                else:
                    messagebox.showerror("Error", "Invalid user.")
                    return
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def create_widgets(self):        
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/doctor_dashboard.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        # title
        title_label = tk.Label(self, text=f"Welcome Dr.{self.name.split()[0]}", font=("Poppins", 36, "bold"), fg='black', bg=self.master.doctor_bg)
        title_label.place(x=261, y=28)

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.doctor_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.doctor_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # patient
        self.get_patient_amt()
        patient_title_label = tk.Label(self, text="Patients", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        patient_title_label.place(x=311, y=172)
        patient_amount_label = tk.Label(self, text=self.pat_amt, font=("Poppins Semibold", 32), fg=self.master.font_color2, bg='white')
        patient_amount_label.place(x=311, y=208)

        # time
        time_title_label = tk.Label(self, text="Time", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        time_title_label.place(x=504, y=172)
        self.time_label = tk.Label(self, text="16:00", font=("Poppins Semibold", 32), fg=self.master.font_color2, bg='white')
        self.time_label.place(x=504, y=208)
        self.update_time()

        self.create_patient_view()

        # today booking
        today_booking_label = tk.Label(self, text="Today's Booking", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        today_booking_label.place(x=311, y=352)
        self.create_today_booking_scroll()
    
    def fetch_patients(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        bb.BookingId, 
                        bb.PatientId, 
                        u.Email, 
                        bb.PatientName,
                        u.Gender,
                        u.PhoneNumber, 
                        p.ProfilePicture,
                        DATE_FORMAT(bb.AppointmentDate, '%Y-%m-%d') AS AppointmentDate, 
                        DATE_FORMAT(bb.AppointmentHour, '%H:%i') AS AppointmentHour, 
                        bb.AppointmentStatus, 
                        bb.CheckUpType, 
                        bb.ReasonOfVisit,
                        p.DateOfBirth
                    FROM BranchBookings bb
                    JOIN `User` u ON bb.PatientId = u.UserId
                    LEFT JOIN Patient p ON bb.PatientId = p.PatientId
                    WHERE bb.DoctorId = %s AND bb.AppointmentStatus = 'Pending'
                    ORDER BY bb.AppointmentDate ASC, STR_TO_DATE(bb.AppointmentHour, '%H:%i') ASC;
                """
                cursor.execute(query, (self.user_id, ))
                result = cursor.fetchall()
                
                self.patients = []
                for row in result:
                    patient = {
                        "booking_id": row[0],
                        "patient_id": row[1],
                        "email": row[2],
                        "name": row[3],
                        "gender": "Male" if row[4] == 0 else "Female",
                        "telp": row[5],
                        "profile_pic": row[6],
                        "date": row[7],
                        "hour": row[8],
                        "status": row[9],
                        "check_type": row[10],
                        "reason": row[11] if row[11] else "N/A",
                        "dob" : row[12]
                    }
                    self.patients.append(patient)
                
                # print(f"Number of patients fetched: {len(self.patients)}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
            self.display_patient_info()

    def display_patient_info(self):
        if self.patients:
            if hasattr(self, 'desc_label'):
                self.desc_label.destroy()

            patient = self.patients[self.current_patient_index]
            # print(patient['profile_pic'])
            
            if patient["profile_pic"]:
                try:
                    img = Image.open(patient["profile_pic"])
                    img = img.resize((90, 90), Image.Resampling.LANCZOS)
                    self.profile_pic = ImageTk.PhotoImage(img)
                    self.profile_pic_label.config(image=self.profile_pic)
                    self.profile_pic_label.image = self.profile_pic
                except Exception as e:
                    print(f"Error loading profile picture: {e}")
                    self.profile_pic_label.config(image=self.default_pic)
                    self.profile_pic_label.image = self.default_pic
            else:
                self.profile_pic_label.config(image=self.default_pic)
                self.profile_pic_label.image = self.default_pic
            
            self.medical_btn = tk.Button(self, text='Medical History', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0, 
                                     command=lambda: self.open_medical(patient['patient_id'], patient['name']))
            self.medical_btn.place(x=780, y=373, width=127, height=39)

            text_desc = f'Patient Full Name : {patient["name"]} \nGender: {patient["gender"]} \nDate of Birth: {patient["dob"]} \nEmail: {patient["email"]} \
            \nTelp: {patient["telp"]} \nDate: {patient["date"]} \nHour: {patient["hour"]} \nCheck Up Type: {patient["check_type"]}'

            self.desc_label = tk.Label(self, text=text_desc, font=("Poppins", 12),
                                justify="left", fg=self.master.font_color2, bg='white')
            self.desc_label.place(x=933, y=235)
            self.create_scrollable_reason(patient["reason"])

            self.cancel_button = tk.Label(self, image=self.cancel_pic, bd=0, highlightthickness=0, bg='white')
            self.cancel_button.bind("<Button-1>", lambda event, id=patient["booking_id"], status='Cancelled': self.update_status_booking(id, status))
            self.cancel_button.place(x=1267, y=186)

            self.complete_button = tk.Label(self, image=self.complete_pic, bd=0, highlightthickness=0, bg='white')
            self.complete_button.bind("<Button-1>", lambda event, id=patient["booking_id"], status='Completed': self.update_status_booking(id, status))
            self.complete_button.place(x=1226, y=186)
        else:
            desc_label = tk.Label(self, text='No patients available', font=("Poppins", 16),
                                fg=self.master.font_color2, bg='white')
            desc_label.place(x=907, y=255)

    def get_medhistory(self, id):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                    d.DiseaseName,  
                    (CASE m.Status 
                        WHEN 0 THEN 'Ongoing'
                        ELSE 'Recovered'
                    END) AS MedStatus
                    FROM MedicalHistory m JOIN Disease d 
                    ON m.DiseaseId = d.DiseaseId
                    WHERE m.PatientId = %s
                    ORDER BY m.Status ASC;
                """
                cursor.execute(query, (id,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def open_medical(self, patient_id, patient_name):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Medical History")
        child_window.geometry("533x676")  

        medical_history = self.get_medhistory(patient_id)

        # medical label
        mhtitle_label = tk.Label(child_window, text=f"{patient_name.split()[0]} Medical History",font=("Poppins Semibold", 24), 
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

        for i, entry in enumerate(medical_history):
            disease = entry[0]
            status = entry[1]
    
            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=disease, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

            # desc label
            desc_label = tk.Label(row_frame, text=status,
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w",padx=(5, 10), pady=(0, 10))
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=206, y=615, width=116, height=40)
        child_window.resizable(False, False)

    def update_status_booking(self, booking_id, status):
        try:
            print('bookingid ', booking_id)
            conn = connect_to_db()
            cursor = conn.cursor()

            query = """
                UPDATE Booking 
                SET AppointmentStatus = %s
                WHERE BookingId = %s
            """
            cursor.execute(query, (status, booking_id))
            conn.commit()

            messagebox.showinfo("Success", "Booking updated successfully!")

        except Exception as e:
            print(f"Error occurred: {e}")
            messagebox.showerror("Error", f"Failed to update booking: {e}")
        finally:
            if conn:
                conn.close()
            self.fetch_patients()

    def create_patient_view(self):
        # patient view
        patient_view_label = tk.Label(self, text="Pending Patients", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        patient_view_label.place(x=780, y=186)

        self.profile_pic_label = tk.Label(self,  bg='white', width=90, height=90)
        self.profile_pic_label.place(x=797, y=251)
        self.profile_pic_label.config(image=self.profile_pic)

        note_title_label = tk.Label(self, text="Reason of Visit", font=("Poppins Semibold", 14), fg=self.master.font_color2, bg='white')
        note_title_label.place(x=782, y=462)

        self.fetch_patients()
        next_btn = tk.Button(self, bg='white',bd=0, text=">", fg='black',
                             font=("Poppins", 24), command=self.next_patient)
        next_btn.place(x=1276, y=664, width=15, height=24)

    def next_patient(self):
        if self.patients:
            self.current_patient_index = (self.current_patient_index + 1) % len(self.patients)
            self.display_patient_info()
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.config(text=current_time)
        self.after(60000, self.update_time)

    def create_scrollable_reason(self, reason):
        frame1 = tk.Frame(self, bd=0, highlightbackground=self.master.separator_color, highlightthickness=1)
        frame1.place(x=785, y=498, width=510, height=150)
        
        canvas1 = tk.Canvas(frame1, bg='white')
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white', bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        note_label = tk.Label(content1, text=reason, font=("Poppins", 12), fg=self.master.font_color2,
                            bg='white', bd=0, wraplength=490, justify="left")
        note_label.pack(fill='x', pady=10)

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas1))

    def create_today_booking_scroll(self):
        # scrollpane today booking
        frame1 = tk.Frame(self)
        frame1.place(x=301, y=418)

        canvas1 = tk.Canvas(frame1, width=379, height=271, bg='white',bd=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white',bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        today = datetime.now().strftime("%Y-%m-%d")

        for pat in self.patients:
            if pat['date'] == today:            
                label = tk.Label(content1, text=f"{pat['name']}, {pat['check_type']} ({pat['hour']})", justify='left',
                                font=("Poppins", 11), wraplength=380, fg=self.master.font_color2, bg='white')
                label.pack(fill='x', pady=(0, 10))

                separator = tk.Frame(content1, height=1, bg=self.master.separator_color)
                separator.pack(fill='x', pady=(0, 10))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  
            canvas.yview_scroll(-1, "units")
        else:  
            canvas.yview_scroll(1, "units")
