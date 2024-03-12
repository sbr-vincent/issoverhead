import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import smtplib
import time

load_dotenv()
MY_LAT = 34.052235 # Your latitude
MY_LONG = -118.243683 # Your longitude
MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')


# Your position is within +5 or -5 degrees of the ISS position.
def in_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        if MY_LAT-5 <= iss_latitude <= MY_LAT+5:
            return True

    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

    return False


# If the ISS is close to my current position
# and it is currently dark
while True:
    time.sleep(60)
    if in_position() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Check Out the Sky\n\nThe ISS is above you!!!"
            )
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



