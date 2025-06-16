import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .generator import create_rectangle_qr_image, create_luggage_tag_qr_image
from .utils import extract_slug, get_default_save_dir
from .qr_info import get_max_chars, get_module_size

def launch_gui():
    # ======= Internal helper functions =======

    # Triggered when "Create" button is pressed
    def on_create():
        url = url_entry.get().strip()
        slug = extract_slug(url) # this is for a clear filename

        # Get version + error correction level from UI
        try:
            version = int(version_entry.get())
        except ValueError:
            version = 4  # fallback

        error_level = error_level_var.get()  # "L", "M", "Q", or "H"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save QR code as...",
            initialfile=f"{slug}.png",
            initialdir=get_default_save_dir()
        )
        if not file_path:
            return  # User cancelled

        qr_type = qr_type_var.get()

        try:
            version = int(version_entry.get())
        except ValueError:
            version = 4  # Fallback default

        # --- Mode: Luggage Tag QR ---
        if qr_type == "Luggage Tag QR":
            try:
                tag_x = int(tag_x_entry.get())
                tag_y = int(tag_y_entry.get())
                tag_width = int(tag_width_entry.get())
                tag_height = int(tag_height_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid tag dimensions.")
                return
            template_path = None if use_template_var.get() else custom_template_path.get().strip() or None
            create_luggage_tag_qr_image(
                url, version, error_level, file_path, template_path,
                (tag_x, tag_y, tag_width, tag_height)
            )
        # --- Mode: Rectangular QR ---
        else:
            try:
                width_mm = float(rect_width_entry.get())
                height_mm = float(rect_height_entry.get())
                dpi = int(rect_dpi_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid rectangle QR settings.")
                return
            create_rectangle_qr_image(
                url, width_mm, height_mm, dpi,
                version, error_level, filename=file_path
            )

        messagebox.showinfo("Success", f"QR code saved to:\n{file_path}")

    def on_cancel():
        root.destroy()

    def browse_for_template():
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], title="Select tag template PNG")
        if path:
            custom_template_path.set(path)

    def toggle_template_fields(*_):
        # Enable/disable custom template entry + button
        use_default = use_template_var.get()
        state = "disabled" if use_default else "normal"
        template_path_entry.config(state=state)
        template_browse_btn.config(state=state)

    def toggle_mode_fields(*_):
        # Show only relevant settings based on QR type
        use_tag = qr_type_var.get() == "Luggage Tag QR"
        for widget in tag_frame.winfo_children():
            try: widget.config(state="normal" if use_tag else "disabled")
            except tk.TclError: pass
        for widget in rect_frame.winfo_children():
            try: widget.config(state="disabled" if use_tag else "normal")
            except tk.TclError: pass
        toggle_template_fields()

    def show_error_info():
        messagebox.showinfo(
            "QR Error Correction Levels",
            "L (Low): ~7% error recovery\n"
            "M (Medium): ~15% (default)\n"
            "Q (Quartile): ~25%\n"
            "H (High): ~30%\n\n"
            "Higher levels are more robust but store less data."
        )

    def update_qr_stats(*args):
        # Update stats shown based on version/error level
        try:
            version = int(version_entry.get())
            level = error_level_var.get()
            module_count = get_module_size(version)
            max_chars = get_max_chars(version, level)
            if max_chars == -1:
                qr_size_label.config(text="(version >8 not supported for stats)")
            else:
                qr_size_label.config(text=f"QR: {module_count}×{module_count} squares, Max chars: ~{max_chars}")
        except:
            qr_size_label.config(text="QR: ?×? squares, Max chars: ?")

    # ======= UI Layout =======

    root = tk.Tk()
    root.title("Sensibee QR Generator")
    root.resizable(False, False)

    # --- URL input field ---
    tk.Label(root, text="Enter URL:").pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(padx=20)

    # --- QR encoding settings (version + error level) ---
    version_frame = tk.LabelFrame(root, text="QR Encoding Settings")
    version_frame.pack(padx=10, pady=5, fill="x")

    tk.Label(version_frame, text="QR version (1–40, default 4):").grid(row=0, column=0, sticky="e")
    version_entry = tk.Entry(version_frame, width=10)
    version_entry.insert(0, "4")
    version_entry.grid(row=0, column=1, padx=5)

    tk.Label(version_frame, text="Error correction:").grid(row=0, column=2, sticky="e")
    error_level_var = tk.StringVar(value="M")
    error_level_dropdown = ttk.Combobox(version_frame, textvariable=error_level_var,
        values=["L", "M", "Q", "H"], state="readonly", width=5)
    error_level_dropdown.grid(row=0, column=3, padx=5)

    tk.Button(version_frame, text="?", width=2, command=show_error_info).grid(row=0, column=4)

    qr_size_label = tk.Label(version_frame, text="QR: ?×? squares, Max chars: ?")
    qr_size_label.grid(row=1, column=0, columnspan=5)
    version_entry.bind("<KeyRelease>", update_qr_stats)
    error_level_var.trace_add("write", update_qr_stats)
    update_qr_stats()

    # --- QR Code Type dropdown ---
    qr_type_var = tk.StringVar(value="Rectangular QR")
    tk.Label(root, text="QR Code Type:").pack()
    qr_type_dropdown = ttk.Combobox(root, textvariable=qr_type_var,
        values=["Rectangular QR", "Luggage Tag QR"], state="readonly")
    qr_type_dropdown.pack()

    # --- Rectangle QR settings ---
    rect_frame = tk.LabelFrame(root, text="Rectangle QR Settings")
    rect_frame.pack(padx=10, pady=5, fill="x")

    tk.Label(rect_frame, text="Width (mm):").grid(row=0, column=0, sticky="e")
    rect_width_entry = tk.Entry(rect_frame, width=10)
    rect_width_entry.insert(0, "50")
    rect_width_entry.grid(row=0, column=1)

    tk.Label(rect_frame, text="Height (mm):").grid(row=0, column=2, sticky="e")
    rect_height_entry = tk.Entry(rect_frame, width=10)
    rect_height_entry.insert(0, "30")
    rect_height_entry.grid(row=0, column=3)

    tk.Label(rect_frame, text="DPI:").grid(row=1, column=0, sticky="e")
    rect_dpi_entry = tk.Entry(rect_frame, width=10)
    rect_dpi_entry.insert(0, "300")
    rect_dpi_entry.grid(row=1, column=1)

    # --- Luggage tag QR settings ---
    tag_frame = tk.LabelFrame(root, text="Luggage Tag Settings")
    tag_frame.pack(padx=10, pady=5, fill="x")

    tk.Label(tag_frame, text="Top-left X:").grid(row=0, column=0, sticky="e")
    tag_x_entry = tk.Entry(tag_frame, width=10)
    tag_x_entry.insert(0, "0")
    tag_x_entry.grid(row=0, column=1)

    tk.Label(tag_frame, text="Top-left Y:").grid(row=0, column=2, sticky="e")
    tag_y_entry = tk.Entry(tag_frame, width=10)
    tag_y_entry.insert(0, "0")
    tag_y_entry.grid(row=0, column=3)

    tk.Label(tag_frame, text="QR Zone Width:").grid(row=1, column=0, sticky="e")
    tag_width_entry = tk.Entry(tag_frame, width=10)
    tag_width_entry.insert(0, "827")
    tag_width_entry.grid(row=1, column=1)

    tk.Label(tag_frame, text="QR Zone Height:").grid(row=1, column=2, sticky="e")
    tag_height_entry = tk.Entry(tag_frame, width=10)
    tag_height_entry.insert(0, "472")
    tag_height_entry.grid(row=1, column=3)

    # --- Template selector for luggage tag ---
    use_template_var = tk.BooleanVar(value=True)
    use_template_checkbox = tk.Checkbutton(tag_frame, text="Use default tag template", variable=use_template_var)
    use_template_checkbox.grid(row=2, column=0, padx=5)

    custom_template_path = tk.StringVar()
    custom_file_row = tk.Frame(tag_frame)
    tk.Label(custom_file_row, text="Custom PNG Path:").pack(side="left")
    template_path_entry = tk.Entry(custom_file_row, textvariable=custom_template_path, width=40, state="disabled")
    template_path_entry.pack(side="left", padx=5)
    template_browse_btn = tk.Button(custom_file_row, text="Browse", command=browse_for_template, state="disabled")
    template_browse_btn.pack(side="left")
    custom_file_row.grid(row=3, column=0, columnspan=4, pady=5)

    # --- Action buttons ---
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Create", width=10, command=on_create).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).grid(row=0, column=1, padx=5)

    # --- Reactive logic bindings ---
    use_template_var.trace_add("write", toggle_template_fields)
    qr_type_var.trace_add("write", toggle_mode_fields)
    toggle_mode_fields()  # Initial state

    root.mainloop()
