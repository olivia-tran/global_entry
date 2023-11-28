#!/usr/bin/env python
"""Check for Global Entry interview openings in your city."""
from twilio.rest import Client
import requests
import datetime
import os
import sys
from dotenv import load_dotenv
load_dotenv()


def log(text):
    """Write a one-line log message."""
    print("{dt}\t{msg}".format(
        dt=datetime.datetime.now(),
        msg=text))


def send_start_message():
    """Send a message that the script has started."""
    client = Client(
        os.environ.get('TWILIO_ACCOUNT'),
        os.environ.get('TWILIO_TOKEN')
    )
    message = client.messages.create(
        to=os.environ.get('TO_NUMBER'),
        from_=os.environ.get('TWILIO_FROM_NUMBER'),
        body="Script has started"
    )
    log("Start message sent")


if __name__ == '__main__':
    print("script started")
    send_start_message()  # Send a message that the script has started
    now = datetime.datetime.now()
    delta = datetime.timedelta(weeks=int(os.environ.get('LOOK_AHEAD_WEEKS')))
    future = now + delta
    request_url = os.environ.get('GLOBAL_ENTRY_QUERY_URL').format(
        timestamp=future.strftime("%Y-%m-%d"))
    result = requests.get(request_url).json()
    cities = [o.get('city').lower() for o in result]

    search_string = os.environ.get('SEARCH_STRING').lower()
    if search_string in cities:
        client = Client(
            os.environ.get('TWILIO_ACCOUNT'),
            os.environ.get('TWILIO_TOKEN')
        )
        message = client.messages.create(
            to=os.environ.get('TO_NUMBER'),
            from_=os.environ.get('TWILIO_FROM_NUMBER'),
            body=f"Global Entry interview opportunity in {search_string} \
opened up just now!")
        log("text message sent")
        sys.exit(0)
    log("no news")
    sys.exit(1)
