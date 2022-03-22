
from twilio.rest import Client
import os

TWILIO_SD = "AC2aa8b84eb0d70d00cbbe48c4e84237b0"
TWILIO_AUTH_TOKEN = os.environ.get('API_TOKEN')
TWILIO_VIR_NUM = "+1xxxxxxxx"
TWILIO_VERIFIED_NUM = "+44xxxxxxx"


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SD, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIR_NUM,
            to=TWILIO_VERIFIED_NUM,
        )
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )