import time

import requests
from datetime import datetime
import smtplib

my_email = "youremail@gmail.com"
my_pass = "generate password as new app password in gmail"

MY_LAT = 12.540010  # Your latitude
MY_LONG = 75.009677  # Your longitude


def is_up():
    response = requests.get(url="http://api.open-notify.org/iss-now.json") #ISS location API
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(iss_latitude)
    print(iss_longitude)
    # Your position is within +5 or -5 degrees of the ISS position.

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters) #Sunrise-Sunset API
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    reg_format_date = datetime.utcnow().isoformat() + "Z"  # convert to UTC
    my_hour = int(reg_format_date.split("T")[1].split(":")[0])

    if my_hour >= sunset or my_hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_up() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:  # smtp can change according to your Email.
            connection.starttls()
            connection.login(my_email, my_pass)
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg=f"Subject:Look Up\n\nISS is over your head")
    else:
        print("No ISS Found")
