import tkinter as tk
from tkinter import messagebox, ttk
import random
import mysql.connector
import time


class SimonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simon Game")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Y@sh8105',
            'database': 'sbl'
        }

        # Current user
        self.current_user = None

        # Create frames for different pages
        self.frames = {}
        for F in (LoginPage, RegisterPage, ProfilePage, GamePage):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show login page initially
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_db_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            return None

    def login(self, username, password):
        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM users 
                WHERE username = %s AND password = %s
            """, (username, password))
            
            user = cursor.fetchone()
            
            if user:
                self.current_user = username
                # Update last login time
                cursor.execute("""
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP 
                    WHERE username = %s
                """, (username,))
                conn.commit()
                
                self.frames["ProfilePage"].update_profile()
                self.show_frame("ProfilePage")
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                return False

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")
            return False
        finally:
            conn.close()

    def register(self, username, password):
        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Registration Failed", "Username already exists")
                return False

            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """, (username, password))
            
            # Create high score entry
            cursor.execute("""
                INSERT INTO high_scores (user_id, high_score, games_played)
                SELECT id, 0, 0 FROM users WHERE username = %s
            """, (username,))
            
            conn.commit()
            messagebox.showinfo("Registration Successful", "Account created successfully!")
            return True

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Registration failed: {err}")
            return False
        finally:
            conn.close()

    def update_score(self, score):
        if not self.current_user:
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            
            # Get user_id
            cursor.execute("SELECT id FROM users WHERE username = %s", (self.current_user,))
            user_id = cursor.fetchone()[0]
            
            # Insert game session
            cursor.execute("""
                INSERT INTO game_sessions (user_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (user_id, score, score + 1))
            
            # Update high score if new score is higher
            cursor.execute("""
                UPDATE high_scores 
                SET high_score = GREATEST(high_score, %s),
                    games_played = games_played + 1
                WHERE user_id = %s
            """, (score, user_id))
            
            conn.commit()
            self.frames["ProfilePage"].update_profile()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update score: {err}")
        finally:
            conn.close()

    def get_user_stats(self):
        if not self.current_user:
            return None

        conn = self.get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT h.high_score, h.games_played, u.created_at, u.last_login 
                FROM users u
                JOIN high_scores h ON u.id = h.user_id
                WHERE u.username = %s
            """, (self.current_user,))
            
            return cursor.fetchone()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to get user stats: {err}")
            return None
        finally:
            conn.close()


