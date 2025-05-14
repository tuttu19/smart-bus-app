import qrcode
import os

QR_DIR = "generated_qr"

def generate_qr(data, filename):
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)

    path = os.path.join(QR_DIR, filename)
    qr = qrcode.make(data)
    qr.save(path)
    return path
