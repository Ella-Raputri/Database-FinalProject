import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from connection import connect_to_db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdminDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # user
        self.user_id = None
        self.email = None
        self.name = None
        self.branch_no = None

        # branch info
        self.doctor_amt = None
        self.booking_amt = None
        self.today_booking_amt = None

        # chart info
        self.chart_point = None
        
        # booking and doctor info
        self.recent_booking = None
        self.recent_booking_time = None
        self.today_booking = None
        self.today_doctor = None

        self.master = parent        
    
    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
        # print("user print ", self.user_id)
    
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

    def get_branch_amt(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query1 = "SELECT COUNT(DoctorId) FROM Doctor WHERE BranchNo = %s"
                cursor.execute(query1, (self.branch_no,))
                result = cursor.fetchone()
                
                if result:
                    self.doctor_amt = result[0]
                else:
                    messagebox.showerror("Error", "Invalid command.")
                    return

                query2 = """
                    SELECT COUNT(BookingId) 
                    FROM BranchBookings 
                    WHERE BranchNo = %s
                """
                cursor.execute(query2, (self.branch_no,))
                result2 = cursor.fetchone()
                
                if result2:
                    self.booking_amt = result2[0]
                else:
                    messagebox.showerror("Error", "Branch details not found.")
                    return

                today = date.today()  
                query3 = """
                    SELECT COUNT(BookingId) 
                    FROM BranchBookings 
                    WHERE BranchNo = %s AND AppointmentDate = %s
                """
                cursor.execute(query3, (self.branch_no, today))
                result3 = cursor.fetchone()
                
                if result3:
                    self.today_booking_amt = result3[0]
                else:
                    messagebox.showerror("Error", "No bookings found for today.")
                    return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def navigate_doctor(self):
        self.master.admin_doctor_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_doctor_page)
    
    def navigate_patient(self):
        self.master.admin_patient_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_patient_page)
    
    def navigate_booking(self):
        self.master.admin_booking_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_booking_page)
        
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg=self.master.bg_color1, fg="white", 
                                  font=("Poppins Semibold", 18))
        self.home_btn.place(x=0, y=120, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg=self.master.bg_color1)  
        home_label.place(x=23, y=130)

        # doctor
        self.doctor_btn = tk.Button(self, text="Doctor", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18),
                                    command=self.navigate_doctor)
        self.doctor_btn.place(x=0, y=183,  width=213, height=52)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg='#64C1F6')  
        doctor_label.place(x=23, y=196)

        # patient
        self.patient_btn = tk.Button(self, text="Patient", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_patient)
        self.patient_btn.place(x=0, y=243, width=213, height=52)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg='#5FBBF5')  
        patient_label.place(x=23, y=255)

        # booking
        self.booking_btn = tk.Button(self, text=" Booking", bd=0,bg='#5BB7F4', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_booking)
        self.booking_btn.place(x=0, y=300, width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#5BB7F4')  
        booking_label.place(x=23, y=311)

    def get_today_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                # get total bookings per month
                query1 = """
                    SELECT 
                        DATE_FORMAT(AppointmentDate, '%Y-%m') AS BookingMonth, 
                        COUNT(*) AS TotalBookings
                    FROM BranchBookings
                    WHERE BranchNo = %s
                    GROUP BY BookingMonth
                    ORDER BY BookingMonth;"""
                
                cursor.execute(query1, (self.branch_no,))
                results = cursor.fetchall()
                
                if results:
                    self.chart_point = [{"BookingMonth": row[0], "TotalBookings": row[1]} for row in results]
                else:
                    self.chart_point = []
                    messagebox.showerror("Error", "Invalid command.")
                    return

                # get recent booking for this branch
                query2 = """
                    SELECT 
                        SUBSTRING_INDEX(DoctorName, ' ', 1) AS DoctorFirstName, 
                        AppointmentDate, 
                        DATE_FORMAT(AppointmentHour, '%H:%i') AS AppointmentTime
                    FROM BranchBookings 
                    WHERE BranchNo = %s
                    ORDER BY AppointmentDate DESC LIMIT 1
                """
                cursor.execute(query2, (self.branch_no,))
                result2 = cursor.fetchone()
                
                if result2:
                    self.recent_booking = f"Dr. {result2[0]} ({result2[1]}, {result2[2]})"
                else:
                    messagebox.showerror("Error", "Booking details not found.")
                    return

                # get today's booking list
                today = date.today()  
                query3 = """
                    SELECT 
                        SUBSTRING_INDEX(DoctorName, ' ', 1) AS DoctorFirstName, 
                        SUBSTRING_INDEX(PatientName, ' ', 1) AS PatientFirstName, 
                        DATE_FORMAT(AppointmentHour, '%H:%i') AS AppointmentTime
                    FROM BranchBookings 
                    WHERE BranchNo = %s AND AppointmentDate = %s

                """
                cursor.execute(query3, (self.branch_no, today))
                result3 = cursor.fetchall()
                
                if result3:
                    self.today_booking = [
                        {
                            'DoctorName': row[0],
                            'PatientName': row[1],
                            'AppointmentTime': row[2]
                        } 
                        for row in result3
                    ]
                else:
                    self.today_booking = []
                    print("No bookings found for today.")
                
                # get today's doctor list
                query4 = """
                    SELECT DISTINCT
                        SUBSTRING_INDEX(b.DoctorName, ' ', 1) AS DoctorFirstName, 
                        DATE_FORMAT(ds.StartHour, '%H:%i') AS StartTime, 
                        DATE_FORMAT(ds.EndHour, '%H:%i') AS EndTime
                    FROM DoctorSchedule ds
                    INNER JOIN BranchBookings b ON ds.DoctorId = b.DoctorId
                    WHERE ds.DayOfWeek = %s AND b.BranchNo = %s;
                """
                cursor.execute(query4, (today.strftime('%A'), self.branch_no))  
                result4 = cursor.fetchall()

                if result4:
                    self.today_doctor = [
                        {
                            'DoctorName': row[0],
                            'StartHour': row[1],
                            'EndHour': row[2]
                        }
                        for row in result4
                    ]
                else:
                    self.today_doctor = []
                    print("No doctors are scheduled to practice today.")


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_area_chart(self):
        points = self.chart_point[:12]
        months = [item["BookingMonth"].split('-')[1] for item in points]  
        totals = [item["TotalBookings"] for item in points]

        fig, ax = plt.subplots(figsize=(5, 3))  
        
        ax.fill_between(months, totals, color="skyblue", alpha=0.4)
        ax.plot(months, totals, color="Slateblue", alpha=0.7, linewidth=2)

        ax.set_title("Total Bookings per Month", fontsize=10)
        ax.set_xlabel("Month", fontsize=8)
        ax.set_ylabel("Total Bookings", fontsize=8)
        ax.grid(True, alpha=0.3)
        
        ax.set_xticks(months)  
        ax.tick_params(axis="x", labelrotation=45, labelsize=7)  
        ax.tick_params(axis="y", labelsize=7)  
        plt.tight_layout(pad=1.0)

        canvas = FigureCanvasTkAgg(fig, master=self)  
        canvas.draw()
        
        canvas.get_tk_widget().place(x=265, y=137, width=410, height=300)  

    def create_widgets(self):        
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/admin_dashboard.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()

        # title
        title_label = tk.Label(self, text="Dashboard", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=261, y=28)

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        self.get_branch_amt()
        self.get_today_info()
        self.create_area_chart()

        today = datetime.today()
        current_month = today.month
        diff = self.chart_point[current_month]['TotalBookings'] - self.chart_point[current_month-1]['TotalBookings']
        percent = (diff / self.chart_point[current_month-1]['TotalBookings']) * 100

        # percent amount
        if (diff > 0):
            percent_amount_label = tk.Label(self, text=f"+{percent:.2f}% from last month", font=("Poppins", 12), fg=self.master.font_color2, bg='white')
        else:
            percent_amount_label = tk.Label(self, text=f"{percent:.2f}% from last month", font=("Poppins", 12), fg=self.master.font_color2, bg='white')
        percent_amount_label.place(x=470, y=502)

        # percent title
        percent_title_label = tk.Label(self, text="Total Booking", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        percent_title_label.place(x=283, y=494)

        # doctor amount
        doctor_amount_label = tk.Label(self, text=self.doctor_amt, font=("Poppins", 36, 'bold'), fg=self.master.font_color2, bg='white')
        doctor_amount_label.place(x=747, y=184)

        # doctor title
        doctor_title_label = tk.Label(self, text="Doctors", font=("Poppins Semibold", 20), fg=self.master.font_color1, bg='white')
        doctor_title_label.place(x=747, y=147)

        # booking amount
        booking_amount_label = tk.Label(self, text=self.booking_amt, font=("Poppins", 36, 'bold'), fg=self.master.font_color2, bg='white')
        booking_amount_label.place(x=1001, y=184)

        # booking title
        booking_title_label = tk.Label(self, text="Bookings", font=("Poppins Semibold", 20), fg=self.master.font_color1, bg='white')
        booking_title_label.place(x=1001, y=147)

        # new bookings amt
        new_booking_amt_label = tk.Label(self, text=f"Today: {self.today_booking_amt}", font=("Poppins Semibold", 12), fg=self.master.green_font, bg='white')
        new_booking_amt_label.place(x=1204, y=240)

        # today's booking 
        today_book_label = tk.Label(self, text="Today's Booking", font=("Poppins Semibold", 20), fg=self.master.font_color1, bg='white')
        today_book_label.place(x=1060, y=333)

        # scrollpane today booking
        frame1 = tk.Frame(self)
        frame1.place(x=1035, y=393)

        canvas1 = tk.Canvas(frame1, width=265, height=310, bg='white',bd=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white',bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        for booking in self.today_booking:
            doctor_name = booking['DoctorName']
            patient_name = booking['PatientName']
            appointment_time = booking['AppointmentTime']
            
            label = tk.Label(content1, text=f"Dr. {doctor_name}, {patient_name} ({appointment_time})", 
                             font=("Poppins", 11), wraplength=260, fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10))

            separator = tk.Frame(content1, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # today's doctor
        today_doct_label = tk.Label(self, text="Today's Doctor", font=("Poppins Semibold", 20), fg=self.master.font_color1, bg='white')
        today_doct_label.place(x=745, y=333)

        # scrollpane today doctor
        frame2 = tk.Frame(self)
        frame2.place(x=720, y=393)

        canvas2 = tk.Canvas(frame2, width=250, height=310, bg='white',bd=0, highlightthickness=0)
        scrollbar2 = tk.Scrollbar(frame2, orient="vertical", command=canvas2.yview, bg='white')
        canvas2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.pack(side="right", fill="y")
        canvas2.pack(side="left", fill="both", expand=True)

        content2 = tk.Frame(canvas2, bg='white',bd=0, highlightthickness=0)
        canvas2.create_window((0, 0), window=content2, anchor="nw")

        for doct in self.today_doctor:
            doctor_name = doct['DoctorName']
            start = doct['StartHour']
            end = doct['EndHour']
            
            label = tk.Label(content2, text=f"Dr. {doctor_name} ({start} - {end})", font=("Poppins", 12), fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10))

            separator = tk.Frame(content2, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10),padx=15)

        content2.update_idletasks()
        canvas2.config(scrollregion=canvas2.bbox("all"))
        canvas2.bind("<MouseWheel>", lambda event, canvas=canvas2: self.on_mouse_wheel(event, canvas))
    

        # recent booking
        recent_label = tk.Label(self, text="Latest Booking", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        recent_label.place(x=284, y=592)

        # recent date 
        recent_date_label = tk.Label(self, text=self.recent_booking, font=("Poppins", 14), fg=self.master.font_color2, bg='white')
        recent_date_label.place(x=284, y=632)

        # view more button
        view_more_btn = tk.Button(self, text='View More', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0)
        view_more_btn.place(x=571, y=673, width=99, height=33)

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  # Scroll up
            canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            canvas.yview_scroll(1, "units")
