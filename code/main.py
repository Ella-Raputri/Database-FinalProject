import tkinter as tk
from login import LoginPage
from register import RegisterPage
from Admin.admin_dashboard import AdminDashboard
from Admin.admin_doctors import AdminDoctorPage
from Admin.admin_patient import AdminPatientPage
from Admin.admin_booking import AdminBookingPage
from Doctor.doctor_dashboard import DoctorDashboard
from Doctor.history import DoctorHistory
from Doctor.profile import DoctorProfile

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1360x768')
        self.title('Clinic Box Appointment System')

        self.center_window()
        self.font_color1 = '#5182B8' #blue
        self.font_color2 = '#4E4E4E' #black
        self.font_color3 = '#818181' #grey
        self.separator_color = '#B7B7B7'

        self.green_font = '#2FA514'
        self.yellow_font = '#A38500'
        self.red_font = '#8F0101'
        self.bg_color1 = '#358FEE'
        self.disabled_color = '#EBEBEB'

        # login and register
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)

        # admin
        self.admin_bg = '#F5F5F5'
        self.admin_doctor_page = AdminDoctorPage(self)
        self.admin_dashboard = AdminDashboard(self)
        self.admin_patient_page = AdminPatientPage(self)
        self.admin_booking_page = AdminBookingPage(self)

        # doctor
        self.doctor_bg = '#F1F9FF'
        self.doctor_dashboard = DoctorDashboard(self)
        self.doctor_history = DoctorHistory(self)
        self.doctor_profile = DoctorProfile(self)

        self.show_frame(self.login_page)

    # user1@example.com
    # doctor4@example.com

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (1360 // 2)
        y = (screen_height // 2) - (768 // 2)
        self.geometry(f'1360x768+{x}+{y}')
    

    def show_frame(self, frame):
        for widget in self.winfo_children():  
            widget.pack_forget()
        frame.pack(fill='both', expand=True)        
        # frame.pack(pady=30)


if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.mainloop()
