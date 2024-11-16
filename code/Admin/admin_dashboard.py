import tkinter as tk

class AdminDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.create_widgets()

    def create_navbar(self):
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg=self.master.bg_color1, fg="white", font=("Poppins Semibold", 18))
        self.home_btn.place(x=0, y=120, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg=self.master.bg_color1)  
        home_label.place(x=30, y=132)

        # doctor
        self.doctor_btn = tk.Label(self, text="Doctor", bd=0,bg='#64C1F6', fg="white", font=("Poppins Semibold", 18))
        self.doctor_btn.place(x=72, y=191)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg='#64C1F6')  
        doctor_label.place(x=30, y=198)

        # patient
        self.patient_btn = tk.Label(self, text="Patient", bd=0,bg='#5FBBF5', fg="white", font=("Poppins Semibold", 18))
        self.patient_btn.place(x=72, y=248)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg='#5FBBF5')  
        patient_label.place(x=30, y=255)

        # booking
        self.booking_btn = tk.Label(self, text="Booking", bd=0,bg='#5BB7F4', fg="white", font=("Poppins Semibold", 18))
        self.booking_btn.place(x=72, y=310)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#5BB7F4')  
        booking_label.place(x=30, y=317)

    

    def create_widgets(self):
        # background
        self.background_photo = tk.PhotoImage(file='images/admin_dashboard.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()

        # title
        title_label = tk.Label(self, text="Dashboard", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=261, y=28)

        # name login
        name_label = tk.Label(self.master, text="Name", font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self.master, text="Email: ellaraputribinus2023@mail.com", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # patient amount
        patient_amount_label = tk.Label(self, text="8700", font=("Poppins", 36, 'bold'), fg=self.master.font_color2, bg='white')
        patient_amount_label.place(x=283, y=184)

        # patient title
        patient_title_label = tk.Label(self, text="Patients", font=("Poppins Semibold", 20), fg=self.master.font_color2, bg='white')
        patient_title_label.place(x=283, y=147)

        # doctor amount
        doctor_amount_label = tk.Label(self, text="120", font=("Poppins", 36, 'bold'), fg=self.master.font_color2, bg='white')
        doctor_amount_label.place(x=494, y=184)

        # doctor title
        doctor_title_label = tk.Label(self, text="Doctors", font=("Poppins Semibold", 20), fg=self.master.font_color2, bg='white')
        doctor_title_label.place(x=494, y=147)

        # booking amount
        booking_amount_label = tk.Label(self, text="12530", font=("Poppins", 36, 'bold'), fg=self.master.font_color2, bg='white')
        booking_amount_label.place(x=688, y=184)

        # booking title
        booking_title_label = tk.Label(self, text="Bookings", font=("Poppins Semibold", 20), fg=self.master.font_color2, bg='white')
        booking_title_label.place(x=688, y=147)

        # new bookings
        new_booking_label = tk.Label(self, text="New Bookings", font=("Poppins Semibold", 18), fg=self.master.font_color2, bg='white')
        new_booking_label.place(x=942, y=139)

        # new patients
        new_patient_label = tk.Label(self, text="New Patients", font=("Poppins Semibold", 18), fg=self.master.font_color2, bg='white')
        new_patient_label.place(x=942, y=232)

        # new bookings amt
        new_booking_amt_label = tk.Label(self, text="+100 today", font=("Poppins Semibold", 12), fg=self.master.green_font, bg='white')
        new_booking_amt_label.place(x=1200, y=145)

        # new patients amt
        new_patient_amt_label = tk.Label(self, text="+12 today", font=("Poppins Semibold", 12), fg=self.master.green_font, bg='white')
        new_patient_amt_label.place(x=1200, y=239)

        # today's booking 
        today_book_label = tk.Label(self, text="Today's Booking", font=("Poppins Semibold", 20), fg=self.master.font_color2, bg='white')
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

        for i in range(20):
            label = tk.Label(content1, text=f"Dr. Doctor, Patients Name (14:00) {i+1}",font=("Poppins", 12), fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10))  

            separator = tk.Frame(content1, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # today's doctor
        today_doct_label = tk.Label(self, text="Today's Doctor", font=("Poppins Semibold", 20), fg=self.master.font_color2, bg='white')
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

        for i in range(20):
            label = tk.Label(content2, text=f"Dr. Doctor (14:00 -19:00){i+1}",font=("Poppins", 12), fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10), padx=15)  

            separator = tk.Frame(content2, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10),padx=15)

        content2.update_idletasks()
        canvas2.config(scrollregion=canvas2.bbox("all"))
        canvas2.bind("<MouseWheel>", lambda event, canvas=canvas2: self.on_mouse_wheel(event, canvas))
    

        # recent booking
        recent_label = tk.Label(self, text="Recent Booking", font=("Poppins Semibold", 18), fg=self.master.font_color2, bg='white')
        recent_label.place(x=284, y=592)

        # recent date 
        recent_date_label = tk.Label(self, text="Dr. Doctor (DD-MM-YYYY, 14:00)", font=("Poppins", 14), fg=self.master.font_color2, bg='white')
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
