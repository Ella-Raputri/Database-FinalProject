import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PatientBooking():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1360x768")

        # Big picture goes first! It cover all place.
        self.bg_image = Image.open("images/booking dashboard.png")
        self.bg_image = self.bg_image.resize((1360, 768), Image.Resampling.LANCZOS)  # Resize picture to fit big cave
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Picture covers everything

        # Big button "Home" go here
        self.home_btn = tk.Label(self.root, text="Home", bd=0, bg='#69C6F7', fg="white", font=("Poppins Semibold", 18))
        self.home_btn.place(x=72, y=125)
        self.home_icon = tk.PhotoImage(file='images/home_icon.png')
        home_label = tk.Label(self.root, image=self.home_icon, bd=0, bg='#69C6F7')
        home_label.place(x=30, y=130)

        # Big button "Booking" go here
        self.booking_btn = tk.Label(self.root, text="Booking", bd=0, bg='#69C6F7', fg="white",
                                    font=("Poppins Semibold", 18))
        self.booking_btn.place(x=72, y=185)
        self.booking_icon = tk.PhotoImage(file='images/booking_icon.png')
        booking_label = tk.Label(self.root, image=self.booking_icon, bd=0, bg='#69C6F7')
        booking_label.place(x=30, y=190)

        # Create place to choose "Branch" and "Specialty" from list
        filter_frame = tk.Frame(self.root, bg='white', bd=2)
        filter_frame.place(x=385, y=130, width=1260, height=100)

        # Choose "Branch" go here
        self.branch_var = tk.StringVar()
        branch_options = ["All", "General Hospital", "Heart Institute", "Neurology Center", "Orthopedic Center",
                          "Skin Clinic"]
        self.branch_var.set("All")  # Default branch

        branch_label = tk.Label(filter_frame, text="Select Branch:", font=("Arial", 12), bg='white')
        branch_label.grid(row=0, column=0, padx=80, pady=5, sticky="w")  # Branch label
        self.branch_menu = tk.OptionMenu(filter_frame, self.branch_var, *branch_options)
        self.branch_menu.config(width=20, font=("Arial", 12))
        self.branch_menu.grid(row=1, column=0, padx=80, pady=5, sticky="w")  # Branch list

        # Choose "Specialty" go here
        self.specialty_var = tk.StringVar()
        specialty_options = ["All", "Cardiology", "Dermatology", "Orthopedics", "Neurology", "General Practice",
                             "Pediatrics", "Psychiatry"]
        self.specialty_var.set("All")  # Default specialty

        specialty_label = tk.Label(filter_frame, text="Select Specialty:", font=("Arial", 12), bg='white')
        specialty_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # Specialty label
        self.specialty_menu = tk.OptionMenu(filter_frame, self.specialty_var, *specialty_options)
        self.specialty_menu.config(width=20, font=("Arial", 12))
        self.specialty_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")  # Specialty list

        # Search for doctor! Big button with picture
        search_image = Image.open("images/search.png")  # Big search picture
        search_image = search_image.resize((80, 40), Image.Resampling.LANCZOS)  # Resize image small
        search_photo = ImageTk.PhotoImage(search_image)

        # Button to search for doctor
        search_button = tk.Button(filter_frame, image=search_photo, bg='white', command=self.filter_profiles)
        search_button.image = search_photo  # Keep search image
        search_button.grid(row=1, column=2, padx=80, pady=5)  # Search button

        # Big scroll area to see doctor profiles
        self.canvas = tk.Canvas(self.root)
        self.canvas.place(x=400, y=250, width=800, height=400)

        # Scroll to move up and down
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=1200, y=250, height=400)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create place to hold doctor profiles
        self.scrollable_frame = tk.Frame(self.canvas)

        # Attach frame to canvas so it moves
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Make list of doctors (for testing)
        self.doctors = [
            {"name": "Doctor 1", "specialty": "Cardiology", "branch": "Heart Institute",
             "description": "Cardiologist with 10 years of practice."},
            {"name": "Doctor 2", "specialty": "Dermatology", "branch": "Skin Clinic",
             "description": "Treats skin issues like acne and eczema."},
            {"name": "Doctor 3", "specialty": "Neurology", "branch": "Neurology Center",
             "description": "Expert in brain and spine health."},
            {"name": "Doctor 4", "specialty": "Orthopedics", "branch": "Orthopedic Center",
             "description": "Fix bones and joints!"}
        ]

        self.filtered_doctors = self.doctors  # No filter at first

        # Make profiles visible
        self.create_doctor_profiles()

        # Make sure scroll region is right size
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.root.mainloop()

    def create_doctor_profiles(self):
        # Remove old profiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Put new profiles in grid
        row = 0
        for doctor in self.filtered_doctors:
            # Make frame for each doctor profile
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=2, relief="solid", width=1200, height=150)
            frame.grid(row=row, column=0, padx=20, pady=10, sticky="ew")

            # Profile picture (or no picture if none)
            try:
                profile_image = Image.open('images/Screenshot (16).png')  # Use image if can
                profile_image = profile_image.resize((100, 100), Image.Resampling.LANCZOS)
                profile_pic = ImageTk.PhotoImage(profile_image)
                profile_label = tk.Label(frame, image=profile_pic, bg="white")
                profile_label.image = profile_pic  # Keep the picture
            except:
                profile_label = tk.Label(frame, text="No Image", bg="white", width=10, height=5)
            profile_label.grid(row=0, column=0, padx=10, pady=10)

            # Write name, specialty, and branch here
            basic_info_frame = tk.Frame(frame, bg="white")
            basic_info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            name_label = tk.Label(basic_info_frame, text=doctor["name"], font=("Arial", 16, "bold"), bg="white")
            name_label.grid(row=0, column=0, sticky="w")

            specialty_label = tk.Label(basic_info_frame, text=f"Specialty: {doctor['specialty']}", font=("Arial", 12),
                                       bg="white")
            specialty_label.grid(row=1, column=0, sticky="w")

            branch_label = tk.Label(basic_info_frame, text=f"Branch: {doctor['branch']}", font=("Arial", 12),
                                    bg="white")
            branch_label.grid(row=2, column=0, sticky="w")

            # Book appointment button with image
            book_image = Image.open("images/book.png")  # Big book button
            book_image = book_image.resize((100, 40), Image.Resampling.LANCZOS)  # Resize image small
            book_photo = ImageTk.PhotoImage(book_image)

            # Book button to click
            book_button = tk.Button(frame, image=book_photo, bg="white",
                                    command=lambda d=doctor: self.book_appointment(d))
            book_button.image = book_photo  # Keep book image
            book_button.grid(row=1, column=0, padx=10, pady=10)

            # Description of doctor
            description_box = tk.Frame(frame, bg="lightgrey", bd=2, relief="groove", width=400, height=120)
            description_box.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

            description_label = tk.Label(description_box, text=doctor["description"], font=("Arial", 12),
                                         bg="lightgrey", wraplength=380)
            description_label.place(x=10, y=10)

            row += 1

    def filter_profiles(self):
        selected_branch = self.branch_var.get()
        selected_specialty = self.specialty_var.get()

        # Filter doctors by branch and specialty
        self.filtered_doctors = [
            doctor for doctor in self.doctors
            if (selected_branch == "All" or doctor["branch"] == selected_branch) and
               (selected_specialty == "All" or doctor["specialty"] == selected_specialty)
        ]

        # Show only filtered doctors
        self.create_doctor_profiles()

    def book_appointment(self, doctor):
        """ Make appointment with doctor! """
        print(f"Booking appointment with {doctor['name']} ({doctor['specialty']})")


PatientBooking()
