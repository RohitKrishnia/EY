import streamlit as st
from calculator import new_calculator
from visual import make_graph, stacked_bar_graph
import pandas as pd
from st_aggrid import AgGrid
import requests
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



st.set_page_config(layout="wide",page_title= "Freight Estimator")


col1, col2 = st.columns([0.3,0.7], gap= "large")


api_key = "AmetSecxnjXnu1gNdjM0CsdD-IFZu2D6aIeZq4odevpoCWe0Ru4xNHSwivJvp4gQ"

distance_km = get_distance(26.998745, 75.880252, 28.322013, 77.169248, api_key)

if "distance" not in st.session_state:
    st.session_state.distance = 0
if "origin" not in st.session_state:
    st.session_state.origin = ""
if "destination" not in st.session_state:
    st.session_state.origin = ""
if "weight" not in st.session_state:
    st.session_state.weight = 0
if "mileage" not in st.session_state:
    st.session_state.mileage = 0



# Centered title using Markdown
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


with col1:
    st.markdown("<h1 style='text-align: center;'>Freight Assessment Tool </h1>", unsafe_allow_html=True)
    # st.title("Freight Assessment Tool")
    # st.session_state.origin = st.text_input("Enter Origin Coordinates",value =  st.session_state.origin)
    # st.session_state.destination = st.text_input("Enter Destination Coordinates", value = st.session_state.destination)
    st.write("Origin and destination will be pulled from sales order and distance will be calculated accordingly")
    st.session_state.distance = st.number_input("Distance (in kilometers)", min_value=0.0, max_value=500.0,value= float(st.session_state.distance), step=1.0) 
    st.session_state.weight = st.number_input("Weight in metric ton (in 1000 Kg) [Will be pulled from Sales data]",value = float(st.session_state.weight), min_value=0.0,max_value=45.0, step=1.0)
    truck_types = ['Trailer', 'Bulker', 'Truck']
    truck_type = st.selectbox('Select Vehicle Type [Default selection as per payload, can be changed manually]', truck_types,index=2)
    st.session_state.mileage = st.number_input("Mileage with load in kmpl [Has to be written as a function of vehicle type & Payload]",value = float(st.session_state.mileage), max_value = 15.0 ,min_value=0.0, step=1.0)
    if(truck_type == "Bulker"):
        is_bulk_cement = "Yes"
    else:
        is_bulk_cement = "No"
    reverse_logistics = st.radio("Reverse Haulage applicable? (Will be pulled from purchase register) ", ["Yes", "No"],key = "Yes")
    submit_button = st.button('Submit')
    

with col2:
  
   if submit_button:
        st.markdown("<h1 style='text-align: center;'>Cost Headers vs Values </h1>", unsafe_allow_html=True)
        cost_headers_values_dict, total_cost= new_calculator(st.session_state.distance,st.session_state.weight,truck_type,is_bulk_cement,reverse_logistics,st.session_state.mileage)
        temp = sorted(cost_headers_values_dict.items(),key=lambda item: item[1])
        keys = []
        values = []
        for key,value in temp:
            keys.append(key)
            values.append(value)     
        # st.write(f" Total cost for transportation =  {toal_cost}")
        # st.write (f"PTPK price = {toal_cost/(distance*weight)}")
        final_data = {'Total Price ': f"₹ {round(total_cost,2)}",'PTPK' : f" ₹ {round(total_cost/(st.session_state.distance*st.session_state.weight),2)}"}
        # final_data = {'Total Price ': f"₹ {toal_cost}"}
        dct = {k:[v] for k,v in final_data.items()}  # WORKAROUND
        new_dict = {}
        for key,value in cost_headers_values_dict.items():
            new_dict[key] = value*100 / total_cost
        
        finaldf = pd.DataFrame(dct)
        
        # st.dataframe(percentage_df,hide_index=True)
        # st.write(finaldf.style.hide())
        st.plotly_chart(make_graph(keys,values))
        # st.box("Graph Container", make_graph(keys,values))
        st.dataframe(finaldf,hide_index=True,use_container_width=True)
        # st.write(finaldf.shape)
        # AgGrid(finaldf)
        
        # st.dataframe(finaldf.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]), hide_index=True)


