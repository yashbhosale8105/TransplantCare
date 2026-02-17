import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import mysql.connector
import HomePage
import matching_feature
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
from PyPDF2 import PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1280x720")
        self.configure(bg="white")

        # Database connection
        self.conn = None
        self.cursor = None
        self.connect_to_database()

        self.show_dashboard()

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

    def show_dashboard(self):
        """Displays the dashboard after login."""
        self.clear_frame()

        # Sidebar
        sidebar = tk.Frame(self, bg="#2c3e50", width=250, height=720)
        sidebar.pack(side="left", fill="y")

        buttons = [
            ("Donor Details", self.show_donor_details),
            ("Patient Details", self.show_patient_details),
            ("Approved Donor", self.show_approved_donor),
            ("Matched Pairs", self.show_matched_pairs),
            ("Organ Donate Process", self.show_organ_donation),
            ("Logout", self.logout)
        ]

        for text, command in buttons:
            tk.Button(sidebar, text=text, font=("Trebuchet MS", 18, "bold"),
                      bg="#E1FFFD", fg="black", bd=0, padx=15, pady=10,
                      command=command).pack(fill="x", pady=5)

        # Main Content Frame
        self.main_content = tk.Frame(self, bg="white")
        self.main_content.pack(side="right", fill="both", expand=True)

        # Create frames for each section (initially hidden)
        self.donor_frame = tk.Frame(self.main_content, bg="white")
        self.patient_frame = tk.Frame(self.main_content, bg="white")
        self.approved_donor_frame = tk.Frame(self.main_content, bg="white")
        self.matched_pairs_frame = tk.Frame(self.main_content, bg="white")
        self.organ_donation_frame = tk.Frame(self.main_content, bg="white")

        # Initialize content for each frame
        self.initialize_donor_frame()
        self.initialize_patient_frame()
        self.initialize_approved_donor_frame()
        self.initialize_matched_pairs_frame()
        self.initialize_organ_donation_frame()

        # Load Default Page (Donor Details)
        self.show_donor_details()

    def logout(self):
        """Handles user logout."""
        if self.conn:
            self.conn.close()
        self.destroy()
        import admin_login
        app = admin_login.LoginApp()
        app.mainloop()

    def initialize_donor_frame(self):
        """Initialize donor details frame with content."""
        title_frame = tk.Frame(self.donor_frame, bg="white")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Donor Details", font=("Arial", 36, "bold"), bg="white").pack(pady=10)

        # Create a container for donor information
        info_frame = tk.Frame(self.donor_frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add search functionality
        search_frame = tk.Frame(info_frame, bg="white")
        search_frame.pack(fill="x", pady=10)

        tk.Label(search_frame, text="Search Donor:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
        self.donor_search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.donor_search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.search_donors).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_donor_data).pack(side="left", padx=5)

        # Donor list display area with treeview
        donor_list_frame = tk.Frame(info_frame, bg="white")
        donor_list_frame.pack(fill="both", expand=True, pady=10)

        # Create Treeview with updated columns
        columns = ("id", "name", "age", "gender", "contact_number", "address", "city", "state", "blood_type", "organ", "status")
        self.donor_tree = ttk.Treeview(donor_list_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.donor_tree.heading("id", text="ID")
        self.donor_tree.heading("name", text="Name")
        self.donor_tree.heading("age", text="Age")
        self.donor_tree.heading("gender", text="Gender")
        self.donor_tree.heading("contact_number", text="Contact Number")
        self.donor_tree.heading("address", text="Street Address")
        self.donor_tree.heading("city", text="City")
        self.donor_tree.heading("state", text="State")
        self.donor_tree.heading("blood_type", text="Blood Group")
        self.donor_tree.heading("organ", text="Organ")
        self.donor_tree.heading("status", text="Status")

        # Define columns
        self.donor_tree.column("id", width=50, anchor="center")
        self.donor_tree.column("name", width=150, anchor="w")
        self.donor_tree.column("age", width=50, anchor="center")
        self.donor_tree.column("gender", width=80, anchor="center")
        self.donor_tree.column("contact_number", width=120, anchor="center")
        self.donor_tree.column("address", width=150, anchor="w")
        self.donor_tree.column("city", width=100, anchor="w")
        self.donor_tree.column("state", width=100, anchor="w")
        self.donor_tree.column("blood_type", width=100, anchor="center")
        self.donor_tree.column("organ", width=100, anchor="center")
        self.donor_tree.column("status", width=100, anchor="center")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(donor_list_frame, orient="vertical", command=self.donor_tree.yview)
        self.donor_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.donor_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons for donor management
        button_frame = tk.Frame(info_frame, bg="white")
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Approve", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.approve_donor).pack(side="left", padx=5)
        tk.Button(button_frame, text="Not Approve", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.not_approve_donor).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Selected", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.delete_donor).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_donor_data).pack(side="left", padx=5)

        # Initialize with data
        self.load_donor_data()

    def load_donor_data(self):
        """Load donor data from database into the treeview."""
        # Clear existing data
        for item in self.donor_tree.get_children():
            self.donor_tree.delete(item)

        try:
            # Fetch donor data with address, city, and state
            self.cursor.execute("SELECT id, name, age, gender, contact_number, address, city, state, blood_type, organ, status FROM donors ORDER BY id DESC")
            donors = self.cursor.fetchall()
            
            # Consume any remaining results to avoid "Unread result found" error
            while self.cursor.nextset():
                pass

            # Insert into treeview
            for donor in donors:
                values = (
                    donor['id'],
                    donor['name'],
                    donor['age'],
                    donor['gender'],
                    donor['contact_number'],
                    donor['address'],
                    donor['city'],
                    donor['state'],
                    donor['blood_type'],
                    donor['organ'],
                    donor['status']
                )
                self.donor_tree.insert("", "end", values=values)

            # Update status bar if it exists
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Total donors: {len(donors)}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading donor data: {err}")

    def search_donors(self):
        """Search donors based on the search entry."""
        search_term = self.donor_search_entry.get().strip()

        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        # Clear existing data
        for item in self.donor_tree.get_children():
            self.donor_tree.delete(item)

        try:
            # Create search query with multiple conditions
            query = """SELECT id, name, age, gender, contact_number, address, city, state, blood_type, organ, status 
                      FROM donors 
                      WHERE name LIKE %s 
                      OR contact_number LIKE %s 
                      OR blood_type LIKE %s 
                      OR organ LIKE %s 
                      OR city LIKE %s
                      OR state LIKE %s
                      ORDER BY id DESC"""

            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                                      search_pattern, search_pattern, search_pattern))
            donors = self.cursor.fetchall()
            
            # Consume any remaining results to avoid "Unread result found" error
            while self.cursor.nextset():
                pass

            # Insert into treeview
            for donor in donors:
                values = (
                    donor['id'],
                    donor['name'],
                    donor['age'],
                    donor['gender'],
                    donor['contact_number'],
                    donor['address'],
                    donor['city'],
                    donor['state'],
                    donor['blood_type'],
                    donor['organ'],
                    donor['status']
                )
                self.donor_tree.insert("", "end", values=values)

            # Show search results count
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Search results: {len(donors)}")

            if len(donors) == 0:
                messagebox.showinfo("Search Results", "No matching donors found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching donor data: {err}")

    def approve_donor(self):
        """Approve the selected donor, add to approved_donor table, and send an approval email."""
        selected_item = self.donor_tree.selection()

        if not selected_item:
            messagebox.showinfo("Approve Donor", "Please select a donor to approve.")
            return

        # Get the selected donor's data
        donor_id = self.donor_tree.item(selected_item, "values")[0]
        donor_name = self.donor_tree.item(selected_item, "values")[1]

        # Fetch the donor's email from the database
        try:
            self.cursor.execute("SELECT email FROM donors WHERE id = %s", (donor_id,))
            donor_email = self.cursor.fetchone()["email"]
            # Consume any remaining results
            while self.cursor.nextset():
                pass
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching donor email: {err}")
            return

        # Confirm approval
        confirm = messagebox.askyesno("Confirm Approval", f"Are you sure you want to approve donor '{donor_name}'?")

        if confirm:
            try:
                # Fetch the donor's details
                self.cursor.execute("SELECT * FROM donors WHERE id = %s", (donor_id,))
                donor = self.cursor.fetchone()
                # Consume any remaining results
                while self.cursor.nextset():
                    pass

                # Insert into approved_donor table with status 'available'
                self.cursor.execute("""INSERT INTO approved_donor 
                                      (name, age, gender, contact_number, address, city, state, blood_type, organ, status)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'available')""",
                                    (donor['name'], donor['age'], donor['gender'], donor['contact_number'],
                                     donor['address'], donor['city'], donor['state'], 
                                     donor['blood_type'], donor['organ']))
                self.conn.commit()
                # Consume any remaining results
                while self.cursor.nextset():
                    pass

                # Update the donor's status in the donors table
                self.cursor.execute("UPDATE donors SET status = 'Approved' WHERE id = %s", (donor_id,))
                self.conn.commit()
                # Consume any remaining results
                while self.cursor.nextset():
                    pass

                # Send approval email
                self.send_approval_email(donor_email, donor_name)

                # Refresh the data
                self.load_donor_data()

                messagebox.showinfo("Approve Donor", f"Donor '{donor_name}' approved successfully.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error approving donor: {err}")

    def send_approval_email(self, receiver_email, donor_name):
        """Send an approval email to the donor with customized PDF attachment."""
        SENDER_EMAIL = "transplantcare1234@gmail.com"
        APP_PASSWORD = "rafckrpsrsuooqvk"
        PDF_TEMPLATE_PATH = "C:/Users/ASUS/Desktop/Transplant Care/transplant_report_template.txt"

        # Get donor details from the database
        try:
            self.cursor.execute("""
                SELECT name, gender, blood_type, organ
                FROM donors
                WHERE name = %s
            """, (donor_name,))
            donor_details = self.cursor.fetchone()
            # Consume any remaining results
            while self.cursor.nextset():
                pass

            # List of physician names for random selection
            physicians = [
                "Dr. Rajesh Kumar",
                "Dr. Priya Sharma",
                "Dr. Amit Patel",
                "Dr. Neha Gupta",
                "Dr. Sanjay Verma",
                "Dr. Anjali Singh",
                "Dr. Vikram Malhotra",
                "Dr. Meera Reddy",
                "Dr. Arun Kumar",
                "Dr. Deepika Sharma"
            ]
            physician_name = random.choice(physicians)
            current_date = datetime.now().strftime("%d-%m-%Y")

            # Create a new PDF using reportlab
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica-Bold", 24)
            can.drawString(150, 750, "TRANSPLANT CARE REPORT")
            
            can.setFont("Helvetica", 12)
            y = 700
            can.drawString(50, y, "Patient Information:")
            y -= 20
            can.drawString(50, y, f"Name: {donor_details['name']}")
            y -= 20
            can.drawString(50, y, f"Gender: {donor_details['gender']}")
            y -= 20
            can.drawString(50, y, f"Blood Type: {donor_details['blood_type']}")
            
            y -= 40
            can.drawString(50, y, "Medical History: No chronic illnesses, infections, or high-risk behaviors.")
            
            y -= 40
            can.drawString(50, y, "Clinical Status:")
            y -= 20
            can.drawString(50, y, "- Stable vital signs")
            y -= 20
            can.drawString(50, y, "- No contraindications in imaging/lab tests")
            y -= 20
            can.drawString(50, y, "- Neurological assessment: Brain death confirmed / Not confirmed")
            
            y -= 40
            can.drawString(50, y, "Organ Suitability:")
            y -= 20
            can.drawString(50, y, f"Selected Organ for Donation: {donor_details['organ']}")
            
            y -= 40
            can.drawString(50, y, "Conclusion: Donor is **Eligible** for organ donation.")
            
            y -= 40
            can.drawString(50, y, f"Physician: {physician_name}")
            can.drawString(50, y-20, f"Date: {current_date}")
            
            y -= 60
            can.drawString(50, y, "Signature: _____________________")
            
            can.save()

            # Create the temporary PDF file
            packet.seek(0)
            temp_pdf_path = "temp_transplant_report.pdf"
            with open(temp_pdf_path, "wb") as temp_file:
                temp_file.write(packet.getvalue())

            subject = f"Organ Donation Approval - {donor_name}"
            message = f"""Dear {donor_name},

We are pleased to inform you that you have been approved as an organ donor in our system. Your willingness to help those in need is truly admirable and has the potential to save lives.

Status: Approved & Available for Matching

We will notify you as soon as a matching recipient is found. In the meantime, if you have any questions or need further assistance, please feel free to contact us at [1800000].

Please find attached the detailed Transplant Care Report for your reference.

Thank you for your generosity and for making a difference!"""

            try:
                # Set up the email message
                msg = MIMEMultipart()
                msg["From"] = SENDER_EMAIL
                msg["To"] = receiver_email
                msg["Subject"] = subject
                
                # Attach the message body
                msg.attach(MIMEText(message, "plain"))

                # Attach the generated PDF file
                from email.mime.application import MIMEApplication
                with open(temp_pdf_path, "rb") as pdf_file:
                    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                    pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                           filename="Transplant_Care_Report.pdf")
                    msg.attach(pdf_attachment)

                # Connect to SMTP server
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)

                # Send email
                server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
                server.quit()

                # Clean up temporary file
                import os
                os.remove(temp_pdf_path)

                messagebox.showinfo("Success", "Approval email sent successfully with customized PDF attachment!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to send approval email: {e}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching donor details: {err}")

    def not_approve_donor(self):
        """Mark the selected donor as not approved, update status, and send a notification email."""
        selected_item = self.donor_tree.selection()

        if not selected_item:
            messagebox.showinfo("Not Approve Donor", "Please select a donor to mark as not approved.")
            return

        # Get the selected donor's data
        donor_id = self.donor_tree.item(selected_item, "values")[0]
        donor_name = self.donor_tree.item(selected_item, "values")[1]

        # Fetch the donor's email from the database
        try:
            self.cursor.execute("SELECT email FROM donors WHERE id = %s", (donor_id,))
            donor_email = self.cursor.fetchone()["email"]
            # Consume any remaining results
            while self.cursor.nextset():
                pass
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching donor email: {err}")
            return

        # Confirm not approval
        confirm = messagebox.askyesno("Confirm Not Approve", f"Are you sure you want to mark donor '{donor_name}' as not approved?")

        if confirm:
            try:
                # Update the donor's status in the donors table
                self.cursor.execute("UPDATE donors SET status = 'Not Approved' WHERE id = %s", (donor_id,))
                self.conn.commit()
                # Consume any remaining results
                while self.cursor.nextset():
                    pass

                # Send not approval email
                self.send_not_approval_email(donor_email, donor_name)

                # Refresh the data
                self.load_donor_data()

                messagebox.showinfo("Not Approve Donor", f"Donor '{donor_name}' marked as not approved successfully.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error marking donor as not approved: {err}")

    def send_not_approval_email(self, receiver_email, donor_name):
        """Send a not approval email to the donor."""
        SENDER_EMAIL = "transplantcare1234@gmail.com"
        APP_PASSWORD = "rafckrpsrsuooqvk"

        subject = f"Organ Donation Status - {donor_name}"
        message = f"""Dear {donor_name},

We regret to inform you that your application to become an organ donor has not been approved at this time. 

Status: Not Approved

If you have any questions or would like further clarification, please feel free to contact us at [1800000].

Thank you for your understanding.

Best regards,
TransplantCare Team"""

        try:
            # Set up the email message
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            # Connect to SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)

            # Send email
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
            server.quit()

            messagebox.showinfo("Success", "Not approval email sent successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send not approval email: {e}")

    def delete_donor(self):
        """Delete the selected donor."""
        selected_item = self.donor_tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Donor", "Please select a donor to delete.")
            return

        # Get the selected donor's data
        donor_id = self.donor_tree.item(selected_item, "values")[0]
        donor_name = self.donor_tree.item(selected_item, "values")[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete donor '{donor_name}'?")

        if confirm:
            try:
                # Delete the donor
                self.cursor.execute("DELETE FROM donors WHERE id = %s", (donor_id,))
                self.conn.commit()
                # Consume any remaining results
                while self.cursor.nextset():
                    pass

                # Refresh the data
                self.load_donor_data()

                messagebox.showinfo("Delete Donor", f"Donor '{donor_name}' deleted successfully.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting donor: {err}")

    def initialize_patient_frame(self):
        """Initialize patient details frame with content."""
        title_frame = tk.Frame(self.patient_frame, bg="white")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Patient Details", font=("Arial", 36, "bold"), bg="white").pack(pady=10)

        # Create a container for patient information
        info_frame = tk.Frame(self.patient_frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add search functionality
        search_frame = tk.Frame(info_frame, bg="white")
        search_frame.pack(fill="x", pady=10)

        tk.Label(search_frame, text="Search Patient:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
        self.patient_search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.patient_search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.search_patients).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_patient_data).pack(side="left", padx=5)

        # Patient list display area with treeview
        patient_list_frame = tk.Frame(info_frame, bg="white")
        patient_list_frame.pack(fill="both", expand=True, pady=10)

        # Create Treeview with updated columns
        columns = (
            "id", "name", "age", "gender", "phone", "email", "address", "city", "state", 
            "blood_group", "needed_organ", "urgency", "aadhaar", "medical_history"
        )
        self.patient_tree = ttk.Treeview(patient_list_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.patient_tree.heading("id", text="ID")
        self.patient_tree.heading("name", text="Name")
        self.patient_tree.heading("age", text="Age")
        self.patient_tree.heading("gender", text="Gender")
        self.patient_tree.heading("phone", text="Phone")
        self.patient_tree.heading("email", text="Email")
        self.patient_tree.heading("address", text="Street Address")
        self.patient_tree.heading("city", text="City")
        self.patient_tree.heading("state", text="State")
        self.patient_tree.heading("blood_group", text="Blood Group")
        self.patient_tree.heading("needed_organ", text="Organ Needed")
        self.patient_tree.heading("urgency", text="Urgency")
        self.patient_tree.heading("aadhaar", text="Aadhaar")
        self.patient_tree.heading("medical_history", text="Medical History")

        # Define columns
        self.patient_tree.column("id", width=50, anchor="center")
        self.patient_tree.column("name", width=150, anchor="w")
        self.patient_tree.column("age", width=50, anchor="center")
        self.patient_tree.column("gender", width=70, anchor="center")
        self.patient_tree.column("phone", width=120, anchor="center")
        self.patient_tree.column("email", width=150, anchor="w")
        self.patient_tree.column("address", width=150, anchor="w")
        self.patient_tree.column("city", width=100, anchor="w")
        self.patient_tree.column("state", width=100, anchor="w")
        self.patient_tree.column("blood_group", width=80, anchor="center")
        self.patient_tree.column("needed_organ", width=100, anchor="center")
        self.patient_tree.column("urgency", width=80, anchor="center")
        self.patient_tree.column("aadhaar", width=120, anchor="center")
        self.patient_tree.column("medical_history", width=150, anchor="w")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(patient_list_frame, orient="vertical", command=self.patient_tree.yview)
        self.patient_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.patient_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add horizontal scrollbar for many columns
        h_scrollbar = ttk.Scrollbar(patient_list_frame, orient="horizontal", command=self.patient_tree.xview)
        self.patient_tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        # Buttons for patient management
        button_frame = tk.Frame(info_frame, bg="white")
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Delete Selected", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.delete_patient).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_patient_data).pack(side="left", padx=5)

        # Initialize with data
        self.load_patient_data()

    def load_patient_data(self):
        """Load patient data from database into the treeview."""
        # Clear existing data
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        try:
            # First, let's figure out what the actual ID column name is
            self.cursor.execute("DESCRIBE patients")
            columns = self.cursor.fetchall()
            # Consume any remaining results
            while self.cursor.nextset():
                pass
                
            id_column = None
            for col in columns:
                if col['Field'].lower().endswith('id') or col['Key'] == 'PRI':
                    id_column = col['Field']
                    break

            # If we couldn't find it, use a safe default
            if not id_column:
                id_column = "id"  # Try a common default

            # Fetch patient data with correct column name and address components
            self.cursor.execute(f"""SELECT {id_column}, PatientName, PatientAge, Gender, PatientPhone, Email, 
                                  PatientAddress, City, State, PatientBloodGrp, NeededOrgan, Urgency, 
                                  Aadhaar, MedicalHistory 
                                  FROM patients ORDER BY {id_column} DESC""")
            patients = self.cursor.fetchall()
            # Consume any remaining results
            while self.cursor.nextset():
                pass

            # Insert into treeview
            for patient in patients:
                values = (
                    patient.get(id_column, "N/A"),
                    patient.get('PatientName', "N/A"),
                    patient.get('PatientAge', "N/A"),
                    patient.get('Gender', "N/A"),
                    patient.get('PatientPhone', "N/A"),
                    patient.get('Email', "N/A"),
                    patient.get('PatientAddress', "N/A"),
                    patient.get('City', "N/A"),
                    patient.get('State', "N/A"),
                    patient.get('PatientBloodGrp', "N/A"),
                    patient.get('NeededOrgan', "N/A"),
                    patient.get('Urgency', "N/A"),
                    patient.get('Aadhaar', "N/A"),
                    patient.get('MedicalHistory', "N/A")
                )
                self.patient_tree.insert("", "end", values=values)

            # Update status bar if it exists
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Total patients: {len(patients)}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading patient data: {err}")

    def search_patients(self):
        """Search patients based on the search entry."""
        search_term = self.patient_search_entry.get().strip()

        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        # Clear existing data
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        try:
            # First, let's figure out what the actual ID column name is
            self.cursor.execute("DESCRIBE patients")
            columns = self.cursor.fetchall()
            id_column = None
            for col in columns:
                if col['Field'].lower().endswith('id') or col['Key'] == 'PRI':
                    id_column = col['Field']
                    break

            # If we couldn't find it, use a safe default
            if not id_column:
                id_column = "id"  # Try a common default

            # Create search query with multiple conditions
            query = f"""SELECT {id_column}, PatientName, PatientAge, Gender, PatientPhone, Email, 
                       PatientAddress, City, State, PatientBloodGrp, NeededOrgan, Urgency, 
                       Aadhaar, MedicalHistory 
                       FROM patients 
                       WHERE PatientName LIKE %s 
                       OR PatientPhone LIKE %s 
                       OR PatientBloodGrp LIKE %s 
                       OR NeededOrgan LIKE %s
                       OR Urgency LIKE %s
                       OR Email LIKE %s
                       OR City LIKE %s
                       OR State LIKE %s
                       ORDER BY {id_column} DESC"""

            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern,
                                      search_pattern, search_pattern, search_pattern,
                                      search_pattern, search_pattern))
            patients = self.cursor.fetchall()

            # Insert into treeview
            for patient in patients:
                values = (
                    patient.get(id_column, "N/A"),
                    patient.get('PatientName', "N/A"),
                    patient.get('PatientAge', "N/A"),
                    patient.get('Gender', "N/A"),
                    patient.get('PatientPhone', "N/A"),
                    patient.get('Email', "N/A"),
                    patient.get('PatientAddress', "N/A"),
                    patient.get('City', "N/A"),
                    patient.get('State', "N/A"),
                    patient.get('PatientBloodGrp', "N/A"),
                    patient.get('NeededOrgan', "N/A"),
                    patient.get('Urgency', "N/A"),
                    patient.get('Aadhaar', "N/A"),
                    patient.get('MedicalHistory', "N/A")
                )
                self.patient_tree.insert("", "end", values=values)

            # Show search results count
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Search results: {len(patients)}")

            if len(patients) == 0:
                messagebox.showinfo("Search Results", "No matching patients found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching patient data: {err}")

    def delete_patient(self):
        """Delete the selected patient."""
        selected_item = self.patient_tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Patient", "Please select a patient to delete.")
            return

        # Get the selected patient's data
        values = self.patient_tree.item(selected_item, "values")
        patient_id = values[0]
        patient_name = values[1]

        # First, identify the correct id column
        try:
            self.cursor.execute("DESCRIBE patients")
            columns = self.cursor.fetchall()
            id_column = None
            for col in columns:
                if col['Field'].lower().endswith('id') or col['Key'] == 'PRI':
                    id_column = col['Field']
                    break

            # If we couldn't find it, use a safe default
            if not id_column:
                id_column = "id"  # Try a common default

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete",
                                          f"Are you sure you want to delete patient '{patient_name}'?")

            if confirm:
                # Delete the patient with the correct ID column
                self.cursor.execute(f"DELETE FROM patients WHERE {id_column} = %s", (patient_id,))
                self.conn.commit()

                # Refresh the data
                self.load_patient_data()

                messagebox.showinfo("Delete Patient", f"Patient '{patient_name}' deleted successfully.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting patient: {err}")

    def initialize_approved_donor_frame(self):
        """Initialize approved donor frame with content."""
        title_frame = tk.Frame(self.approved_donor_frame, bg="white")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Approved Donors", font=("Arial", 36, "bold"), bg="white").pack(pady=10)

        # Create a container for approved donors information
        info_frame = tk.Frame(self.approved_donor_frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add filter functionality
        filter_frame = tk.Frame(info_frame, bg="white")
        filter_frame.pack(fill="x", pady=10)

        tk.Label(filter_frame, text="Filter by Organ:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
        organ_options = ["All", "Heart", "Kidney", "Liver", "Lung", "Pancreas"]
        self.organ_var = tk.StringVar(value=organ_options[0])
        organ_menu = tk.OptionMenu(filter_frame, self.organ_var, *organ_options)
        organ_menu.config(font=("Arial", 12))
        organ_menu.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Apply Filter", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.load_approved_donor_data).pack(side="left", padx=5)

        # Approved donor list display area with treeview
        approved_list_frame = tk.Frame(info_frame, bg="white")
        approved_list_frame.pack(fill="both", expand=True, pady=10)

        # Create Treeview with updated columns
        columns = ("id", "name", "age", "gender", "contact_number", "address", "city", "state", "blood_type", "organ", "status")
        self.approved_donor_tree = ttk.Treeview(approved_list_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.approved_donor_tree.heading("id", text="ID")
        self.approved_donor_tree.heading("name", text="Name")
        self.approved_donor_tree.heading("age", text="Age")
        self.approved_donor_tree.heading("gender", text="Gender")
        self.approved_donor_tree.heading("contact_number", text="Contact Number")
        self.approved_donor_tree.heading("address", text="Street Address")
        self.approved_donor_tree.heading("city", text="City")
        self.approved_donor_tree.heading("state", text="State")
        self.approved_donor_tree.heading("blood_type", text="Blood Group")
        self.approved_donor_tree.heading("organ", text="Organ")
        self.approved_donor_tree.heading("status", text="Status")

        # Define columns
        self.approved_donor_tree.column("id", width=50, anchor="center")
        self.approved_donor_tree.column("name", width=150, anchor="w")
        self.approved_donor_tree.column("age", width=50, anchor="center")
        self.approved_donor_tree.column("gender", width=80, anchor="center")
        self.approved_donor_tree.column("contact_number", width=120, anchor="center")
        self.approved_donor_tree.column("address", width=150, anchor="w")
        self.approved_donor_tree.column("city", width=100, anchor="w")
        self.approved_donor_tree.column("state", width=100, anchor="w")
        self.approved_donor_tree.column("blood_type", width=100, anchor="center")
        self.approved_donor_tree.column("organ", width=100, anchor="center")
        self.approved_donor_tree.column("status", width=100, anchor="center")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(approved_list_frame, orient="vertical", command=self.approved_donor_tree.yview)
        self.approved_donor_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.approved_donor_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons for approved donor management
        button_frame = tk.Frame(info_frame, bg="white")
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Delete Selected", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.delete_approved_donor).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_approved_donor_data).pack(side="left", padx=5)

        # Initialize with data
        self.load_approved_donor_data()

    def load_approved_donor_data(self):
        """Load approved donor data from database into the treeview."""
        # Clear existing data
        for item in self.approved_donor_tree.get_children():
            self.approved_donor_tree.delete(item)

        try:
            # Fetch approved donor data with address components
            organ_filter = self.organ_var.get()
            if organ_filter == "All":
                self.cursor.execute("SELECT id, name, age, gender, contact_number, address, city, state, blood_type, organ, status FROM approved_donor ORDER BY id DESC")
            else:
                self.cursor.execute("SELECT id, name, age, gender, contact_number, address, city, state, blood_type, organ, status FROM approved_donor WHERE organ = %s ORDER BY id DESC", (organ_filter,))
            approved_donors = self.cursor.fetchall()

            # Insert into treeview
            for donor in approved_donors:
                values = (
                    donor['id'],
                    donor['name'],
                    donor['age'],
                    donor['gender'],
                    donor['contact_number'],
                    donor['address'],
                    donor['city'],
                    donor['state'],
                    donor['blood_type'],
                    donor['organ'],
                    donor['status']
                )
                self.approved_donor_tree.insert("", "end", values=values)

            # Update status bar if it exists
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Total approved donors: {len(approved_donors)}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading approved donor data: {err}")

    def delete_approved_donor(self):
        """Delete the selected approved donor."""
        selected_item = self.approved_donor_tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Approved Donor", "Please select an approved donor to delete.")
            return

        # Get the selected approved donor's data
        donor_id = self.approved_donor_tree.item(selected_item, "values")[0]
        donor_name = self.approved_donor_tree.item(selected_item, "values")[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete approved donor '{donor_name}'?")

        if confirm:
            try:
                # Delete the approved donor
                self.cursor.execute("DELETE FROM approved_donor WHERE id = %s", (donor_id,))
                self.conn.commit()

                # Refresh the data
                self.load_approved_donor_data()

                messagebox.showinfo("Delete Approved Donor", f"Approved donor '{donor_name}' deleted successfully.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting approved donor: {err}")

    def initialize_matched_pairs_frame(self):
        """Initialize matched pairs frame with content."""
        title_frame = tk.Frame(self.matched_pairs_frame, bg="white")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Matched Pairs", font=("Arial", 36, "bold"), bg="white").pack(pady=10)

        # Create a container for matched pairs information
        info_frame = tk.Frame(self.matched_pairs_frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add search functionality
        search_frame = tk.Frame(info_frame, bg="white")
        search_frame.pack(fill="x", pady=10)

        tk.Label(search_frame, text="Search Matches:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
        self.matched_search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.matched_search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.search_matches).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_matched_pairs_data).pack(side="left", padx=5)

        # Matched pairs list display area with treeview
        matched_list_frame = tk.Frame(info_frame, bg="white")
        matched_list_frame.pack(fill="both", expand=True, pady=10)

        # Create Treeview
        columns = ("id", "donor_name", "recipient_name", "organ", "blood_type", "match_date")
        self.matched_tree = ttk.Treeview(matched_list_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.matched_tree.heading("id", text="ID")
        self.matched_tree.heading("donor_name", text="Donor Name")
        self.matched_tree.heading("recipient_name", text="Recipient Name")
        self.matched_tree.heading("organ", text="Organ")
        self.matched_tree.heading("blood_type", text="Blood Type")
        self.matched_tree.heading("match_date", text="Match Date")

        # Define columns
        self.matched_tree.column("id", width=50, anchor="center")
        self.matched_tree.column("donor_name", width=150, anchor="w")
        self.matched_tree.column("recipient_name", width=150, anchor="w")
        self.matched_tree.column("organ", width=100, anchor="center")
        self.matched_tree.column("blood_type", width=100, anchor="center")
        self.matched_tree.column("match_date", width=150, anchor="center")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(matched_list_frame, orient="vertical", command=self.matched_tree.yview)
        self.matched_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.matched_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons for matched pairs management
        button_frame = tk.Frame(info_frame, bg="white")
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Delete Selected", font=("Arial", 12), bg="#2c3e50", fg="white",
                  command=self.delete_matched_pair).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", font=("Arial", 12), bg="#3498db", fg="white",
                  command=self.load_matched_pairs_data).pack(side="left", padx=5)

        # Initialize with data
        self.load_matched_pairs_data()

    def load_matched_pairs_data(self):
        """Load matched pairs data from database into the treeview."""
        # Clear existing data
        for item in self.matched_tree.get_children():
            self.matched_tree.delete(item)

        try:
            # Fetch matched pairs data
            self.cursor.execute("SELECT * FROM matches ORDER BY match_date DESC")
            matches = self.cursor.fetchall()

            # Insert into treeview
            for match in matches:
                match_date = match['match_date'].strftime("%Y-%m-%d %H:%M") if isinstance(match['match_date'], datetime) else str(match['match_date'])
                values = (
                    match['id'],
                    match['donor_name'],
                    match['recipient_name'],
                    match['organ'],
                    match['blood_type'],
                    match_date
                )
                self.matched_tree.insert("", "end", values=values)

            # Update status bar if it exists
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Total matched pairs: {len(matches)}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading matched pairs data: {err}")

    def search_matches(self):
        """Search matched pairs based on the search entry."""
        search_term = self.matched_search_entry.get().strip()

        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        # Clear existing data
        for item in self.matched_tree.get_children():
            self.matched_tree.delete(item)

        try:
            # Create search query with multiple conditions
            query = """SELECT * FROM matches 
                      WHERE donor_name LIKE %s 
                      OR recipient_name LIKE %s 
                      OR organ LIKE %s 
                      OR blood_type LIKE %s 
                      ORDER BY match_date DESC"""

            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            matches = self.cursor.fetchall()

            # Insert into treeview
            for match in matches:
                match_date = match['match_date'].strftime("%Y-%m-%d %H:%M") if isinstance(match['match_date'], datetime) else str(match['match_date'])
                values = (
                    match['id'],
                    match['donor_name'],
                    match['recipient_name'],
                    match['organ'],
                    match['blood_type'],
                    match_date
                )
                self.matched_tree.insert("", "end", values=values)

            # Show search results count
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Search results: {len(matches)}")

            if len(matches) == 0:
                messagebox.showinfo("Search Results", "No matching pairs found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching matched pairs data: {err}")

    def delete_matched_pair(self):
        """Delete the selected matched pair."""
        selected_item = self.matched_tree.selection()

        if not selected_item:
            messagebox.showinfo("Delete Matched Pair", "Please select a matched pair to delete.")
            return

        # Get the selected matched pair's data
        matched_id = self.matched_tree.item(selected_item, "values")[0]
        donor_name = self.matched_tree.item(selected_item, "values")[1]
        recipient_name = self.matched_tree.item(selected_item, "values")[2]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the matched pair between '{donor_name}' and '{recipient_name}'?")

        if confirm:
            try:
                # Delete the matched pair
                self.cursor.execute("DELETE FROM matches WHERE id = %s", (matched_id,))
                self.conn.commit()

                # Refresh the data
                self.load_matched_pairs_data()

                messagebox.showinfo("Delete Matched Pair", "Matched pair deleted successfully.")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting matched pair: {err}")

    def initialize_organ_donation_frame(self):
        """Initialize the organ donation frame with content."""
        title_frame = tk.Frame(self.organ_donation_frame, bg="white")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Organ Donation Process", font=("Arial", 36, "bold"), bg="white").pack(pady=10)

        # Create a container for organ donation information
        info_frame = tk.Frame(self.organ_donation_frame, bg="white")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add some content to the organ donation frame
        tk.Label(info_frame, text="This section will provide information about the organ donation process.",
                 font=("Arial", 18), bg="white").pack(pady=20)

    def show_donor_details(self):
        """Displays donor details."""
        self.clear_main_content()
        self.donor_frame.pack(fill="both", expand=True)

    def show_patient_details(self):
        """Displays patient details."""
        self.clear_main_content()
        self.patient_frame.pack(fill="both", expand=True)

    def show_approved_donor(self):
        """Displays approved donor details."""
        self.clear_main_content()
        self.approved_donor_frame.pack(fill="both", expand=True)

    def show_matched_pairs(self):
        """Displays matched pairs details."""
        self.clear_main_content()
        self.matched_pairs_frame.pack(fill="both", expand=True)

    def show_organ_donation(self):
        """Opens the organ donation matching system."""
        self.destroy()
        import matching_feature
        matching_feature.OrganDonorSystem().run()

    def clear_frame(self):
        """Clears all widgets from the main window."""
        for widget in self.winfo_children():
            widget.destroy()

    def clear_main_content(self):
        """Hides all frames in the main content area."""
        if hasattr(self, 'donor_frame'):
            self.donor_frame.pack_forget()
        if hasattr(self, 'patient_frame'):
            self.patient_frame.pack_forget()
        if hasattr(self, 'approved_donor_frame'):
            self.approved_donor_frame.pack_forget()
        if hasattr(self, 'matched_pairs_frame'):
            self.matched_pairs_frame.pack_forget()
        if hasattr(self, 'organ_donation_frame'):
            self.organ_donation_frame.pack_forget()

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()