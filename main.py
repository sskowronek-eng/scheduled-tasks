import requests
import os
import smtplib

api_key = os.environ.get("OWM_API_KEY")
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

my_lat = 42.652401
my_long = -83.132561

parameters = {
    "lat": my_lat,
    "lon": my_long,
    "cnt": 4,
    "appid": api_key
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()
data = response.json()
weather_id_list = [data["list"][number]["weather"][0]["id"] for number in range(0,4)
                   if data["list"][number]["weather"][0]["id"] < 700]

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    if len(weather_id_list) > 0:
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg="Subject:TUT TUT\n\n"
                                "Rain is in the forecast. Remember your umbrella!")
    else:
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg="Subject:FROM NOW ON\n\n"
                                "Blue skies smiling at me!")
