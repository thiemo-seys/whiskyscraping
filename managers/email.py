import yagmail
from credentials.credentials_email import *

def send_email(sender=SENDER ,password=PASSWORD ,receiver=RECEIVER ,subject="new whisky bottles" ,message="New whisky bottles have been released!"):
        yag = yagmail.SMTP(sender,password)
        yag.send(
            to=receiver,
            subject=subject,
            contents=[message])