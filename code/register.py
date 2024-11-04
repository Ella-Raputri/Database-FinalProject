import tkinter as tk

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, highlightbackground=parent.font_color1,
                         highlightthickness=3)
        self.configure(width=400, height=420)
        self.create_widgets()

    def create_widgets(self):
        heading_label = tk.Label(self, text="Welcomessss to System",
                                  fg='white', bg=self.master.font_color1, font=('Bold', 18))
        heading_label.place(x=0, y=0, width=400)

    #     heading_label = tk.Label(self, text="Student Login Page",
    #                               fg='white', bg=self.master.bg_color, font=('Bold', 18))
    #     heading_label.place(x=0, y=0, width=400)

    #     stud_icon_label = tk.Label(self, image=self.master.login_stud_icon)
    #     stud_icon_label.place(x=150, y=40)

    #     id_num_label = tk.Label(self, text='Enter Student ID Number:',
    #                              font=('Bold', 15), fg=self.master.bg_color)
    #     id_num_label.place(x=80, y=140)

    #     self.id_num_ent = tk.Entry(self, font=('Bold', 15), justify=tk.CENTER,
    #                                highlightcolor=self.master.bg_color,
    #                                highlightbackground='gray', highlightthickness=2)
    #     self.id_num_ent.place(x=80, y=190)

    #     pass_label = tk.Label(self, text='Enter Password:',
    #                           font=('Bold', 15), fg=self.master.bg_color)
    #     pass_label.place(x=80, y=240)

    #     self.pass_ent = tk.Entry(self, font=('Bold', 15), justify=tk.CENTER,
    #                              highlightcolor=self.master.bg_color,
    #                              highlightbackground='gray', highlightthickness=2,
    #                              show='*')
    #     self.pass_ent.place(x=80, y=290)

    #     self.show_hide_btn = tk.Button(self, image=self.master.locked_icon,
    #                                     bd=0, command=self.show_hide_password)
    #     self.show_hide_btn.place(x=310, y=280)

    #     login_btn = tk.Button(self, text='Login',
    #                           font=('Bold', 15), bg=self.master.bg_color, fg='white')
    #     login_btn.place(x=95, y=340, width=200, height=40)

    #     forget_pass_btn = tk.Button(self, text='⚠️\nForget Password',
    #                                  fg=self.master.bg_color, bd=0)
    #     forget_pass_btn.place(x=150, y=390)

    # def show_hide_password(self):
    #     if self.pass_ent['show'] == '*':
    #         self.pass_ent.config(show='')
    #         self.show_hide_btn.config(image=self.master.unlocked_icon)
    #     else:
    #         self.pass_ent.config(show='*')
    #         self.show_hide_btn.config(image=self.master.locked_icon)