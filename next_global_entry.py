#!/usr/bin/env python
"""Check for Global Entry interview openings in your city."""
from twilio.rest import Client
import requests
import datetime
import os
import time
from dotenv import load_dotenv
load_dotenv()


def log(text):
    """Write a one-line log message."""
    print("{dt}\t{msg}".format(dt=datetime.datetime.now(), msg=text))


def send_start_message():
    """Send a message that the script has started."""
    client = Client(os.environ.get('TWILIO_ACCOUNT'),
                    os.environ.get('TWILIO_TOKEN'))
    message = client.messages.create(
        to=os.environ.get('TO_NUMBER'),
        from_=os.environ.get('TWILIO_FROM_NUMBER'),
        body="Script has started"
    )
    log("Start message sent")


def check_openings():
    """Check for interview openings."""
    log("check_openings method started")
    now = datetime.datetime.now()
    delta = datetime.timedelta(weeks=int(os.environ.get('LOOK_AHEAD_WEEKS')))
    future = now + delta
    request_url = os.environ.get('GLOBAL_ENTRY_QUERY_URL').format(
        timestamp=future.strftime("%Y-%m-%d"))
    result = requests.get(request_url).json()
    cities = [o.get('city').lower() for o in result]

    search_string = os.environ.get('SEARCH_STRING').lower()
    log(f"search_string==== {search_string}")
    log(f"cities==== {cities}")
    log(f"delta==== {delta}")
    log(f"request_url==== {request_url}")
    log(f"result===== {result}")
    if search_string in cities:
        client = Client(os.environ.get('TWILIO_ACCOUNT'),
                        os.environ.get('TWILIO_TOKEN'))
        message = client.messages.create(
            to=os.environ.get('TO_NUMBER'),
            from_=os.environ.get('TWILIO_FROM_NUMBER'),
            body=f"Global Entry interview opportunity in {search_string} opened up just now!")
        log("text message sent")
    else:
        log("no news")


if __name__ == '__main__':
    while True:  # Continuous execution
        log("script started")
        send_start_message()
        check_openings()

        # Sleep for a certain amount of time before next check
        sleep_duration = 3600  # 1 hour in seconds, adjust as needed
        time.sleep(sleep_duration)
