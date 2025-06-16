import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from .generator import create_rectangle_qr_image, create_luggage_tag_qr_image
from .utils import extract_slug, get_default_save_dir

def launch_gui():
    def on_create():
        url = url_entry.get().strip() # remove any leading/trailing whitespace
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
    
        # get user QR type selection
        qr_type = qr_type_var.get()   
        
        if qr_type == "Luggage Tag QR":
            try:
                tag_x = int(tag_x_entry.get())
                tag_y = int(tag_y_entry.get())
                tag_width = int(tag_width_entry.get())
                tag_height = int(tag_height_entry.get())
                version = int(version_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid tag dimensions or version.")
                return

            if not (1 <= version <= 40):
                version = 4
            
            if use_template_var.get():
                # Checkbox is selected → use the default built-in template
                template_path = None
            else:
                # Checkbox is not selected → use the custom path entered by the user
                user_input = custom_template_path.get().strip()

                if user_input == "":
                    # If the input is empty or just spaces, fall back to None (e.g. user didn't pick a file)
                    template_path = None
                else:
                    # Use the trimmed path
                    template_path = user_input


            create_luggage_tag_qr_image(
                url,
                version=version,
                filename=file_path,
                template_path=template_path,
                qr_zone=(tag_x, tag_y, tag_width, tag_height)
            )
        else:
            try:
                width_mm = float(rect_width_entry.get())
                height_mm = float(rect_height_entry.get())
                dpi = int(rect_dpi_entry.get())
                version = int(version_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid rectangle QR settings.")
                return

            if not (1 <= version <= 40):
                version = 4

            if width_mm <= 0 or height_mm <= 0 or dpi < 72:
                messagebox.showerror("Error", "Enter sensible dimensions and DPI (min 72).")
                return

            create_rectangle_qr_image(
                url,
                width_mm,
                height_mm,
                dpi,
                version,
                filename=file_path
            )

            
        messagebox.showinfo("Success", f"QR code saved to:\n{file_path}")

    def on_cancel():
        root.destroy()

    root = tk.Tk()
    root.title("Sensibee QR Generator")
    root.resizable(False, False)

    # Settings for all QR code generation
    tk.Label(root, text="Enter URL:").pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(padx=20)

    tk.Label(root, text="QR version (1–40, default 4):").pack()
    version_entry = tk.Entry(root, width=10)
    version_entry.insert(0, "4")
    version_entry.pack()


    # QR Type selection
    qr_type_var = tk.StringVar(value="Rectangular QR")
    tk.Label(root, text="QR Code Type:").pack(pady=(10, 0))
    qr_type_dropdown = ttk.Combobox(root, textvariable=qr_type_var, state="readonly")
    qr_type_dropdown['values'] = ("Rectangular QR", "Luggage Tag QR")
    qr_type_dropdown.pack(pady=(0, 10))


    # Frame for rectangle QR options
    rect_frame = tk.LabelFrame(root, text="Rectangle QR Settings")
    rect_frame.pack(padx=10, pady=5, fill="x")

    tk.Label(rect_frame, text="Width (mm):").grid(row=0, column=0, sticky="e")
    rect_width_entry = tk.Entry(rect_frame, width=10)
    rect_width_entry.insert(0, "50")
    rect_width_entry.grid(row=0, column=1, padx=5)

    tk.Label(rect_frame, text="Height (mm):").grid(row=0, column=2, sticky="e")
    rect_height_entry = tk.Entry(rect_frame, width=10)
    rect_height_entry.insert(0, "30")
    rect_height_entry.grid(row=0, column=3, padx=5)

    tk.Label(rect_frame, text="DPI (default 300):").grid(row=1, column=0, sticky="e")
    rect_dpi_entry = tk.Entry(rect_frame, width=10)
    rect_dpi_entry.insert(0, "300")
    rect_dpi_entry.grid(row=1, column=1, padx=5)


    # Frame for luggage tag options
    tag_frame = tk.LabelFrame(root, text="Luggage Tag Settings")
    tag_frame.pack(padx=10, pady=5, fill="x")

    # Top-left X
    tk.Label(tag_frame, text="Top-left X:").grid(row=0, column=0, sticky="e")
    tag_x_entry = tk.Entry(tag_frame, width=10)
    tag_x_entry.insert(0, "0")
    tag_x_entry.grid(row=0, column=1, padx=5)

    # Top-left Y
    tk.Label(tag_frame, text="Top-left Y:").grid(row=0, column=2, sticky="e")
    tag_y_entry = tk.Entry(tag_frame, width=10)
    tag_y_entry.insert(0, "0")
    tag_y_entry.grid(row=0, column=3, padx=5)

    # QR zone Width
    tk.Label(tag_frame, text="QR Zone Width:").grid(row=1, column=0, sticky="e")
    tag_width_entry = tk.Entry(tag_frame, width=10)
    tag_width_entry.insert(0, "827")
    tag_width_entry.grid(row=1, column=1, padx=5)

    # QR zone Height
    tk.Label(tag_frame, text="QR Zone Height:").grid(row=1, column=2, sticky="e")
    tag_height_entry = tk.Entry(tag_frame, width=10)
    tag_height_entry.insert(0, "472")
    tag_height_entry.grid(row=1, column=3, padx=5)

    # use default tag template
    use_template_var = tk.BooleanVar(value=True)
    use_template_checkbox = tk.Checkbutton(
        tag_frame,
        text="Use default tag template",
        variable=use_template_var
    )
    use_template_checkbox.grid(row=2, column=0, padx=5)

    custom_template_path = tk.StringVar()
    custom_file_row = tk.Frame(tag_frame)
    tk.Label(custom_file_row, text="Custom PNG Path:").pack(side="left")
    template_path_entry = tk.Entry(custom_file_row, textvariable=custom_template_path, width=40, state="disabled")
    template_path_entry.pack(side="left", padx=5)
    tk.Button(custom_file_row, text="Browse", command=lambda: browse_for_template()).pack(side="left")
    custom_file_row.grid(row=3, column=0, columnspan=4, pady=5)

    def browse_for_template():
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], title="Select tag template PNG")
        if path:
            custom_template_path.set(path)

    def toggle_template_path():
        if use_template_var.get():
            template_path_entry.configure(state="disabled")
        else:
            template_path_entry.configure(state="normal")

    use_template_var.trace_add("write", lambda *args: toggle_template_path())
    toggle_template_path()  # Run once at start


    # Disable these fields initially
    for widget in tag_frame.winfo_children():
        try:
            widget.configure(state="disabled")
        except tk.TclError:
            pass  # Skip widgets that don't support 'state'

    # function to toggle these fields
    def toggle_fields(*args):
        use_tag = qr_type_var.get() == "Luggage Tag QR"

        # Enable/disable tag frame
        for widget in tag_frame.winfo_children():
            try:
                widget.configure(state="disabled")
            except tk.TclError:
                pass  # Skip widgets that don't support 'state'

        # Enable/disable rectangular frame
        for widget in rect_frame.winfo_children():
            widget.configure(state="disabled" if use_tag else "normal")

    qr_type_var.trace_add("write", toggle_fields)


    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Create", width=10, command=on_create).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).grid(row=0, column=1, padx=5)

    root.mainloop()
