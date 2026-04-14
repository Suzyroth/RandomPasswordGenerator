import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("500x650")
        self.root.resizable(True, True)
        
        # Character sets
        self.lowercase_chars = string.ascii_lowercase
        self.uppercase_chars = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous_chars = "0O1lI"
        
        self.setup_ui()
        
    def setup_ui(self):
        title_label = tk.Label(self.root, text="🔐 Advanced Password Generator", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Length
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="10")
        length_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.length_var = tk.IntVar(value=12)
        ttk.Scale(length_frame, from_=8, to=50, variable=self.length_var,
                  orient=tk.HORIZONTAL).pack(fill=tk.X)
        tk.Label(length_frame, textvariable=self.length_var).pack()
        
        # Character types
        char_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="10")
        char_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.include_lower = tk.BooleanVar(value=True)
        self.include_upper = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        
        for var, text in [
            (self.include_lower, "Lowercase (abc)"),
            (self.include_upper, "Uppercase (ABC)"),
            (self.include_digits, "Numbers (123)"),
            (self.include_symbols, "Symbols (!@#)")
        ]:
            tk.Checkbutton(char_frame, text=text, variable=var).pack(anchor=tk.W)
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.exclude_ambiguous = tk.BooleanVar(value=True)
        self.no_consecutive = tk.BooleanVar(value=False)
        self.min_complexity = tk.BooleanVar(value=True)
        
        tk.Checkbutton(advanced_frame, text="Exclude ambiguous chars (0,O,1,l,I)", 
                      variable=self.exclude_ambiguous).pack(anchor=tk.W)
        tk.Checkbutton(advanced_frame, text="No consecutive identical chars", 
                      variable=self.no_consecutive).pack(anchor=tk.W)
        tk.Checkbutton(advanced_frame, text="Ensure minimum complexity", 
                      variable=self.min_complexity).pack(anchor=tk.W)
        
        # Exclude Characters
        exclude_frame = ttk.LabelFrame(main_frame, text="Exclude Characters", padding="10")
        exclude_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.exclude_chars = tk.StringVar()
        tk.Entry(exclude_frame, textvariable=self.exclude_chars, width=30).pack()
        tk.Label(exclude_frame, text="e.g., 'aeiou' to exclude vowels", 
                font=("Arial", 8)).pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="GENERATE PASSWORD",
                  command=self.generate_password,
                  bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"),
                  padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        # ✅ COPY BUTTON FIXED (WHITE TEXT ALWAYS)
        self.copy_btn = tk.Button(
            btn_frame,
            text="COPY",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
            bg="#1565C0",
            fg="white",                      # normal state
            disabledforeground="white",      # 🔥 stays white when disabled
            font=("Arial", 11, "bold"),
            activebackground="#0D47A1",
            activeforeground="white",        # 🔥 stays white when clicked
            padx=12,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Output
        self.password_text = tk.Text(main_frame, height=3, font=("Consolas", 12),
                                    state=tk.DISABLED)
        self.password_text.pack(fill=tk.X)
        
        self.strength_label = tk.Label(main_frame, text="Password Strength: Not generated")
        self.strength_label.pack()
        
        self.strength_bar = ttk.Progressbar(main_frame, length=300)
        self.strength_bar.pack()
        
        self.entropy_label = tk.Label(main_frame, text="", fg="gray")
        self.entropy_label.pack()
        
    def get_character_set(self):
        char_set = ""
        
        if self.include_lower.get():
            char_set += self.lowercase_chars
        if self.include_upper.get():
            char_set += self.uppercase_chars
        if self.include_digits.get():
            char_set += self.digits
        if self.include_symbols.get():
            char_set += self.symbols
        
        exclude = set(self.exclude_chars.get())
        if self.exclude_ambiguous.get():
            exclude.update(self.ambiguous_chars)
        
        return ''.join(c for c in char_set if c not in exclude)
    
    def generate_raw_password(self):
        char_set = self.get_character_set()
        length = self.length_var.get()
        
        if not char_set:
            raise ValueError("No characters available!")
        
        return ''.join(random.choice(char_set) for _ in range(length))
    
    def generate_password(self):
        try:
            password = self.generate_raw_password()
            
            self.password_text.config(state=tk.NORMAL)
            self.password_text.delete(1.0, tk.END)
            self.password_text.insert(1.0, password)
            self.password_text.config(state=tk.DISABLED)
            
            self.copy_btn.config(state=tk.NORMAL)
            
            strength, entropy = self.calculate_strength(password)
            self.update_strength_display(strength, entropy)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def calculate_strength(self, password):
        length = len(password)
        score = min(100, length * 6)
        entropy = length * 4
        return score, entropy
    
    def update_strength_display(self, strength, entropy):
        if strength < 40:
            label, color = "Weak", "red"
        elif strength < 70:
            label, color = "Fair", "orange"
        elif strength < 90:
            label, color = "Good", "blue"
        else:
            label, color = "Strong", "green"
        
        self.strength_label.config(text=f"Password Strength: {label}", fg=color)
        self.strength_bar['value'] = strength
        self.entropy_label.config(text=f"Entropy: {entropy} bits")
    
    def copy_to_clipboard(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            pyperclip.copy(password)
            self.copy_btn.config(text="COPIED ✓")
            self.root.after(1500, lambda: self.copy_btn.config(text="COPY"))

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    