import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import donorform
import admin_login
from patientform import OrganRecipientForm
import donorlogin
import patientlogin
import bar_chart

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organ Donation System")
        self.geometry("1280x720")

        self.load_background()
        self.create_buttons()

    def load_background(self):
        """Loads and sets the background image."""
        screen_width = 1280
        screen_height = 720
        image_path = r"C:\Users\ASUS\Downloads\home login start (5).png"

        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            messagebox.showerror("Error", "Background image file not found!")
            self.destroy()
            exit()

    def create_buttons(self):
        """Creates the Stats, Donor, Patient, and Admin buttons."""
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        try:
            # Load and resize blood drop image
            image_path = r"C:\Users\ASUS\Desktop\Transplant Care\Image folder\blood1.png"
            blood_image = Image.open(image_path)
            blood_image = blood_image.resize((30, 30), Image.LANCZOS)  # Smaller size to match navigation
            self.blood_photo = ImageTk.PhotoImage(blood_image)

            # Create blood donation button
            blood_button = tk.Button(
                button_frame,
                image=self.blood_photo,
                bg="white",
                cursor="hand2",
                command=self.open_blood_donation,
                relief="flat",
                bd=0,
                highlightthickness=0
            )
            blood_button.pack(side=tk.RIGHT, padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load blood drop image: {str(e)}")

        # Stats Button
        stats_label = tk.Label(button_frame, text="Statistics", font=("Arial", 22, "bold"), fg="grey",
                               bg="white", cursor="hand2", padx=20, pady=10)
        stats_label.bind("<Button-1>", self.open_stats_section)

        # Donor Button
        donor_label = tk.Label(button_frame, text="Donor", font=("Arial", 22, "bold"), fg="grey",
                               bg="white", cursor="hand2", padx=20, pady=10)
        donor_label.bind("<Button-1>", self.open_donor_login)

        # Patient Button
        patient_label = tk.Label(button_frame, text="Patient", font=("Arial", 22, "bold"), fg="grey",
                                 bg="white", cursor="hand2", padx=20, pady=10)
        patient_label.bind("<Button-1>", self.open_patient_login)

        # Admin Button
        admin_label = tk.Label(button_frame, text="Admin", font=("Arial", 22, "bold"), fg="grey",
                               bg="white", cursor="hand2", padx=20, pady=10)
        admin_label.bind("<Button-1>", self.open_admin_section)

        # Pack buttons in the desired order
        admin_label.pack(side=tk.RIGHT, padx=5)
        patient_label.pack(side=tk.RIGHT, padx=5)
        donor_label.pack(side=tk.RIGHT, padx=5)
        stats_label.pack(side=tk.RIGHT, padx=5)

    def open_blood_donation(self):
        """Opens the Blood Donation Camp window."""
        try:
            from blood import BloodCampScheduleApp
            self.destroy()
            root = tk.Tk()
            app = BloodCampScheduleApp(root)
            app.run()
        except ImportError:
            messagebox.showerror("Error", "Blood Donation module not found!")

    def open_stats_section(self, event=None):
        self.destroy()
        app = bar_chart.OrganDonationAnalysis()
        app.mainloop()

    def open_donor_login(self, event=None):
        """Opens the DonorForm window."""
        self.destroy()
        app = donorlogin.DonorLogin()
        app.mainloop()

    def open_patient_login(self, event=None):
        """Opens the OrganRecipientForm window."""
        self.destroy()
        app = patientlogin.PatientLogin()
        app.mainloop()

    def open_admin_section(self, event=None):
        """Opens the Admin section."""
        self.destroy()
        app = admin_login.LoginApp()
        app.mainloop()

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()