import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db

class DoctorHistory(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None

        self.patient_id = None
        self.patient_name = None
        self.filter_field = "CONCAT(AppointmentDate, ' ', STR_TO_DATE(bb.AppointmentHour, '%H:%i'))"
        self.sort_order = 'ASC'
        self.table_data = []

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                  font=("Poppins Semibold", 18),
                                    command=self.navigate_home)
        self.home_btn.place(x=0, y=119, width=213, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=25, y=130)

        # history
        self.history_btn = tk.Button(self, text="History", bd=0,bg=self.master.bg_color1, fg="white", 
                                    font=("Poppins Semibold", 18))
        self.history_btn.place(x=0, y=186,  width=213, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg=self.master.bg_color1)  
        history_label.place(x=23, y=198)

        # profile
        self.profile_btn = tk.Button(self, text="Profile", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_profile)
        self.profile_btn.place(x=0, y=246, width=213, height=52)
        self.profile_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        profile_label = tk.Label(self, image=self.profile_icon, bd=0, bg='#5FBBF5')  
        profile_label.place(x=23, y=257)

    def navigate_home(self):
        self.master.doctor_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.doctor_dashboard)
    
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

    def create_widgets(self):        
        self.get_user_info()
        # background
        self.background_photo = tk.PhotoImage(file='images/doctor_default.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        # title
        title_label = tk.Label(self, text=f"Booking History", font=("Poppins", 36, "bold"), fg='black', bg=self.master.doctor_bg)
        title_label.place(x=261, y=28)

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.doctor_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.doctor_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select(event):
            selected_option = combo.get()
            if selected_option == 'Date & Hour': selected_option = "CONCAT(AppointmentDate, ' ', STR_TO_DATE(bb.AppointmentHour, '%H:%i'))"
            elif selected_option == 'Name': selected_option = 'bb.PatientName'
            elif selected_option == 'DOB': selected_option = 'p.DateOfBirth'
            elif selected_option == 'Status': selected_option = 'bb.AppointmentStatus'            
            
            self.filter_field = selected_option  
            self.create_table()

        options = ["Date & Hour", "Name", "DOB", "Status"]
        combo = ttk.Combobox(self, values=options, font=("Poppins", 12), state='readonly')
        combo.set("Filter")
        combo.place(x=1214, y=112, width=135, height=42)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.sort_img = tk.PhotoImage(file='images/sort_ascending.png')  
        sort_icon = tk.Label(self, image=self.sort_img, bg=self.master.doctor_bg)
        sort_icon.place(x=1182, y=124)

        def toggle_sort():
            if self.sort_order == 'ASC':
                self.sort_order = 'DESC'
                self.sort_img = tk.PhotoImage(file='images/sort_descending.png')
            else:
                self.sort_order = 'ASC'
                self.sort_img = tk.PhotoImage(file='images/sort_ascending.png')
            sort_icon.config(image=self.sort_img)
            self.create_table() 

        sort_icon.bind("<Button-1>", lambda e: toggle_sort()) 
        self.create_table()

        # medical panel
        self.medical_panel = tk.Frame(self, bg=self.master.disabled_color,bd=1,relief='groove')
        self.medical_panel.place(x=1170, y=180, width=165, height=200)

        self.medical_label = tk.Label(self.medical_panel, text="Med. History", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg=self.master.disabled_color)
        self.medical_label.place(x=10, y=11)
        
        mdview_more_btn = tk.Button(self.medical_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12),state=tk.DISABLED, bd=0)
        mdview_more_btn.place(x=30, y=148, width=110, height=35)

    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = f"""
                    SELECT 
                        bb.BookingId, 
                        bb.PatientId, 
                        DATE_FORMAT(bb.AppointmentDate, '%Y-%m-%d') AS AppointmentDate, 
                        DATE_FORMAT(bb.AppointmentHour, '%H:%i') AS AppointmentHour,
                        bb.PatientName,
                        CASE u.Gender 
                            WHEN 0 THEN 'Male'
                            ELSE 'Female'
                        END AS Gender,
                        p.DateOfBirth,
                        u.Email,
                        u.PhoneNumber,  
                        bb.AppointmentStatus, 
                        bb.CheckUpType, 
                        bb.ReasonOfVisit
                    FROM BranchBookings bb
                    JOIN `User` u ON bb.PatientId = u.UserId
                    LEFT JOIN Patient p ON bb.PatientId = p.PatientId
                    WHERE bb.DoctorId = %s
                    ORDER BY 
                        {self.filter_field} {self.sort_order};                
                """
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchall()
                self.table_data = result  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def create_table(self):
        self.get_table_data()
        self.patient_ids = {}

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Semibold", 14))
        style.configure("Treeview", rowheight=40, font=("Poppins", 12))

        table_frame = tk.Frame(self)
        table_frame.place(x=248, y=114, width=900, height=610)

        columns = ['Appointment Date','Appointment Hour','Name', 'Gender', 'Date of Birth',
                   'Email', 'Phone Number', 'Status', 'Check-Up Type', 'Reason of Visit']  
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=230, anchor=tk.CENTER)

        for i, row in enumerate(self.table_data):
            display_row = row[2:]
            tags = "odd_row" if i % 2 == 0 else "even_row"
            item_id = self.table.insert("", tk.END, values=display_row, tags=(tags,))
            self.patient_ids[item_id] = row[1]
        
        self.table.tag_configure("odd_row", background="#f2f7fd", font=("Poppins", 12))
        self.table.tag_configure("even_row", background="white", font=("Poppins", 12))

        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<<TreeviewSelect>>", lambda event: self.update_medical_panel(event))

    def update_medical_panel(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            item_id = selected_item[0]
            self.patient_id = self.patient_ids.get(item_id)
            self.history = self.get_medhistory()

            item = self.table.item(item_id)
            self.patient_name = item['values'][2]

            for widget in self.medical_panel.winfo_children():
                widget.destroy()  

            self.medical_panel.config(bg='white')
            self.medical_label = tk.Label(self.medical_panel, text="Med. History", 
                                           font=("Poppins Semibold", 15), fg=self.master.font_color2, bg='white')
            self.medical_label.place(x=6, y=11)

            if self.history:
                for i, entry in enumerate(self.history[:3]):  
                    label = tk.Label(self.medical_panel, text=f"• {entry}", font=("Poppins", 10), bg="white", anchor="w")
                    label.place(x=6, y=49 + i * 25)
            else:
                label = tk.Label(self.medical_panel, text="No history", font=("Poppins", 10), bg="white", anchor="w")
                label.place(x=6, y=49)
            
            self.mdview_more_btn = tk.Button(self.medical_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11), command=self.open_medical,bd=0)
            self.mdview_more_btn.place(x=30, y=148, width=110, height=35)
        
    def get_medhistory(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                    CONCAT(d.DiseaseName, ': ', 
                            CASE m.Status 
                                WHEN 0 THEN 'Ongoing'
                                ELSE 'Recovered'
                            END
                        ) AS MedHistory
                    FROM MedicalHistory m JOIN Disease d 
                    ON m.DiseaseId = d.DiseaseId
                    WHERE m.PatientId = %s
                    ORDER BY m.Status ASC;
                """
                cursor.execute(query, (self.patient_id,))
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def open_medical(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Medical History")
        child_window.geometry("533x676")  

        # medical label
        mhtitle_label = tk.Label(child_window, text=f"{self.patient_name.split()[0]} Medical History",font=("Poppins Semibold", 24), 
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

        self.delete_photo = tk.PhotoImage(file='images/delete_icon.png')
        self.edit_photo = tk.PhotoImage(file='images/edit_icon.png')

        for i, entry in enumerate(self.history):
            disease = entry.split(':')[0].strip()
            status = entry.split()[-1].strip()
    
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
    
    def populate_disease(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT DiseaseName FROM Disease")
                self.all_diseases = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch diseases: {e}")
            return
        finally:
            if conn:
                conn.close()
    
    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  
            canvas.yview_scroll(-1, "units")
        else:  
            canvas.yview_scroll(1, "units")
