import requests
import csv

# STATICLY LOADING SOME DATA


# This script loads data from a csv file and generatets a post request to the API using his data 
# Includes a post_data function that sends a post request to the end point
# Includes a load_and_post function that takes load csv data from a file called data.csv and posts all the loaded data to the end point
# Includes a delete_data function that deletes all the events in the database
# You can run this script in interactive mode to use the functions as you please, running python -i data_generation.py in your console


url="http://127.0.0.1:8000/"
post_url = "http://127.0.0.1:8000/create_event"


def post_data(event: dict):
    global post_url
    """
    generates a post request 
    """
    response = requests.post(post_url,  json=event)
    return response


def load_and_post():
    """
    loads data from a file and posts it to the end point
    """
    with open("data.csv", "r") as d:
        reader = csv.DictReader(d)

        for row in reader:
            r = post_data(row)
            print(r.status_code)


def delete_events():
    """
    Deletes every single event recorded in the database
    """
    events = requests.get(url).json()
    for event in events:
        r = requests.delete(url+"del/"+str(event['id']))
        print(event['name'], "delete response:", r.status_code)


# dict e serves to make an incorrect post request. Incorrect 'type' and missing date
e = {'name': 'Comp A', 'type': 'comm', 'description': 'Lanzamiento de producto'}
