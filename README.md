A simple Python app to generate printable QR codes with a label underneath.

## HOW TO USE:

Clone and open this project.

Make sure you have Python 3.8 or newer installed.

Open a terminal in this folder.

(Optional but reccomended)
Create a virtual environment:
    python -m venv .venv

activate this environment:
    source .venv\Scripts\activate   # On Windows
    source .venv/bin/activate   # On Mac/Linux

## 1st Time running - Install Requirements

Install the required packages:
    pip install -r requirements.txt

REQUIREMENTS:

Python 3.8+
qrcode==8.2
pillow==11.2.1
colorama==0.4.6

## System Dependencies

Before using this app, make sure `tkinter` is installed:
    sudo apt install python3.12-tk

## Running the app

activate this environment (if not done):
    source .venv/Scripts/activate   # On git bash (windows)
    source .venv/bin/activate   # On Mac/Linux

then run:
    python -m src.main


## WHAT IT DOES:

Lets you enter a URL or choose a .csv for a list of URLs
The .csv file needs to have a 1st value representing the main registration link: 
'https://my.sensibee.io/register?deviceId='

then following values:

'faithful-hoverfly-66,
gigantic-moth-10
brave-damselfly-22, 
etc...'

will be added to the end of main link to create a batch of links: e.g. 'https://my.sensibee.io/register?deviceId=faithful-hoverfly-66'

Choose QR code settings

Select either:
    plain Rectangular QR - can choose .svg or .png with URL
    laggage tag QR - .png with URL on template

Then select relevant settings for selection

Generates a PNG with a QR code and the URL below it

Saves the image to your Downloads folder by default (or Desktop if Downloads not found)

