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
        self.branch_no = None
        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((100, 100)))
        
        # patient
        self.profile_pic = self.default_pic
        self.patient_name = None
        self.patient_email = None
        self.patient_gender = None
        self.patient_telp = None
        self.patient_check_type = None
        self.patient_reason = None
        self.patient_date = None
        self.patient_hour = None

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
        print ("navigate_history")
        # self.master.admin_patient_page.set_user_id(self.user_id)
        # self.master.show_frame(self.master.admin_patient_page)
    
    def navigate_profile(self):
        print ("navigate profile")
        # self.master.admin_booking_page.set_user_id(self.user_id)
        # self.master.show_frame(self.master.admin_booking_page)

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

                query2 = "SELECT BranchNo FROM Doctor WHERE DoctorId = %s"
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
        patient_title_label = tk.Label(self, text="Patients", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        patient_title_label.place(x=311, y=172)
        patient_amount_label = tk.Label(self, text="6", font=("Poppins Semibold", 32), fg=self.master.font_color2, bg='white')
        patient_amount_label.place(x=311, y=208)

        # time
        time_title_label = tk.Label(self, text="Time", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        time_title_label.place(x=504, y=172)
        self.time_label = tk.Label(self, text="16:00", font=("Poppins Semibold", 32), fg=self.master.font_color2, bg='white')
        self.time_label.place(x=504, y=208)
        self.update_time()

        # today booking
        today_booking_label = tk.Label(self, text="Today's Booking", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        today_booking_label.place(x=311, y=352)

        # patient view
        patient_view_label = tk.Label(self, text="Patient", font=("Poppins Semibold", 18), fg=self.master.font_color1, bg='white')
        patient_view_label.place(x=780, y=186)

        self.profile_pic_label = tk.Label(self,  bg='white', width=90, height=90)
        self.profile_pic_label.place(x=797, y=251)
        self.profile_pic_label.config(image=self.profile_pic)

        text_desc = "Patient Full Name \nGender : Male \nEmail : 23 \nTelp : 0000 - 0000 - 0000 \
            \nDate : YYYY-MM-DD \nHour : 18.00 - 19.00 \nCheck Up Type: Type 1"
        
        desc_label = tk.Label(self, text=text_desc, font=("Poppins", 12), 
                              justify="left",fg=self.master.font_color2, bg='white')
        desc_label.place(x=933, y=250)

        note_title_label = tk.Label(self, text="Reason of Visit", font=("Poppins Semibold", 14), fg=self.master.font_color2, bg='white')
        note_title_label.place(x=782, y=462)
        self.create_scrollable_reason()

        medical_btn = tk.Button(self, text='Medical History', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0)
        medical_btn.place(x=780, y=373, width=127, height=39)

        self.create_today_booking_scroll()
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.config(text=current_time)
        self.after(60000, self.update_time)

    def create_scrollable_reason(self):
        dummy = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus mollis aliquam ex, in mattis 
ipsum blandit nec. Donec maximus lectus vel augue iaculis tempus. 
Cras facilisis tristique libero, quis imperdiet enim accumsan 
sit amet. Sed in commodo 
"""

        frame1 = tk.Frame(self, bd=0, highlightbackground=self.master.separator_color, highlightthickness=1)
        frame1.place(x=785, y=498, width=510, height=160)

        canvas1 = tk.Canvas(frame1, bg='white')
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
        canvas1.config(yscrollcommand=scrollbar1.set)

        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white', bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        note_label = tk.Label(content1, text=dummy, font=("Poppins", 12), fg=self.master.font_color2, 
                            bg='white', bd=0, wraplength=490, justify="left")
        note_label.pack(fill='x',pady=5)

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

        for i in range(0, 20):            
            label = tk.Label(content1, text=f"Dr. {i}, {i} ({i})", 
                             font=("Poppins", 11), wraplength=260, fg=self.master.font_color2, bg='white')
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
