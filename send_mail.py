import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(to_email, subject, message_body, attachment_path=None):
    # SMTP server configuration
    smtp_server = 'localhost'  # Change to your SMTP server or use localhost for testing
    smtp_port = 8000           # Default for MailHog or change to your server's port
    from_email = 'your_email@theankit.com'  # Your email address
    password = ''  # Only needed if using a real server like Gmail

    # Create the message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    # Add attachment if provided
    if attachment_path:
        try:
            # Open the file in binary mode
            with open(attachment_path, "rb") as attachment:
                # Create a MIMEBase object
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode the payload in Base64
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path.split('/')[-1]}"
            )

            # Attach the file to the email
            msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file. Error: {e}")

    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        # If using a real SMTP server (like Gmail), you'll need to login
        # server.starttls()  # Uncomment this line if you're using a server with TLS (e.g., Gmail)
        # server.login(from_email, password)
        
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

if __name__ == "__main__":
    to_email = "recipient@theankit.com"  # Replace with the recipient's email
    subject = "Test Email with Attachment"
    message_body = "Hello, this email contains an attachment."
    attachment_path = "/home/ankit/Ankit/projects/Python_Mail_server/attachment.pdf"  # Replace with the path to your attachment

    send_email(to_email, subject, message_body, attachment_path)
