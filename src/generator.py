from PIL import Image, ImageDraw, ImageFont
import qrcode

def create_qr_image(url: str, size: int, filename="qr_output.png"):
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_size = int(size * 0.8)
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    qr_x = (size - qr_size) // 2
    img.paste(qr_img, (qr_x, 10))

    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    text = url if len(url) <= 40 else url[:37] + "..."
    text_width, _ = draw.textsize(text, font=font)
    draw.text(((size - text_width) // 2, qr_size + 20), text, fill="black", font=font)

    img.save(filename)
