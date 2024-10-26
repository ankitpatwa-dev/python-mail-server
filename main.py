import asyncio
from aiosmtpd.controller import Controller
import email
from email import message_from_string
import os


class CustomSMTPHandler:

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        print('This is RCPT')
        if not address.endswith('@theankit.com'):
            print('emnail is not for us')
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_HELO(self, server, session, envelope, hostname) -> str:
        # Log or print information about the HELO handshake
        print(f"Received HELO from client with hostname: {hostname}")
        # print(f"Server hostname: {server.hostname}")
        # print(f"Session information: {session}")
        # print(f"Envelope sender: {envelope.mail_from}")

        # Process or store any relevant information from the HELO command here
        response_message = f"250 Hello {hostname}, pleased to meet you"

        # Return the HELO response string
        return response_message

    # async def handle_EHLO(self, server, session, envelope, hostname, responses):
    #     print('First Call')
    #     # Base response acknowledging the EHLO command
    #     responses = [
    #         f"250-{server.hostname} Hello {hostname}, pleased to meet you",
    #         # "250-SIZE 10485760",  # Support for message size up to 10MB
    #         # "250-8BITMIME",       # Support for 8-bit MIME encoding
    #         # "250-STARTTLS",       # Support for STARTTLS for secure connections
    #         # "250 AUTH LOGIN PLAIN"  # Authentication mechanisms supported
    #         '250 HELP'
    #     ]
        
    #     # Print the list of EHLO responses for debugging
    #     print("EHLO Responses:", responses)

    #     return responses
    
    async def handle_MAIL(self, server, session, envelope, address, mail_options) -> str:
        # Log or print information about the MAIL FROM command
        # print(f"Received MAIL FROM command with address: {address}")
        # print(f"Server hostname: {server.hostname}")
        # print(f"Session details: {session}")
        # print(f"Envelope before processing: {envelope}")

        # Update the envelope with the sender's address
        envelope.mail_from = address

        # Process any mail options if needed
        if mail_options:
            print(f"Mail options received: {mail_options}")
            # Handle specific mail options here (e.g., SIZE, BODY=8BITMIME)

        # Return a 250 OK response to acknowledge the MAIL FROM command
        response_message = "250 OK"
        return response_message
    
    async def handle_DATA(self, server, session, envelope):
        print('handle Data')
        self.extracting_data(server,session,envelope)
        return '250 OK'

    def extracting_data(self, server, session, envelope):
        raw_content = envelope.content.decode('utf-8')

        # Parse the content as an email message
        email_message = message_from_string(raw_content)

        # Extract headers and body parts into a dictionary
        structured_data = {
            'server_hostname': server.hostname,
            'session_host_name': session.host_name,
            'from': email_message.get('From'),
            'to': email_message.get('To'),
            'subject': email_message.get('Subject'),
            'content': {
                'plain_text': None,  # Placeholder for plain text content
                'html': None         # Placeholder for HTML content
            },
            'attachments': []        # Placeholder for attachments
        }

        # Extract email body parts (plain text or HTML)
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                disposition = str(part.get('Content-Disposition'))

                # Get the plain text part
                if content_type == 'text/plain' and 'attachment' not in disposition:
                    structured_data['content']['plain_text'] = part.get_payload(decode=True).decode('utf-8')

                # Get the HTML part
                elif content_type == 'text/html' and 'attachment' not in disposition:
                    structured_data['content']['html'] = part.get_payload(decode=True).decode('utf-8')

                # Handle attachments
                elif 'attachment' in disposition:
                    attachment = {
                        'filename': part.get_filename(),
                        'content_type': part.get_content_type(),
                        'size': len(part.get_payload(decode=True))
                    }
                    self.handle_attachments(part, './mailAttachemnts/')
                    structured_data['attachments'].append(attachment)
        else:
            # Non-multipart email (single body)
            content_type = email_message.get_content_type()
            if content_type == 'text/plain':
                structured_data['content']['plain_text'] = email_message.get_payload(decode=True)
            elif content_type == 'text/html':
                structured_data['content']['html'] = email_message.get_payload(decode=True)

        # Print the structured data dictionary
        print('Structured Data Content:', structured_data)

        return structured_data

    def handle_attachments(self,part, save_dir):
        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Check if the part is an attachment
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            if filename:
                # Decode and save the attachment
                file_path = os.path.join(save_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Attachment saved to: {file_path}")
                return {
                    'filename': filename,
                    'content_type': part.get_content_type(),
                    'size': os.path.getsize(file_path),
                    'path': file_path
                }
        return None

# Create the SMTP controller and pass the handler class
controller = Controller(CustomSMTPHandler(), hostname='0.0.0.0', port=25)

if __name__ == "__main__":
    try:
        # Start the server
        controller.start()
        print("SMTP server running on port 25 jsut check it")
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        controller.stop()
