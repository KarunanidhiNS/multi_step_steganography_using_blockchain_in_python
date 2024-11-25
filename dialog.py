import tkinter as tk
from tkinter import filedialog, messagebox

def ask_password_and_image(callback):
    def submit_data():
        selected_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not selected_file:
            messagebox.showerror("Error", "Verification image is required.")
            return
        callback(password_entry.get(), selected_file)
        popup_window.destroy()

    popup_window = tk.Toplevel()
    popup_window.title("Enter Details")
    popup_window.geometry("400x250")

    tk.Label(popup_window, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(popup_window, show="*", width=30, font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Button(popup_window, text="Select Verification Image", command=submit_data, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
