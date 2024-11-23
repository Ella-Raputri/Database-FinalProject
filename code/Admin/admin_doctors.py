import tkinter as tk
from tkinter import ttk

class AdminDoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
    
    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def navigate_home(self):
        self.master.admin_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_dashboard)
    
    def navigate_patient(self):
        self.master.admin_patient_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_patient_page)
    
    def navigate_booking(self):
        self.master.admin_booking_page.set_user_id(self.user_id)
        self.master.show_frame(self.master.admin_booking_page)
    
    def create_navbar(self):
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                 font=("Poppins Semibold", 18), command=self.navigate_home)
        self.home_btn.place(x=0, y=120, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=23, y=130)

        # doctor
        self.doctor_btn = tk.Button(self, text="Doctor", bd=0,bg=self.master.bg_color1, fg="white", 
                                    font=("Poppins Semibold", 18))
        self.doctor_btn.place(x=0, y=183,  width=213, height=52)
        self.doctor_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        doctor_label = tk.Label(self, image=self.doctor_icon, bd=0, bg=self.master.bg_color1)  
        doctor_label.place(x=23, y=196)

        # patient
        self.patient_btn = tk.Button(self, text="Patient", bd=0,bg='#5FBBF5', fg="white", 
                                    font=("Poppins Semibold", 18), command=self.navigate_patient)
        self.patient_btn.place(x=0, y=243, width=213, height=52)
        self.patient_icon = tk.PhotoImage(file='images/patient_icon.png')  
        patient_label = tk.Label(self, image=self.patient_icon, bd=0, bg='#5FBBF5')  
        patient_label.place(x=23, y=255)

        # booking
        self.booking_btn = tk.Button(self, text=" Booking", bd=0,bg='#5BB7F4', fg="white", 
                                    font=("Poppins Semibold", 18),command=self.navigate_booking)
        self.booking_btn.place(x=0, y=300, width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#5BB7F4')  
        booking_label.place(x=23, y=311)


    def create_widgets(self):
        # background
        self.background_photo = tk.PhotoImage(file='images/admin_default.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()

        # title
        title_label = tk.Label(self, text="Doctors", font=("Poppins", 38, "bold"), fg='black', bg=self.master.admin_bg)
        title_label.place(x=248, y=20)

        # name login
        name_label = tk.Label(self, text="Name", font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text="Email: ellaraputribinus2023@mail.com", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select():
            selected_option = combo.get()
            print(f"Selected: {selected_option}")

        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        combo = ttk.Combobox(self, values=options, font=("Poppins", 16),state='readonly')
        combo.set("Filter")  
        combo.place(x=1220, y=112, width=114, height=42)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.filter_img = tk.PhotoImage(file='images/filter_icon.png')
        filter_icon = tk.Label(self, image=self.filter_img)  
        filter_icon.place(x=1182, y=124) 

        # specialty panel
        self.specialty_panel = tk.Frame(self, bg='white',bd=1,relief='groove')
        self.specialty_panel.place(x=1170, y=180, width=165, height=215)

        self.specialty_label = tk.Label(self.specialty_panel, text="Specialty", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg='white')
        self.specialty_label.place(x=10, y=11)

        alist = ["First item", "Second item", "Third item", "Fourth item"]

        if len(alist) >= 4:
            for i in range(3):  
                label = tk.Label(self.specialty_panel, text=f"• {alist[i]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  
                
        else:
            for i in range(len(alist)): 
                label = tk.Label(self.specialty_panel, text=f"• {alist[i]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  

        
        spview_more_btn = tk.Button(self.specialty_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0, command=self.open_specialties)
        spview_more_btn.place(x=30, y=161, width=110, height=32)


        # schedule panel
        self.schedule_panel = tk.Frame(self, bg='white',bd=1,relief='groove')
        self.schedule_panel.place(x=1170, y=180 + 215 + 10, width=165, height=165)

        self.schedule_label = tk.Label(self.schedule_panel, text="Schedule", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg='white')
        self.schedule_label.place(x=10, y=11)

        alist = ["First item", "Second item", "Third item", "Fourth item"]

        if len(alist) >= 3:
            for i in range(2):  
                label = tk.Label(self.schedule_panel, text=f"• {alist[i]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  
                
        else:
            for i in range(len(alist)): 
                label = tk.Label(self.schedule_panel, text=f"• {alist[i]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  

        
        scview_more_btn = tk.Button(self.schedule_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), command=self.open_schedule,bd=0)
        scview_more_btn.place(x=30, y=120, width=110, height=32)

        # add btn
        add_btn = tk.Button(self, text='Add', bg='white',
                                     fg=self.master.green_font, font=('Poppins Medium', 14), bd=0)
        add_btn.place(x=1180, y=590, width=135, height=35)

        # edit btn
        edit_btn = tk.Button(self, text='Edit', bg='white',
                                     fg=self.master.yellow_font, font=('Poppins Medium', 14), bd=0)
        edit_btn.place(x=1180, y=641, width=135, height=35)

        # delete btn
        delete_btn = tk.Button(self, text='Delete', bg='white',
                                     fg=self.master.red_font, font=('Poppins Medium', 14), bd=0)
        delete_btn.place(x=1180, y=692, width=135, height=35)

        self.create_table()

    
    def create_table(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Semibold", 12))

        table_frame = tk.Frame(self)
        table_frame.place(x=248, y=114, width=900, height=610)

        columns = [f"Column {i+1}" for i in range(8)]  
        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor=tk.CENTER)

        for i in range(50):  
            row = [f"Row {i+1} Col {j+1}" for j in range(8)]
            table.insert("", tk.END, values=row)
            table.insert("", tk.END, values=[""] * 8)
        
        table.tag_configure("odd_row", background="#f2f7fd", font=("Poppins", 12))
        table.tag_configure("even_row", background="white", font=("Poppins", 12))

        # # Assign odd/even row tags
        for i, item in enumerate(table.get_children()):
            table.item(item, tags=("odd_row" if ((i % 4 == 0) or (i % 4 == 1)) else "even_row"))
            table.item(item, open=True)

        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=table.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        table.pack(fill=tk.BOTH, expand=True)


    def open_specialties(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Specialty")
        child_window.geometry("533x676")  

        # specialty label
        sptitle_label = tk.Label(child_window, text="Specialties",font=("Poppins Semibold", 32), 
                                 fg='black', bg='white')
        sptitle_label.place(x=142, y=18)

        # scrollpane specialties
        frame1 = tk.Frame(child_window, bd=1, highlightthickness=1)
        frame1.place(x=26, y=100)

        canvas1 = tk.Canvas(frame1, width=470, height=486, bg='white')
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white')
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        self.delete_photo = tk.PhotoImage(file='images/delete_icon.png')
        self.edit_photo = tk.PhotoImage(file='images/edit_icon.png')

        for i in range(20):
            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=f"Cardiology {i+1}", font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                   command=lambda i=i: print(f'edit sp {i+1}'))
            edit_button.grid(row=0, column=1, padx=(10, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda i=i: print(f'delete sp {i+1}'))
            delete_button.grid(row=0, column=2, padx=(5, 0), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text="This is a wrapped label. The text will wrap if it exceeds the specified width.",
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w")
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=lambda: print(f'add sp'))
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=211, y=615, width=116, height=40)

        child_window.resizable(False, False)


    def open_schedule(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Schedule")
        child_window.geometry("533x676")  

        # schedule label
        sctitle_label = tk.Label(child_window, text="Dr Doctor Schedule",font=("Poppins Semibold", 28), 
                                 fg='black', bg='white')
        sctitle_label.place(x=90, y=18)

        # scrollpane schedule
        frame1 = tk.Frame(child_window, bd=1, highlightthickness=1)
        frame1.place(x=26, y=100)

        canvas1 = tk.Canvas(frame1, width=470, height=486, bg='white')
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white')
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        self.delete_photo = tk.PhotoImage(file='images/delete_icon.png')
        self.edit_photo = tk.PhotoImage(file='images/edit_icon.png')

        for i in range(20):
            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=f"Day {i+1}", font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                   command=lambda i=i: print(f'edit sc {i+1}'))
            edit_button.grid(row=0, column=1, padx=(0, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda i=i: print(f'delete sc {i+1}'))
            delete_button.grid(row=0, column=2, padx=(0, 5), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text="This is a wrapped label. The text will wrap if it exceeds the specified width.",
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w",padx=(5, 10), pady=(0, 10))
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=lambda: print(f'add sc'))
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=206, y=615, width=116, height=40)

        child_window.resizable(False, False)


    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  # Scroll up
            canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            canvas.yview_scroll(1, "units")

    
    