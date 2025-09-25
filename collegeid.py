from PIL import Image, ImageDraw, ImageFont
import qrcode
import barcode
from barcode.writer import ImageWriter
import os

# --- Constants ---
CARD_WIDTH, CARD_HEIGHT = 1000, 600
HEADER_HEIGHT = 140
SEPARATOR_HEIGHT = 40
BG_COLOR_FRONT = (255, 255, 255)
HEADER_COLOR = (11, 84, 129)
SEPARATOR_COLOR = (232, 240, 232)
FOOTER_COLOR = (80, 80, 80)
TEXT_COLOR = (0, 0, 0)
VALUE_COLOR = (40, 100, 40)
SIGN_TEXT_COLOR = (60, 60, 60)
PADDING = 40
LINE_HEIGHT = 38

# --- Paths (update accordingly) ---
logo_path = r"logo.png"
photo_path = r"photo.png"
sign_path = r"signature.png"
output_front = r"ID_front.png"
output_back = r"ID_back.png"
background_front = r"front_bg.png"
background_back = r"back_bg.png"

# --- College & Student Info ---
college = {
    "name": "Maharana Pratap Engineering College",
    "address": "Kothi, Mandhana, Kanpur, Uttar Pradesh",
    "contact": "+91-8081210087 / +91-8953400862",
    "toll_free": "1800-123-456",
    "website": "www.mpgi.edu.in"
}

student = {
    "name": "Edward Norton",
    "roll": "FGTCLB2983",
    "course": "B.Tech - Computer Science",
    "dob": "28-Feb-2000",
    "valid_upto": "31-May-2026"
}

emergency_contact = "Emergency Contact: +91-8081210087"

