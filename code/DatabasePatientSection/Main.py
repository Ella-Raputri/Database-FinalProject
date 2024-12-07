import tkinter as tk
from Booking import Booking
from Home import PatientHome
from History import History
from PIL import Image, ImageTk
import mysql.connector

import mysql.connector

# Connect to MySQL database
def connect_to_db():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",  # or "127.0.0.1"
            user="root",       # MySQL username
            password="BinusSQL2005",  # Your MySQL password
            database="ClinicSystemDB"  # The database name
        )
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clinic Appointment System")
        self.geometry("1360x768")

        # Load background image
        self.bg_image = Image.open("images/main background.png")  # Ensure the path is correct
        self.bg_image = self.bg_image.resize((1360, 768), Image.Resampling.LANCZOS)  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Label widget to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Make the background image fill the window



        # Sidebar buttons (Labels with icons)
        self.home_icon = Image.open("images/home.png")  # Your home icon
        self.home_icon = self.home_icon.resize((230, 50), Image.Resampling.LANCZOS)
        self.home_icon_photo = ImageTk.PhotoImage(self.home_icon)

        self.home_label = tk.Label(self, text="Home", image=self.home_icon_photo, compound="left",
                                   fg="white", font=("Poppins Semibold", 18), bd=0, padx=30, bg=self["bg"], cursor='hand2')
        self.home_label.place(x=-30, y=120)

        self.booking_icon = Image.open("images/booking (2).png")  # Your booking icon
        self.booking_icon = self.booking_icon.resize((270, 60), Image.Resampling.LANCZOS)
        self.booking_icon_photo = ImageTk.PhotoImage(self.booking_icon)

        self.booking_label = tk.Label(self, image=self.booking_icon_photo, compound="left",
                                      fg="white", font=("Poppins Semibold", 18), bd=0, padx=30, bg=self["bg"], cursor='hand2')
        self.booking_label.place(x=-25, y=180)

        self.history_icon = Image.open("images/booking_icon.png")  # Your history icon
        self.history_icon = self.history_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.history_icon_photo = ImageTk.PhotoImage(self.history_icon)

        self.history_label = tk.Label(self, text="History", image=self.history_icon_photo, compound="left",
                                      fg="white", font=("Poppins Semibold", 18), bd=0)
        self.history_label.pack(pady=20)

        # Main content frame (place it next to the sidebar)
        self.content_frame = tk.Frame(self, bg='white')
        self.content_frame.place(relx=0.17, rely=0, relwidth=0.85, relheight=1)

        # Add event bindings for labels
        self.home_label.bind("<Button-1>", self.show_home)
        self.booking_label.bind("<Button-1>", self.show_booking)
        self.history_label.bind("<Button-1>", self.show_history)

    def show_home(self, event=None):
        # Clear content and show home
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        PatientHome(self.content_frame)

    def show_booking(self, event=None):
        # Clear content and show booking
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Booking(self.content_frame)

    def show_history(self, event=None):
        # Clear content and show history
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        History(self.content_frame)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
