import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from .generator import create_qr_image
from .utils import extract_slug, get_default_save_dir

def launch_gui():
    def on_create():
        url = url_entry.get()
        try:
            width_mm = float(width_entry.get())
            height_mm = float(height_entry.get())
            dpi = int(dpi_entry.get())
            version = int(version_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if not (1 <= version <= 40):
            version = 4

        if width_mm <= 0 or height_mm <= 0 or dpi < 72:
            messagebox.showerror("Error", "Enter sensible dimensions and DPI (min 72).")
            return
        
        slug = extract_slug(url)

        # get the save path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save QR code as...",
            initialfile=f"{slug}.png",
            initialdir=get_default_save_dir()

        )
        if not file_path:
            return  # User cancelled

        create_qr_image(url, width_mm, height_mm, dpi, version, filename=file_path)
        messagebox.showinfo("Success", f"QR code saved to:\n{file_path}")

    def on_cancel():
        root.destroy()

    root = tk.Tk()
    root.title("QR Sticker App")
    root.resizable(False, False)

    tk.Label(root, text="Enter URL:").pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(padx=20)

    tk.Label(root, text="Width (mm):").pack()
    width_entry = tk.Entry(root, width=10)
    width_entry.insert(0, "50")
    width_entry.pack()

    tk.Label(root, text="Height (mm):").pack()
    height_entry = tk.Entry(root, width=10)
    height_entry.insert(0, "30")
    height_entry.pack()

    tk.Label(root, text="DPI (default 300):").pack()
    dpi_entry = tk.Entry(root, width=10)
    dpi_entry.insert(0, "300")
    dpi_entry.pack()

    tk.Label(root, text="QR version (1–40, default 4):").pack()
    version_entry = tk.Entry(root, width=10)
    version_entry.insert(0, "4")
    version_entry.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Create", width=10, command=on_create).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).grid(row=0, column=1, padx=5)

    root.mainloop()
