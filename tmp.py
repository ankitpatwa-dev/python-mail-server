import email
from email import message_from_string

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Handling Data')

        # Decode the envelope content
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

        return '250 OK'
