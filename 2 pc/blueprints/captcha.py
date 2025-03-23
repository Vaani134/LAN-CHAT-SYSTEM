# captcha.py
from flask import Blueprint, send_file
import random
import string
from PIL import Image, ImageDraw, ImageFont
import io

captcha_blueprint = Blueprint('captcha', __name__)

# Function to generate random 4-digit CAPTCHA text
def generate_captcha_text(length=4):
    return ''.join(random.choices(string.digits, k=length))

# Function to generate CAPTCHA image
def generate_captcha_image(captcha_text):
    width, height = 120, 40  # Dimensions of the CAPTCHA image
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # You can change the font path according to your system
    font = ImageFont.load_default()
    
    # Draw the text in the image
    draw.text((30, 5), captcha_text, font=font, fill=(255, 255, 255))

    # Save the image to a byte buffer
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return img_io

@captcha_blueprint.route('/generate_captcha')
def generate_captcha():
    captcha_text = generate_captcha_text()
    
    # Store the CAPTCHA text in session
    from flask import session
    session['captcha'] = captcha_text
    
    # Generate and return CAPTCHA image
    img_io = generate_captcha_image(captcha_text)
    return send_file(img_io, mimetype='image/png')
