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
        self.booking_btn.place(x=0, y=186,  width=213, height=52)
        self.booking_icon = tk.PhotoImage(file='images/pat_booking_icon.png')  
        booking_label = tk.Label(self, image=self.booking_icon, bd=0, bg='#64C1F6')  
        booking_label.place(x=23, y=195)

        # history
        self.history_btn = tk.Button(self, text="  History", bd=0,bg=self.master.bg_color1, fg="white", 
                                     font=("Poppins Semibold", 18))
        self.history_btn.place(x=0, y=246, width=213, height=52)
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