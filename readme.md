# 🎓 Student ID Card Generator (Python, PIL, QR, Barcode)

Auther: Sumit Kumar

This project generates **front and back student ID cards** with customizable details like student photo, logo, signature, QR code, and barcode.  
It demonstrates how to use Python imaging and barcode libraries to create structured graphics.

⚠️ **Disclaimer**:  
This project is **strictly for learning purposes**. The generated ID cards **do not represent real IDs** and **must not be used for illegal, fraudulent, or official purposes**.  
Always respect privacy, institutional, and legal boundaries when experimenting with this code.

---

## ✨ Features

- **Front Side**
  - Logo
  - Student photo
  - Student details (Name, Roll No., Course, DOB, Address, Validity)
  - Authorized signature section
  - Footer with contact details
  - Optional **semi-transparent background**

- **Back Side**
  - Logo
  - QR code (encodes student roll number + name)
  - Barcode (Code128 for roll number)
  - Rules & instructions
  - Footer & header stripe
  - Optional **semi-transparent background**

---

## 🛠️ Libraries Used

- **[Pillow (PIL)](https://pillow.readthedocs.io/)** → For image creation, drawing, and text rendering.
- **[qrcode](https://pypi.org/project/qrcode/)** → To generate QR codes.
- **[python-barcode](https://pypi.org/project/python-barcode/)** → To generate barcodes (Code128).
- **[pillow (ImageWriter)](https://pillow.readthedocs.io/)** → To save barcodes as images.
- **os** → For temporary file handling (deletes barcode temp images after use).

---

## 📦 Installation

Make sure you have **Python 3.8+** installed. Then install dependencies:

```bash
pip install pillow qrcode python-barcode

```
run collegeid.py once dependecy is installed, output would be generated as ID_front and ID_back file.


Special Instructions:
Photo size would look better with size in multiple of 160*200.