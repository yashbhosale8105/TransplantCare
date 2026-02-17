import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import threading
import time
import matplotlib.dates as mdates


class OrganDonationAnalysis(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organ Donations Analysis")
        self.geometry("1280x720")
        self.configure(bg="white")

        # Initialize database connection
        self.conn = None
        self.cursor = None
        self.connect_to_database()

        # Add home button and refresh button
        self.add_buttons()
        
        # Initialize canvas and figure as class attributes
        self.canvas = None
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        
        # Create graphs
        self.create_graphs()
        
        # Start auto-refresh thread
        self.refresh_thread = threading.Thread(target=self.auto_refresh, daemon=True)
        self.refresh_thread.start()

    def connect_to_database(self):
        """Establishes connection to the database."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Y@sh8105",
                database="Transplant"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to database: {e}")

    def add_buttons(self):
        """Adds home and refresh buttons to the top right corner."""
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        # Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2196F3",  # Blue color
            padx=15,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED,
            command=self.refresh_graphs
        )
        refresh_button.pack(side=tk.RIGHT, padx=5)

        # Home button
        home_button = tk.Button(
            button_frame,
            text="Home",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#4CAF50",  # Green color
            padx=15,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED,
            command=self.go_to_home
        )
        home_button.pack(side=tk.RIGHT)

    def get_donation_data(self):
        """Fetches donation data from the database."""
        try:
            # Get organ donation counts
            self.cursor.execute("""
                SELECT organ, COUNT(*) as count 
                FROM approved_donor 
                WHERE status = 'matched'
                GROUP BY organ
            """)
            organ_counts = {row['organ']: row['count'] for row in self.cursor.fetchall()}

            # Get donation dates for scatter plot
            self.cursor.execute("""
                SELECT match_date, organ
                FROM matches
                ORDER BY match_date
            """)
            donation_dates = self.cursor.fetchall()

            # Prepare data for graphs
            organs = ["Kidney", "Heart", "Liver", "Lung", "Pancreas", "Cornea"]
            values = [organ_counts.get(organ, 0) for organ in organs]

            # Prepare scatter plot data
            dates = [row['match_date'] for row in donation_dates]
            organ_types = [row['organ'] for row in donation_dates]
            y_values = [organs.index(organ) for organ in organ_types]

            return organs, values, dates, y_values

        except Error as e:
            print(f"Error fetching data: {e}")
            return [], [], [], []

    def create_graphs(self):
        """Creates and displays pie chart and scatter plot in Tkinter."""
        # Clear existing widgets if this is the first creation
        if self.canvas is None:
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame) and widget != self.winfo_children()[0]:  # Keep button frame
                    widget.destroy()

        # Get real data from database
        organs, values, dates, y_values = self.get_donation_data()

        # Create figure with two subplots if this is the first creation
        if self.fig is None:
            self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 6))
            self.fig.subplots_adjust(wspace=0.4)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()

        # Pie Chart - Organ donations distribution
        if sum(values) > 0:  # Only create pie chart if there's data
            self.ax1.pie(values, labels=organs, autopct='%1.1f%%', 
                        colors=['red', 'blue', 'green', 'orange', 'purple', 'cyan'],
                        startangle=90)
            self.ax1.set_title("Organ Donations Distribution")
        else:
            self.ax1.text(0.5, 0.5, "No donations yet", ha='center', va='center')
            self.ax1.set_title("Organ Donations Distribution")

        # Scatter Plot - Donation timeline
        if dates and y_values:
            self.ax2.scatter(dates, y_values, c='blue', alpha=0.6)
            self.ax2.set_xlabel("Date")
            self.ax2.set_ylabel("Organ Type")
            self.ax2.set_title("Donation Timeline")
            self.ax2.set_yticks(range(len(organs)))
            self.ax2.set_yticklabels(organs)
            self.ax2.grid(True, alpha=0.3)
            
            # Format x-axis to show date as dd/mm/yy
            self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            plt.setp(self.ax2.get_xticklabels(), rotation=45, ha='right')

        # Optimize layout
        self.fig.tight_layout()
        
        # Update canvas
        self.canvas.draw()

    def refresh_graphs(self):
        """Refreshes the graphs with latest data."""
        self.create_graphs()

    def auto_refresh(self):
        """Automatically refreshes the graphs every 30 seconds."""
        while True:
            time.sleep(30)  # Wait for 30 seconds
            self.refresh_graphs()

    def go_to_home(self):
        """Redirects to the home page."""
        self.destroy()
        import HomePage
        app = HomePage.HomePage()
        app.mainloop()

    def __del__(self):
        """Cleanup database connection when window is closed."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()


if __name__ == "__main__":
    app = OrganDonationAnalysis()
    app.mainloop()