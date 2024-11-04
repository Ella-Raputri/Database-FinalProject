import tkinter as tk
from login import LoginPage
from register import RegisterPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1360x768')
        self.title('Clinic Box Appointment System')

        self.center_window()
        self.font_color1 = '#5182B8'
        self.bg_color1 = '#358FEE'
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.show_frame(self.login_page)
    

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
    app.mainloop()
