import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db
import os, shutil,re

class PatientHistory(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None

        self.filter_field = "CONCAT(AppointmentDate, ' ', STR_TO_DATE(bb.AppointmentHour, '%H:%i'))"
        self.sort_order = 'ASC'
        self.table_data = []

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                  font=("Poppins Semibold", 18), command=self.navigate_home)
        self.home_btn.place(x=0, y=119, width=226, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=27, y=130)

        # booking
        self.booking_btn = tk.Button(self, text="    Booking", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18),
                                    command=self.navigate_booking)
        self.booking_btn.place(x=0, y=186,  width=226, height=52)
        self.booking_icon = tk.PhotoImage(file='images/pat_booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#64C1F6')  
        booking_label.place(x=23, y=195)

        # history
        self.history_btn = tk.Button(self, text="  History", bd=0,bg=self.master.bg_color1, fg="white", 
                                     font=("Poppins Semibold", 18))
        self.history_btn.place(x=0, y=246, width=226, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg=self.master.bg_color1)  
        history_label.place(x=26, y=257)

    def navigate_home(self):
        self.master.patient_home.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_home)
    
    def navigate_booking(self):
        self.master.patient_booking.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_booking)

    def get_user_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT Email, FirstName, LastName FROM User WHERE UserId = %s"
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.email, fname, lname = result
                    self.name = f'{fname} {lname}'
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
        self.background_photo = tk.PhotoImage(file='images/patient_main_background.png')  
        background_label = tk.Label(self, image=self.background_photo)  
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        # title
        self.title_label = tk.Label(self, text="Booking History", font=("Poppins", 32, "bold"), fg='black', bg='white')
        self.title_label.place(x=261, y=28)

        # name login
        self.name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg='white')
        self.name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        self.email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg='white')
        self.email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # filter dropdown
        def on_select(event):
            selected_option = combo.get()
            if selected_option == 'Date & Hour': selected_option = "CONCAT(AppointmentDate, ' ', STR_TO_DATE(bb.AppointmentHour, '%H:%i'))"
            elif selected_option == 'Name': selected_option = 'bb.DoctorName'
            elif selected_option == 'Branch Name': selected_option = 'br.BranchName'
            elif selected_option == 'Status': selected_option = 'bb.AppointmentStatus'            
            
            self.filter_field = selected_option  
            self.create_table()

        options = ["Date & Hour", "Name", "Branch Name", "Status"]
        combo = ttk.Combobox(self, values=options, font=("Poppins", 12), state='readonly')
        combo.set("Filter")
        combo.place(x=1214, y=112, width=135, height=42)
        combo.bind("<<ComboboxSelected>>", on_select)

        self.sort_img = tk.PhotoImage(file='images/sort_ascending.png')  
        sort_icon = tk.Label(self, image=self.sort_img, bg='white')
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
    
    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = f"""
                    SELECT  
                        bb.DoctorId,
                        DATE_FORMAT(bb.AppointmentDate, '%Y-%m-%d') AS AppointmentDate, 
                        DATE_FORMAT(bb.AppointmentHour, '%H:%i') AS AppointmentHour,
                        bb.DoctorName,
                        CASE u.Gender 
                            WHEN 0 THEN 'Male'
                            ELSE 'Female'
                        END AS Gender,
                        s.SpecialtyName, 
                        br.BranchName,
                        bb.AppointmentStatus, 
                        bb.CheckUpType, 
                        bb.ReasonOfVisit
                    FROM BranchBookings bb
                    JOIN `User` u ON bb.DoctorId = u.UserId
                    LEFT JOIN Doctor d ON bb.DoctorId = d.DoctorId
                    LEFT JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
                    LEFT JOIN ClinicBranch br ON d.BranchNo = br.BranchNo
                    WHERE bb.PatientId = %s
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

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Semibold", 14))
        style.configure("Treeview", rowheight=40, font=("Poppins", 12))

        table_frame = tk.Frame(self)
        table_frame.place(x=248, y=114, width=900, height=610)

        columns = ['Appointment Date','Appointment Hour','Doctor Name', 'Gender', 'Specialty',
                'Branch Name', 'Status', 'Check-Up Type', 'Reason of Visit']  
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=210, anchor=tk.CENTER)

        for i, row in enumerate(self.table_data):
            display_row = row[1:]
            tags = "odd_row" if i % 2 == 0 else "even_row"
            item_id = self.table.insert("", tk.END, values=display_row, tags=(tags,))
        
        self.table.tag_configure("odd_row", background="#f2f7fd", font=("Poppins", 12))
        self.table.tag_configure("even_row", background="white", font=("Poppins", 12))

        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.table.pack(fill=tk.BOTH, expand=True)
        # self.table.bind("<<TreeviewSelect>>", lambda event: self.update_medical_panel(event))