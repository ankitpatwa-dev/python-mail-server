import asyncio
from aiosmtpd.controller import Controller

class CustomSMTPHandler:
    async def handle_DATA(self, *args,**kwargs):
        print('handle Data')
        print('Arrgs',args)
        print('kw',kwargs)
        return '250 OK'

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
