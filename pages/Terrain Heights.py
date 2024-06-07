import streamlit as st
import requests
import folium
import pydeck as pdk
from streamlit_folium import folium_static


st.title("Elevation Information")
api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ"
if "origin" not in st.session_state:
    st.session_state.origin = ""
if "destination" not in st.session_state:
    st.session_state.destination = ""
def categorize_location(height):
    if height < 600:
        return "Lowland"
    elif 600 <= height < 1500:
        return "Hilly Region (Low Hills)"
    elif 1500 <= height < 2500:
        return "Mid-Hills"
    elif 2500 <= height < 3500:
        return "High Hills"
    elif 3500 <= height < 4500:
        return "Alpine Region"
    else:
        return "Snow-Capped Peaks and Glaciers"


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
# User input for origin coordinates

st.session_state.origin = st.text_input("Enter Origin Coordinates (Will be pulled from sales data)",value =  st.session_state.origin)
st.session_state.destination = st.text_input("Enter Destination Coordinates (Will be pulled from sales data)", value = st.session_state.destination)






submit_button = st.button('Submit')
if submit_button:
  
    origin_lat = float(st.session_state.origin.split(",")[0])
    origin_lon = float(st.session_state.origin.split(",")[1])
    dest_lat = float(st.session_state.destination.split(",")[0])
    dest_lon = float(st.session_state.destination.split(",")[1])

    origin_elevation = get_elevation(origin_lat, origin_lon,api_key)
    dest_elevation = get_elevation(dest_lat, dest_lon,api_key)

    origin_category = categorize_location (origin_elevation)

    destination_category = categorize_location(dest_elevation)

    st.write(f"Origin Elevation: **{origin_elevation} meters**")
    st.write((f"The location is in the category: **{origin_category}**"))
    st.write(f"Destination Elevation: **{dest_elevation} meters**")
    st.write(f"The location is in the category: **{destination_category}**")

    midpoint_lat = (origin_lat + dest_lat) / 2
    midpoint_lon = (origin_lon + dest_lon) / 2
    m = folium.Map(location=[midpoint_lat, midpoint_lon], zoom_start=16)

    # Add markers for origin and destination
    folium.Marker([origin_lat, origin_lon], popup="Origin").add_to(m)
    folium.Marker([dest_lat, dest_lon], popup="Destination").add_to(m)

    # Add a polyline for the actual route
    # folium.PolyLine(locations=route_coordinates, color="blue").add_to(m)

    # Set the map view to fit the bounds of the polyline
    sw = [min(origin_lat, dest_lat), min(origin_lon, dest_lon)]
    ne = [max(origin_lat, dest_lat), max(origin_lon, dest_lon)]

    # Set the map view to fit the bounds
    m.fit_bounds([sw, ne])


    # Display the map
    folium_static(m)


    # Display results


    # You can further visualize this data using a map library (e.g., Folium or PyDeck).

