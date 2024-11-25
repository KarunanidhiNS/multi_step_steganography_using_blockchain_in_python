from cryptography.fernet import Fernet
from hashlib import sha256
from PIL import Image, ImageTk
import os
from tkinter import messagebox

storage_path = "steganography_data"
if not os.path.exists(storage_path):
    os.makedirs(storage_path)

key = Fernet.generate_key()
cipher = Fernet(key)

def hash_image(image_path):
    with open(image_path, "rb") as f:
        return sha256(f.read()).hexdigest()

def display_image(img_path, label):
    img = Image.open(img_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def save_image_with_encrypted_data(main_image_path, password, verification_image_path, text_to_encrypt, uploaded_image_label):
    try:
        encrypted_text = cipher.encrypt(text_to_encrypt.encode())
        verification_image_hash = hash_image(verification_image_path)

        main_save_path = os.path.join(storage_path, os.path.basename(main_image_path))
        img = Image.open(main_image_path)
        img.save(main_save_path, "PNG")

        metadata_path = f"{main_save_path}.meta"
        with open(metadata_path, "wb") as f:
            f.write(password.encode() + b"\n" + verification_image_hash.encode() + b"\n" + encrypted_text)

        display_image(main_save_path, uploaded_image_label)
        messagebox.showinfo("Success", "Image saved with encrypted data.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

def decrypt_image_and_display(main_image_path, password, verification_image_path, decrypted_image_label):
    try:
        metadata_path = f"{main_image_path}.meta"
        if not os.path.exists(metadata_path):
            messagebox.showerror("Error", "No metadata found for the selected image.")
            return

        with open(metadata_path, "rb") as f:
            saved_password, verification_image_hash, encrypted_text = f.read().split(b"\n", 2)

        if password.encode() != saved_password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        if hash_image(verification_image_path).encode() != verification_image_hash:
            messagebox.showerror("Error", "Verification image does not match.")
            return

        decrypted_text = cipher.decrypt(encrypted_text).decode()
        messagebox.showinfo("Decrypted Text", decrypted_text)
        display_image(main_image_path, decrypted_image_label)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decrypt image: {e}")
