import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import sqlite3
import mysql.connector
from datetime import datetime, timedelta
import calendar
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Add email configuration
SENDER_EMAIL = "transplantcare1234@gmail.com"
APP_PASSWORD = "rafckrpsrsuooqvk"

class BloodCampScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation Camp Schedule")
        self.root.geometry("1200x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize databases
        self.conn = sqlite3.connect(':memory:')  # Using in-memory database for camps data
        self.mysql_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Y@sh8105",
            database="transplant"
        )
        
        # Create MySQL table if it doesn't exist-*
        self.setup_mysql_database()
        
        self.create_sample_data()
        self.setup_ui()
    
    def setup_mysql_database(self):
        cursor = self.mysql_conn.cursor()
        
        # Create blood_donors table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_donors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            camp_id VARCHAR(20),
            full_name VARCHAR(100),
            age INT,
            blood_group VARCHAR(5),
            mobile VARCHAR(15),
            email VARCHAR(100),
            address TEXT,
            registration_date DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.mysql_conn.commit()
        cursor.close()
    
    def create_sample_data(self):
        # Create tables and insert sample data
        cursor = self.conn.cursor()
        
        # Create states table
        cursor.execute('''
        CREATE TABLE states (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        ''')
        
        # Create districts table
        cursor.execute('''
        CREATE TABLE districts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            state_id INTEGER,
            FOREIGN KEY (state_id) REFERENCES states(id)
        )
        ''')
        
        # Create camps table
        cursor.execute('''
        CREATE TABLE camps (
            id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT,
            state_id INTEGER,
            district_id INTEGER,
            contact TEXT,
            conducted_by TEXT,
            organized_by TEXT,
            date TEXT,
            time TEXT,
            FOREIGN KEY (state_id) REFERENCES states(id),
            FOREIGN KEY (district_id) REFERENCES districts(id)
        )
        ''')
        
        # Insert all Indian states
        states = [
            (1, "Andhra Pradesh"), (2, "Arunachal Pradesh"), (3, "Assam"), (4, "Bihar"),
            (5, "Chhattisgarh"), (6, "Delhi"), (7, "Goa"), (8, "Gujarat"),
            (9, "Haryana"), (10, "Himachal Pradesh"), (11, "Jammu and Kashmir"),
            (12, "Jharkhand"), (13, "Karnataka"), (14, "Kerala"), (15, "Ladakh"),
            (16, "Lakshadweep"), (17, "Madhya Pradesh"), (18, "Maharashtra"),
            (19, "Manipur"), (20, "Meghalaya"), (21, "Mizoram"), (22, "Nagaland"),
            (23, "Odisha"), (24, "Puducherry"), (25, "Punjab"), (26, "Rajasthan"),
            (27, "Sikkim"), (28, "Tamil Nadu"), (29, "Telangana"), (30, "Tripura"),
            (31, "Uttar Pradesh"), (32, "Uttarakhand"), (33, "West Bengal")
        ]
        cursor.executemany("INSERT INTO states VALUES (?, ?)", states)
        
        # Insert districts for each state
        districts = [
            # Andhra Pradesh
            (1, "Visakhapatnam", 1), (2, "Vijayawada", 1), (3, "Guntur", 1),
            (4, "Nellore", 1), (5, "Kurnool", 1),
            # Arunachal Pradesh
            (6, "Itanagar", 2), (7, "Tawang", 2), (8, "Pasighat", 2),
            (9, "Naharlagun", 2), (10, "Bomdila", 2),
            # Assam
            (11, "Guwahati", 3), (12, "Silchar", 3), (13, "Dibrugarh", 3),
            (14, "Jorhat", 3), (15, "Nagaon", 3),
            # Bihar
            (16, "Patna", 4), (17, "Gaya", 4), (18, "Muzaffarpur", 4),
            (19, "Bhagalpur", 4), (20, "Darbhanga", 4),
            # Chhattisgarh
            (21, "Raipur", 5), (22, "Bilaspur", 5), (23, "Bhilai", 5),
            (24, "Korba", 5), (25, "Raigarh", 5),
            # Delhi
            (26, "North Delhi", 6), (27, "South Delhi", 6), (28, "East Delhi", 6),
            (29, "West Delhi", 6), (30, "Central Delhi", 6),
            # Goa
            (31, "Panaji", 7), (32, "Margao", 7), (33, "Vasco da Gama", 7),
            (34, "Ponda", 7), (35, "Bicholim", 7),
            # Gujarat
            (36, "Ahmedabad", 8), (37, "Surat", 8), (38, "Vadodara", 8),
            (39, "Rajkot", 8), (40, "Bhavnagar", 8),
            # Haryana
            (41, "Gurugram", 9), (42, "Faridabad", 9), (43, "Chandigarh", 9),
            (44, "Hisar", 9), (45, "Rohtak", 9),
            # Himachal Pradesh
            (46, "Shimla", 10), (47, "Manali", 10), (48, "Dharamshala", 10),
            (49, "Kullu", 10), (50, "Dalhousie", 10),
            # Jammu and Kashmir
            (51, "Srinagar", 11), (52, "Jammu", 11), (53, "Baramulla", 11),
            (54, "Anantnag", 11), (55, "Pulwama", 11),
            # Jharkhand
            (56, "Ranchi", 12), (57, "Jamshedpur", 12), (58, "Dhanbad", 12),
            (59, "Bokaro", 12), (60, "Deoghar", 12),
            # Karnataka
            (61, "Bangalore", 13), (62, "Mysore", 13), (63, "Hubli", 13),
            (64, "Mangalore", 13), (65, "Belgaum", 13),
            # Kerala
            (66, "Thiruvananthapuram", 14), (67, "Kochi", 14), (68, "Kozhikode", 14),
            (69, "Thrissur", 14), (70, "Kollam", 14),
            # Ladakh
            (71, "Leh", 15), (72, "Kargil", 15), (73, "Nubra", 15),
            (74, "Zanskar", 15), (75, "Changthang", 15),
            # Lakshadweep
            (76, "Kavaratti", 16), (77, "Agatti", 16), (78, "Minicoy", 16),
            (79, "Andrott", 16), (80, "Kadmat", 16),
            # Madhya Pradesh
            (81, "Bhopal", 17), (82, "Indore", 17), (83, "Jabalpur", 17),
            (84, "Gwalior", 17), (85, "Ujjain", 17),
            # Maharashtra
            (86, "Mumbai", 18), (87, "Pune", 18), (88, "Nagpur", 18),
            (89, "Thane", 18), (90, "Nashik", 18),
            # Manipur
            (91, "Imphal", 19), (92, "Thoubal", 19), (93, "Bishnupur", 19),
            (94, "Churachandpur", 19), (95, "Senapati", 19),
            # Meghalaya
            (96, "Shillong", 20), (97, "Tura", 20), (98, "Jowai", 20),
            (99, "Nongstoin", 20), (100, "Williamnagar", 20),
            # Mizoram
            (101, "Aizawl", 21), (102, "Lunglei", 21), (103, "Champhai", 21),
            (104, "Saiha", 21), (105, "Kolasib", 21),
            # Nagaland
            (106, "Kohima", 22), (107, "Dimapur", 22), (108, "Mokokchung", 22),
            (109, "Tuensang", 22), (110, "Wokha", 22),
            # Odisha
            (111, "Bhubaneswar", 23), (112, "Cuttack", 23), (113, "Puri", 23),
            (114, "Rourkela", 23), (115, "Sambalpur", 23),
            # Puducherry
            (116, "Puducherry", 24), (117, "Karaikal", 24), (118, "Mahe", 24),
            (119, "Yanam", 24), (120, "Ozhukarai", 24),
            # Punjab
            (121, "Chandigarh", 25), (122, "Ludhiana", 25), (123, "Amritsar", 25),
            (124, "Jalandhar", 25), (125, "Patiala", 25),
            # Rajasthan
            (126, "Jaipur", 26), (127, "Jodhpur", 26), (128, "Udaipur", 26),
            (129, "Kota", 26), (130, "Bikaner", 26),
            # Sikkim
            (131, "Gangtok", 27), (132, "Namchi", 27), (133, "Mangan", 27),
            (134, "Gyalshing", 27), (135, "Soreng", 27),
            # Tamil Nadu
            (136, "Chennai", 28), (137, "Coimbatore", 28), (138, "Madurai", 28),
            (139, "Salem", 28), (140, "Tiruchirappalli", 28),
            # Telangana
            (141, "Hyderabad", 29), (142, "Warangal", 29), (143, "Nizamabad", 29),
            (144, "Karimnagar", 29), (145, "Khammam", 29),
            # Tripura
            (146, "Agartala", 30), (147, "Udaipur", 30), (148, "Dharmanagar", 30),
            (149, "Kailashahar", 30), (150, "Belonia", 30),
            # Uttar Pradesh
            (151, "Lucknow", 31), (152, "Kanpur", 31), (153, "Agra", 31),
            (154, "Varanasi", 31), (155, "Prayagraj", 31),
            # Uttarakhand
            (156, "Dehradun", 32), (157, "Haridwar", 32), (158, "Rishikesh", 32),
            (159, "Nainital", 32), (160, "Mussoorie", 32),
            # West Bengal
            (161, "Kolkata", 33), (162, "Howrah", 33), (163, "Durgapur", 33),
            (164, "Siliguri", 33), (165, "Asansol", 33)
        ]
        cursor.executemany("INSERT INTO districts VALUES (?, ?, ?)", districts)
        
        # Generate fixed dates for camps
        from datetime import datetime, timedelta
        
        def get_camp_dates(district_id, camp_index):
            # Start from January 1st, 2025
            base_date = datetime(2025, 1, 1)
            
            # Calculate the day of the year (0-364)
            day_of_year = camp_index % 365
            
            # Add the day offset to base date
            camp_date = base_date + timedelta(days=day_of_year)
            
            return camp_date.strftime("%d-%m-%Y")

        def generate_camp_name():
            venues = [
                "Community Center", "Public School", "College", "Hospital", "Medical Center",
                "University Campus", "Corporate Park", "Tech Hub", "Sports Complex",
                "Municipal Hall", "Cultural Center", "Convention Center", "Youth Center",
                "City Hall", "Public Library", "Shopping Mall", "Business Center",
                "Educational Institute", "Research Center", "Wellness Center"
            ]
            
            prefixes = [
                "District", "City", "Regional", "Central", "Main", "Public", "State",
                "Community", "Municipal", "Local", "Government", "National", "Urban",
                "Metropolitan", "Civic", "Town", "Area", "Zonal", "Primary"
            ]
            
            organizations = [
                "Red Cross", "Lions Club", "Rotary Club", "Medical Association",
                "Health Foundation", "Welfare Society", "NGO Foundation", "Care Foundation",
                "Social Services", "Healthcare Initiative", "Charitable Trust",
                "Community Services", "Health Department", "Medical Society"
            ]
            
            venue = random.choice(venues)
            prefix = random.choice(prefixes)
            org = random.choice(organizations)
            
            name_formats = [
                f"{prefix} {venue} Blood Donation Drive",
                f"{org} Blood Donation Camp",
                f"{prefix} {org} Blood Drive",
                f"{venue} Blood Donation Initiative",
                f"{org} at {prefix} {venue}"
            ]
            
            return random.choice(name_formats)

        def generate_address(district_name):
            areas = [
                "Main Road", "Central Avenue", "Market Area", "City Center",
                "Business District", "Commercial Complex", "Industrial Area",
                "Residential Zone", "Downtown", "Uptown", "Old City", "New Town",
                "Civic Center", "Township", "Urban Estate", "Sector", "Colony",
                "Extension", "Nagar", "Plaza"
            ]
            
            landmarks = [
                "Near Bus Stand", "Opposite Railway Station", "Next to Park",
                "Behind Municipal Office", "Near Police Station", "Beside Hospital",
                "Near Metro Station", "Adjacent to Mall", "Near School",
                "Opposite Post Office", "Near Market", "Behind Library",
                "Near Stadium", "Next to Temple", "Near College"
            ]
            
            area = random.choice(areas)
            landmark = random.choice(landmarks)
            building_no = random.randint(1, 999)
            
            address_formats = [
                f"{building_no}, {area}, {landmark}, {district_name}",
                f"Plot No. {building_no}, {area}, {district_name}, {landmark}",
                f"{building_no}/{chr(random.randint(65, 70))}, {area}, {district_name}",
                f"{area} Complex, {landmark}, {district_name}",
                f"Building {building_no}, {area}, {district_name}, {landmark}"
            ]
            
            return random.choice(address_formats)

        def generate_contact_number():
            # Generate a realistic 10-digit mobile number
            prefixes = ['6', '7', '8', '9']  # Valid Indian mobile prefixes
            prefix = random.choice(prefixes)
            remaining = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            return f"+91 {prefix}{remaining}"

        def generate_organization_name():
            organizations = [
                "Red Cross Society",
                "Lions Club International",
                "Rotary Club",
                "Indian Medical Association",
                "National Blood Transfusion Council",
                "State Blood Transfusion Council",
                "District Blood Bank",
                "Apollo Hospitals",
                "Fortis Healthcare",
                "Max Healthcare",
                "Narayana Health",
                "Manipal Hospitals",
                "AIIMS",
                "PGIMER",
                "Christian Medical College",
                "KEM Hospital",
                "Safdarjung Hospital",
                "Ram Manohar Lohia Hospital",
                "All India Institute of Medical Sciences",
                "Sir Ganga Ram Hospital"
            ]
            return random.choice(organizations)

        def generate_organizer_name():
            organizers = [
                "Dr. Rajesh Kumar",
                "Dr. Priya Sharma",
                "Dr. Amit Patel",
                "Dr. Neha Gupta",
                "Dr. Sanjay Verma",
                "Dr. Anjali Singh",
                "Dr. Vikram Malhotra",
                "Dr. Meera Reddy",
                "Dr. Arun Kumar",
                "Dr. Deepika Sharma",
                "Dr. Rahul Verma",
                "Dr. Pooja Gupta",
                "Dr. Aditya Singh",
                "Dr. Ritu Malhotra",
                "Dr. Karan Reddy",
                "Dr. Shweta Kumar",
                "Dr. Manish Sharma",
                "Dr. Tanvi Patel",
                "Dr. Rohit Verma",
                "Dr. Ananya Singh"
            ]
            return random.choice(organizers)

        # Insert multiple camps for each district
        camp_id = 1
        camps = []
        
        # Generate camps for every day of 2025
        for day in range(365):  # 365 days in 2025
            for district_id in range(1, 95):  # 94 districts
                # Get district name for address generation
                cursor.execute("SELECT name FROM districts WHERE id = ?", (district_id,))
                district_name = cursor.fetchone()[0]
                
                # Randomly decide number of camps for this district (1-5)
                num_camps = random.randint(1, 5)
                
                # Generate camps for this district
                for camp_index in range(num_camps):
                    camp_date = get_camp_dates(district_id, day)
                    
                    # Fixed time slots for better organization
                    time_slots = [
                        "09:00-12:00",  # Morning slot
                        "13:00-16:00",  # Afternoon slot
                        "16:00-19:00"   # Evening slot
                    ]
                    # Randomly select a time slot
                    time = random.choice(time_slots)
                    
                    # Generate contact number
                    contact = generate_contact_number()
                    
                    # Get state_id for this district
                    cursor.execute("SELECT state_id FROM districts WHERE id = ?", (district_id,))
                    state_id = cursor.fetchone()[0]
                    
                    # Generate organization and organizer names
                    conducted_by = generate_organization_name()
                    organized_by = generate_organizer_name()
                    
                    # Create camp entry with random name and address
                    camp = (
                        camp_id,
                        generate_camp_name(),
                        generate_address(district_name),
                        state_id,
                        district_id,
                        contact,
                        conducted_by,
                        organized_by,
                        camp_date,
                        time
                    )
                    camps.append(camp)
                    camp_id += 1
        
        cursor.executemany("INSERT INTO camps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", camps)
        
        self.conn.commit()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#c1272d", height=60)
        header_frame.pack(fill=tk.X)
        
        # Back to Home button
        back_button = tk.Button(
            header_frame,
            text="← Back to Home",
            font=("Arial", 12, "bold"),
            bg="#c1272d",
            fg="white",
            bd=0,
            cursor="hand2",
            activebackground="#a61f24",
            activeforeground="white",
            command=self.back_to_home
        )
        back_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        header_label = tk.Label(header_frame, text="Camp Schedule", font=("Arial", 20, "bold"), 
                               bg="#c1272d", fg="white", pady=10)
        header_label.pack()
        
        # Search panel
        search_frame = tk.Frame(self.root, bg="white", pady=20, padx=20)
        search_frame.pack(fill=tk.X)
        
        # Get states for dropdown
        states = self.get_states()
        
        # State dropdown
        state_label = tk.Label(search_frame, text="Select State:", bg="white")
        state_label.grid(row=0, column=0, padx=10)
        
        self.state_var = tk.StringVar()
        self.state_dropdown = ttk.Combobox(search_frame, textvariable=self.state_var, width=20)
        self.state_dropdown['values'] = states
        self.state_dropdown.grid(row=0, column=1, padx=10)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.on_state_selected)
        
        # District dropdown
        district_label = tk.Label(search_frame, text="Select District:", bg="white")
        district_label.grid(row=0, column=2, padx=10)
        
        self.district_var = tk.StringVar()
        self.district_dropdown = ttk.Combobox(search_frame, textvariable=self.district_var, width=20)
        self.district_dropdown.grid(row=0, column=3, padx=10)
        
        # Date entry with calendar button
        date_label = tk.Label(search_frame, text="Date:", bg="white")
        date_label.grid(row=0, column=4, padx=10)
        
        self.date_var = tk.StringVar()
        # Remove the default date setting
        # self.date_var.set(datetime.now().strftime("%d-%m-%Y"))
        
        # Create a frame for date entry and calendar button
        date_frame = tk.Frame(search_frame, bg="white")
        date_frame.grid(row=0, column=5, padx=10)
        
        date_entry = tk.Entry(date_frame, textvariable=self.date_var, width=15)
        date_entry.pack(side=tk.LEFT)
        
        # Calendar button
        calendar_btn = tk.Button(date_frame, text="📅", command=self.show_calendar)
        calendar_btn.pack(side=tk.LEFT, padx=5)
        
        # Search button
        search_button = tk.Button(search_frame, text="Search", bg="#c1272d", fg="white", 
                                 padx=15, command=self.search_camps)
        search_button.grid(row=0, column=6, padx=20)
        
        # Results panel
        self.results_frame = tk.Frame(self.root, bg="white", pady=10, padx=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for displaying camps
        self.tree = ttk.Treeview(self.results_frame, columns=("sl_no", "date", "camp_name", "address", 
                                                           "state", "district", "contact", "conducted_by", 
                                                           "organized_by", "register", "time"))
        
        # Define column headings
        self.tree.heading("sl_no", text="S.No.")
        self.tree.heading("date", text="Date")
        self.tree.heading("camp_name", text="Camp Name")
        self.tree.heading("address", text="Address")
        self.tree.heading("state", text="State")
        self.tree.heading("district", text="District")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("conducted_by", text="Conducted By")
        self.tree.heading("organized_by", text="Organized by")
        self.tree.heading("register", text="Register")
        self.tree.heading("time", text="Time")
        
        # Configure columns
        self.tree.column("sl_no", width=50)
        self.tree.column("date", width=100)
        self.tree.column("camp_name", width=150)
        self.tree.column("address", width=200)
        self.tree.column("state", width=100)
        self.tree.column("district", width=100)
        self.tree.column("contact", width=100)
        self.tree.column("conducted_by", width=150)
        self.tree.column("organized_by", width=150)
        self.tree.column("register", width=100)
        self.tree.column("time", width=100)
        
        # Remove default first column
        self.tree['show'] = 'headings'
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Showing Blood Banks as per the selection from the list")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add register button functionality
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
    
    def get_states(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM states ORDER BY name")
        return [row[0] for row in cursor.fetchall()]
    
    def get_districts(self, state):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.name FROM districts d
            JOIN states s ON d.state_id = s.id
            WHERE s.name = ?
            ORDER BY d.name
        """, (state,))
        return [row[0] for row in cursor.fetchall()]
    
    def on_state_selected(self, event):
        state = self.state_var.get()
        if state:
            districts = self.get_districts(state)
            self.district_dropdown['values'] = districts
            self.district_var.set("All District" if districts else "")
    
    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            # Check if register column (10th column)
            if column == "#10":  # Register column
                values = self.tree.item(item_id, 'values')
                if values:
                    # Pop up registration form
                    self.open_registration_form(values)
    
    def open_registration_form(self, camp_values):
        # Create a new window for registration
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Register as Voluntary Donor")
        reg_window.geometry("400x500")
        reg_window.configure(bg="white")
        
        # Store camp values for later use in registration
        self.selected_camp_details = camp_values
        
        # Camp details
        camp_frame = tk.Frame(reg_window, bg="white", pady=10)
        camp_frame.pack(fill=tk.X)
        
        tk.Label(camp_frame, text=f"Registration for: {camp_values[2]}", 
                font=("Arial", 14, "bold"), bg="white").pack()
        tk.Label(camp_frame, text=f"Date: {camp_values[1]} | Time: {camp_values[10]}", 
                bg="white").pack()
        tk.Label(camp_frame, text=f"Location: {camp_values[3]}", bg="white").pack()
        
        # Registration form
        form_frame = tk.Frame(reg_window, bg="white", pady=10)
        form_frame.pack(fill=tk.BOTH)
        
        fields = [
            ("Full Name:", "name"),
            ("Age:", "age"),
            ("Blood Group:", "blood_group"),
            ("Mobile Number:", "mobile"),
            ("Email:", "email"),
            ("Address:", "address")
        ]
        
        self.reg_vars = {}
        self.address_text = None  # Store reference to address Text widget
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text, bg="white", anchor="w").grid(
                row=i, column=0, padx=10, pady=5, sticky="w")
            
            if field_name == "address":
                self.reg_vars[field_name] = tk.StringVar()
                self.address_text = tk.Text(form_frame, height=3, width=30)
                self.address_text.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            else:
                self.reg_vars[field_name] = tk.StringVar()
                entry = tk.Entry(form_frame, textvariable=self.reg_vars[field_name], width=30)
                if field_name == "mobile":
                    # Add validation for mobile number
                    def validate_mobile(P):
                        if len(P) <= 10 and P.isdigit() or P == "":
                            return True
                        return False
                    vcmd = (self.root.register(validate_mobile), '%P')
                    entry.config(validate='key', validatecommand=vcmd)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        # Add blood group dropdown
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        blood_group_dropdown = ttk.Combobox(form_frame, textvariable=self.reg_vars["blood_group"], 
                                          values=blood_groups, width=27)
        blood_group_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Checkbox for terms
        self.terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(form_frame, text="I agree to donate blood voluntarily", 
                                   variable=self.terms_var, bg="white")
        terms_check.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)
        
        # Submit button
        submit_button = tk.Button(form_frame, text="Register", bg="#c1272d", fg="white", 
                               padx=15, command=lambda: self.submit_registration(camp_values[0]))
        submit_button.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=10)
    
    def submit_registration(self, camp_id):
        # Validate required fields
        if not all([self.reg_vars["name"].get(), self.reg_vars["age"].get(), 
                   self.reg_vars["blood_group"].get(), self.reg_vars["mobile"].get()]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # Validate age
        try:
            age = int(self.reg_vars["age"].get())
            if age < 18 or age > 65:
                messagebox.showerror("Error", "Age must be between 18 and 65 years")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age")
            return

        # Validate mobile number
        mobile = self.reg_vars["mobile"].get()
        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Error", "Please enter a valid 10-digit mobile number")
            return

        # Validate email format
        email = self.reg_vars["email"].get()
        if email and '@' not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        # Check terms agreement
        if not self.terms_var.get():
            messagebox.showerror("Error", "Please agree to donate blood voluntarily")
            return

        # Get the address from the Text widget
        address = self.address_text.get("1.0", tk.END).strip()
        
        # Insert donor data into MySQL database
        mysql_cursor = self.mysql_conn.cursor()
        try:
            mysql_cursor.execute('''
                INSERT INTO blood_donors 
                (camp_id, full_name, age, blood_group, mobile, email, address, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                str(camp_id),
                self.reg_vars["name"].get(),
                age,
                self.reg_vars["blood_group"].get(),
                mobile,
                email,
                address,
                datetime.now()
            ))
            self.mysql_conn.commit()
            
            # Send confirmation email if email is provided
            if email:
                try:
                    # Create email message
                    msg = MIMEMultipart()
                    msg["From"] = SENDER_EMAIL
                    msg["To"] = email
                    msg["Subject"] = f"Blood Donation Registration Confirmation - {self.selected_camp_details[2]}"
                    
                    # Email body with selected camp details
                    body = f"""Dear {self.reg_vars["name"].get()},

Thank you for registering as a voluntary blood donor. Your registration has been confirmed for the following blood donation camp:

Camp Details:
-------------
Camp Name: {self.selected_camp_details[2]}
Date: {self.selected_camp_details[1]}
Time: {self.selected_camp_details[10]}
Location: {self.selected_camp_details[3]}
State: {self.selected_camp_details[4]}
District: {self.selected_camp_details[5]}
Contact Number: {self.selected_camp_details[6]}
Conducted By: {self.selected_camp_details[7]}
Camp Organizer: {self.selected_camp_details[8]}

Your Registration Details:
-------------------------
Name: {self.reg_vars["name"].get()}
Age: {age}
Blood Group: {self.reg_vars["blood_group"].get()}
Mobile: {mobile}
Address: {address}

Important Instructions:
----------------------
1. Please arrive at the camp location 15 minutes before your scheduled time
2. Bring a valid government-issued photo ID proof
3. Get adequate rest the night before donation
4. Have a light meal before coming to the camp
5. Stay hydrated by drinking plenty of water
6. Wear comfortable clothing with sleeves that can be easily rolled up

For any queries or rescheduling, please contact the camp organizer at {self.selected_camp_details[6]}.

Thank you for your noble gesture! Your donation can save up to three lives.

Best regards,
Blood Donation Camp Team
{self.selected_camp_details[7]}"""
                    
                    msg.attach(MIMEText(body, "plain"))
                    
                    # Connect to SMTP server and send email
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.sendmail(SENDER_EMAIL, email, msg.as_string())
                    server.quit()
                    
                except Exception as e:
                    print(f"Failed to send email: {str(e)}")
                    # Don't show error to user as registration was successful
            
            messagebox.showinfo("Registration Successful", 
                             "You have successfully registered as a voluntary donor. Thank you!" +
                             ("\nA confirmation email has been sent to your email address." if email else ""))
                             
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to save registration: {str(e)}")
        finally:
            mysql_cursor.close()
    
    def search_camps(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        state = self.state_var.get()
        district = self.district_var.get()
        date = self.date_var.get()
        
        if not state:
            self.status_var.set("Please select a state")
            return
        
        # Validate date format
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in DD-MM-YYYY format")
            return
        
        # Build query based on selections
        query = """
            SELECT c.id, c.date, c.name, c.address, s.name, d.name, c.contact,
                   c.conducted_by, c.organized_by, c.time
            FROM camps c
            JOIN states s ON c.state_id = s.id
            JOIN districts d ON c.district_id = d.id
            WHERE s.name = ?
        """
        params = [state]
        
        if district and district != "All District":
            query += " AND d.name = ?"
            params.append(district)
        
        if date:
            query += " AND c.date = ?"
            params.append(date)
        
        query += " ORDER BY c.date, c.time"
        
        # Debug print
        print(f"Query: {query}")
        print(f"Params: {params}")
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Debug print
        print(f"Number of results: {len(results)}")
        
        # Update status
        if results:
            self.status_var.set(f"Showing {len(results)} blood donation camps")
        else:
            # Debug query to check available dates for the selected state/district
            debug_query = """
                SELECT DISTINCT c.date
                FROM camps c
                JOIN states s ON c.state_id = s.id
                JOIN districts d ON c.district_id = d.id
                WHERE s.name = ?
            """
            debug_params = [state]
            if district and district != "All District":
                debug_query += " AND d.name = ?"
                debug_params.append(district)
            debug_query += " ORDER BY c.date LIMIT 5"
            
            cursor.execute(debug_query, debug_params)
            available_dates = cursor.fetchall()
            if available_dates:
                self.status_var.set(f"No camps found for {date}. Available dates: {', '.join([d[0] for d in available_dates])}")
            else:
                self.status_var.set("No blood donation camps found for the selected criteria")
        
        # Populate treeview
        for i, row in enumerate(results):
            camp_id, date, name, address, state_name, district_name, contact, conducted_by, organized_by, time = row
            
            # Register button will be implemented as text for now
            register = "Register"
            
            self.tree.insert("", tk.END, values=(i+1, date, name, address, state_name,
                                              district_name, contact, conducted_by,
                                              organized_by, register, time))
    
    def show_calendar(self):
        # Create a new window for the calendar
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Select Date")
        cal_window.geometry("300x400")
        cal_window.configure(bg="white")
        
        # Get current date
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        
        # Create month and year selection
        control_frame = tk.Frame(cal_window, bg="white")
        control_frame.pack(pady=10)
        
        # Month selection
        month_var = tk.StringVar(value=calendar.month_name[month])
        month_menu = ttk.Combobox(control_frame, textvariable=month_var, 
                                values=list(calendar.month_name)[1:], width=10)
        month_menu.pack(side=tk.LEFT, padx=5)
        
        # Year selection
        year_var = tk.StringVar(value=str(year))
        year_spinbox = ttk.Spinbox(control_frame, from_=year, to=year+1, 
                                 textvariable=year_var, width=5)
        year_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Calendar frame
        cal_frame = tk.Frame(cal_window, bg="white")
        cal_frame.pack(pady=10)
        
        # Weekday headers
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            tk.Label(cal_frame, text=day, width=4, bg="white").grid(row=0, column=i)
        
        # Function to update calendar
        def update_calendar(*args):
            # Clear existing calendar
            for widget in cal_frame.grid_slaves():
                if int(widget.grid_info()["row"]) > 0:
                    widget.destroy()
            
            # Get selected month and year
            selected_month = list(calendar.month_name).index(month_var.get())
            selected_year = int(year_var.get())
            
            # Get calendar data
            cal_data = calendar.monthcalendar(selected_year, selected_month)
            
            # Create calendar buttons
            for week_num, week in enumerate(cal_data, 1):
                for day_num, day in enumerate(week):
                    if day != 0:
                        btn = tk.Button(cal_frame, text=str(day), width=4, height=2,
                                      command=lambda d=day: select_date(d, selected_month, selected_year))
                        btn.grid(row=week_num, column=day_num)
        
        # Function to select date
        def select_date(day, month, year):
            selected_date = datetime(year, month, day)
            self.date_var.set(selected_date.strftime("%d-%m-%Y"))
            cal_window.destroy()
        
        # Bind update events
        month_var.trace('w', update_calendar)
        year_var.trace('w', update_calendar)
        
        # Initial calendar display
        update_calendar()
    
    def back_to_home(self):
        """Returns to the homepage."""
        self.root.destroy()
        import HomePage
        app = HomePage.HomePage()
        app.mainloop()
    
    def run(self):
        self.root.mainloop()

    def __del__(self):
        # Close database connections when the application is closed
        if hasattr(self, 'mysql_conn'):
            self.mysql_conn.close()
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = BloodCampScheduleApp(root)
    app.run()