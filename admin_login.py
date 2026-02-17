import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import HomePage
import admin_dashboard

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("1280x720")
        self.configure(bg="white")

        # Load and set background image
        self.bg_image_path = r"C:\Users\ASUS\PycharmProjects\TransplantCare\Image folder\ADMIN LOGIN.png"
        self.set_background()

        # Database connection
        self.conn = None
        self.cursor = None
        self.connect_to_database()

        self.show_login_page()

    def connect_to_database(self):
        """Establish database connection."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")

    def set_background(self):
        """Set the background image."""
        try:
            bg_image = Image.open(self.bg_image_path)
            bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def show_login_page(self):
        """Displays the login page."""
        self.clear_frame()
        self.set_background()

        # Labels & Entry Fields
        tk.Label(self, text="Username:", bg="#E1FFFD", font=("Trebuchet MS", 20, "bold")).place(relx=0.5, rely=0.30,
                                                                                                anchor="center")
        self.username_entry = tk.Entry(self, font=("Arial", 18), width=35)
        self.username_entry.place(relx=0.5, rely=0.38, anchor="center")

        tk.Label(self, text="Password:", bg="#E1FFFD", font=("Trebuchet MS", 20, "bold")).place(relx=0.5, rely=0.45,
                                                                                                anchor="center")
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 18), width=35)
        self.password_entry.place(relx=0.5, rely=0.53, anchor="center")

        # Buttons
        tk.Button(self, text="Login", command=self.login, bg="#2c3e50", fg="white",
                  font=("Arial", 18), width=20, height=2).place(relx=0.5, rely=0.65, anchor="center")
        tk.Button(self, text="Back to Home", command=self.back_to_home,
                  bg="red", fg="white", font=("Arial", 14), width=25).place(relx=0.5, rely=0.75, anchor="center")

    def back_to_home(self):
        if self.conn:
            self.conn.close()
        self.destroy()
        app = HomePage.HomePage()
        app.mainloop()

    def login(self):
        """Handles user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = self.cursor.fetchone()

        if user:
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def show_dashboard(self):
        """Opens the admin dashboard."""
        if self.conn:
            self.conn.close()
        self.destroy()
        app = admin_dashboard.AdminDashboard()
        app.mainloop()

    def clear_frame(self):
        """Clears all widgets from the main window."""
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()