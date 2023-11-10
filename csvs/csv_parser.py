import qrcode
import base64
from io import BytesIO
from django.core.files import File
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

def parse_csv(reader):
    next(reader, None)
    for row in reader:
        # This is the current email slot in the CSV file.
        # This might need to change to grab needed values more intelligently.
        email = row[1]
        qr_code_image = generate_qr_code(email)
        send_email_with_qr_code(email, qr_code_image)

def generate_qr_code(email):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add additional information to QR code here.
    qr.add_data(email)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def send_email_with_qr_code(email, qr_code_image):
    qr_code_base64 = base64.b64encode(qr_code_image.getvalue()).decode()
    qr_code_url = f'data:image/png;base64,{qr_code_base64}'
    # These are values that will be injected into the HTML template.
    # These need to be passed into this function from where it's called.
    context = {
        'qr_code_url': qr_code_url
        # 'user_name': user_name,
        # 'event_name': event_name,
    }
    html_content = render_to_string('qr_email_template.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='Your subject here', # Update to correct subject line, and include the program's name.
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['yomen.tohmaz@gmail.com'] # Remove hard coding.
    )
    email.attach_alternative(html_content, "text/html")
    email.send()