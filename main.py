import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import lxml.html

c = Calendar()

months = ["July", "August"]

url = "https://olympics.com/tokyo-2020/en/schedule/"

request = requests.get(url)

soup = BeautifulSoup(request.text, "lxml")

events = []

table = soup.find('div', class_="schBoxInner table-responsive")

eventsTable = soup.find('tbody')

for row in eventsTable.find_all('tr'):
    for column in row.find_all('img', src=True, alt=True):
        columnAlt = column['alt']
        columnAlt = columnAlt.split(" ")
        eventName = ""
        eventDate = ""

        for i in columnAlt:
            if i not in months and not i.isdigit() and '(' not in i:
                eventName += i + " "
            elif i in months and '(' not in i:
                if i == "July":
                    eventDate += "Jul-2021"
                    continue
                eventDate += "Aug-2021"
            elif i.isdigit():
                if i[0] == '0':
                    eventDate += i[1:] + "-"
                    continue
                elif "Round" in eventName and len(i) == 1:
                    print("lol")
                    eventName += i
                    continue
                eventDate += i + "-"

        e = Event()
        e.name = eventName
        if eventName == "Aquatics/Water Polo（Men）Final ":
            print("lol")
            eventDate = "7-Aug-2021"
        e.begin = datetime.strptime(eventDate, "%d-%b-%Y").strftime("%Y-%m-%d") + "00:00::00"
        c.events.add(e)

with open('my.ics', 'w') as f:
    f.write(str(c))

