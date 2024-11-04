import tkinter as tk

class RegisterPage(tk.Frame):
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
        
        def show_hide_confirm_password():
            if confirm_password_entry['show'] == '*':
                confirm_password_entry.config(show='')
                confirm_show_hide_btn.config(image=self.hide_pass_img)
            else:
                confirm_password_entry.config(show='*')
                confirm_show_hide_btn.config(image=self.show_pass_img)



        # background
        self.background_photo = tk.PhotoImage(file='images/signup_bg.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        title_label = tk.Label(self, text="Register", font=("Poppins", 40, "bold"), fg=self.master.font_color1, bg='white')
        title_label.place(x=111, y=85)

        # instruction
        instruction_label = tk.Label(self, text="Please fill in the required information.",
                                     font=("Poppins", 16), fg=self.master.font_color1, 
                                     bg='white')
        instruction_label.place(x=111, y=163)
        
        # email field
        email_label = tk.Label(self, text="Email",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        email_label.place(x=111, y=232)

        email_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        email_entry.place(x=111, y=273)


        # password field
        password_label = tk.Label(self, text="Password",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        password_label.place(x=111, y=359)

        password_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white', show='*')
        password_entry.place(x=111, y=401)

        show_hide_btn = tk.Button(self, image=self.show_pass_img, 
                            bd=0, command=show_hide_password, bg='white')
        show_hide_btn.place(x=565, y=412)


        # confirm password field
        confirm_password_label = tk.Label(self, text="Confirm Password",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        confirm_password_label.place(x=111, y=494)

        confirm_password_entry = tk.Entry(self, font=('Poppins',16), width=39,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white', show='*')
        confirm_password_entry.place(x=111, y=532)

        confirm_show_hide_btn = tk.Button(self, image=self.show_pass_img, 
                            bd=0, command=show_hide_confirm_password, bg='white')
        confirm_show_hide_btn.place(x=565, y=544)


        # login label
        login_label = tk.Label(self, text="Already have an account?",
                                     font=("Poppins", 16), fg=self.master.font_color1, 
                                     bg='white', justify='center')
        login_label.place(x=136, y=645)

        # here label
        here_label = tk.Label(self, text="Login here",
                                     font=("Poppins", 16, 'underline'), fg=self.master.font_color1, 
                                     bg='white', justify='center', cursor="hand2")
        here_label.place(x=415, y=645)
        here_label.bind("<Button-1>", self.click_label_login)


        # fname field
        fname_label = tk.Label(self, text="First Name",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        fname_label.place(x=679, y=102)

        fname_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        fname_entry.place(x=679, y=145)


        # lname field
        lname_label = tk.Label(self, text="Last Name",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        lname_label.place(x=978, y=102)

        lname_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        lname_entry.place(x=978, y=145)

        # phone field
        phone_label = tk.Label(self, text="Phone Number",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        phone_label.place(x=679, y=230)

        phone_entry = tk.Entry(self, font=('Poppins',16), width=42,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        phone_entry.place(x=679, y=273)


        # dob field
        dob_label = tk.Label(self, text="Date of Birth",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        dob_label.place(x=679, y=358)

        dob_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        dob_entry.place(x=679, y=401)


        # city field
        city_label = tk.Label(self, text="Last Name",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        city_label.place(x=978, y=358)

        city_entry = tk.Entry(self, font=('Poppins',16), width=19,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        city_entry.place(x=978, y=401)

        # address field
        address_label = tk.Label(self, text="Address Details",font=("Poppins Semibold", 18), 
                               fg=self.master.font_color1, bg='white')
        address_label.place(x=679, y=494)

        address_entry = tk.Entry(self, font=('Poppins',16), width=42,
                        highlightcolor=self.master.font_color1,
                        highlightbackground='grey',highlightthickness=2,
                        bd=0, bg='white')
        address_entry.place(x=679, y=532)


        # submit btn
        submit_btn = tk.Button(self, text='Submit', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins Semibold', 18), bd=0)
        submit_btn.place(x=1120, y=635, width=128, height=49)
    

    def click_label_login(self, event):
        self.master.show_frame(self.master.login_page)