import requests
import math
import json

def get_address(lat,long):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={long}"

    response = requests.get(url)
    try:
        data = response.json()

        if 'address' in data:
            address = data['address']
            road = address.get('road', '')
            suburb = address.get('suburb', '')
            city = address.get('city', address.get('town', ''))
            state = address.get('state', '')
            country = address.get('country', '')
            postcode = address.get('postcode', '')
            display = data["display_name"]

            specific_address = f"{road}, {suburb},{display}"
            return specific_address
        else:
            return ""
    except:
        return ""
    


def get_distance(coord1, coord2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of Earth in kilometers. Use 3956 for miles
    r = 6371
    return round(c * r,2)

from geopy.geocoders import Nominatim

def get_coordinates(address):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="my_geocoding_script_123")
    
    # Get location based on the address
    location = geolocator.geocode(address)
    
    if location:
        # Extract the latitude and longitude
        return location.latitude, location.longitude
    else:
        return None, None

#Example usage for an Indian address:
# address = "Mahima Tower, Bhubaneswar, Odisha 752101"
# latitude, longitude = get_coordinates(address)

# if latitude and longitude:
#     print(f"Latitude: {latitude}, Longitude: {longitude}")
# else:
#     print("Coordinates not found.")

#print(get_coordinates("Mahima Tower, Bhubaneswar, Odisha 752101"))