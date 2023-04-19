import datetime
import logging
import ssl
import time
import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

success_sended = False

bike_url = "https://www.canyon.com/de-de/gravel-bikes/bike-packing/grizl/al/grizl-7/2709.html?dwvar_2709_pv_rahmenfarbe=GN"
# bike_url = "https://www.canyon.com/de-de/gravel-bikes/bike-packing/grizl/cf-sl/grizl-cf-sl-7-throwback/3107.html?dwvar_3107_pv_rahmenfarbe=R095_P05&dwvar_3107_pv_rahmengroesse=L"
bike_size = "S"

email_sender = "gravelbikechecker@googlemail.com"
email_password = "bcktpcupbyrexsui"
email_reciever = ["boldrick.isabel@gmail.com", "florian.boldrick@googlemail.com"]

email_subject = "Dein Fahrrad ist jetzt verfügbar"
email_body = f"""
Hi Isabel,

dein gewünschtes Fahrrad 'Canyon GRIZL 7 AL' ist jetzt verfügbar.
Sei schnell und schnapp es dir.

Nutze diesen Link um direkt auf die Seite zu gelangen: {bike_url}

Mit freundlichen Grüßen
Dein Gravel Bike Checker

"""


def check_website(url, size):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.find_all(attrs={'data-product-size': size})

        if len(elements) == 1:
            div = elements.pop()
            availability = div.find(class_='productConfiguration__availabilityMessage')
            return check_availability(availability)
        else:
            print("Found to many HTML Elements")
            return False

    else:
        print("Error occured while resolving URL")
        return False


def check_availability(element):
    if element is not None:
        if 'Bald verfügbar' in element.get_text():
            print("Bike is 'Bald verfügbar'")
            return False
        if 'Ausverkauft' in element.get_text():
            print("Bike is 'Ausverkauft'")
            return False
        if 'Niedriger Bestand' in element.get_text():
            print("Bike is 'Niedriger Bestand'")
            return send_mail('Niedriger Bestand')
        if 'Auf Lager' in element.get_text():
            print("Bike is 'Auf Lager'")
            return send_mail('Auf Lager')
    else:
        print('No Information about the Availability of that Bike')


def send_mail(status):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = ", ".join(email_reciever)
    em['Subject'] = email_subject
    em.set_content(email_body.format(bike_url))

    ssl_default_contect = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_default_contect) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())
        return True


if __name__ == '__main__':
    while True:
        if success_sended:
            print("Benachritigung wurde versendet | Exit")
            exit(0)
        else:
            print("Überprüfe Website")
            success_sended = check_website(bike_url, bike_size)
        time.sleep(60)
