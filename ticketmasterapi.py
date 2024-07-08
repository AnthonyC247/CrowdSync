import requests 
import os
import json
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

#Preqs for the TicketMaster API credentials defined in .env

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events"
#BASE_URL = os.environ.get('BASE_URL')

#BASE_URL = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword='concert'&apikey={API_KEY}&description=1"
#url:"https://app.ticketmaster.com/discovery/v2/events.json?size=1&apikey={apikey}", for reference

response = requests.get(BASE_URL)

print(API_KEY)
print(API_SECRET)
print(BASE_URL)
#print(response.json())
pprint(response.json())

def get_event_details (event_id):
    '''retrieve info about a specific event
        input: event_id (str) identifier to retrieve details for
        return: dictionary containing event name's, date, venue, attractions and return None if request failed or event not found

    '''
    #construct url for specific event
    url = f"{BASE_URL}/{event_id}"

    search_params = {
        "apikey": API_KEY
    }

    #make the GET request to the TicketMasterAPI 
    response = requests.get(url, params=search_params)

    #check if response okay (if it is 200)
    if response.status_code == 200:
        event_data = response.json() #parse the data 
        event_obj = {}

        #extract relevant event details
        event_obj['name'] = event_data["name"]
        event_obj['date'] = event_data["dates"]["start"]["localDate"]
        event_obj['venue'] = event_data['_embedded']['venues'][0]['name']
        attractions = event_data["_embedded"]["attractions"]
        event_obj['attractions'] = [attractions[i]['name'] for i in range(len(attractions))]
        return event_obj

def search_events(search):

    '''searching for events based on a search type string using the TicketMasterAPI

    Inputs: search (string): The search keyword to query for events


    Outputs: return list of dictionaries holding info about found events
         each dictionary includes the names, date

    '''

    #define the search parameters including the apikey and the search keyword
    search_params = {
        "apikey": API_KEY,
        "keyword": search,
        "size": 10 #Amount of results to grab

    }

    #make the GET request to the TicketMasterAPI to search for events
    response = requests.get(BASE_URL, params=search_params)

    if response.status_code == 200:
        data = response.json()
        events = data["_embedded"]["events"] #extract the list of the events

        for event in events:
            event_id = event["id"]
            print(get_event_details(event_id))
    else:
        print("Error:", response.status_code)

search = input("Search for an event: ")
search_events(search)

    
