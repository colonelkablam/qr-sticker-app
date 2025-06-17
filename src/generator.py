from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from pathlib import Path

# Map string to constant
ERROR_CORRECTION_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

def create_luggage_tag_qr_image(url: str, version: int = 4, error_level: str = 'M', filename="tag_output.png", template_path=None, qr_zone=(0, 0, 827, 472)):
    """
    Generates a QR code and URL image composited onto a tag template background.
    The tag template is assumed to be 2598x472px, and the QR zone is 827x472px at (0,0).
    """
    # Load the background template
    if template_path is None:
        BASE_DIR = Path(__file__).resolve().parent.parent
        template_path = BASE_DIR / "assets" / "tag_template.png"
    
    TEMPLATE_PATH = Path(template_path)
    
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template image not found at {TEMPLATE_PATH}")
    
    background = Image.open(TEMPLATE_PATH).convert("RGBA")
    # Unpack the QR zone
    zone_x, zone_y, qr_zone_width, qr_zone_height = qr_zone

    # Make the QR code image with text below (on a transparent canvas)
    qr_size = int(qr_zone_height * 0.75)  # ~75% of vertical space
    qr_img = qrcode.QRCode(
        version=version,
        error_correction=ERROR_CORRECTION_MAP.get(error_level.upper(), ERROR_CORRECT_M),
        box_size=10,
        border=1
    )
    qr_img.add_data(url)
    qr_img.make(fit=True)

    # warn if version number different to user selection
    actual_version = qr_img.version
    if actual_version != version:
        from tkinter import messagebox
        messagebox.showinfo(
            "Version Adjusted",
            f"The selected QR version ({version}) was too small to fit {len(url)} chars.\n"
            f"It has been increased to version {actual_version} to fit your data."
        )

    qr_rendered = qr_img.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_rendered = qr_rendered.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Prepare a transparent image for the QR zone
    qr_zone_img = Image.new("RGBA", (qr_zone_width, qr_zone_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(qr_zone_img)

    # Paste QR code in middle
    qr_x = (qr_zone_width - qr_size) // 2
    qr_y = (qr_zone_height - qr_size) // 2
    qr_zone_img.paste(qr_rendered, (qr_x, qr_y))

    # Prepare URL text
    padding = int(qr_zone_width * 0.05)
    max_text_width = qr_zone_width - 2 * padding
    text = url if len(url) <= 80 else url[:77] + "..."
    font_size = 28

    while font_size > 5:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            break
        bbox = draw.textbbox((0, 0), text, font=font)
        # get text width in pixels of this iteration
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width:
            break
        font_size -= 1

    text_x = (qr_zone_width - text_width) // 2

    # calculate text height
    text_height = bbox[3] - bbox[1]
    remaining_space = qr_zone_height - qr_size
    text_y = qr_size + (remaining_space//2)

    draw.text((text_x, text_y), text, fill="black", font=font)

    # Paste QR zone onto background at specified position
    background.paste(qr_zone_img, (zone_x, zone_y), qr_zone_img)

    background.save(filename)


def create_rectangle_qr_image(url: str, width_mm: float, height_mm: float, dpi: int = 300, version: int = 4, error_level: str = 'M', filename="qr_output.png"):
    """
    Generates an rectangular image of QR code with URL text underneath of a given size at a DPI of 300
    """
    # Convert mm to pixels
    width_px = int((width_mm / 25.4) * dpi)
    height_px = int((height_mm / 25.4) * dpi)

    # QR code size = ~80% of vertical space
    qr_height = int(height_px * 0.75)

    qr = qrcode.QRCode(
        version=version,
        error_correction=ERROR_CORRECTION_MAP.get(error_level.upper(), ERROR_CORRECT_M),
        box_size=10,
        border=1
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_img = qr_img.resize((qr_height, qr_height), Image.Resampling.LANCZOS)

    img = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(img)

    # Center QR
    qr_x = (width_px - qr_height) // 2
    img.paste(qr_img, (qr_x, 10))

    # Draw text below QR
    padding = int(width_px * 0.05)  # 5% padding left and right
    max_text_width = width_px - 2 * padding

    text = url if len(url) <= 80 else url[:77] + "..."

    # Try decreasing font size until it fits
    font_size = int(dpi / 3)  # start around 25pt at 300 DPI
    while font_size > 6:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            break  # Can't resize default font
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width:
            break
        font_size -= 1

    # Centered text position
    text_x = (width_px - text_width) // 2
    text_y = qr_height + 20
    draw.text((text_x, text_y), text, fill="black", font=font)

    img.save(filename, dpi=(dpi, dpi))
