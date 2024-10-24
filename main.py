import asyncio
from aiosmtpd.controller import Controller
import email


class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('handle Data')
        print('Arrgs',server.hostname, session.host_name, envelope.mail_from, envelope.content.decode('utf-8'))
        print(envelope.original_content)
        print('swad', email.message_from_string(envelope.content.decode('utf-8')))
        email_message = email.message_from_string(envelope.content.decode('utf-8'))
        print(email_message.get('body'), type(email_message))
        # print('kw',kwargs)
        return '250 OK'


    async def handle_HELO(self,server, session, envelope, hostname):
        print('this is HELO method')
        print(server,session,envelope,hostname)
        print("end of HELO")
        return '250 {}'.format(server.hostname)

    # async def handle_MAIL(self, *args, **kwargs):
    #     print('handel mail')
    #     print('Arrgs',args)
    #     print('kw',kwargs)
    #     return '250 OK'

    # async def handle_RCPT(self, *args, **kwargs):
    #     print('handel RCPT')
    #     print('Arrgs',args)
    #     print('kw',kwargs)
    #     return '250 OK'

    # async def handle_EHLO(self,server, session, envelope, hostname, *args, **kwargs):
    #     print('handel EHLO',server,session,hostname)
    #     print('Arrgs',args)
    #     print('kw',kwargs)
    #     return '250 OK'


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
