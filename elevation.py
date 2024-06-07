import requests

def get_elevation(lat, lon, api_key):
    base_url = "http://dev.virtualearth.net/REST/v1/Elevation/List"
    params = {
        "points": f"{lat},{lon}",
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "resourceSets" in data and data["resourceSets"]:
            elevations = data["resourceSets"][0]["resources"][0]["elevations"]
            return elevations[0]  # Elevation in meters
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching elevation data: {e}")
        return None

if __name__ == "__main__":
    # latitude = 47.6062  # Replace with your desired latitude
    # longitude = -122.3321  # Replace with your desired longitude
    latitude = 28.69957156909607
    longitude = 77.09662333997034
    api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ"  # Replace with your actual API key

    elevation = get_elevation(latitude, longitude, api_key)
    if elevation is not None:
        print(f"Elevation at ({latitude}, {longitude}): {elevation} meters")
    else:
        print("Error fetching elevation data.")
