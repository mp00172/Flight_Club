from data_and_keys import *
from email.message import EmailMessage
import ssl
import smtplib

EMAIL_RECEIVERS = [
    "martin.petracic@gmail.com"
]

EMAIL_SUBJECT = "CHEAP FLIGHT notification"
EMAIL_BODY_HEADER_TEXT = "We found some interesting offers for you!"
EMAIL_BODY_HEADER_BACKGROUNDCOLOR = "#867070"
EMAIL_BODY_HEADER_TEXTCOLOR = "#F5EBEB"
EMAIL_BODY_DIV_BACKGROUNDCOLOR1 = "#F5EBEB"
EMAIL_BODY_DIV_BACKGROUNDCOLOR2 = "#E4D0D0"
EMAIL_BODY_DIV_TEXTCOLOR = "#867070"

EMAIL_HTML_START = """
<!DOCTYPE html>
<html>
    <body>
"""

EMAIL_HTML_HEADER = """
        <div style="background-color:{};padding:5px 10px;">
            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color{};"><center>{}</center></h2>
        </div>
"""

EMAIL_HTML_FLIGHT_ENRTY = """
        <div style="background-color:{};padding:1px 5px;">
            <p>{} ({}) - {} ({})
            <br>Price: {} {}
            <br>Departure: {} at {} (local time)
            <br>Arrival: {} at {} (local time)
            <br>Nights in destination: {}
            <br><a href="{}">Open flight details</a></p>
        </div>
"""

EMAIL_HTML_END = """
    </body>
</html>
"""


class NotificationManager:
    def __init__(self):
        self.email_body = """"""

    def create_email_body(self, flight_data):
        self.email_body += EMAIL_HTML_START
        self.email_body += EMAIL_HTML_HEADER.format(EMAIL_BODY_HEADER_BACKGROUNDCOLOR,
                                                    EMAIL_BODY_HEADER_TEXTCOLOR,
                                                    EMAIL_BODY_HEADER_TEXT)
        count = 2
        for flight in flight_data:
            if count % 2 == 0:
                self.email_body += EMAIL_HTML_FLIGHT_ENRTY.format(EMAIL_BODY_DIV_BACKGROUNDCOLOR1,
                                                                  flight["cityFrom"], flight["countryFromCode"],
                                                                  flight["cityTo"], flight["countryToCode"],
                                                                  flight["price"], flight["currency"],
                                                                  flight["departureDate"],
                                                                  flight["departureLocalTime"], flight["arrivalDate"],
                                                                  flight["arrivalLocalTime"],
                                                                  flight["nightsInDestination"], flight["deepLink"])
            else:
                self.email_body += EMAIL_HTML_FLIGHT_ENRTY.format(EMAIL_BODY_DIV_BACKGROUNDCOLOR2,
                                                                  flight["cityFrom"], flight["countryFromCode"],
                                                                  flight["cityTo"], flight["countryToCode"],
                                                                  flight["price"], flight["currency"],
                                                                  flight["departureDate"],
                                                                  flight["departureLocalTime"], flight["arrivalDate"],
                                                                  flight["arrivalLocalTime"],
                                                                  flight["nightsInDestination"], flight["deepLink"])
            count += 1
        self.email_body += EMAIL_HTML_END

    def send_emails(self):
        for email_receiver in EMAIL_RECEIVERS:
            em = EmailMessage()
            em["From"] = GMAIL_USERNAME
            em["To"] = email_receiver
            em["Subject"] = EMAIL_SUBJECT
            em.set_content(self.email_body, subtype="html")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(GMAIL_USERNAME, GMAIL_SECURITY_CODE)
                smtp.sendmail(GMAIL_USERNAME, email_receiver, em.as_string())
            print("Email sent to {}".format(email_receiver))
