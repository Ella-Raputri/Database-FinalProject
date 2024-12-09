import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io

class PatientHome():
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Patient Dashboard")
        self.root.geometry("1360x768")
        self.root.configure(bg='white')

        # Create left sidebar
        self.sidebar = tk.Frame(self.root, bg='#69C6F7', width=250, height=768)
        self.sidebar.place(x=0, y=0)

        # Home Button
        self.home_btn = tk.Label(self.root, text="🏠 Home", bd=0, bg='#69C6F7', fg="white", 
                                font=("Arial", 18, "bold"))
        self.home_btn.place(x=30, y=125)

        # Booking Button
        self.booking_btn = tk.Label(self.root, text="📅 Booking", bd=0, bg='#69C6F7', fg="white",
                                    font=("Arial", 18, "bold"))
        self.booking_btn.place(x=30, y=185)

        # Welcome message for patient
        self.patient_name = tk.Label(text='Welcome, Patient', font=('Arial', 25, "bold"), bg='white')
        self.patient_name.place(x=280, y=40)

        # Create a default profile picture (grey circle)
        self.create_default_profile()
        self.profile_label = tk.Label(self.root, image=self.profile_pic, bg='white')
        self.profile_label.place(x=280, y=110)

        # Change Profile Button
        self.change_profile_button = tk.Button(self.root, text="Change Profile Picture",
                                             font=("Arial", 12), command=lambda: self.change_profile_pic(None))
        self.change_profile_button.place(x=470, y=120)

        # Remove Profile Button
        self.remove_button = tk.Button(self.root, text="Remove Picture",
                                     font=("Arial", 12), command=lambda: self.remove_profile_pic(None))
        self.remove_button.place(x=470, y=170)

        # Display appointment information
        self.appointment = tk.Label(self.root, text='Appointment Time', 
                                  font=('Arial', 18, "bold"), bg='white')
        self.appointment.place(x=1000, y=100)
        self.date = tk.Label(self.root, text='Monday, 05 November 2030', 
                           font=('Arial', 17), bg='white')
        self.date.place(x=970, y=160)
        self.time = tk.Label(self.root, text='Time: 14:00', 
                           font=('Arial', 13), bg='white')
        self.time.place(x=970, y=200)

        # Patient info labels
        info_labels = [
            ("Full Name:", "John Doe"),
            ("Sex:", "Male"),
            ("Date Of Birth:", "01/01/1990"),
            ("Address:", "123 Main St."),
            ("Email:", "johndoe@example.com"),
            ("Phone Number:", "+1234567890"),
            ("Emergency Contact:", "Jane Doe"),
            ("Insurance:", "ABC Insurance")
        ]

        self.labels = {}
        self.entries = {}
        
        for i, (label_text, default_value) in enumerate(info_labels):
            y_pos = 300 + (i * 50)
            
            # Create label
            label = tk.Label(self.root, text=label_text, font=("Arial", 14), bg='white')
            label.place(x=300, y=y_pos)
            self.labels[label_text] = label
            
            # Create entry (initially hidden)
            entry = tk.Entry(self.root, font=("Arial", 14), state='disabled')
            entry.insert(0, default_value)
            self.entries[label_text] = entry

        # Edit Button
        self.edit_button = tk.Button(self.root, text="✏️ Edit", font=("Arial", 12), 
                                   command=lambda: self.enable_edit(None))
        self.edit_button.place(x=750, y=280)

        # Save button (initially hidden)
        self.save_button = tk.Button(self.root, text="Save Changes", 
                                   font=("Arial", 14), command=self.save_changes)
        self.save_button.place_forget()

        # Medical History Button
        self.medhistory = tk.Label(self.root, text='Medical History', 
                                 font=('Arial', 18, 'bold'), bg='white')
        self.medhistory.place(x=1020, y=370)
        self.viewmore = tk.Button(self.root, text="View More", 
                                font=('Arial', 12), bg='#69C6F7', fg='white')
        self.viewmore.place(x=1040, y=420)

    def create_default_profile(self):
        # Create a default profile picture as a grey circle
        default_image = Image.new('RGB', (150, 150), color='grey')
        self.default_profile = default_image
        self.profile_pic = ImageTk.PhotoImage(default_image)

    def change_profile_pic(self, event):
        file_path = filedialog.askopenfilename(
            title='Select Image',
            filetypes=(('Image files', "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*.*"))
        )

        if file_path:
            try:
                new_image = Image.open(file_path)
                new_image = new_image.resize((150, 150), Image.Resampling.LANCZOS)
                self.profile_pic = ImageTk.PhotoImage(new_image)
                self.profile_label.config(image=self.profile_pic)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def remove_profile_pic(self, event):
        self.profile_pic = ImageTk.PhotoImage(self.default_profile)
        self.profile_label.config(image=self.profile_pic)

    def enable_edit(self, event):
        for label_text, entry in self.entries.items():
            entry.place(x=460, y=self.labels[label_text].winfo_y(), width=300)
            entry.config(state='normal')

        self.save_button.place(x=600, y=280)

    def save_changes(self):
        for label_text, entry in self.entries.items():
            self.labels[label_text].config(text=f"{label_text} {entry.get()}")
            entry.config(state='disabled')
            entry.place_forget()

        self.save_button.place_forget()

if __name__ == "__main__":
    app = PatientHome()
    app.root.mainloop()