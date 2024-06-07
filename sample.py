import requests
import pandas as pd

def get_distance(lat1, lon1, lat2, lon2, bing_maps_api_key):
    base_url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix"
    origins = f"{lat1},{lon1}"
    destinations = f"{lat2},{lon2}"
    travel_mode = "driving"  # You can change this to "walking" or "transit" if needed

    params = {
        "origins": origins,
        "destinations": destinations,
        "travelMode": travel_mode,
        "key": bing_maps_api_key,
    }

    response = requests.get(base_url, params=params, verify=False)
    data = response.json()

    if "resourceSets" in data and data["resourceSets"]:
        distance = data["resourceSets"][0]["resources"][0]["results"][0]["travelDistance"]
        return distance
    else:
        return None

# Example usage
bing_maps_api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ"
distance_km = get_distance(26.998745, 75.880252, 28.322013, 77.169248, bing_maps_api_key)
print(f"Distance between Green Park, Delhi and Nilgiris District: {distance_km} km")
