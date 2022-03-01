import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
FROM_EMAIL = "dani.day.32.python@gmail.com"
PASSWORD = os.environ["PYTHON_MAIL_PASSWORD"]
TO_EMAIL = "dest_mail@client.com"


class NotificationManager:
    def __init__(self, flight_search):
        self.flight_search = flight_search

    def send_mail(self):
        if self.flight_search.found_flights:
            email_message = EmailMessage()
            email_message.set_content(self.email_message())
            email_message["From"] = FROM_EMAIL
            email_message["To"] = TO_EMAIL
            email_message["Subject"] = self.email_subject()
            with smtplib.SMTP(SMTP_SERVER) as connection:
                print("Sending email...")
                connection.starttls()
                connection.login(user=FROM_EMAIL, password=PASSWORD)
                connection.send_message(email_message)
                print("Email sent")
        else:
            print("No flights found. No need to send mail.")

    def email_subject(self):
        subj = "✈️  Cheap flights to "
        for city in self.flight_search.possible_cities:
            subj += f"{city}, "
        return subj[:-2] + "."

    def email_message(self):
        msg = "Found the following cheap trips:\n\n"
        for trip in self.flight_search.possible_trips:
            msg += f"To {trip['destination']} for {trip['price']}€ " \
                   f"leaving on {trip['departure_date'][:-6]} and returning on {trip['return_date'][:-6]}\n" \
                   f"Departure flight: {trip['leave_flight']} from {trip['departure']}-{trip['leave_departure_airport']} " \
                   f"to {trip['destination']}-{trip['leave_arrival_airport']} on {trip['departure_date']}\n" \
                   f"Return flight: {trip['return_flight']} from {trip['destination']}-{trip['return_departure_airport']} " \
                   f"to {trip['departure']}-{trip['return_arrival_airport']} on {trip['return_date']} (arriving at {trip['arrival_date']})\n\n"
        return msg
