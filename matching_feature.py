from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from PIL import Image, ImageTk
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class OrganDonorSystem:
    # Predefined sender credentials
    SENDER_EMAIL = "transplantcare1234@gmail.com"
    APP_PASSWORD = "rafckrpsrsuooqvk"
    
    def __init__(self):
        self.setup_database()
        self.setup_gui()

    def load_background(self):
        """Loads and sets the background image."""
        screen_width = 1280
        screen_height = 720
        image_path = r"C:\Users\ASUS\Downloads\bg for yash 2].png"

        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            messagebox.showerror("Error", "Background image file not found!")
            self.root.destroy()
            exit()

    def setup_database(self):
        """Ensure required tables exist."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    donor_name VARCHAR(255) NOT NULL,
                    recipient_name VARCHAR(255) NOT NULL,
                    organ VARCHAR(100) NOT NULL,
                    blood_type VARCHAR(10) NOT NULL,
                    match_date DATETIME NOT NULL
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
        except Error as err:
            messagebox.showerror("Database Error", f"Error setting up database: {err}")

    def back_to_db(self):
        """Navigate back to the admin dashboard."""
        self.root.destroy()
        import admin_dashboard
        admin_dashboard.AdminDashboard().mainloop()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Organ Transplant Matching System")
        self.root.geometry("1280x720")

        # Load background first
        self.load_background()

        self.donors = []
        self.recipients = []
        self.matches = []

        # Create a frame for content with transparent background
        content_frame = tk.Frame(self.root, bg='white')
        content_frame.pack(pady=20)

        # Title
        tk.Label(content_frame, text="Organ Transplant Matching System", 
                font=("Arial", 20, "bold"), bg='white').pack(pady=10)

        # Dashboard Button
        tk.Button(content_frame, text="Dashboard", command=self.back_to_db,
                  bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), 
                  width=15, height=2).pack(pady=10)

        # Create frames for lists
        lists_frame = tk.Frame(content_frame, bg='white')
        lists_frame.pack(pady=10)

        # Donor List Frame
        donor_frame = tk.Frame(lists_frame, bg='white')
        donor_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(donor_frame, text="Available Donors", 
                font=("Arial", 14), bg='white').pack()
        self.donor_listbox = tk.Listbox(donor_frame, height=15, width=50, 
                                      exportselection=False, font=("Arial", 12))
        self.donor_listbox.pack()

        # Recipient List Frame
        recipient_frame = tk.Frame(lists_frame, bg='white')
        recipient_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(recipient_frame, text="Available Recipients", 
                font=("Arial", 14), bg='white').pack()
        self.recipient_listbox = tk.Listbox(recipient_frame, height=15, width=50, 
                                          exportselection=False, font=("Arial", 12))
        self.recipient_listbox.pack()

        # Find Match Button (renamed from Match Selected)
        tk.Button(content_frame, text="Find a Match", command=self.find_match,
                  bg="green", fg="white", font=("Arial", 14), 
                  width=20).pack(pady=10)

        # Matched Pairs List
        tk.Label(content_frame, text="Matched Pairs", 
                font=("Arial", 14), bg='white').pack()
        self.match_listbox = tk.Listbox(content_frame, height=8, width=110, 
                                      font=("Arial", 12))
        self.match_listbox.pack(pady=10)

        # Automatically update listboxes on load
        self.update_listboxes()

    def fetch_donors_from_db(self):
        """Fetch donors from the 'approved_donor' table where status is 'available'."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT name, blood_type, organ, City, State 
                FROM approved_donor 
                WHERE status='available' 
                AND name NOT IN (SELECT donor_name FROM matches)
                ORDER BY name
            """)
            self.donors = cursor.fetchall()
            print("Fetched donors:", self.donors)  # Debug print
            cursor.close()
            conn.close()
        except Error as err:
            messagebox.showerror("Database Error", f"Error fetching donors: {err}")
            print(f"Database Error: {err}")  # Debug print

    def fetch_recipients_from_db(self):
        """Fetch all unmatched patients from the patients table sorted by urgency."""
        try:
            print("Attempting to connect to database...")  # Debug print
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor(dictionary=True)
            print("Executing query to fetch unmatched patients...")  # Debug print
            # Modified query to exclude matched recipients and check status
            cursor.execute("""
                SELECT PatientName, PatientBloodGrp, NeededOrgan, Urgency, Email, City, State 
                FROM patients 
                WHERE (status IS NULL OR status != 'matched')
                AND PatientName NOT IN (SELECT recipient_name FROM matches)
                ORDER BY CAST(Urgency AS DECIMAL(10,2)) DESC, PatientName
            """)
            self.recipients = cursor.fetchall()
            print(f"Number of unmatched patients fetched: {len(self.recipients)}")  # Debug print
            print(f"Unmatched patients data: {self.recipients}")  # Debug print
            cursor.close()
            conn.close()
        except Error as err:
            print(f"Database Error: {err}")  # Debug print
            messagebox.showerror("Database Error", f"Error fetching patients: {err}")

    def fetch_matches_from_db(self):
        """Fetch matched pairs."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT donor_name, recipient_name, organ, blood_type, match_date FROM matches ORDER BY match_date DESC")
            self.matches = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as err:
            messagebox.showerror("Database Error", f"Error fetching matches: {err}")

    def update_listboxes(self):
        """Refresh donor, recipient, and matches lists automatically."""
        self.fetch_donors_from_db()
        self.fetch_recipients_from_db()
        self.fetch_matches_from_db()

        self.donor_listbox.delete(0, tk.END)
        self.recipient_listbox.delete(0, tk.END)
        self.match_listbox.delete(0, tk.END)

        for donor in self.donors:
            print("Processing donor:", donor)  # Debug print
            donor_info = f"{donor['name']} - {donor['blood_type']} - {donor['organ']}"
            if donor.get('City') and donor.get('State'):
                donor_info += f" ({donor['City']}, {donor['State']})"
            print("Formatted donor info:", donor_info)  # Debug print
            self.donor_listbox.insert(tk.END, donor_info)

        for recipient in self.recipients:
            recipient_info = f"{recipient['PatientName']} - {recipient['PatientBloodGrp']} - {recipient['NeededOrgan']}"
            if recipient.get('Urgency'):
                recipient_info += f" - {recipient['Urgency']}"
            if recipient.get('City') and recipient.get('State'):
                recipient_info += f" ({recipient['City']}, {recipient['State']})"
            self.recipient_listbox.insert(tk.END, recipient_info)

        for match in self.matches:
            match_date = match['match_date'].strftime("%Y-%m-%d %H:%M") if isinstance(match['match_date'], datetime) else str(match['match_date'])
            self.match_listbox.insert(tk.END, f"{match['donor_name']} ➡ {match['recipient_name']} - {match['organ']} - {match_date}")

    def send_notification_email(self, receiver_email, subject, message):
        """Send an email notification."""
        try:
            # Set up the email message
            msg = MIMEMultipart()
            msg["From"] = self.SENDER_EMAIL
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            # Connect to SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.SENDER_EMAIL, self.APP_PASSWORD)

            # Send email
            server.sendmail(self.SENDER_EMAIL, receiver_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Email Error: Failed to send email to {receiver_email}: {e}")
            return False

    def get_donor_email(self, donor_name):
        """Fetch donor email from database."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor(dictionary=True, buffered=True)  # Use buffered cursor
            
            # Get email from donors table
            cursor.execute("SELECT email FROM donors WHERE name = %s", (donor_name,))
            result = cursor.fetchone()
            
            if result and 'email' in result:
                print(f"Found email for donor {donor_name}: {result['email']}")
                return result['email']
            
            print(f"No email found for donor {donor_name}")
            return None
                
        except Error as err:
            print(f"Database Error: Error fetching donor email: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_recipient_email(self, recipient_name):
        """Fetch recipient email from database."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT Email FROM patients WHERE PatientName = %s", (recipient_name,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result.get('Email') if result else None
        except Error as err:
            print(f"Database Error: Error fetching recipient email: {err}")
            return None

    def approve_match(self, donor, recipient, match_dialog):
        """Handle the approval of a match."""
        # Create the match in database
        if self.add_match_to_database(donor, recipient):
            # Send email notifications
            donor_email = self.get_donor_email(donor['name'])
            recipient_email = recipient.get('Email')

            emails_sent = True

            # Send email to donor
            if donor_email:
                donor_subject = "Organ Donation Match Found"
                donor_message = f"""Dear {donor['name']},

We are pleased to inform you that a match has been found for your {donor['organ']} donation.

Match Details:
- Organ: {donor['organ']}
- Blood Type: {donor['blood_type']}
- Status: Successfully Matched

Our medical team will contact you shortly to discuss the next steps in the donation process. Please ensure your contact information is up to date.

Thank you for your generosity in helping save lives.

Best regards,
TransplantCare Team"""
                if not self.send_notification_email(donor_email, donor_subject, donor_message):
                    emails_sent = False
                    print(f"Failed to send email to donor: {donor['name']} at {donor_email}")

            # Send email to recipient
            if recipient_email:
                recipient_subject = "Organ Transplant Match Found"
                recipient_message = f"""Dear {recipient['PatientName']},

We have great news! A compatible donor has been found for your {recipient['NeededOrgan']} transplant.

Match Details:
- Organ: {recipient['NeededOrgan']}
- Blood Type: {recipient['PatientBloodGrp']}
- Status: Successfully Matched

Our transplant team will contact you soon to discuss the next steps and schedule your pre-transplant evaluation.

Please ensure you are available and can be reached at your registered contact information.

Best regards,
TransplantCare Team"""
                if not self.send_notification_email(recipient_email, recipient_subject, recipient_message):
                    emails_sent = False
                    print(f"Failed to send email to recipient: {recipient['PatientName']} at {recipient_email}")

            # Show appropriate message based on email sending status
            if emails_sent:
                messagebox.showinfo("Success", "Match approved and notifications sent successfully!")
            else:
                messagebox.showwarning("Partial Success", "Match approved but there were issues sending some notifications.")

            # Refresh the lists
            self.update_listboxes()
        else:
            messagebox.showerror("Error", "Failed to create match in database.")
        
        match_dialog.destroy()

    def deny_match(self, match_dialog):
        """Handle the denial of a match."""
        messagebox.showinfo("Match Denied", "Match has been denied.")
        match_dialog.destroy()

    def find_match(self):
        """Find a compatible donor for the selected recipient."""
        recipient_idx = self.recipient_listbox.curselection()

        if not recipient_idx:
            messagebox.showerror("Selection Error", "Please select a recipient first!")
            return

        recipient = self.recipients[recipient_idx[0]]
        
        # Find compatible donors, first prioritizing same city
        city_matches = []
        state_matches = []
        
        for donor in self.donors:
            # Check basic compatibility (blood type and organ)
            if (donor['blood_type'] == recipient['PatientBloodGrp'] and 
                donor['organ'] == recipient['NeededOrgan']):
                
                # First priority: Same city match
                if donor['City'] == recipient['City'] and donor['State'] == recipient['State']:
                    city_matches.append(donor)
                # Second priority: Same state match
                elif donor['State'] == recipient['State']:
                    state_matches.append(donor)

        # Use city matches if available, otherwise use state matches
        compatible_donors = city_matches if city_matches else state_matches

        if not compatible_donors:
            messagebox.showinfo("No Match", "No compatible donors found in the same city or state for the selected recipient.")
            return

        # Create match dialog
        match_dialog = tk.Toplevel(self.root)
        match_dialog.title("Match Found")
        match_dialog.geometry("400x500")
        match_dialog.transient(self.root)
        match_dialog.grab_set()
        match_dialog.configure(bg='white')

        # Main content frame
        main_frame = tk.Frame(match_dialog, bg='white')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # Display match details
        tk.Label(main_frame, text="Match Found!", font=("Arial", 16, "bold"), bg='white').pack(pady=10)
        
        # Recipient details
        recipient_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=1)
        recipient_frame.pack(pady=10, padx=10, fill='x')
        tk.Label(recipient_frame, text="Recipient:", font=("Arial", 12, "bold"), bg='white').pack(pady=5)
        tk.Label(recipient_frame, text=f"Name: {recipient['PatientName']}", bg='white').pack()
        tk.Label(recipient_frame, text=f"Blood Type: {recipient['PatientBloodGrp']}", bg='white').pack()
        tk.Label(recipient_frame, text=f"Organ Needed: {recipient['NeededOrgan']}", bg='white').pack()
        tk.Label(recipient_frame, text=f"Location: {recipient['City']}, {recipient['State']}", bg='white').pack(pady=5)

        # Donor details (show first compatible donor)
        donor = compatible_donors[0]
        donor_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=1)
        donor_frame.pack(pady=10, padx=10, fill='x')
        tk.Label(donor_frame, text="Compatible Donor:", font=("Arial", 12, "bold"), bg='white').pack(pady=5)
        tk.Label(donor_frame, text=f"Name: {donor['name']}", bg='white').pack()
        tk.Label(donor_frame, text=f"Blood Type: {donor['blood_type']}", bg='white').pack()
        tk.Label(donor_frame, text=f"Organ: {donor['organ']}", bg='white').pack()
        tk.Label(donor_frame, text=f"Location: {donor['City']}, {donor['State']}", bg='white').pack(pady=5)

        # Add match type label
        match_type = "Same City Match" if donor in city_matches else "Same State Match"
        match_type_label = tk.Label(
            main_frame,
            text=match_type,
            font=("Arial", 12, "bold"),
            bg='#e8f5e9' if donor in city_matches else '#fff3e0',
            fg='#2e7d32' if donor in city_matches else '#ef6c00',
            pady=5
        )
        match_type_label.pack(pady=10)

        # Button frame at the bottom
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(side='bottom', pady=20)

        # Style the buttons
        approve_button = tk.Button(
            button_frame, 
            text="Approve Match", 
            command=lambda: self.approve_match(donor, recipient, match_dialog),
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 11, "bold"),
            width=15,
            height=2,
            relief='raised'
        )
        approve_button.pack(side=tk.LEFT, padx=10)

        deny_button = tk.Button(
            button_frame, 
            text="Deny Match", 
            command=lambda: self.deny_match(match_dialog),
            bg="#f44336", 
            fg="white", 
            font=("Arial", 11, "bold"),
            width=15,
            height=2,
            relief='raised'
        )
        deny_button.pack(side=tk.LEFT, padx=10)

        # Center the dialog
        match_dialog.update_idletasks()
        width = match_dialog.winfo_width()
        height = match_dialog.winfo_height()
        x = (match_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (match_dialog.winfo_screenheight() // 2) - (height // 2)
        match_dialog.geometry(f'{width}x{height}+{x}+{y}')

    def update_matches_listbox(self):
        """Update only the matches listbox."""
        self.fetch_matches_from_db()
        self.match_listbox.delete(0, tk.END)
        for match in self.matches:
            match_date = match['match_date'].strftime("%Y-%m-%d %H:%M") if isinstance(match['match_date'], datetime) else str(match['match_date'])
            self.match_listbox.insert(tk.END, f"{match['donor_name']} ➡ {match['recipient_name']} - {match['organ']} - {match_date}")

    def add_match_to_database(self, donor, recipient):
        """Add match and update donor-recipient status."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            cursor = conn.cursor()
            
            # First check if either donor or recipient is already matched
            cursor.execute("""
                SELECT COUNT(*) FROM matches 
                WHERE donor_name = %s OR recipient_name = %s
            """, (donor['name'], recipient['PatientName']))
            
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "This donor or recipient has already been matched!")
                cursor.close()
                conn.close()
                return False

            # If no existing match, proceed with creating the match
            cursor.execute("""
                INSERT INTO matches 
                (donor_name, recipient_name, organ, blood_type, match_date) 
                VALUES (%s, %s, %s, %s, %s)
            """, (donor['name'], recipient['PatientName'], donor['organ'], donor['blood_type'], datetime.now()))
            
            # Update donor status
            cursor.execute("""
                UPDATE approved_donor 
                SET status = 'matched' 
                WHERE name = %s
            """, (donor['name'],))
            
            # Update recipient status
            cursor.execute("""
                UPDATE patients 
                SET status = 'matched' 
                WHERE PatientName = %s
            """, (recipient['PatientName'],))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as err:
            print(f"Database Error in add_match_to_database: {err}")  # Debug print
            messagebox.showerror("Database Error", f"Error adding match: {err}")
            return False

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    system = OrganDonorSystem()
    system.run()