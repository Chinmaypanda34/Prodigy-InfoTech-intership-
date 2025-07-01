import tkinter as tk
from tkinter import ttk
import re
from math import log

class PasswordChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Complexity Checker")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Modern dark theme with neon accents
        self.bg_color = "#121212"
        self.text_color = "#ffffff"
        self.accent_color = "#00ff9d"
        self.weak_color = "#ff5555"
        self.medium_color = "#ffcc00"
        self.strong_color = "#00ff9d"
        
        self.root.configure(bg=self.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TEntry', fieldbackground="#252525", foreground=self.text_color)
        self.style.configure('TButton', background=self.accent_color, foreground="#000000")
        self.style.map('TButton', background=[('active', self.accent_color)])
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Password Strength Analyzer",
            font=("Helvetica", 16, "bold"),
            foreground=self.accent_color
        )
        title.pack(pady=(0, 20))
        
        # Password entry
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Enter Password:").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(
            input_frame,
            show="•",
            font=("Helvetica", 12)
        )
        self.password_entry.pack(fill=tk.X, pady=5)
        self.password_entry.bind("<KeyRelease>", self.check_password)
        
        # Strength meter
        self.strength_meter = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.strength_meter.pack(pady=10)
        
        # Strength label
        self.strength_label = ttk.Label(
            main_frame,
            text="Strength: None",
            font=("Helvetica", 12),
            foreground=self.text_color
        )
        self.strength_label.pack()
        
        # Feedback frame
        feedback_frame = ttk.Frame(main_frame)
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        ttk.Label(
            feedback_frame,
            text="Password Requirements:",
            font=("Helvetica", 10, "bold"),
            foreground=self.accent_color
        ).pack(anchor=tk.W)
        
        # Requirement checkboxes
        self.length_var = tk.BooleanVar()
        self.upper_var = tk.BooleanVar()
        self.lower_var = tk.BooleanVar()
        self.number_var = tk.BooleanVar()
        self.special_var = tk.BooleanVar()
        
        ttk.Checkbutton(
            feedback_frame,
            text="Minimum 8 characters",
            variable=self.length_var,
            state="disabled"
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            feedback_frame,
            text="Contains uppercase letters",
            variable=self.upper_var,
            state="disabled"
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            feedback_frame,
            text="Contains lowercase letters",
            variable=self.lower_var,
            state="disabled"
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            feedback_frame,
            text="Contains numbers",
            variable=self.number_var,
            state="disabled"
        ).pack(anchor=tk.W)
        
        ttk.Checkbutton(
            feedback_frame,
            text="Contains special characters",
            variable=self.special_var,
            state="disabled"
        ).pack(anchor=tk.W)
    
    def check_password(self, event=None):
        password = self.password_entry.get()
        
        # Reset all checks
        self.length_var.set(False)
        self.upper_var.set(False)
        self.lower_var.set(False)
        self.number_var.set(False)
        self.special_var.set(False)
        
        if not password:
            self.strength_meter["value"] = 0
            self.strength_label.config(text="Strength: None", foreground=self.text_color)
            return
        
        # Check requirements
        score = 0
        feedback = []
        
        # Length check
        length = len(password)
        if length >= 8:
            self.length_var.set(True)
            score += 1
        
        # Uppercase check
        if re.search(r'[A-Z]', password):
            self.upper_var.set(True)
            score += 1
        
        # Lowercase check
        if re.search(r'[a-z]', password):
            self.lower_var.set(True)
            score += 1
        
        # Number check
        if re.search(r'[0-9]', password):
            self.number_var.set(True)
            score += 1
        
        # Special character check
        if re.search(r'[^A-Za-z0-9]', password):
            self.special_var.set(True)
            score += 1
        
        # Calculate entropy
        pool_size = 0
        if self.lower_var.get():
            pool_size += 26
        if self.upper_var.get():
            pool_size += 26
        if self.number_var.get():
            pool_size += 10
        if self.special_var.get():
            pool_size += 32  # Common special characters
        
        if pool_size > 0:
            entropy = length * log(pool_size, 2)
            strength_percent = min(100, (entropy / 128) * 100)  # 128 bits is very strong
        else:
            strength_percent = 0
        
        self.strength_meter["value"] = strength_percent
        
        # Determine strength level
        if strength_percent < 40:
            strength = "Weak"
            color = self.weak_color
        elif strength_percent < 70:
            strength = "Medium"
            color = self.medium_color
        else:
            strength = "Strong"
            color = self.strong_color
        
        self.strength_label.config(text=f"Strength: {strength}", foreground=color)
        
        # Update meter color
        self.style.configure("Horizontal.TProgressbar", troughcolor=self.bg_color, background=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordChecker(root)
    root.mainloop()
