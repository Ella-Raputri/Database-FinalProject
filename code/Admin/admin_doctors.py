import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from connection import connect_to_db

class AdminDoctorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.user_id = None
        self.email = None
        self.name = None
        self.branch_no = None

        self.table_data = None
        self.specialty_data = None
    
    def set_user_id(self, user_id):
        self.user_id = user_id
        self.create_widgets()
    
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

                query2 = "SELECT BranchNo FROM Admin WHERE AdminId = %s"
                cursor.execute(query2, (self.user_id,))
                result2 = cursor.fetchone()

                if result2: 
                    self.branch_no = result2[0]
                else:
                    messagebox.showerror("Error", "Admin details not found.")
                    return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    
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

        self.get_user_info()

        # name login
        name_label = tk.Label(self, text=self.name, font=("Poppins", 16), fg=self.master.font_color3, bg=self.master.admin_bg)
        name_label.place(x=-10, y=9, relx=1.0, anchor='ne')

        # email login
        email_label = tk.Label(self, text=f"Email: {self.email}", font=("Poppins", 12), fg=self.master.font_color3, bg=self.master.admin_bg)
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

        splist = self.get_specialty_list()

        if len(splist) >= 4:
            for i in range(3):  
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  
        else:
            for i in range(len(splist)): 
                label = tk.Label(self.specialty_panel, text=f"• {splist[i][0]}", font=("Poppins", 12), bg="white", anchor="w")
                label.place(x=10, y=49 + i * 25)  

        
        spview_more_btn = tk.Button(self.specialty_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 12), bd=0, command=self.open_specialties)
        spview_more_btn.place(x=30, y=161, width=110, height=32)


        # schedule panel
        self.schedule_panel = tk.Frame(self, bg=self.master.disabled_color,bd=1,relief='groove')
        self.schedule_panel.place(x=1170, y=180 + 215 + 10, width=165, height=165)

        self.schedule_label = tk.Label(self.schedule_panel, text="Schedule", font=("Poppins Semibold", 16), 
                                fg=self.master.font_color2, bg=self.master.disabled_color)
        self.schedule_label.place(x=10, y=11)

        
        self.scview_more_btn = tk.Button(self.schedule_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11), command=self.open_schedule,bd=0)
        self.scview_more_btn.place(x=30, y=120, width=110, height=32)

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

    def get_specialty_list(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = "SELECT SpecialtyName FROM Specialty"
                cursor.execute(query1)
                result = cursor.fetchall()
                return result  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
        
    def get_table_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:  
                query1 = """
                    SELECT 
                        d.DoctorId,
                        s.SpecialtyName AS Specialty,
                        u.Email,
                        CONCAT(u.FirstName, ' ', u.LastName) AS Name,
                        CASE u.Gender 
                            WHEN 0 THEN 'Male'
                            ELSE 'Female'
                        END AS Gender,
                        u.PhoneNumber,
                        u.City,
                        u.AddressDetail AS Address,
                        COUNT(b.BookingId) AS TotalBookings,
                        SUM(
                            CASE 
                                WHEN MONTH(b.AppointmentDate) = MONTH(CURRENT_DATE) 
                                    AND YEAR(b.AppointmentDate) = YEAR(CURRENT_DATE)
                                THEN 1 
                                ELSE 0 
                            END
                        ) AS ThisMonthsBookings
                    FROM 
                        Doctor d
                    LEFT JOIN 
                        Specialty s ON d.SpecialtyID = s.SpecialtyID
                    LEFT JOIN 
                        `User` u ON d.DoctorId = u.UserId
                    LEFT JOIN 
                        Booking b ON d.DoctorId = b.DoctorId
                    WHERE d.BranchNo = %s
                    GROUP BY 
                        d.DoctorId, s.SpecialtyName, u.Email, u.FirstName, u.LastName,
                        u.Gender, u.PhoneNumber, u.City, u.AddressDetail
                    ORDER BY 
                        d.DoctorId;                
                """
                cursor.execute(query1, (self.branch_no,))
                result = cursor.fetchall()
                return result  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def create_table(self):
        data = self.get_table_data()
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Semibold", 14))
        style.configure("Treeview", rowheight=40, font=("Poppins", 12))

        table_frame = tk.Frame(self)
        table_frame.place(x=248, y=114, width=900, height=610)

        columns = ['DoctorId','Specialty','Email','Name','Gender','Phone Number',
                   'City','Address','Total Bookings',"This Month's Bookings"]  
        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor=tk.CENTER)

        for i, row in enumerate(data):
            tags = "odd_row" if i % 2 == 0 else "even_row"
            table.insert("", tk.END, values=row, tags=(tags,))
        
        table.tag_configure("odd_row", background="#f2f7fd", font=("Poppins", 12))
        table.tag_configure("even_row", background="white", font=("Poppins", 12))

        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=table.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        table.pack(fill=tk.BOTH, expand=True)
        table.bind("<<TreeviewSelect>>", lambda event: self.update_schedule_panel(table))

    def update_schedule_panel(self, table):
        selected_item = table.selection()
        if selected_item:
            item = table.item(selected_item[0])
            doctor_id = item['values'][0]
            schedule = self.get_doctor_schedule(doctor_id)

            for widget in self.schedule_panel.winfo_children():
                widget.destroy()  

            self.schedule_panel.config(bg='white')
            self.schedule_label = tk.Label(self.schedule_panel, text="Schedule", 
                                           font=("Poppins Semibold", 15), fg=self.master.font_color2, bg='white')
            self.schedule_label.place(x=6, y=11)

            if schedule:
                for i, entry in enumerate(schedule[:3]):  
                    label = tk.Label(self.schedule_panel, text=f"• {entry}", font=("Poppins", 11), bg="white", anchor="w")
                    label.place(x=6, y=49 + i * 25)
            else:
                label = tk.Label(self.schedule_panel, text="No schedule available", font=("Poppins", 11), bg="white", anchor="w")
                label.place(x=6, y=49)
            
            self.scview_more_btn = tk.Button(self.schedule_panel, text='View Details', bg=self.master.bg_color1,
                                     fg='white', font=('Poppins', 11), command=self.open_schedule,bd=0)
            self.scview_more_btn.place(x=30, y=125, width=110, height=26)

    def get_doctor_schedule(self, doctor_id):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        CONCAT(LEFT(DayOfWeek, 3), ': ', 
                        TIME_FORMAT(StartHour, '%H:%i'), '-', 
                        TIME_FORMAT(EndHour, '%H:%i')) AS Schedule
                    FROM DoctorSchedule
                    WHERE DoctorId = %s
                    ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
                """
                cursor.execute(query, (doctor_id,))
                result = cursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_specialty_data(self):
        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = """
                    SELECT 
                        SpecialtyId,
                        SpecialtyName, 
                        SpecialtyDescription
                    FROM Specialty
                """
                cursor.execute(query)
                result = cursor.fetchall()
                self.specialty_data = [(row[0], row[1], row[2]) for row in result]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.specialty_data = []
        finally:
            if conn:
                conn.close()

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
        self.get_specialty_data()

        for i, (id, name, desc) in enumerate(self.specialty_data):
            # row container
            row_frame = tk.Frame(content1, bg='white')
            row_frame.pack(fill='x', pady=(0, 10))

            # name label
            name_label = tk.Label(row_frame, text=name, font=("Poppins Medium", 16), 
                                fg=self.master.font_color2, bg='white', anchor="w")
            name_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

            # edit button
            edit_button = tk.Button(row_frame, image=self.edit_photo, 
                                    command=lambda id=id, child_window=child_window: self.edit_specialty(id,child_window))
            edit_button.grid(row=0, column=1, padx=(10, 5), sticky="e")

            # delete button            
            delete_button = tk.Button(row_frame, image=self.delete_photo, 
                                    command=lambda id=id, name=name, child_window=child_window: self.delete_specialty(id,name,child_window))
            delete_button.grid(row=0, column=2, padx=(5, 0), sticky="e")

            # desc label
            desc_label = tk.Label(row_frame, text=desc, font=("Poppins", 12), 
                                fg=self.master.font_color2, bg='white', 
                                wraplength=450, justify="left", anchor="w")
            desc_label.grid(row=1, column=0, columnspan=3, sticky="w")

        content1.update_idletasks()
        canvas1.config(scrollregion=canvas1.bbox("all"))
        canvas1.bind("<MouseWheel>", lambda event, canvas=canvas1: self.on_mouse_wheel(event, canvas))

        # add btn
        self.add_photo = tk.PhotoImage(file='images/add_icon.png')
        add_button = tk.Button(child_window, image=self.add_photo, 
                                command=self.add_specialty)
        add_button.place(x=475, y=100)

        # ok btn
        ok_button = tk.Button(child_window, text="OK", font=("Poppins Semibold", 18), bg=self.master.bg_color1, 
                                fg="white", command=child_window.destroy)
        ok_button.place(x=211, y=615, width=116, height=40)

        child_window.resizable(False, False)

    def add_specialty(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Specialty")
        add_window.geometry("500x400")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Specialty Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spname_entry = tk.Entry(add_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        spname_entry.pack(pady=5)

        tk.Label(add_window, text="Specialty Description:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spdesc_entry = tk.Text(add_window, font=("Poppins", 12), width=30, height=5, bd=2, relief="solid")
        spdesc_entry.pack(pady=5)

        def save_specialty():
            spname = spname_entry.get().strip()
            spdesc = spdesc_entry.get("1.0", tk.END).strip()

            if not spname or not spdesc:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT SpecialtyID FROM Specialty ORDER BY SpecialtyID DESC LIMIT 1")
                    last_sp_id = cursor.fetchone()

                    if last_sp_id:
                        last_id = last_sp_id[0]  
                        numeric_part = int(last_id[2:])  
                        new_numeric_part = numeric_part + 1
                    else:
                        new_numeric_part = 1
                    
                    new_sp_id = f"SP{str(new_numeric_part).zfill(7)}"

                    query = """
                        INSERT INTO Specialty (SpecialtyId, SpecialtyName, SpecialtyDescription)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (new_sp_id,spname, spdesc))
                    conn.commit()
                    messagebox.showinfo("Success", "New specialty added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add specialty: {e}")
            finally:
                if conn:
                    conn.close()
                add_window.destroy() 
                self.open_specialties()  

        save_button = tk.Button(add_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_specialty)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def edit_specialty(self, specialty_id, spwindow):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Specialty")
        edit_window.geometry("500x400")
        edit_window.configure(bg="white")

        try:
            conn = connect_to_db()
            with conn.cursor() as cursor:
                query = "SELECT SpecialtyName, SpecialtyDescription FROM Specialty WHERE SpecialtyID = %s"
                cursor.execute(query, (specialty_id,))
                specialty = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch specialty: {e}")
            return
        finally:
            if conn:
                conn.close()

        if not specialty:
            messagebox.showerror("Error", "Specialty not found!")
            return

        current_name, current_description = specialty

        tk.Label(edit_window, text="Specialty Name:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spname_entry = tk.Entry(edit_window, font=("Poppins", 12), width=30, bd=2, relief="solid")
        spname_entry.pack(pady=5)
        spname_entry.insert(0, current_name)  

        tk.Label(edit_window, text="Specialty Description:", font=("Poppins", 14), bg="white").pack(pady=(20, 5))
        spdesc_entry = tk.Text(edit_window, font=("Poppins", 12), width=30, height=5, bd=2, relief="solid")
        spdesc_entry.pack(pady=5)
        spdesc_entry.insert("1.0", current_description)  

        def save_changes():
            new_name = spname_entry.get().strip()
            new_description = spdesc_entry.get("1.0", tk.END).strip()

            if not new_name or not new_description:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = connect_to_db()
                with conn.cursor() as cursor:
                    query = """
                        UPDATE Specialty
                        SET SpecialtyName = %s, SpecialtyDescription = %s
                        WHERE SpecialtyID = %s
                    """
                    cursor.execute(query, (new_name, new_description, specialty_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Specialty updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update specialty: {e}")
            finally:
                if conn:
                    conn.close()
                    
                edit_window.destroy()
                spwindow.destroy()  # Ensure old child_window is properly closed
                self.open_specialties() 

        save_button = tk.Button(edit_window, text="Save", font=("Poppins", 14), bg=self.master.bg_color1, fg="white", command=save_changes)
        save_button.pack(pady=(20, 10), ipadx=10, ipady=2)

    def delete_specialty(self, specialty_id, specialty_name, spwindow):
        try:
            conn = connect_to_db()
            if not conn:
                messagebox.showerror("Error", "Database connection failed.")
                return

            with conn.cursor() as cursor:
                query = "SELECT COUNT(DoctorId) FROM Doctor WHERE SpecialtyId = %s"
                cursor.execute(query, (specialty_id,))
                amt = cursor.fetchone()[0]  

                if amt > 0:
                    messagebox.showerror(
                        "Error",
                        f"Cannot delete '{specialty_name}' because there are {amt} doctor(s) with this specialty."
                    )
                    return

                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete the specialty '{specialty_name}'?"
                )
                if confirm:
                    query = "DELETE FROM Specialty WHERE SpecialtyId = %s"
                    cursor.execute(query, (specialty_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Specialty '{specialty_name}' has been deleted.")
                    spwindow.destroy()
                    self.open_specialties()  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete specialty: {e}")
        finally:
            if conn:
                conn.close()


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

    
    