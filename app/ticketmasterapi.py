import requests 
import os
import json
from pprint import pprint
from datetime import datetime
import certifi
import ssl
from geopy.geocoders import Nominatim
import geohash2
from dotenv import load_dotenv
load_dotenv()

#Preqs for the TicketMaster API credentials defined in .env
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events"

#turns zipcode into a geohash
def get_location(zip_code):
    try:
        print(f'zipcode {zip_code}')
        ctx = ssl.create_default_context(cafile=certifi.where())
        geolocator = Nominatim(user_agent="zip_to_latlon", ssl_context=ctx)
        location = geolocator.geocode(f"{zip_code}, USA")
        print(f'lat: {location.latitude}, long: {location.longitude}')
        if location:
            geohash = geohash2.encode(location.latitude, location.longitude, precision=5)
            return geohash
        else:
            return None
        
    except Exception as e:
        print(f"Error during geocoding: {e}")
        return None, None


def process_event_data(event_data):
    final_event_dict = {'num_events': 0, 'event_list': {}}

    # Check if _embedded and events exist in event_data
    if '_embedded' in event_data and 'events' in event_data['_embedded']:
        events = event_data['_embedded']['events']
        final_event_dict['num_events'] = len(events)
        
        for event in events:
            event_name = event['name']

            # Assume there's at least one venue
            venue = event['_embedded']['venues'][0]
            venue_name = venue['name']
            venue_address = f"{venue['address']['line1']}, {venue['city']['name']}, {venue['state']['stateCode']} {venue['postalCode']}"
            
            final_event_dict['event_list'][event_name] = {
                'event_name': event_name,
                'distance': event.get('distance', None),
                'images': event.get('images', []),
                'venue_name': venue_name,
                'venue_address': venue_address,
                'dates': event['dates'],
                'event_url': event['url']
            }
    return final_event_dict

def search_events(zip_city, start_date, end_date, query):

    #turns the start and end date into a valid format
    start = datetime.strptime(start_date, "%m/%d/%Y")
    end = datetime.strptime(end_date, "%m/%d/%Y")
    formatted_start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
    formatted_end = end.strftime('%Y-%m-%dT%H:%M:%SZ')
        
    search_params = {
        "apikey": API_KEY,
        "keyword": query,
        "startDateTime": formatted_start,
        "endDateTime": formatted_end,
        "includeTBA": "yes",
        "includeTBD": "yes",
        "radius": "300",
        "unit": "miles"
    }

    #checks if a zipcode or city was provided
    if zip_city.isdigit():
        geohash = get_location(zip_city)
        search_params["geoPoint"] = geohash
    else:
        search_params["city"] = zip_city
    
    response = requests.get(BASE_URL, params=search_params)

    if response.status_code == 200:
        event_data = response.json()
        if event_data.get('_embedded'):
            event_info = process_event_data(event_data)
            return event_info
        else:
           print("No events found.") 
    else:
        print(f"RESPONSE STATUS CODE: {response.status_code}")
        print(f"RESPONSE TEXT: {response.text}")

