A simple Python app to generate printable QR codes with a label underneath.

HOW TO USE:

Make sure you have Python 3.8 or newer installed.

Open a terminal in this folder.

(Optional) Create a virtual environment:

python -m venv .venv
    source .venv\Scripts\activate   # On Windows
    source .venv/bin/activate   # On Mac/Linux

Install the required packages:
    pip install -r requirements.txt

## System Dependencies

Before using this app, make sure `tkinter` is installed:
    sudo apt install python3.12-tk

Run the app:
    python -m src.main


WHAT IT DOES:

Lets you enter a URL, sticker size (in mm), DPI, and QR version

Generates a PNG with a QR code and the URL below it

Saves the image to your Downloads folder by default (or Desktop if Downloads not found)

REQUIREMENTS:

Python 3.8+

qrcode==8.2

pillow==11.2.1

colorama==0.4.6