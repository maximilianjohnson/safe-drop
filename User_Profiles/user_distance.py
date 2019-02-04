from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def get_distance(address, city):
    geolocator = Nominatim(user_agent="SafeDrop", timeout=10) #timeout stops the search from ending before a result is found - far away locations may produce an error still
    user_location = geolocator.geocode("%s %s" %(address, city))
    safedrop_location = geolocator.geocode("6133 University Blvd Vancouver") #for now its the UBC nest
    distance = great_circle((user_location.latitude, user_location.longitude),(safedrop_location.latitude, safedrop_location.longitude)).kilometers
    return distance
