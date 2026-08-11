import os
import datetime as dt
import pandas
import random
import smtplib

now = dt.datetime.now()
current_month = float(now.month)
current_day = float(now.day)

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

df = pandas.read_csv("birthdays.csv")

birthdays = []

if current_month in df.month.values and current_day in df.day.values:
    birthday = df.loc[
        (df.month == current_month) &
        (df.day == current_day)
    ]
    birthdays = birthday.name.tolist()

for recipient in birthdays:
    num = random.randint(1,3)
    with open(f"letter_templates/letter_{num}.txt") as letter:
        letter_contents = letter.read()
        new_letter = letter_contents.replace("[NAME]",recipient)

    row = df[df.name == recipient]
    email = row.email.iloc[0]

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs=email,
                            msg=f"subject:Happy Birthday\n\n{new_letter}")
