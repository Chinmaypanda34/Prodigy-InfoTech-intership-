import tkinter as tk
from tkinter import ttk, messagebox

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher Tool")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.bg_color = "#f0f0f0"
        self.button_color = "#4a7a8c"
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message input
        ttk.Label(main_frame, text="Message:").pack(anchor=tk.W)
        self.message_entry = tk.Text(main_frame, height=5, font=('Helvetica', 11))
        self.message_entry.pack(fill=tk.X, pady=5)
        
        # Shift input
        shift_frame = ttk.Frame(main_frame)
        shift_frame.pack(fill=tk.X, pady=5)
        ttk.Label(shift_frame, text="Shift Value:").pack(side=tk.LEFT)
        self.shift_entry = ttk.Entry(shift_frame, width=10)
        self.shift_entry.pack(side=tk.LEFT, padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Encrypt", command=self.encrypt).pack(side=tk.LEFT, expand=True)
        ttk.Button(btn_frame, text="Decrypt", command=self.decrypt).pack(side=tk.LEFT, expand=True)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, expand=True)
        
        # Result
        ttk.Label(main_frame, text="Result:").pack(anchor=tk.W)
        self.result_text = tk.Text(main_frame, height=5, state=tk.DISABLED, font=('Helvetica', 11))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.message_entry.focus()
    
    def encrypt(self):
        self.process_text(encrypt=True)
    
    def decrypt(self):
        self.process_text(encrypt=False)
    
    def process_text(self, encrypt):
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message!")
            return
        
        try:
            shift = int(self.shift_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Shift must be a number!")
            return
        
        result = []
        for char in message:
            if char.isupper():
                base = ord('A')
            elif char.islower():
                base = ord('a')
            else:
                result.append(char)
                continue
            
            if encrypt:
                new_pos = (ord(char) - base + shift) % 26
            else:
                new_pos = (ord(char) - base - shift) % 26
            result.append(chr(base + new_pos))
        
        self.show_result(''.join(result))
    
    def show_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.config(state=tk.DISABLED)
    
    def clear(self):
        self.message_entry.delete("1.0", tk.END)
        self.shift_entry.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.message_entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()
