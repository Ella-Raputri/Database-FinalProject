import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from connection import connect_to_db
import os, shutil,re

class PatientBooking(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None

        self.branch_options = []
        self.specialty_options = []

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
    def create_navbar(self):      
        # home
        self.home_btn = tk.Button(self, text="Home", bd=0, bg='#69C6F7', fg="white", 
                                  font=("Poppins Semibold", 18),
                                    command=self.navigate_home)
        self.home_btn.place(x=0, y=119, width=226, height=52)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')  
        home_label = tk.Label(self, image=self.home_icon, bd=0, bg='#69C6F7')  
        home_label.place(x=27, y=130)

        # booking
        self.booking_btn = tk.Button(self, text="    Booking", bd=0,bg=self.master.bg_color1, fg="white", 
                                    font=("Poppins Semibold", 18))
        self.booking_btn.place(x=0, y=186,  width=226, height=52)
        self.booking_icon = tk.PhotoImage(file='images/pat_booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg=self.master.bg_color1)  
        booking_label.place(x=23, y=195)

        # history
        self.history_btn = tk.Button(self, text="  History", bd=0,bg='#5FBBF5', fg="white", 
                                     font=("Poppins Semibold", 18),
                                     command=self.navigate_history)
        self.history_btn.place(x=0, y=246, width=226, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg='#5FBBF5')  
        history_label.place(x=26, y=257)

    def navigate_history(self):
        self.master.patient_history.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_history)
    
    def navigate_home(self):
        self.master.patient_home.set_user_id(self.user_id)
        self.master.show_frame(self.master.patient_home)

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

    def populate_branch(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT BranchNo, BranchName FROM ClinicBranch"
                cursor.execute(query1)
                result = cursor.fetchall()
                self.branch_options = [row[1] for row in result] 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def populate_specialty(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT SpecialtyId, SpecialtyName FROM Specialty"
                cursor.execute(query1)
                result = cursor.fetchall()
                self.specialty_options = [row[1] for row in result] 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print("Error", f"An error occurred: {e}")
            return []
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
        self.title_label = tk.Label(self, text="Search and Book Doctor", font=("Poppins", 32, "bold"), fg='black', bg='white')
        self.title_label.place(x=500, y=28)

        # name login
        self.name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg='white')
        self.name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        self.email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg='white')
        self.email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # Branch selection
        self.populate_branch()
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 16))
        self.branch_combobox = ttk.Combobox(self, font=('Poppins', 16), width=23, state="readonly", style="Custom.TCombobox")
        self.branch_combobox['values'] = self.branch_options
        self.branch_combobox.set('All')
        self.branch_combobox.place(x=339, y=172)

        branch_label = tk.Label(self, text="Select Branch:", font=("Poppins", 18), bg='white')
        branch_label.place(x=339, y=122)

        # Specialty selection
        self.populate_specialty()
        self.sp_combobox = ttk.Combobox(self, font=('Poppins', 16), width=30, state="readonly", style="Custom.TCombobox")
        self.sp_combobox['values'] = self.specialty_options
        self.sp_combobox.set('All')
        self.sp_combobox.place(x=678, y=172)
        specialty_label = tk.Label(self, text="Select Branch:", font=("Poppins", 18), bg='white')
        specialty_label.place(x=678, y=122)

        # Search button
        search_button = tk.Button(self, text="Search",fg='white',bg=self.master.bg_color1,font=("Poppins", 18), 
                                  command=self.filter_profiles)
        search_button.place(x=1109, y=170, width=126, height=46)

        self.create_canvas_booking()
    
    def create_canvas_booking(self):
        frame1 = tk.Frame(self, bd=0, highlightthickness=1, highlightbackground=self.master.font_color2)
        frame1.place(x=306, y=240)

        canvas1 = tk.Canvas(frame1, width=960, height=470, bg='white',bd=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview, bg='white')
        canvas1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)

        content1 = tk.Frame(canvas1, bg='white',bd=0, highlightthickness=0)
        canvas1.create_window((0, 0), window=content1, anchor="nw")

        for i in range(0, 20):           
            label = tk.Label(content1, text=f'test {i}', justify='left',
                            font=("Poppins", 14), wraplength=310, fg=self.master.font_color2, bg='white')
            label.pack(fill='x', pady=(0, 10))

            separator = tk.Frame(content1, height=1, bg=self.master.separator_color)
            separator.pack(fill='x', pady=(0, 10))

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))
    
    def filter_profiles(self):
        print('clicked')
        # selected_branch = self.branch_var.get()
        # selected_specialty = self.specialty_var.get()

        # # Filter doctors
        # self.filtered_doctors = [
        #     doctor for doctor in self.doctors
        #     if (selected_branch == "All" or doctor["branch"] == selected_branch) and
        #        (selected_specialty == "All" or doctor["specialty"] == selected_specialty)
        # ]

        # self.create_doctor_profiles()

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  
            canvas.yview_scroll(-1, "units")
        else:  
            canvas.yview_scroll(1, "units")
