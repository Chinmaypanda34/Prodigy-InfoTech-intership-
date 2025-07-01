import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

class ImageEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool - Prodigy Infotech")
        self.root.geometry("800x600")
        
        # Variables
        self.original_image = None
        self.encrypted_image = None
        self.key = tk.StringVar()
        
        # GUI Components
        self.create_widgets()
        
    def create_widgets(self):
        # Main frames
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        image_frame = tk.Frame(self.root)
        image_frame.pack(expand=True, fill=tk.BOTH)
        
        # Control buttons
        tk.Button(control_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Encrypt", command=self.encrypt_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Decrypt", command=self.decrypt_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Key entry
        tk.Label(control_frame, text="Encryption Key:").pack(side=tk.LEFT, padx=5)
        tk.Entry(control_frame, textvariable=self.key, width=20).pack(side=tk.LEFT, padx=5)
        
        # Image display
        self.original_label = tk.Label(image_frame, text="Original Image")
        self.original_label.pack(side=tk.LEFT, expand=True)
        
        self.encrypted_label = tk.Label(image_frame, text="Encrypted/Decrypted Image")
        self.encrypted_label.pack(side=tk.RIGHT, expand=True)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                self.encrypted_image = None
                self.display_image(None, self.encrypted_label)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, label):
        if image:
            # Resize for display while maintaining aspect ratio
            width, height = image.size
            ratio = min(350/width, 350/height)
            new_size = (int(width*ratio), int(height*ratio))
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(resized_image)
            label.config(image=photo, text="")
            label.image = photo
        else:
            label.config(image=None, text="No image available")
            label.image = None
    
    def process_image(self, encrypt=True):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        key = self.key.get()
        if not key:
            messagebox.showwarning("Warning", "Please enter an encryption key!")
            return
        
        try:
            # Convert image to numpy array
            img_array = np.array(self.original_image)
            
            # Convert key to numeric value
            key_value = sum(ord(c) for c in key) % 256
            
            # Perform XOR operation on each pixel
            if encrypt:
                processed_array = np.bitwise_xor(img_array, key_value)
            else:
                processed_array = np.bitwise_xor(img_array, key_value)
            
            # Convert back to image
            self.encrypted_image = Image.fromarray(processed_array)
            self.display_image(self.encrypted_image, self.encrypted_label)
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
    
    def encrypt_image(self):
        self.process_image(encrypt=True)
    
    def decrypt_image(self):
        self.process_image(encrypt=False)
    
    def save_image(self):
        if not self.encrypted_image:
            messagebox.showwarning("Warning", "No processed image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if file_path:
            try:
                self.encrypted_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptor(root)
    root.mainloop()
