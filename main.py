import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils import hash_image, display_image, cipher, storage_path
from dialog import ask_password_and_image

uploaded_image_label = None
decrypted_image_label = None

def save_image_with_data():
    global uploaded_image_label

    main_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not main_image_path:
        return

    text_to_encrypt = text_entry.get("1.0", tk.END).strip()
    if not text_to_encrypt:
        messagebox.showerror("Error", "Text to encrypt is required.")
        return

    def process_save(password, verification_image_path):
        from utils import save_image_with_encrypted_data 
        save_image_with_encrypted_data(main_image_path, password, verification_image_path, text_to_encrypt, uploaded_image_label)

    ask_password_and_image(process_save)


def decrypt_image():
    global decrypted_image_label

    main_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not main_image_path:
        return

    def process_decrypt(password, verification_image_path):
        from utils import decrypt_image_and_display
        decrypt_image_and_display(main_image_path, password, verification_image_path, decrypted_image_label)

    ask_password_and_image(process_decrypt)


root = tk.Tk()
root.title("Steganography with Enhanced Security")
root.geometry("900x650")

background_photo = ImageTk.PhotoImage(Image.open("background.jpg").resize((900, 650), Image.ANTIALIAS))
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

content_frame = tk.Frame(root, bg="white", padx=20, pady=20, relief="ridge", borderwidth=5)
content_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(content_frame, text="Text to Encrypt:", bg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="ne")
text_entry = tk.Text(content_frame, height=5, width=40, font=("Arial", 12))
text_entry.grid(row=0, column=1, padx=10, pady=5)

save_button = tk.Button(content_frame, text="Save Image with Data", command=save_image_with_data, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
save_button.grid(row=1, column=0, columnspan=2, pady=10)

decrypt_button = tk.Button(content_frame, text="Decrypt Image", command=decrypt_image, bg="#2196F3", fg="white", font=("Arial", 12), width=20)
decrypt_button.grid(row=2, column=0, columnspan=2, pady=10)

uploaded_image_label = tk.Label(content_frame, text="Uploaded Image Will Appear Here", bg="#f0f0f0", font=("Arial", 10), borderwidth=2, relief="groove")
uploaded_image_label.grid(row=3, column=0, padx=10, pady=10)

decrypted_image_label = tk.Label(content_frame, text="Decrypted Image Will Appear Here", bg="#f0f0f0", font=("Arial", 10), borderwidth=2, relief="groove")
decrypted_image_label.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()
