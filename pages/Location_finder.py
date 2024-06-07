import streamlit as st
import geopy
import requests
api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ" # Replace with your Bing Maps API key

def get_district_from_postal_code(api_key, postal_code):
    base_url = "https://dev.virtualearth.net/REST/v1/Locations"
    query_params = {
        "postalCode": postal_code,
        "key": api_key,
    }

    try:
        response = requests.get(base_url, params=query_params,verify=False)
        data = response.json()

        if "resourceSets" in data and data["resourceSets"]:
            location = data["resourceSets"][0]["resources"][0]
            address = location.get("address")
            district = address.get("locality")  # District information

            return district
        else:
            return None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def address_to_coordinates(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude
geolocator = geopy.geocoders.Bing(api_key)

if "pincode" not in st.session_state:
    st.session_state.pincode = ""

st.session_state.pincode = st.text_input("Enter PinCode of the destination",value=st.session_state.pincode)

submit_button = st.button('Submit')
if submit_button:
    latitude,longitude = address_to_coordinates(st.session_state.pincode)
    district = get_district_from_postal_code(api_key,st.session_state.pincode)
    if district:
        st.write(f"The district for postal code {st.session_state.pincode} is {district}.")
    else:
        st.write(f"Unable to retrieve district information for postal code {st.session_state.pincode}.")

    st.write(f"Coordinates for the location = {latitude}, {longitude} ")






