import tkinter as tk
from PIL import Image, ImageTk


class Booking:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white')
        self.frame.pack(fill='both', expand=True)

        # Filter frame for branch and specialty
        filter_frame = tk.Frame(self.frame, bg='white', bd=2)
        filter_frame.place(x=180, y=130, width=775, height=100)

        self.searchdoctor = tk.Label(self.frame, text='Search and Book Doctors', font=("Poppins Semibold", 25), bg='white')
        self.searchdoctor.place(x=400, y=50)

        # Branch selection
        self.branch_var = tk.StringVar()
        branch_options = ["All", "General Hospital", "Heart Institute", "Neurology Center", "Orthopedic Center",
                          "Skin Clinic"]
        self.branch_var.set("All")

        branch_label = tk.Label(filter_frame, text="Select Branch:", font=("Arial", 12), bg='white')
        branch_label.grid(row=0, column=0, padx=80, pady=5, sticky="w")
        self.branch_menu = tk.OptionMenu(filter_frame, self.branch_var, *branch_options)
        self.branch_menu.config(width=20, font=("Arial", 12))
        self.branch_menu.grid(row=1, column=0, padx=80, pady=5, sticky="w")

        # Specialty selection
        self.specialty_var = tk.StringVar()
        specialty_options = ["All", "Cardiology", "Dermatology", "Orthopedics", "Neurology", "General Practice",
                             "Pediatrics", "Psychiatry"]
        self.specialty_var.set("All")

        specialty_label = tk.Label(filter_frame, text="Select Specialty:", font=("Arial", 12), bg='white')
        specialty_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.specialty_menu = tk.OptionMenu(filter_frame, self.specialty_var, *specialty_options)
        self.specialty_menu.config(width=20, font=("Arial", 12))
        self.specialty_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Search button
        search_button = tk.Button(filter_frame, text="Search", bg='#69C6F7', command=self.filter_profiles)
        search_button.grid(row=1, column=2, padx=10, pady=5)

        # Canvas for displaying doctor profiles
        self.canvas = tk.Canvas(self.frame)
        self.canvas.place(x=180, y=250, width=800, height=450)


        # Scrollbar for canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=980, y=250, height=450)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scrollable frame for doctor profiles
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Example doctors for display (replace with real data later)
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

        self.filtered_doctors = self.doctors  # No filter initially

        self.create_doctor_profiles()

        # Ensure the scrollable area is properly sized
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_doctor_profiles(self):
        # Clear old profiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add new profiles
        row = 0
        for doctor in self.filtered_doctors:
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=2, relief="solid", width=1200, height=150)
            frame.grid(row=row, column=0, padx=20, pady=10, sticky="ew")

            # Profile picture placeholder
            try:
                profile_image = Image.open("images/Screenshot (16).png")
                profile_image = profile_image.resize((100, 100), Image.Resampling.LANCZOS)
                profile_pic = ImageTk.PhotoImage(profile_image)
                profile_label = tk.Label(frame, image=profile_pic, bg="white")
                profile_label.image = profile_pic
            except:
                profile_label = tk.Label(frame, text="No Image", bg="white", width=10, height=5)
            profile_label.grid(row=0, column=0, padx=10, pady=10)

            # Doctor information
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

            # Description box
            description_box = tk.Frame(frame, bg="lightgrey", bd=2, relief="groove", width=400, height=120)
            description_box.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
            description_label = tk.Label(description_box, text=doctor["description"], font=("Arial", 12),
                                         bg="lightgrey", wraplength=380)
            description_label.place(x=10, y=10)

            row += 1

    def filter_profiles(self):
        selected_branch = self.branch_var.get()
        selected_specialty = self.specialty_var.get()

        # Filter doctors
        self.filtered_doctors = [
            doctor for doctor in self.doctors
            if (selected_branch == "All" or doctor["branch"] == selected_branch) and
               (selected_specialty == "All" or doctor["specialty"] == selected_specialty)
        ]

        self.create_doctor_profiles()

