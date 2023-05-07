import random
from twilio.rest import Client

account_sid = 'AC9bc3fe01eeb793284285e0f6d8c7de87'
auth_token = 'aa040c6927b0731e17afd90461f49620'
num = '+14345058895' 


def otp_created(mobile):

    otp = str(random.randint(000000, 999999)) 
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=f"Your otp is {otp}",
                        from_='+14345058895',
                        to=f'{mobile}'
                    )

    print(message.sid)
    return otp