class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1a1a2e")
        self.parent = parent
        
        # Create a gradient-like background effect
        self.bg_canvas = tk.Canvas(self, width=1280, height=720, bg="#1a1a2e", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Create decorative circles in the background
        for i in range(10):
            x = random.randint(0, 1280)
            y = random.randint(0, 720)
            size = random.randint(50, 200)
            color = random.choice(["#16213e", "#0f3460", "#1a1a2e"])
            self.bg_canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
        
        # Main content frame
        self.content_frame = tk.Frame(self, bg="#1a1a2e")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create decorative logo
        self.logo_frame = tk.Frame(self.content_frame, bg="#1a1a2e", bd=0)
        self.logo_frame.pack(pady=20)
        
        # Simon logo colors with more vibrant colors
        colors = ["#e94560", "#00ff9d", "#ffd700", "#4e54c8"]
        size = 60
        
        # Create 2x2 grid of colored squares for logo with rounded corners effect
        for i in range(2):
            for j in range(2):
                square = tk.Frame(self.logo_frame, width=size, height=size, bg=colors[i * 2 + j], bd=0)
                square.grid(row=i, column=j, padx=8, pady=8)
                
                # Create a rounded corner effect using a canvas
                corner_canvas = tk.Canvas(square, width=size, height=size, bg=colors[i * 2 + j], highlightthickness=0)
                corner_canvas.place(x=0, y=0)
                corner_canvas.create_oval(0, 0, 15, 15, fill=colors[i * 2 + j], outline="")
                corner_canvas.create_oval(size-15, 0, size, 15, fill=colors[i * 2 + j], outline="")
                corner_canvas.create_oval(0, size-15, 15, size, fill=colors[i * 2 + j], outline="")
                corner_canvas.create_oval(size-15, size-15, size, size, fill=colors[i * 2 + j], outline="")
        
        # Title with modern font and glow effect
        self.title_frame = tk.Frame(self.content_frame, bg="#1a1a2e")
        self.title_frame.pack(pady=10)
        
        self.title_label = tk.Label(self.title_frame, text="SIMON GAME", 
                                    font=("Arial", 36, "bold"), 
                                    bg="#1a1a2e", 
                                    fg="#ffffff")
        self.title_label.pack()
        
        # Subtitle
        self.subtitle_label = tk.Label(self.title_frame, text="Test Your Memory", 
                                      font=("Arial", 16), 
                                      bg="#1a1a2e", 
                                      fg="#aaaaaa")
        self.subtitle_label.pack(pady=5)
        
        # Login frame with glass-like effect
        self.login_frame = tk.Frame(self.content_frame, bg="#16213e", bd=0)
        self.login_frame.pack(pady=30, padx=50, fill="both")
        
        # Add a subtle border effect
        self.border_frame = tk.Frame(self.login_frame, bg="#e94560", bd=0)
        self.border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.inner_frame = tk.Frame(self.border_frame, bg="#16213e", bd=0)
        self.inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Login header
        self.login_header = tk.Label(self.inner_frame, text="LOGIN", 
                                    font=("Arial", 20, "bold"), 
                                    bg="#16213e", 
                                    fg="#ffffff")
        self.login_header.pack(pady=20)
        
        # Username with icon
        self.username_frame = tk.Frame(self.inner_frame, bg="#16213e")
        self.username_frame.pack(fill="x", padx=40, pady=10)
        
        self.username_label = tk.Label(self.username_frame, text="👤", 
                                      font=("Arial", 14), 
                                      bg="#16213e", 
                                      fg="#ffffff")
        self.username_label.pack(side="left", padx=5)
        
        self.username_entry = tk.Entry(self.username_frame, 
                                      font=("Arial", 14), 
                                      width=25, 
                                      bg="#0f3460", 
                                      fg="#ffffff", 
                                      insertbackground="#ffffff",
                                      relief="flat",
                                      bd=0)
        self.username_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", lambda e: self.on_entry_click(self.username_entry, "Username"))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.username_entry, "Username"))
        
        # Password with icon
        self.password_frame = tk.Frame(self.inner_frame, bg="#16213e")
        self.password_frame.pack(fill="x", padx=40, pady=10)
        
        self.password_label = tk.Label(self.password_frame, text="🔒", 
                                      font=("Arial", 14), 
                                      bg="#16213e", 
                                      fg="#ffffff")
        self.password_label.pack(side="left", padx=5)
        
        self.password_entry = tk.Entry(self.password_frame, 
                                      show="•", 
                                      font=("Arial", 14), 
                                      width=25, 
                                      bg="#0f3460", 
                                      fg="#ffffff", 
                                      insertbackground="#ffffff",
                                      relief="flat",
                                      bd=0)
        self.password_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", lambda e: self.on_entry_click(self.password_entry, "Password"))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.password_entry, "Password"))
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.inner_frame, bg="#16213e")
        self.buttons_frame.pack(pady=30)
        
        # Login button with hover effect
        self.login_button = tk.Button(self.buttons_frame, 
                                     text="Login", 
                                     font=("Arial", 14, "bold"), 
                                     bg="#e94560", 
                                     fg="white",
                                     command=self.login, 
                                     width=12, 
                                     relief="flat", 
                                     activebackground="#ff6b81",
                                     activeforeground="white",
                                     bd=0)
        self.login_button.grid(row=0, column=0, padx=10)
        self.login_button.bind("<Enter>", lambda e: self.on_hover(self.login_button, "#ff6b81"))
        self.login_button.bind("<Leave>", lambda e: self.on_leave(self.login_button, "#e94560"))
        
        # Register button with hover effect
        self.register_button = tk.Button(self.buttons_frame, 
                                        text="Register", 
                                        font=("Arial", 14, "bold"), 
                                        bg="#4e54c8",
                                        fg="white",
                                        command=lambda: parent.show_frame("RegisterPage"), 
                                        width=12, 
                                        relief="flat", 
                                        activebackground="#6c72cb",
                                        activeforeground="white",
                                        bd=0)
        self.register_button.grid(row=0, column=1, padx=10)
        self.register_button.bind("<Enter>", lambda e: self.on_hover(self.register_button, "#6c72cb"))
        self.register_button.bind("<Leave>", lambda e: self.on_leave(self.register_button, "#4e54c8"))
    
    def on_entry_click(self, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            if default_text == "Password":
                entry.config(show="•")
    
    def on_focus_out(self, entry, default_text):
        if entry.get() == "":
            entry.insert(0, default_text)
            if default_text == "Password":
                entry.config(show="")
    
    def on_hover(self, widget, color):
        widget.config(bg=color)
    
    def on_leave(self, widget, color):
        widget.config(bg=color)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "Username" or password == "Password" or not username or not password:
            messagebox.showerror("Login Failed", "Username and password are required")
            return
        
        self.parent.login(username, password)


class RegisterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2ecc71")
        self.parent = parent

        # Title
        self.title_label = tk.Label(self, text="CREATE ACCOUNT", font=("Arial", 24, "bold"), bg="#2ecc71", fg="white")
        self.title_label.pack(pady=30)

        # Register frame
        self.register_frame = tk.Frame(self, bg="white", bd=5, relief="ridge")
        self.register_frame.pack(pady=20, padx=50, fill="both")

        # Username
        self.username_label = tk.Label(self.register_frame, text="Username:", font=("Arial", 12), bg="white",
                                       fg="#333333")
        self.username_label.pack(anchor="w", padx=20, pady=(20, 0))

        self.username_entry = tk.Entry(self.register_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(padx=20, pady=(0, 10))

        # Password
        self.password_label = tk.Label(self.register_frame, text="Password:", font=("Arial", 12), bg="white",
                                       fg="#333333")
        self.password_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.password_entry = tk.Entry(self.register_frame, show="•", font=("Arial", 12), width=30)
        self.password_entry.pack(padx=20, pady=(0, 10))

        # Confirm Password
        self.confirm_password_label = tk.Label(self.register_frame, text="Confirm Password:", font=("Arial", 12),
                                               bg="white", fg="#333333")
        self.confirm_password_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.confirm_password_entry = tk.Entry(self.register_frame, show="•", font=("Arial", 12), width=30)
        self.confirm_password_entry.pack(padx=20, pady=(0, 20))

        # Buttons frame
        self.buttons_frame = tk.Frame(self.register_frame, bg="white")
        self.buttons_frame.pack(pady=15)

        # Register button
        self.register_button = tk.Button(self.buttons_frame, text="Register", font=("Arial", 12), bg="#2ecc71",
                                         fg="white",
                                         command=self.register, width=10, relief="flat", activebackground="#27ae60")
        self.register_button.grid(row=0, column=0, padx=10)

        # Back button
        self.back_button = tk.Button(self.buttons_frame, text="Back", font=("Arial", 12), bg="#e74c3c", fg="white",
                                     command=lambda: parent.show_frame("LoginPage"), width=10, relief="flat",
                                     activebackground="#c0392b")
        self.back_button.grid(row=0, column=1, padx=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Registration Failed", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Passwords do not match")
            return

        if self.parent.register(username, password):
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.parent.show_frame("LoginPage")


class ProfilePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1a1a2e")
        self.parent = parent

        # Create a gradient-like background effect with smaller canvas
        self.bg_canvas = tk.Canvas(self, width=800, height=600, bg="#1a1a2e", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Create fewer decorative circles in the background
        for i in range(6):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(30, 100)  # Smaller circles
            color = random.choice(["#16213e", "#0f3460", "#1a1a2e"])
            self.bg_canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")

        # Main content container
        self.content_frame = tk.Frame(self, bg="#1a1a2e")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title with smaller font
        self.title_frame = tk.Frame(self.content_frame, bg="#1a1a2e")
        self.title_frame.pack(pady=15)
        
        self.title_label = tk.Label(self.title_frame, 
                                  text="USER PROFILE", 
                                  font=("Helvetica", 36, "bold"), 
                                  bg="#1a1a2e", 
                                  fg="#ffffff")
        self.title_label.pack()

        # Profile frame with reduced padding
        self.profile_frame = tk.Frame(self.content_frame, bg="#16213e", bd=0)
        self.profile_frame.pack(pady=20, padx=30, fill="both")
        
        # Border effect
        self.border_frame = tk.Frame(self.profile_frame, bg="#e94560", bd=0)
        self.border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.inner_frame = tk.Frame(self.border_frame, bg="#16213e", bd=0)
        self.inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # Smaller avatar
        self.avatar_frame = tk.Frame(self.inner_frame, bg="#0f3460", width=100, height=100)
        self.avatar_frame.pack(pady=20)
        self.avatar_frame.pack_propagate(False)
        
        self.avatar_label = tk.Label(self.avatar_frame, text="👤", 
                                   font=("Arial", 48), 
                                   bg="#0f3460", 
                                   fg="#ffffff")
        self.avatar_label.place(relx=0.5, rely=0.5, anchor="center")

        # Username with smaller font
        self.username_label = tk.Label(self.inner_frame, 
                                    text="Username", 
                                    font=("Helvetica", 24, "bold"), 
                                    bg="#16213e",
                                    fg="#ffffff")
        self.username_label.pack(pady=(15, 20))

        # Stats frame with reduced padding
        self.stats_frame = tk.Frame(self.inner_frame, bg="#16213e")
        self.stats_frame.pack(pady=15, fill="both", expand=True)

        # Stats styling with smaller fonts
        stats_style = {
            "label_font": ("Helvetica", 16, "bold"),
            "value_font": ("Helvetica", 16),
            "label_color": "#e94560",
            "value_color": "#ffffff",
            "bg": "#16213e",
            "pady": 8,
            "padx": 20
        }

        # Stats labels and values with reduced size
        stats_data = [
            ("High Score:", "high_score"),
            ("Games Played:", "games_played"),
            ("Last Login:", "last_login"),
            ("Account Created:", "created")
        ]

        for i, (label_text, value_name) in enumerate(stats_data):
            label = tk.Label(self.stats_frame, 
                           text=label_text,
                           font=stats_style["label_font"],
                           bg=stats_style["bg"],
                           fg=stats_style["label_color"])
            label.grid(row=i, column=0, padx=stats_style["padx"], 
                      pady=stats_style["pady"], sticky="e")
            
            value = tk.Label(self.stats_frame,
                           text="0" if "score" in value_name or "played" in value_name else "N/A",
                           font=stats_style["value_font"],
                           bg=stats_style["bg"],
                           fg=stats_style["value_color"])
            value.grid(row=i, column=1, padx=stats_style["padx"],
                      pady=stats_style["pady"], sticky="w")
            
            setattr(self, f"{value_name}_label", label)
            setattr(self, f"{value_name}_value", value)

        # Buttons frame with reduced spacing
        self.buttons_frame = tk.Frame(self.inner_frame, bg="#16213e")
        self.buttons_frame.pack(pady=25)

        # Button style with smaller size
        button_style = {
            "font": ("Helvetica", 16, "bold"),
            "width": 12,
            "height": 1,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2"
        }

        # Play button
        self.play_button = tk.Button(self.buttons_frame, 
                                  text="Play Simon",
                                  bg="#00ff9d",
                                  fg="#16213e",
                                  activebackground="#00cc7d",
                                  activeforeground="#16213e",
                                  command=lambda: parent.show_frame("GamePage"),
                                  **button_style)
        self.play_button.grid(row=0, column=0, padx=15, pady=10)

        # Logout button
        self.logout_button = tk.Button(self.buttons_frame, 
                                    text="Logout",
                                    bg="#e94560",
                                    fg="white",
                                    activebackground="#d63851",
                                    activeforeground="white",
                                    command=self.logout,
                                    **button_style)
        self.logout_button.grid(row=0, column=1, padx=15, pady=10)

        # Add hover effects
        self.play_button.bind("<Enter>", lambda e: e.widget.config(bg="#00cc7d"))
        self.play_button.bind("<Leave>", lambda e: e.widget.config(bg="#00ff9d"))
        self.logout_button.bind("<Enter>", lambda e: e.widget.config(bg="#d63851"))
        self.logout_button.bind("<Leave>", lambda e: e.widget.config(bg="#e94560"))

    def update_profile(self):
        # Update profile page with current user data
        if not self.parent.current_user:
            return

        user_data = self.parent.get_user_stats()
        if user_data:
            self.username_label.config(text=self.parent.current_user)
            self.high_score_value.config(text=str(user_data["high_score"]))
            self.games_played_value.config(text=str(user_data["games_played"]))
            self.last_login_value.config(text=str(user_data["last_login"]))
            self.created_value.config(text=str(user_data["created_at"]))

    def logout(self):
        self.parent.current_user = None
        self.parent.show_frame("LoginPage")


class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#8e44ad")  # Rich purple background
        self.parent = parent

        # Game variables
        self.sequence = []
        self.player_sequence = []
        self.current_level = 0
        self.playing = False
        self.waiting_for_input = False
        self.flash_speed = 500  # Milliseconds

        # Create main container
        self.main_container = tk.Frame(self, bg="#8e44ad")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Game title with modern design
        self.title_frame = tk.Frame(self.main_container, bg="#8e44ad")
        self.title_frame.pack(pady=(0, 30))

        self.title_label = tk.Label(self.title_frame, 
                                  text="SIMON GAME", 
                                  font=("Helvetica", 48, "bold"), 
                                  bg="#8e44ad", 
                                  fg="white")
        self.title_label.pack()

        # Score and Level display with modern styling
        self.stats_frame = tk.Frame(self.main_container, bg="#8e44ad")
        self.stats_frame.pack(pady=(0, 30))

        # Score display with glass effect
        self.score_frame = tk.Frame(self.stats_frame, bg="#9b59b6", bd=0)
        self.score_frame.pack(side="left", padx=20)
        
        self.score_label = tk.Label(self.score_frame, 
                                  text="Score: 0", 
                                  font=("Helvetica", 24, "bold"), 
                                  bg="#9b59b6", 
                                  fg="white",
                                  padx=20,
                                  pady=10)
        self.score_label.pack()

        # Level display with glass effect
        self.level_frame = tk.Frame(self.stats_frame, bg="#9b59b6", bd=0)
        self.level_frame.pack(side="left", padx=20)
        
        self.level_label = tk.Label(self.level_frame, 
                                  text="Level: 1", 
                                  font=("Helvetica", 24, "bold"), 
                                  bg="#9b59b6", 
                                  fg="white",
                                  padx=20,
                                  pady=10)
        self.level_label.pack()

        # Game area frame with modern styling
        self.game_frame = tk.Frame(self.main_container, 
                                 bg="#8e44ad", 
                                 width=400, 
                                 height=400)
        self.game_frame.pack(pady=30)
        self.game_frame.pack_propagate(False)

        # Simon buttons with improved design
        self.colors = {
            "red": {"active": "#ff5252", "normal": "#e74c3c", "sound": 440},     # Bright red
            "green": {"active": "#2ecc71", "normal": "#27ae60", "sound": 554},   # Emerald green
            "blue": {"active": "#3498db", "normal": "#2980b9", "sound": 659},    # Ocean blue
            "yellow": {"active": "#f1c40f", "normal": "#f39c12", "sound": 880}   # Sunflower yellow
        }

        self.buttons = {}
        
        # Create colored buttons in a 2x2 grid with modern styling
        row, col = 0, 0
        for color_name, color_info in self.colors.items():
            button_frame = tk.Frame(self.game_frame, 
                                  bg="#8e44ad",
                                  padx=5,
                                  pady=5)
            button_frame.grid(row=row, column=col)
            
            button = tk.Button(button_frame, 
                             bg=color_info["normal"],
                             activebackground=color_info["active"],
                             width=8,
                             height=4,
                             bd=0,
                             relief="flat",
                             cursor="hand2")  # Hand cursor for better UX
            button.pack(padx=5, pady=5)

            # Add hover effect
            button.bind("<Enter>", lambda e, b=button, c=color_info["active"]: b.config(bg=c))
            button.bind("<Leave>", lambda e, b=button, c=color_info["normal"]: b.config(bg=c))
            
            # Bind button to player input function
            button.bind("<Button-1>", lambda event, c=color_name: self.player_input(c))

            self.buttons[color_name] = button

            # Update row and column for next button
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Control buttons frame with modern design
        self.controls_frame = tk.Frame(self.main_container, bg="#8e44ad")
        self.controls_frame.pack(pady=30)

        # Start button with modern styling
        self.start_button = tk.Button(self.controls_frame, 
                                    text="Start Game",
                                    font=("Helvetica", 16, "bold"),
                                    bg="#2ecc71",  # Green
                                    fg="white",
                                    command=self.start_game,
                                    width=12,
                                    relief="flat",
                                    bd=0,
                                    cursor="hand2",
                                    activebackground="#27ae60",
                                    activeforeground="white")
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Add hover effect to start button
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg="#27ae60"))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg="#2ecc71"))

        # Profile button with modern styling
        self.profile_button = tk.Button(self.controls_frame,
                                      text="Profile",
                                      font=("Helvetica", 16, "bold"),
                                      bg="#3498db",  # Blue
                                      fg="white",
                                      command=lambda: parent.show_frame("ProfilePage"),
                                      width=12,
                                      relief="flat",
                                      bd=0,
                                      cursor="hand2",
                                      activebackground="#2980b9",
                                      activeforeground="white")
        self.profile_button.grid(row=0, column=1, padx=10)
        
        # Add hover effect to profile button
        self.profile_button.bind("<Enter>", lambda e: self.profile_button.config(bg="#2980b9"))
        self.profile_button.bind("<Leave>", lambda e: self.profile_button.config(bg="#3498db"))

        # Status label with modern font
        self.status_label = tk.Label(self.main_container,
                                   text="Press Start to begin!",
                                   font=("Helvetica", 20),
                                   bg="#8e44ad",
                                   fg="white")
        self.status_label.pack(pady=20)

    def flash_button(self, color):
        # Enhanced flash effect
        button = self.buttons[color]
        button.config(bg=self.colors[color]["active"])
        
        # Add 3D effect during flash
        button.config(relief="raised")
        
        def reset_button():
            button.config(bg=self.colors[color]["normal"])
            button.config(relief="flat")
            
        self.after(self.flash_speed, reset_button)

    def start_game(self):
        if not self.parent.current_user:
            messagebox.showinfo("Login Required", "Please login to play the game.")
            self.parent.show_frame("LoginPage")
            return

        # Reset game variables
        self.sequence = []
        self.player_sequence = []
        self.current_level = 0
        self.playing = True
        self.waiting_for_input = False

        # Update UI with animation
        self.score_label.config(text="Score: 0")
        self.level_label.config(text="Level: 1")
        self.status_label.config(text="Watch the sequence...")
        self.start_button.config(state="disabled")

        # Add subtle animation effect
        def flash_all_buttons():
            for color in self.colors:
                self.flash_button(color)
                self.after(200, lambda: None)  # Small delay between flashes
            self.after(1000, self.add_to_sequence)

        flash_all_buttons()

    def add_to_sequence(self):
        # Add a random color to the sequence
        self.sequence.append(random.choice(list(self.colors.keys())))
        self.current_level += 1
        
        # Update level with animation
        self.level_label.config(text=f"Level: {self.current_level}")
        
        # Show the sequence
        self.show_sequence()

    def show_sequence(self):
        self.waiting_for_input = False
        self.status_label.config(text="Watch the sequence...")

        # Schedule the flashing of each button in the sequence
        for i, color in enumerate(self.sequence):
            self.after(i * (self.flash_speed + 100), lambda c=color: self.flash_button(c))

        # After showing the sequence, allow player input
        wait_time = len(self.sequence) * (self.flash_speed + 100) + 500
        self.after(wait_time, self.await_player_input)

    def await_player_input(self):
        self.player_sequence = []
        self.waiting_for_input = True
        self.status_label.config(text="Your turn! Repeat the sequence.")

    def player_input(self, color):
        if not self.waiting_for_input or not self.playing:
            return

        # Flash the button with enhanced effect
        self.flash_button(color)

        # Add the color to player's sequence
        self.player_sequence.append(color)

        # Check if the input matches the sequence so far
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            self.game_over()
            return

        # If player completed the sequence correctly
        if len(self.player_sequence) == len(self.sequence):
            self.score_label.config(text=f"Score: {self.current_level}")
            self.waiting_for_input = False
            self.status_label.config(text="Correct! Next level...")
            
            # Flash all buttons to celebrate
            def celebrate():
                for color in self.colors:
                    self.flash_button(color)
                self.after(1000, self.add_to_sequence)
            
            self.after(500, celebrate)

    def game_over(self):
        self.playing = False
        self.waiting_for_input = False
        
        # Animate game over
        def flash_red():
            self.configure(bg="#e74c3c")  # Flash red
            self.after(200, flash_back)
            
        def flash_back():
            self.configure(bg="#8e44ad")  # Return to normal
            
        flash_red()
        
        self.status_label.config(text=f"Game Over! Score: {self.current_level - 1}")
        self.start_button.config(state="normal")

        # Update user score
        if self.parent.current_user:
            self.parent.update_score(self.current_level - 1)


if __name__ == "__main__":
    app = SimonApp()
    app.mainloop()