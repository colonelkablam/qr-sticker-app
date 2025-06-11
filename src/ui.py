import tkinter as tk
from tkinter import messagebox
from .generator import create_qr_image

def launch_gui():
    def on_create():
        url = url_entry.get()
        size_text = size_entry.get()

        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        try:
            size = int(size_text)
            if size < 100 or size > 2000:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid image size between 100 and 2000.")
            return

        create_qr_image(url, size)
        messagebox.showinfo("Success", "QR code saved as 'qr_output.png'")

    def on_cancel():
        root.destroy()

    root = tk.Tk()
    root.title("QR Code Generator")
    root.geometry("300x180")
    root.resizable(False, False)

    tk.Label(root, text="Enter URL:").pack(pady=(10, 0))
    url_entry = tk.Entry(root, width=40)
    url_entry.pack()

    tk.Label(root, text="Image size (e.g. 300):").pack(pady=(10, 0))
    size_entry = tk.Entry(root, width=10)
    size_entry.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Create", width=10, command=on_create).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).grid(row=0, column=1, padx=5)

    root.mainloop()
