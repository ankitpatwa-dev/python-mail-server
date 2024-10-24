import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, message_body):
    # SMTP server configuration
    smtp_server = 'localhost'  # Change to your SMTP server or use localhost for testing
    smtp_port = 8000           # Default for MailHog or change to your server's port (e.g., 587 for Gmail)
    from_email = 'your_email@example.com'  # Your email address
    password = ''  # Only needed if using a real server like Gmail

    # Create the message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

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
    to_email = "recipient@example.com"  # Replace with the recipient's email
    subject = "Test Email"
    message_body = "Hello, this is a test email from the local server."

    send_email(to_email, subject, message_body)