# --- Utility Functions ---
def load_font(size, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except:
        return ImageFont.load_default()

def load_and_resize_image(path, size):
    img = Image.open(path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    return img

def apply_background(base_card, background_path, alpha=50):
    """Paste semi-transparent background onto base card."""
    if background_path:
        bg = Image.open(background_path).convert("RGBA").resize((CARD_WIDTH, CARD_HEIGHT))
        bg.putalpha(alpha)
        base_card.paste(bg, (0,0), bg)
    return base_card

# --- Generate Front ID ---
def generate_front(background_path=None, alpha=50):
    card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (255,255,255,255))
    
    # Apply semi-transparent background
    card = apply_background(card, background_path, alpha)
    draw = ImageDraw.Draw(card)

    # Header
    draw.rectangle([(0, 0), (CARD_WIDTH, HEADER_HEIGHT)], fill=HEADER_COLOR)
    draw.rectangle([(0, HEADER_HEIGHT), (CARD_WIDTH, HEADER_HEIGHT + SEPARATOR_HEIGHT)], fill=SEPARATOR_COLOR)

    # Fonts
    title_font = load_font(36, True)
    sub_font = load_font(18)
    body_font = load_font(22)
    small_font = load_font(16)

    # Logo
    logo = load_and_resize_image(logo_path, (220, 120))
    card.paste(logo, (PADDING, 10), logo)

    # Header Text
    draw.text((300, 25), college["name"], font=title_font, fill="white")
    draw.text((300, 75), "Founded: 1999", font=sub_font, fill="white")

    # Student Photo
    photo = load_and_resize_image(photo_path, (250, 300))
    card.paste(photo, (PADDING, HEADER_HEIGHT + SEPARATOR_HEIGHT + 40), photo)

    # Student Details
    start_x, y = 350, HEADER_HEIGHT + SEPARATOR_HEIGHT + 40
    labels = [
        ("Student Name:", student["name"]),
        ("Roll No.:", student["roll"]),
        ("Course:", student["course"]),
        ("Date of Birth:", student["dob"]),
        ("Address:", college["address"]),
        ("Valid Upto:", student["valid_upto"]),
    ]
    for label, value in labels:
        draw.text((start_x, y), label, font=body_font, fill=TEXT_COLOR)
        draw.text((start_x + 250, y), value, font=body_font, fill=VALUE_COLOR)
        y += LINE_HEIGHT

    # Signature
    sign = load_and_resize_image(sign_path, (200, 80))
    card.paste(sign, (start_x + 1, y + 1), sign)
    draw.text((start_x, y + 81), "Authorized Signatory", font=small_font, fill=SIGN_TEXT_COLOR)

    # Footer
    footer_text = f"{college['address']}    |    {college['contact']}    |    {college['website']}"
    draw.text((20, CARD_HEIGHT - 30), footer_text, font=small_font, fill=FOOTER_COLOR)

    card = card.convert("RGB")
    card.save(output_front)
    print(f"✅ Front side ID card saved at: {output_front}")

# --- Generate Back ID with Semi-Transparent Background, QR & Barcode ---
def generate_back(background_path=None, alpha=100):
    card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (255,255,255,255))
    
    # Apply semi-transparent background
    card = apply_background(card, background_path, alpha)
    draw = ImageDraw.Draw(card)

    # Header
    draw.rectangle([(0, 0), (CARD_WIDTH, HEADER_HEIGHT)], fill=HEADER_COLOR)
    draw.rectangle([(0, HEADER_HEIGHT), (CARD_WIDTH, HEADER_HEIGHT + SEPARATOR_HEIGHT)], fill=SEPARATOR_COLOR)

    # Fonts
    title_font = load_font(36, True)
    sub_font = load_font(18)
    body_font = load_font(20)
    footer_font = load_font(14)

    # Logo
    logo = load_and_resize_image(logo_path, (220, 120))
    card.paste(logo, (PADDING, 10), logo)

    # Header Text
    draw.text((300, 25), college["name"], font=title_font, fill="white")
    draw.text((300, 75), "Affiliated to AKTU", font=sub_font, fill="white")

    # QR Code
    qr_data = f"{student['roll']} | {student['name']}"
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_size = 200
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_x = CARD_WIDTH - qr_size - 50
    qr_y = 200
    card.paste(qr_img, (qr_x, qr_y))

    # Barcode (Code128)
    try:
        CODE128 = barcode.get_barcode_class('code128')
        bar = CODE128(student["roll"], writer=ImageWriter())
        bar_fname = "barcode_temp"
        bar_path = bar_fname + ".png"
        bar.save(bar_fname)
        bar_img = Image.open(bar_path)
        bar_img = bar_img.resize((400, 100))
        bar_x = 580
        bar_y = 420
        card.paste(bar_img, (bar_x, bar_y))
        os.remove(bar_path)
    except Exception as e:
        print("Barcode generation error:", e)

    # Text fields
    x0 = 50
    y0 = 200
    lines = [
        f"Address: {college['address']}",
        f"Contact: {college['contact']}  |  Toll-Free: {college['toll_free']}",
        emergency_contact,
        "",
        "Rules & Instructions:",
        "- This card is the property of MPGI and must be returned upon request.",
        "- Any misuse or alteration is punishable under institute policy.",
        "- Carry this card always while on campus.",
        "- If found, please return to the college office."
    ]
    for ln in lines:
        draw.text((x0, y0), ln, font=body_font, fill=(10,10,10))
        y0 += 30

    # Footer
    draw.text((20, CARD_HEIGHT - 30), f"{college['website']}    |    {college['name']}", font=footer_font, fill=(80,80,80))

    # Underline stripe
    draw.line([(20, HEADER_HEIGHT), (CARD_WIDTH - 20, HEADER_HEIGHT)], fill=(88,152,62), width=6)

    card = card.convert("RGB")
    card.save(output_back)
    print(f"✅ Back side ID card saved at: {output_back}")

# --- Run ---
generate_front(background_path=background_front, alpha=50)
generate_back(background_path=background_back, alpha=100)
