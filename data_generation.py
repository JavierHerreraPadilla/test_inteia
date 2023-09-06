import requests
from datetime import date
import csv
from app.schemas import EventCreate

url="http://127.0.0.1:8000/"
post_url = "http://127.0.0.1:8000/create_event"


def post_data(event: dict):
    response = requests.post(post_url,  json=event)
    return response


with open("data.csv", "r") as d:
    reader = csv.DictReader(d)

    for row in reader:
        r = post_data(row)
        print(r.status_code)


print("Events added", "\n", requests.get(url=url).json())


def delete_data():
    data = len(requests.get(url).json())
    for i in range(1, data + 1):
        r = requests.delete(url+"del/"+f"{i}")
        print(r.status_code)


#dict e serves to make an incorrect post request. Incorrect 'type' and missing date
e = {'name': 'Comp A', 'type': 'comm', 'description': 'Lanzamiento de producto'}
