import qrcode
from io import BytesIO
from django.core.files import File
from django.core.mail import EmailMessage
from django.conf import settings

def parse_csv(reader):
    emails = []
    next(reader, None)
    qr_codes = []
    for row in reader:
        email = row[1] # This is the current email slot in the CSV file.
        qr_code_image = generate_qr_code(email)
        send_email_with_qr_code(email, qr_code_image)

def generate_qr_code(email):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(email)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def send_email_with_qr_code(email, qr_code_image):
    subject = 'Your QR Code for Event Check-in'
    body = 'Please use the attached QR code to check in at the event.'
    email_message = EmailMessage(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    email_message.attach(f'{email}.png', qr_code_image.getvalue(), 'image/png')
    email_message.send()