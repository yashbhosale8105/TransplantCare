import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from mysql.connector import Error
import re
import HomePage
from datetime import datetime, timedelta
import random
import donorlogin

class DonorForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Donor Information Form")
        self.geometry("1280x720")
        self.resizable(False, False)

        # Store city_menu as instance variable
        self.city_menu = None

        # Load Background Image
        image_path = r"C:\Users\ASUS\Downloads\bg page.png"
        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.canvas = tk.Canvas(self, width=1280, height=720)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            messagebox.showerror("Error", "Background image file not found!")
            self.destroy()
            return

        # Input Variables
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.aadhaar_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.medical_history_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Select")
        self.blood_group_var = tk.StringVar(value="Select")
        self.organ_var = tk.StringVar(value="Select")
        self.state_var = tk.StringVar(value="Select")
        self.city_var = tk.StringVar(value="Select")
        self.pincode_var = tk.StringVar()

        # Create Form Layout
        self.create_form()

    def back_to_home(self):
        self.destroy()
        HomePage.HomePage()

    def validate_phone(self, P):
        return P == "" or (P.isdigit() and len(P) <= 10)

    def validate_age(self, P):
        return P == "" or (P.isdigit() and len(P) <= 2)

    def validate_aadhaar(self, P):
        return P == "" or (P.isdigit() and len(P) <= 12)

    def validate_email(self, email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def validate_pincode(self, P):
        return P == "" or (P.isdigit() and len(P) <= 6)

    def create_form(self):
        # Define Indian states and their cities
        self.states_and_cities = {
            "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati"],
            "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro"],
            "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon"],
            "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"],
            "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Raigarh"],
            "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"],
            "Goa": ["Panaji", "Margao", "Vasco da Gama", "Ponda", "Bicholim"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
            "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Ambala", "Yamunanagar"],
            "Himachal Pradesh": ["Shimla", "Kullu", "Manali", "Dharamshala", "Dalhousie"],
            "Jammu and Kashmir": ["Srinagar", "Jammu", "Baramulla", "Anantnag", "Udhampur"],
            "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar"],
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
            "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
            "Ladakh": ["Leh", "Kargil", "Nubra Valley", "Zanskar", "Drass"],
            "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
            "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Ukhrul"],
            "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongpoh", "Williamnagar"],
            "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai", "Kolasib"],
            "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha"],
            "Odisha": ["Bhubaneswar", "Cuttack", "Puri", "Rourkela", "Sambalpur"],
            "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
            "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
            "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner"],
            "Sikkim": ["Gangtok", "Namchi", "Mangan", "Gyalshing", "Soreng"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
            "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
            "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailasahar", "Belonia"],
            "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Prayagraj"],
            "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Nainital", "Mussoorie"],
            "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"]
        }

        y_offset = 0.25
        x_offsets = [0.15, 0.45, 0.75]  # Adjusted for equal spacing

        # Basic fields - first two rows
        fields_row1_2 = [
            ("Name:", self.name_var),
            ("Age:", self.age_var),
            ("Phone:", self.phone_var),
            ("Email:", self.email_var),
            ("Password:", self.password_var),
            ("Aadhaar Number:", self.aadhaar_var)
        ]

        for i, (label, var) in enumerate(fields_row1_2):
            col = i % 3
            row = i // 3

            tk.Label(self, text=label, font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(relx=x_offsets[col],
                                                                                                    rely=y_offset + (row * 0.12),
                                                                                                    anchor="w")

            entry = tk.Entry(self, textvariable=var, width=25, bg="#D3D3D3", font=("Arial", 14),
                             show="*" if label == "Password:" else "")
            entry.place(relx=x_offsets[col], rely=y_offset + (row * 0.12) + 0.05, anchor="w")

            # Apply validation
            if label == "Phone:":
                entry.config(validate="key", validatecommand=(self.register(self.validate_phone), "%P"))
            if label == "Age:":
                entry.config(validate="key", validatecommand=(self.register(self.validate_age), "%P"))
            if label == "Aadhaar Number:":
                entry.config(validate="key", validatecommand=(self.register(self.validate_aadhaar), "%P"))

        # Address fields row
        y_offset += 0.24  # Move to third row
        
        # Street Address
        tk.Label(self, text="Street Address:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.15, rely=y_offset, anchor="w")
        entry = tk.Entry(self, textvariable=self.address_var, width=25, bg="#D3D3D3", font=("Arial", 14))
        entry.place(relx=0.15, rely=y_offset + 0.05, anchor="w")

        # State
        tk.Label(self, text="State:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.45, rely=y_offset, anchor="w")
        state_menu = tk.OptionMenu(self, self.state_var, *list(self.states_and_cities.keys()))
        state_menu.config(width=20)
        state_menu.place(relx=0.45, rely=y_offset + 0.05, anchor="w")
        self.state_var.trace('w', self.update_cities)

        # City
        tk.Label(self, text="City:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.75, rely=y_offset, anchor="w")
        self.city_menu = tk.OptionMenu(self, self.city_var, *["Select"])
        self.city_menu.config(width=20)
        self.city_menu.place(relx=0.75, rely=y_offset + 0.05, anchor="w")

        # Medical History and Pincode row
        y_offset += 0.12
        
        # Pincode
        tk.Label(self, text="Pincode:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.15, rely=y_offset, anchor="w")
        pincode_entry = tk.Entry(self, textvariable=self.pincode_var, width=25, bg="#D3D3D3", font=("Arial", 14))
        pincode_entry.place(relx=0.15, rely=y_offset + 0.05, anchor="w")
        pincode_entry.config(validate="key", validatecommand=(self.register(self.validate_pincode), "%P"))

        # Medical History
        tk.Label(self, text="Medical History:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.45, rely=y_offset, anchor="w")
        entry = tk.Entry(self, textvariable=self.medical_history_var, width=25, bg="#D3D3D3", font=("Arial", 14))
        entry.place(relx=0.45, rely=y_offset + 0.05, anchor="w")

        # Dropdown fields row
        y_offset += 0.12

        # Gender
        tk.Label(self, text="Gender:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.15, rely=y_offset, anchor="w")
        gender_menu = tk.OptionMenu(self, self.gender_var, "Male", "Female", "Other")
        gender_menu.config(width=20)
        gender_menu.place(relx=0.15, rely=y_offset + 0.05, anchor="w")

        # Blood Group
        tk.Label(self, text="Blood Group:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.45, rely=y_offset, anchor="w")
        blood_menu = tk.OptionMenu(self, self.blood_group_var, "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")
        blood_menu.config(width=20)
        blood_menu.place(relx=0.45, rely=y_offset + 0.05, anchor="w")

        # Organ
        tk.Label(self, text="Organ to Donate:", font=("Trebuchet MS", 16), fg="#000000", bg="#E1FFFD").place(
            relx=0.75, rely=y_offset, anchor="w")
        organ_menu = tk.OptionMenu(self, self.organ_var, "Kidney", "Heart", "Liver", "Lung", "Pancreas", "Cornea")
        organ_menu.config(width=20)
        organ_menu.place(relx=0.75, rely=y_offset + 0.05, anchor="w")

        # Buttons
        y_offset += 0.15
        # Submit Button
        tk.Button(self, text="Submit", command=self.submit, bg="green", fg="white", 
                 width=25, font=("Arial", 14)).place(relx=0.5, rely=0.85, anchor="center")

        # Back to Home Button
        tk.Button(self, text="Back to Home", command=self.back_to_home,
                 bg="red", fg="white", font=("Arial", 14), 
                 width=25).place(relx=0.5, rely=0.92, anchor="center")

    def update_cities(self, *args):
        """Update cities dropdown based on selected state."""
        selected_state = self.state_var.get()
        
        # Get the menu from the OptionMenu widget
        menu = self.city_menu['menu']
        menu.delete(0, 'end')  # Remove all existing cities
        
        if selected_state in self.states_and_cities:
            cities = self.states_and_cities[selected_state]
            for city in cities:
                menu.add_command(label=city, 
                               command=lambda value=city: self.city_var.set(value))
        
        self.city_var.set("Select")  # Reset city selection

    def generate_appointment(self):
        # Generate a random date in the next 7 days
        today = datetime.now()
        appointment_date = today + timedelta(days=random.randint(3, 7))

        # Format the date as dd/mm/yyyy
        date_str = appointment_date.strftime("%d/%m/%Y")

        # Generate a random time between 9 AM and 5 PM
        hour = random.randint(9, 16)  # 9 AM to 4 PM
        minute = random.choice([0, 15, 30, 45])
        time_str = f"{hour:02d}:{minute:02d}"

        # Set a location based on the organ type and donor's city
        hospitals = {
            "Kidney": "City Nephrology Center",
            "Heart": "Cardiac Specialty Hospital",
            "Liver": "Liver Institute",
            "Lung": "Pulmonary Medical Center",
            "Pancreas": "Endocrine Specialty Hospital",
            "Cornea": "Vision Eye Hospital"
        }

        organ = self.organ_var.get()
        donor_city = self.city_var.get()
        hospital_name = hospitals.get(organ, "TransplantCare Hospital")
        location = f"{hospital_name}, {donor_city}"

        return date_str, time_str, location

    def submit(self):
        try:
            # Form validation
            if any(var.get() in ["", "Select"] for var in [
                self.name_var, self.age_var, self.phone_var, self.email_var,
                self.password_var, self.aadhaar_var, self.blood_group_var,
                self.organ_var, self.gender_var, self.state_var, self.city_var
            ]):
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            if not self.validate_email(self.email_var.get()):
                messagebox.showerror("Error", "Invalid email format!")
                return

            # Connect to database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = connection.cursor()

            # Insert data with separate city and state columns
            cursor.execute("""
                INSERT INTO donors (name, age, gender, contact_number, 
                                  email, password, aadhaar, blood_type,
                                  organ, medical_history, status, address,
                                  city, state, pincode)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.name_var.get(), int(self.age_var.get()), self.gender_var.get(),
                self.phone_var.get(), self.email_var.get(), self.password_var.get(),
                self.aadhaar_var.get(), self.blood_group_var.get(),
                self.organ_var.get(), self.medical_history_var.get(), 'Pending',
                self.address_var.get(),  # Store only the street address
                self.city_var.get(),     # Store city separately
                self.state_var.get(),    # Store state separately
                self.pincode_var.get()   # Store pincode separately
            ))

            connection.commit()

            # Generate appointment details
            date_str, time_str, location = self.generate_appointment()

            # Show success message with appointment details
            appointment_msg = f"""Thank you for registering as a donor!

Your appointment has been scheduled for initial screening:

Date: {date_str}
Time: {time_str}
Location: {location}

Please arrive 15 minutes before your scheduled time.
Don't forget to bring your ID and medical records."""

            messagebox.showinfo("Appointment Scheduled", appointment_msg)

            # Clear the form fields after successful submission
            self.clear_form()

        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def clear_form(self):
        """Clear all form fields after submission."""
        self.name_var.set("")
        self.age_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.aadhaar_var.set("")
        self.address_var.set("")
        self.medical_history_var.set("")
        self.gender_var.set("Select")
        self.blood_group_var.set("Select")
        self.organ_var.set("Select")
        self.state_var.set("Select")
        self.city_var.set("Select")
        self.pincode_var.set("")

    def setup_database(self):
        """Ensure required tables exist and have all necessary columns."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = connection.cursor()

            # Create donors table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS donors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    contact_number VARCHAR(15) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    aadhaar VARCHAR(12) NOT NULL,
                    blood_type VARCHAR(5) NOT NULL,
                    organ VARCHAR(20) NOT NULL,
                    medical_history TEXT,
                    status VARCHAR(20) DEFAULT 'Pending',
                    address TEXT NOT NULL
                )
            """)

            # Add new columns if they don't exist
            try:
                cursor.execute("ALTER TABLE donors ADD COLUMN city VARCHAR(100) NOT NULL")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    raise e

            try:
                cursor.execute("ALTER TABLE donors ADD COLUMN state VARCHAR(100) NOT NULL")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    raise e

            try:
                cursor.execute("ALTER TABLE donors ADD COLUMN pincode VARCHAR(6) NOT NULL")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    raise e

            connection.commit()

        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    app = DonorForm()
    app.mainloop()