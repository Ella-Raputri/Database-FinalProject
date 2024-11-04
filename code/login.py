import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.show_pass_img = tk.PhotoImage(file='images/show_pass.png')
        self.hide_pass_img = tk.PhotoImage(file='images/hide_pass.png')
        self.create_widgets()
    

    def create_widgets(self):
        def show_hide_password():
            if password_entry['show'] == '*':
                password_entry.config(show='')
                show_hide_btn.config(image=self.hide_pass_img)
            else:
                password_entry.config(show='*')
                show_hide_btn.config(image=self.show_pass_img)


        # background
        background_photo = tk.PhotoImage(file='images/login_bg.png')
        self.background_photo = background_photo  
        background_label = tk.Label(self.master, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        title_label = tk.Label(self.master, text="Welcome!", font=("Poppins", 44, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=879, y=40)

        # instruction
        instruction_label = tk.Label(self.master, text="Please login to your account before continue.",
                                     wraplength=682, font=("Poppins", 24), fg=self.master.font_color1, 
                                     bg='white', justify='center')
        instruction_label.place(x=735, y=132)
        
        # email field
        email_label = tk.Label(self.master, text="Email",font=("Poppins Semibold", 20), 
                               fg=self.master.font_color1, bg='white')
        email_label.place(x=730, y=257)

        email_entry = tk.Entry(self.master, font=('Poppins',18), width=38,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        email_entry.place(x=735, y=304)

        # password field
        password_label = tk.Label(self.master, text="Password",font=("Poppins Semibold", 20), 
                               fg=self.master.font_color1, bg='white')
        password_label.place(x=730, y=400)

        password_entry = tk.Entry(self.master, font=('Poppins',18), width=38,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white', show='*')
        password_entry.place(x=735, y=448)

        show_hide_btn = tk.Button(self.master, image=self.show_pass_img, 
                            bd=0, command=show_hide_password, bg='white')
        show_hide_btn.place(x=1260, y=460)


        # login button
        login_btn = tk.Button(self.master, text='Login', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins Semibold', 24), bd=0)
        login_btn.place(x=895, y=560, width=258, height=74)


        # sign up label
        signup_label = tk.Label(self.master, text="Don't have an account yet?",
                                     font=("Poppins", 16), fg=self.master.font_color1, 
                                     bg='white', justify='center')
        signup_label.place(x=800, y=670)

        # here label
        here_label = tk.Label(self.master, text="Sign up here",
                                     font=("Poppins", 16, 'underline'), fg=self.master.font_color1, 
                                     bg='white', justify='center', cursor="hand2")
        here_label.place(x=1101, y=670)
        here_label.bind("<Button-1>", self.click_label_signup)
    

    def click_label_signup(self, event):
        self.master.show_frame(self.master.register_page)