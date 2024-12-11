import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os, shutil
from connection import connect_to_db
import re

class DoctorProfile(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None

        self.fname = None
        self.lname = None
        self.gender = None
        self.phone = None
        self.city = None
        self.address = None

        self.sp_id = None
        self.sp_name = None
        self.description = None

        self.default_pic = ImageTk.PhotoImage(Image.open("images/default_profile.png").resize((135, 135)))  
        self.profile_pic = self.default_pic
        self.propic_path = None

        self.editing_inputs = False
        self.edit_photo = tk.PhotoImage(file='images/edit_icon2.png')

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
        self.history_btn = tk.Button(self, text="History", bd=0,bg='#64C1F6', fg="white", 
                                    font=("Poppins Semibold", 18),
                                    command=self.navigate_history)
        self.history_btn.place(x=0, y=186,  width=213, height=52)
        self.history_icon = tk.PhotoImage(file='images/history_icon.png')  
        history_label = tk.Label(self, image=self.history_icon, bd=0, bg='#64C1F6')  
        history_label.place(x=23, y=198)

        # profile
        self.profile_btn = tk.Button(self, text="Profile", bd=0,bg=self.master.bg_color1, fg="white", 
                                     font=("Poppins Semibold", 18))
        self.profile_btn.place(x=0, y=246, width=213, height=52)
        self.profile_icon = tk.PhotoImage(file='images/doctor_icon.png')  
        profile_label = tk.Label(self, image=self.profile_icon, bd=0, bg=self.master.bg_color1)  
        profile_label.place(x=23, y=257)

    def navigate_home(self):
        self.master.doctor_dashboard.set_user_id(self.user_id)
        self.master.show_frame(self.master.doctor_dashboard)
    
    def navigate_history(self):
        self.master.doctor_history.set_user_id(self.user_id)
        self.master.show_frame(self.master.doctor_history)

    def get_user_info(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """SELECT Email, FirstName, LastName, Gender, PhoneNumber, City, AddressDetail
                FROM User WHERE UserId = %s"""
                cursor.execute(query1, (self.user_id,))
                result = cursor.fetchone()
                
                if result:  
                    self.email, self.fname, self.lname, self.gender, self.phone, self.city, self.address= result
                else:
                    messagebox.showerror("Error", "Invalid user.")
                    return
                
                query2 = """SELECT
                        d.ProfilePicture, d.Description, d.SpecialtyId, s.SpecialtyName
                    FROM Doctor d JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
                    WHERE d.DoctorId = %s;"""
                cursor.execute(query2, (self.user_id,))
                result2 = cursor.fetchone()
                if result2:  
                    self.propic_path, self.description, self.sp_id, self.sp_name = result2

                    if(self.propic_path == None): 
                        self.profile_pic = self.default_pic
                    else: 
                        self.profile_pic = ImageTk.PhotoImage(Image.open(self.propic_path).resize((135, 135)))
                else:
                    messagebox.showerror("Error", "Invalid doctor.")
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
        title_label = tk.Label(self, text=f"Profile", font=("Poppins", 36, "bold"), fg='black', bg=self.master.doctor_bg)
        title_label.place(x=290, y=28)

        # name login
        self.name_label = tk.Label(self, text=f'{self.fname} {self.lname}', font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.doctor_bg)
        self.name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.doctor_bg)
        email_label.place(x=-10, y=39, relx=1.0, anchor='ne')

        # profile pic
        self.profile_pic_label = tk.Label(self, image=self.profile_pic, bg=self.master.doctor_bg)
        self.profile_pic_label.image = self.profile_pic
        self.profile_pic_label.place(x=300, y=133)

        change_pic_btn = tk.Button(self, text="Change Picture", bg=self.master.bg_color1, fg="white", font=("Poppins", 14),
                           command=self.change_picture)
        change_pic_btn.place(x=468, y=147, width=192, height=42)

        delete_pic_btn = tk.Button(self, text="Delete Picture", bg="white", font=("Poppins", 14),
                                fg=self.master.bg_color1, command=self.delete_picture)
        delete_pic_btn.place(x=468, y=217, width=192, height=42)

        self.create_specialty_desc_panel()
        self.create_input()
        self.schedule = self.get_doctor_schedule()

        edit_schedule_btn = tk.Button(self, text="Edit Schedule", bg=self.master.bg_color1, fg="white", font=("Poppins", 14),
                           command=self.open_schedule)
        edit_schedule_btn.place(x=298, y=688, width=200, height=47)

        self.edit_inputs_btn = tk.Button(self, text="Edit Basic Info", bd=0, bg=self.master.doctor_bg, fg='#298FFF', 
                                  font=("Poppins", 12), command=self.enable_editing)
        self.edit_inputs_btn.place(x=1157, y=110)
        edit_inputs_label = tk.Label(self, image=self.edit_photo, bd=0, bg=self.master.doctor_bg)  
        edit_inputs_label.place(x=1280, y=119)

        self.ok_btn = tk.Button(self, text="OK", bg=self.master.bg_color1, fg="white", font=("Poppins", 14),
                           state=tk.DISABLED, command=self.save_info)
        self.ok_btn.place(x=1186, y=688, width=116, height=47)
    
    def get_doctor_schedule(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        CONCAT(DayOfWeek, ': ', 
                        TIME_FORMAT(StartHour, '%H:%i'), '-', 
                        TIME_FORMAT(EndHour, '%H:%i')) AS Schedule,
                        ScheduleId
                    FROM DoctorSchedule
                    WHERE DoctorId = %s
                    ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                    StartHour, EndHour;
                """
                cursor.execute(query, (self.user_id,))
                result = cursor.fetchall()
                return [(row[0], row[1]) for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def open_schedule(self):
        child_window = tk.Toplevel(self)
        child_window.configure(bg="white")
        child_window.title("Schedule")
        child_window.geometry("533x676")  

        # schedule label
        sctitle_label = tk.Label(child_window, text=f"Dr.{self.fname} Schedule",
                                 font=("Poppins Semibold", 24), 
                                 fg='black', bg='white',wraplength=500)
        sctitle_label.place(x=30, y=18)

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

        for i, entry in enumerate(self.schedule):
            schedule_text, schedule_id = entry
            day_full, time_range = schedule_text.split(": ", 1)

            # row container 
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=day_full, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                   command=lambda schedule_id=schedule_id, child_window=child_window: self.edit_schedule(schedule_id, child_window))
            edit_button.grid(row=0, column=1, padx=(0, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda schedule_id=schedule_id, child_window=child_window: self.delete_schedule(schedule_id, child_window))
            delete_button.grid(row=0, column=2, padx=(0, 5), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text=time_range,
                                font=("Poppins", 12), fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w",padx=(5, 10), pady=(0, 10))
    

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=self.add_schedule)
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=206, y=615, width=116, height=40)

        child_window.resizable(False, False)
    
    def is_valid_time(self, time_str):
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False  

            hour, minute = map(int, parts)  
            return 0 <= hour < 24 and 0 <= minute < 60  
        except (ValueError, TypeError):
            return False 

    def add_schedule(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Schedule")
        add_window.geometry("500x400")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Day of the Week:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        day_entry = ttk.Combobox(add_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                font=("Poppins", 12), state="readonly", width=28)
        day_entry.pack(pady=5)

        tk.Label(add_window, text="Start Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        start_time_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        start_time_entry.pack(pady=5)

        tk.Label(add_window, text="End Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        end_time_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        end_time_entry.pack(pady=5)

        def save_schedule():
            day = day_entry.get().strip()
            start_time = start_time_entry.get().strip()
            end_time = end_time_entry.get().strip()

            if not day or not start_time or not end_time:
                messagebox.showerror("Error", "All fields are required!")
                add_window.destroy()
                return
            if not self.is_valid_time(start_time) or not self.is_valid_time(end_time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM format.")
                add_window.destroy()
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ScheduleId FROM DoctorSchedule ORDER BY ScheduleId DESC LIMIT 1")
                    last_id = cursor.fetchone()

                    if last_id:
                        last = last_id[0]  
                        numeric_part = int(last[3:])  
                        new_numeric_part = numeric_part + 1
                    else:
                        new_numeric_part = 1
                    
                    new_id = f"SCH{str(new_numeric_part).zfill(7)}"

                    query = """
                        INSERT INTO DoctorSchedule (ScheduleId, DoctorId, DayOfWeek, StartHour, EndHour)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (new_id,self.user_id, day, start_time, end_time))
                    conn.commit()
                    messagebox.showinfo("Success", "New schedule added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add schedule: {e}")
            finally:
                if conn:
                    conn.close()
                add_window.destroy()
                self.schedule = self.get_doctor_schedule()
                self.open_schedule()  

        save_button = tk.Button(add_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_schedule)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def edit_schedule(self, schedule_id, schedule_window):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Schedule")
        edit_window.geometry("500x400")
        edit_window.configure(bg="white")

        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT DayOfWeek, TIME_FORMAT(StartHour, '%H:%i'), TIME_FORMAT(EndHour, '%H:%i')
                    FROM DoctorSchedule
                    WHERE ScheduleId = %s
                """
                cursor.execute(query, (schedule_id,))
                schedule = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch schedule: {e}")
            return
        finally:
            if conn:
                conn.close()

        if not schedule:
            messagebox.showerror("Error", "Schedule not found!")
            return

        current_day, current_start, current_end = schedule

        tk.Label(edit_window, text="Day of the Week:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        day_entry = ttk.Combobox(edit_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                font=("Poppins", 12), state="readonly", width=28)
        day_entry.pack(pady=5)
        day_entry.set(current_day)

        tk.Label(edit_window, text="Start Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        start_time_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        start_time_entry.pack(pady=5)
        start_time_entry.insert(0, current_start)

        tk.Label(edit_window, text="End Time (HH:MM):", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        end_time_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        end_time_entry.pack(pady=5)
        end_time_entry.insert(0, current_end)

        def save_changes():
            new_day = day_entry.get().strip()
            new_start_time = start_time_entry.get().strip()
            new_end_time = end_time_entry.get().strip()

            if not new_day or not new_start_time or not new_end_time:
                messagebox.showerror("Error", "All fields are required!")
                edit_window.destroy()
                return
            if not self.is_valid_time(new_start_time) or not self.is_valid_time(new_end_time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM format.")
                edit_window.destroy()
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    query = """
                        UPDATE DoctorSchedule
                        SET DayOfWeek = %s, StartHour = %s, EndHour = %s
                        WHERE ScheduleId = %s
                    """
                    cursor.execute(query, (new_day, new_start_time, new_end_time, schedule_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update schedule: {e}")
            finally:
                if conn:
                    conn.close()
                    
                edit_window.destroy()
                schedule_window.destroy()  
                self.schedule = self.get_doctor_schedule()
                self.open_schedule()  

        save_button = tk.Button(edit_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_changes)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def delete_schedule(self, schedule_id, schedule_window):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this schedule?"
                )
                if confirm:
                    query = "DELETE FROM DoctorSchedule WHERE ScheduleId = %s"
                    cursor.execute(query, (schedule_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule deleted successfully!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting: {e}")
        finally:
            if conn:
                conn.close()
            schedule_window.destroy()  
            self.schedule = self.get_doctor_schedule()
            self.open_schedule() 

    def create_input(self):
        fname_label = tk.Label(self, text="First Name", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        fname_label.place(x=719, y=149)
        self.fname_entry = tk.Entry(self, font=("Poppins", 14), width=22, bd=1, relief="solid")
        self.fname_entry.place(x=719, y=189)
        self.fname_entry.insert(0, self.fname)
        self.fname_entry.config(state=tk.DISABLED)

        lname_label = tk.Label(self, text="Last Name", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        lname_label.place(x=1016, y=149)
        self.lname_entry = tk.Entry(self, font=("Poppins", 14), width=23, bd=1, relief="solid")
        self.lname_entry.place(x=1016, y=189)
        self.lname_entry.insert(0, self.lname)
        self.lname_entry.config(state=tk.DISABLED)

        phone_label = tk.Label(self, text="Phone Number", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        phone_label.place(x=719, y=270)
        self.phone_entry = tk.Entry(self, font=("Poppins", 14), width=30, bd=1, relief="solid")
        self.phone_entry.place(x=719, y=309)
        self.phone_entry.insert(0, self.phone)
        self.phone_entry.config(state=tk.DISABLED)

        gender_label = tk.Label(self, text="Gender", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        gender_label.place(x=1100, y=270)
        style = ttk.Style()
        style.configure("Custom.TCombobox", font=("Poppins", 14))
        self.gender_combobox = ttk.Combobox(self, font=('Poppins', 14), width=15, 
                                            state="readonly", style="Custom.TCombobox")
        self.gender_combobox['values'] = ("Male", "Female")
        self.gender_combobox.place(x=1100, y=310)
        self.gender_combobox.config(state=tk.DISABLED)
        if self.gender == 0:
            self.gender_combobox.set("Male")
        else: 
            self.gender_combobox.set("Female")

        city_label = tk.Label(self, text="City", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        city_label.place(x=719, y=407)
        self.city_entry = tk.Entry(self, font=("Poppins", 14), width=49, bd=1, relief="solid")
        self.city_entry.place(x=719, y=449)
        self.city_entry.insert(0, self.city)
        self.city_entry.config(state=tk.DISABLED)

        address_label = tk.Label(self, text="Address Details", font=("Poppins Semibold", 18), 
                                fg=self.master.font_color1, bg=self.master.doctor_bg)
        address_label.place(x=719, y=546)
        self.address_entry = tk.Entry(self, font=("Poppins", 14), width=49, bd=1, relief="solid")
        self.address_entry.place(x=719, y=586)
        self.address_entry.insert(0, self.address)
        self.address_entry.config(state=tk.DISABLED)
    
    def enable_editing(self):
        self.fname_entry.config(state=tk.NORMAL)
        self.lname_entry.config(state=tk.NORMAL)
        self.phone_entry.config(state=tk.NORMAL)
        self.gender_combobox.config(state="readonly")
        self.city_entry.config(state=tk.NORMAL)
        self.address_entry.config(state=tk.NORMAL)
        self.ok_btn.config(state=tk.NORMAL)
        self.edit_inputs_btn.config(state=tk.DISABLED)

    def save_info(self):
        self.fname = self.fname_entry.get().strip()
        self.lname = self.lname_entry.get().strip()
        self.phone = self.phone_entry.get().strip()
        updated_gender_val = self.gender_combobox.get().strip()
        self.gender = 0 if updated_gender_val == "Male" else 1

        self.city = self.city_entry.get().strip()
        self.address = self.address_entry.get().strip()

        if not self.fname or not self.lname or not self.phone or not self.city \
            or not self.address or self.gender is None:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not re.match(r'^\d+$', self.phone):
            messagebox.showerror("Error", "Invalid phone number format!")
            return
        
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Update User table
            query1 = """
                UPDATE User
                SET FirstName = %s, LastName = %s, Gender = %s, PhoneNumber = %s, City = %s, AddressDetail = %s
                WHERE UserId = %s
            """
            cursor.execute(query1, (self.fname, self.lname, self.gender, self.phone, self.city, 
                                    self.address, self.user_id))
            conn.commit()
            messagebox.showinfo("Success", "Info updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update doctor: {e}")
        finally:
            if conn:
                conn.close()
        
        self.fname_entry.config(state=tk.DISABLED)
        self.lname_entry.config(state=tk.DISABLED)
        self.phone_entry.config(state=tk.DISABLED)
        self.gender_combobox.config(state=tk.DISABLED)
        self.city_entry.config(state=tk.DISABLED)
        self.address_entry.config(state=tk.DISABLED)
        self.ok_btn.config(state=tk.DISABLED)

        self.name_label.config(text=f'{self.fname} {self.lname}')
        
        self.edit_inputs_btn.config(state=tk.NORMAL)

    def load_specialties(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT CONCAT(SpecialtyId, ': ', SpecialtyName) FROM Specialty"
                cursor.execute(query1)
                result = cursor.fetchall()
                return [item[0] for item in result] 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def edit_specialty(self):
        specialties = self.load_specialties()
        if not specialties:
            messagebox.showerror("Error", "No specialties found.")
            return

        specialty_window = tk.Toplevel(self)
        specialty_window.title("Choose Specialty")
        specialty_window.geometry("300x200")
        specialty_window.configure(bg="white")

        specialty_label = tk.Label(specialty_window, text="Select Specialty", font=("Poppins", 14),bg='white')
        specialty_label.pack(pady=10)
        specialty_combobox = ttk.Combobox(specialty_window, values=specialties, font=("Poppins", 12), state="readonly")
        specialty_combobox.pack(pady=10)

        def on_ok_button_click():
            selected_specialty = specialty_combobox.get()
            if selected_specialty:
                try:
                    conn = connect_to_db()
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "UPDATE Doctor SET SpecialtyId = %s WHERE DoctorId = %s",
                            (selected_specialty.split(':')[0], self.user_id),
                        )
                        conn.commit()
                except Exception as e:
                    print(f"Database error: {e}")
                finally:
                    conn.close()
                    self.dr_specialty_label.config(text=selected_specialty)
                    specialty_window.destroy()  
            else:
                messagebox.showerror("Error", "Please select a specialty.")

        ok_button = tk.Button(specialty_window, text="OK", font=("Poppins", 12), command=on_ok_button_click, bg=self.master.bg_color1)
        ok_button.pack(pady=20, padx=20)

    def open_edit_description_window(self):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Description")
        edit_window.geometry("400x300")
        edit_window.configure(bg='white')

        frame = tk.Frame(edit_window)
        frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        text_widget = tk.Text(frame, font=("Poppins", 12), fg=self.master.font_color2, bg='white', wrap='word', bd=1, relief="solid")
        text_widget.insert(tk.END, self.description)
        text_widget.place(x=20, y=20, width=360, height=180)  

        def save_description_and_close():
            new_description = text_widget.get("1.0", tk.END).strip()
            if new_description != self.description:
                self.description = new_description
                try:
                    conn = connect_to_db()
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "UPDATE Doctor SET Description = %s WHERE DoctorId = %s",
                            (new_description, self.user_id),
                        )
                        conn.commit()
                except Exception as e:
                    print(f"Database error: {e}")
                finally:
                    conn.close()
                    edit_window.destroy()
                    self.create_scrollable_description(self.description)

        save_button = tk.Button(edit_window, text="Save", bg=self.master.bg_color1, fg="white", font=("Poppins", 14), command=save_description_and_close)
        save_button.place(x=150, y=220, width=100, height=40)
        edit_window.update_idletasks()

    def create_specialty_desc_panel(self):
        # specialty panel
        self.specialty_panel = tk.Frame(self, bg='white',bd=1,relief='groove')
        self.specialty_panel.place(x=298, y=315, width=383, height=105)

        specialty_label = tk.Label(self.specialty_panel, text="Specialty", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color1, bg='white')
        specialty_label.place(x=10, y=11)
        self.dr_specialty_label = tk.Label(self.specialty_panel, text=f'{self.sp_id}: {self.sp_name}', font=("Poppins", 12), 
                                fg=self.master.font_color2, bg='white')
        self.dr_specialty_label.place(x=10, y=46)

        edit_sp_btn = tk.Button(self.specialty_panel, image=self.edit_photo, bg='white',relief='flat',command=self.edit_specialty)
        edit_sp_btn.place(x=348, y=13)

        # description panel
        self.desc_panel = tk.Frame(self, bg='white',bd=1,relief='groove')
        self.desc_panel.place(x=298, y=454, width=383, height=183)

        desc_label = tk.Label(self.desc_panel, text="Description", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color1, bg='white')
        desc_label.place(x=10, y=11)
        self.create_scrollable_description(self.description)

        edit_desc_btn = tk.Button(self.desc_panel, image=self.edit_photo, bg='white', relief='flat',command=self.open_edit_description_window)
        edit_desc_btn.place(x=348, y=13)
    
    def create_scrollable_description(self, text):
        frame = tk.Frame(self.desc_panel, bg='white', highlightthickness=0)
        frame.place(x=10, y=46, width=370, height=120)

        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        content_frame = tk.Frame(canvas, bg='white', highlightthickness=0)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        desc_label = tk.Label(content_frame, text=text, font=("Poppins", 12),
                              fg=self.master.font_color2, bg='white', wraplength=350, justify="left")
        desc_label.pack(fill='x', pady=5)
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        canvas.bind("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas))

    def change_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            save_dir = "profile_pictures/doctors"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            file_name = os.path.basename(file_path)
            save_path = os.path.join(save_dir, file_name)
            shutil.copy(file_path, save_path)
            self.propic_path = save_path  

            img = Image.open(save_path)
            img = img.resize((135, 135), Image.Resampling.LANCZOS)  
            self.profile_pic = ImageTk.PhotoImage(img)
            self.profile_pic_label.config(image=self.profile_pic)
            self.profile_pic_label.image = self.profile_pic
            self.update_pic_database(self.propic_path)

    def delete_picture(self):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to reset this photo to default?"
        )
        if confirm:
            if self.propic_path and os.path.exists(self.propic_path):
                os.remove(self.propic_path)
                self.propic_path = None

            self.profile_pic_label.config(image=self.default_pic)
            self.profile_pic_label.image = self.default_pic
            self.profile_pic = self.default_pic
            self.update_pic_database(None)

    def update_pic_database(self, file_path):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                if file_path:
                    cursor.execute(
                        "UPDATE Doctor SET ProfilePicture = %s WHERE DoctorId = %s",
                        (file_path, self.user_id),
                    )
                else:
                    cursor.execute(
                        "UPDATE Doctor SET ProfilePicture = NULL WHERE DoctorId = %s",
                        (self.user_id,),
                    )

            conn.commit()
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def on_mouse_wheel(self, event, canvas):
        if event.delta > 0:  
            canvas.yview_scroll(-1, "units")
        else:  
            canvas.yview_scroll(1, "units")
