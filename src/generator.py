from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_M

def create_qr_image(url: str, width_mm: float, height_mm: float, dpi: int = 300, version: int = 4, filename="qr_output.png"):
    # Convert mm to pixels
    width_px = int((width_mm / 25.4) * dpi)
    height_px = int((height_mm / 25.4) * dpi)

    # QR code size = ~80% of vertical space
    qr_height = int(height_px * 0.75)

    qr = qrcode.QRCode(
        version=version,
        error_correction=ERROR_CORRECT_M,
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
