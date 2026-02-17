from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import mysql.connector
import HomePage
import patientform
from Paitents_Dashboard import PatientDashboard

class PatientLogin(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.title("Patient Login")

        # Define paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"C:\Users\ASUS\Downloads\PATIENT\build\assets\frame0")

        # Create canvas
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load UI elements
        self.create_ui_elements()

        # Make window non-resizable
        self.resizable(False, False)

    def relative_to_assets(self, path):
        return self.assets_path / Path(path)

    def create_ui_elements(self):
        try:
            # Background image
            self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
            self.canvas.create_image(640.0, 360.0, image=self.image_1)

            # Rectangle separator
            self.canvas.create_rectangle(
                -5.0, 92.0, 1280.0, 97.0,
                fill="#000000", outline=""
            )

            # Header image
            self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
            self.canvas.create_image(631.0, 51.0, image=self.image_2)

            # Main form image
            self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
            self.canvas.create_image(640.0, 437.0, image=self.image_3)

            # Title image
            self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
            self.canvas.create_image(640.0, 242.0, image=self.image_4)

            # Register button
            self.button_2_image = PhotoImage(file=self.relative_to_assets("button_2.png"))
            self.button_2 = Button(
                self,
                image=self.button_2_image,
                borderwidth=0,
                highlightthickness=0,
                command=self.login_button_clicked,
                relief="flat"
            )
            self.button_2.place(x=415.0, y=503.0, width=451.0, height=70.0)

            # Username label image
            self.image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
            self.canvas.create_image(640.0, 306.0, image=self.image_5)

            # Username entry
            self.entry_1_bg = PhotoImage(file=self.relative_to_assets("entry_1.png"))
            self.canvas.create_image(639.0, 302.5, image=self.entry_1_bg)
            self.username_entry = Entry(
                self,
                bd=0,
                bg="#FFFFFF",
                fg="#000716",
                highlightthickness=0
            )
            self.username_entry.place(x=402.0, y=292.0, width=474.0, height=19.0)

            # Password label image
            self.image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
            self.canvas.create_image(640.0, 377.0, image=self.image_6)

            # Password field border image
            self.image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
            self.canvas.create_image(640.0, 440.0, image=self.image_7)

            # Password entry
            self.entry_2_bg = PhotoImage(file=self.relative_to_assets("entry_2.png"))
            self.canvas.create_image(641.5, 440.0, image=self.entry_2_bg)
            self.password_entry = Entry(
                self,
                bd=0,
                bg="#FFFFFF",
                fg="#000716",
                highlightthickness=0,
                show="*"
            )
            self.password_entry.place(x=402.0, y=428.0, width=479.0, height=22.0)

        except Exception as e:
            print(f"Error loading images: {e}")

        # Add "To register" label
        self.canvas.create_text(
            540.0, 635.0,
            text="To Register:",
            fill="#000000",
            font=("Arial", 16, "bold")
        )

        # "Fill up patient form" button
        self.patient_form_button = Button(
            self,
            text="Fill up patient form",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            highlightthickness=0,
            command=self.open_patient_form,
            relief="flat"
        )
        self.patient_form_button.place(x=610.0, y=620.0, width=200.0, height=28.0)

        # "Back to Home" button
        self.back_to_home_button = Button(
            self,
            text="Back To Home",
            bg="#E9967A",
            fg="light grey",
            font=("Arial", 11, "bold"),
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_home_page,
            relief="flat"
        )
        self.back_to_home_button.place(x=550.0, y=585.0, width=150.0, height=30.0)

    def login_button_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = connection.cursor(dictionary=True)

            # First check if the patient exists in the patients table
            cursor.execute("SELECT * FROM patients WHERE Email=%s AND Password=%s", (username, password))
            patient = cursor.fetchone()
            
            # Consume any remaining results to avoid "Unread result found" error
            while cursor.nextset():
                pass

            if patient:
                # Check if the patient has filled the form by checking if they have a name
                if patient['PatientName']:
                    # Close resources before switching window
                    if cursor:
                        cursor.close()
                    if connection and connection.is_connected():
                        connection.close()
                        
                    # If they have filled the form, show the dashboard
                    self.destroy()
                    PatientDashboard(username).mainloop()
                else:
                    # Close resources before switching window
                    if cursor:
                        cursor.close()
                    if connection and connection.is_connected():
                        connection.close()
                        
                    # If they haven't filled the form, show a message and redirect to the form
                    messagebox.showinfo("Information", "Please complete your patient form first.")
                    self.open_patient_form()
            else:
                # Close resources before returning
                if cursor:
                    cursor.close()
                if connection and connection.is_connected():
                    connection.close()
                
                messagebox.showerror("Error", "Invalid username or password.")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            
            # Close resources in case of error
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def go_to_home_page(self):
        self.destroy()
        HomePage.HomePage()

    def open_patient_form(self):
        self.destroy()
        patientform.OrganRecipientForm()

if __name__ == "__main__":
    app = PatientLogin()
    app.mainloop()
