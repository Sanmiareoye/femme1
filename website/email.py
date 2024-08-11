import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

def send_email(from_addr, to_addr, subject, content, attachment_path=None):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    # Attach the body of the email
    body = MIMEText(content, 'plain')
    msg.attach(body)

    # Attach the file if provided
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{basename(attachment_path)}"'
                msg.attach(part)
        except FileNotFoundError:
            print(f"Error: The file '{attachment_path}' was not found.")

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login(from_addr, 'nuno nvvj meae vrip')  # Use the correct App Password for Gmail

    # Send the email
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
    server.quit()

    print("Email sent successfully!")
