import datetime
import ssl
import time
import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



success_sended = False

bike_url = "https://www.canyon.com/de-de/gravel-bikes/bike-packing/grizl/cf-sl/grizl-cf-sl-7-throwback/3107.html?dwvar_3107_pv_rahmenfarbe=R095_P05&dwvar_3107_pv_rahmengroesse=L"
bike_size = "L"

email_sender = "gravelbikechecker@googlemail.com"
email_password = "bcktpcupbyrexsui"
email_reciever = "florian.boldrick@googlemail.com"

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
            check_availability(availability)
        else:
            print("Found to many HTML Elements")

    else:
        print("Error occured while resolving URL")


def check_availability(element):
    if element is not None:
        if 'Bald verfügbar' in element.get_text():
            print("Bike is 'Bald verfügbar'")
        if 'Ausverkauft' in element.get_text():
            print("Bike is 'Ausverkauft'")
        if 'Niedriger Bestand' in element.get_text():
            print("Bike is 'Niedriger Bestand'")
            send_mail('Niedriger Bestand')
        if 'Auf Lager' in element.get_text():
            print("Bike is 'Auf Lager'")
            send_mail('Auf Lager')
    else:
        print('No Information about the Availability of that Bike')

def send_mail(status):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = email_subject
    em.set_content(email_body.format(bike_url))

    ssl_default_contect = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_default_contect) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())


if __name__ == '__main__':
    while True:
        if success_sended:
            print("Benachritigung wurde versendet | Exit")
            break
        else:
            print("Überprüfe Website")
            check_website(bike_url, bike_size)
        time.sleep(600)

