import smtplib
import tkinter as tk
from tkinter import messagebox, filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Predefined sender credentials (hidden from UI)
SENDER_EMAIL = "transplantcare1234@gmail.com"  # Replace with your email
APP_PASSWORD = "rafckrpsrsuooqvk"  # Replace with your App Password

# Global variable to store attachment path
attachment_path = None


def attach_file():
    """Function to attach a file."""
    global attachment_path
    file_path = filedialog.askopenfilename(title="Select a File",
                                           filetypes=[("All Files", "*.*")])
    if file_path:
        attachment_path = file_path
        attachment_label.config(text=f"Attached: {os.path.basename(file_path)}")


def send_email():
    """Function to send an email."""
    receiver_email = receiver_entry.get()
    subject = subject_entry.get()
    message = message_entry.get("1.0", tk.END).strip()  # Fix tk.END reference

    if not receiver_email or not subject or not message:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Attach file if selected
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)

        # Connect to SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        # Send email
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", "Email sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")


# Tkinter GUI Setup
root = tk.Tk()
root.title("Secure Email Sender with Attachment")

tk.Label(root, text="Receiver Email:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Label(root, text="Subject:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Label(root, text="Message:").grid(row=2, column=0, sticky="nw", padx=5, pady=5)

receiver_entry = tk.Entry(root, width=40)
subject_entry = tk.Entry(root, width=40)
message_entry = tk.Text(root, width=40, height=10)

receiver_entry.grid(row=0, column=1, padx=5, pady=5)
subject_entry.grid(row=1, column=1, padx=5, pady=5)
message_entry.grid(row=2, column=1, padx=5, pady=5)

attach_button = tk.Button(root, text="Attach File", command=attach_file)
attach_button.grid(row=3, column=1, sticky="w", padx=5, pady=5)

attachment_label = tk.Label(root, text="No file attached")
attachment_label.grid(row=4, column=1, sticky="w", padx=5, pady=5)

send_button = tk.Button(root, text="Send Email", command=send_email)
send_button.grid(row=5, column=1, sticky="w", padx=5, pady=5)

root.mainloop()