# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import datetime as dt
import os
import random
import smtplib
import pandas

# Read credentials passed in by GitHub Actions
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

today = dt.datetime.now()
month = today.month
day = today.day
today_date = (month, day)

birthdays = pandas.read_csv("birthdays.csv")
birthdays_list = {
    (row.month, row.day): row for (index, row) in birthdays.iterrows()
}

if today_date in birthdays_list:
    number = random.randint(1, 3)
    person = birthdays_list[today_date]["person_name"]
    person_email = birthdays_list[today_date]["email"]

    with open(f"letter_templates/letter_{number}.txt", "r") as letter_file:
        file = letter_file.read()
        new_letter = file.replace("[NAME]", person)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        message = f"Subject: Happy Birthday dear 🥳🎂! \n\n {new_letter}"
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=person_email,
            msg=message.encode("utf-8"),
        )
