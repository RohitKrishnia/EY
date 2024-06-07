import requests

def get_route_data(start_coords, end_coords, api_key):
    url = f"http://dev.virtualearth.net/REST/V1/Routes/Driving"
    params = {
        'wp.0': start_coords,
        'wp.1': end_coords,
        'key': api_key,
        'routeAttributes': 'routePath,itinerary'
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def classify_road(name):
    if 'NH' in name or 'National Highway' in name:
        return 'National Highway'
    elif 'SH' in name or 'State Highway' in name:
        return 'State Highway'
    elif 'NE' in name or 'National Expressway' in name or 'Expressway' in name:
        return 'Expressway'
    else:
        return 'Other'

def parse_route_data(route_data):
    road_types = {
        'National Highway': 0,
        'State Highway': 0,
        'Expressway': 0,
        'Other': 0
    }
    total_distance = 0

    if route_data and 'resourceSets' in route_data and route_data['resourceSets']:
        resources = route_data['resourceSets'][0]['resources'][0]
        total_distance = resources.get('travelDistance', 0)  # Get the total distance for the route
        if 'routeLegs' in resources and resources['routeLegs']:
            for leg in resources['routeLegs']:
                for item in leg['itineraryItems']:
                    distance = item.get('travelDistance', 0)  # Distance in kilometers
                    road_name = ""
                    if 'details' in item:
                        for detail in item['details']:
                            if 'names' in detail and detail['names']:
                                road_name = detail['names'][0]
                                break
                    road_type = classify_road(road_name)
                    road_types[road_type] += distance
    return total_distance, road_types

def main():
    # Replace with your actual coordinates and API key
    start_coords = "28.7041,77.1025"  # Example: Delhi
    end_coords = "19.0760,72.8777"    # Example: Mumbai
    api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ"

    route_data = get_route_data(start_coords, end_coords, api_key)
    if route_data:
        total_distance, road_distances = parse_route_data(route_data)
        
        print(f"Total distance: {total_distance:.2f} km")
        print("Distance covered on each type of road:")
        for road_type, distance in road_distances.items():
            print(f"{road_type}: {distance:.2f} km")
        
        sum_distances = sum(road_distances.values())
        print(f"Sum of distances by road type: {sum_distances:.2f} km")
        if abs(sum_distances - total_distance) > 0.1:  # Allowing a small margin for floating-point errors
            print("Warning: Sum of distances by road type does not match total distance")
    else:
        print("Failed to retrieve route data.")

if __name__ == "__main__":
    main()
