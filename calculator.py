import math
import pandas as pd
# df_sheet_name = pd.read_excel('Valid Freights 01052024.xlsx', sheet_name='Sheet1')
def emi_calculator(truck_price, int_rate, tenure_in_years):
    int_rate = int_rate / (12 * 100)  # Monthly interest rate
    tenure_in_months = tenure_in_years*12
    emi = (truck_price * int_rate * pow(1 + int_rate, tenure_in_months)) / (pow(1 + int_rate, tenure_in_months) - 1)
    return emi


toll_per_km = 7
avg_distance_trabelled_per_day = 250
driver_monthly_salary = 25000
helper_monthly_salary = 15000
tyre_life = 70000
tyre_price = 25000
maintenance_per_month = 10000
permit_cost_per_month = 10000
loan_tenure_years = 10
int_rate = 13
loading_unloading_cost_per_bag = 1
packaging_cost_per_bag = 10
weight_of_single_bag = 50
fuel_price = 90
mileage_with_load = 2.5
mileage_without_load = 4
distance_travelled_per_month = 8000
no_of_days_driver_helper_work_in_a_month = 20
transporter_margin = 0.08



trailer_data = {
    'Payload Capacity (Tons)': [35, 42],
    'Number of Tires': [18,22],
    'Ex-showroom Price (approx.)': [4000000, 6000000]
}

truck_data = {
    'Payload Capacity (Tons)': [2.5,7.5,10,14,22,32,38],
    'Number of Tires': [4,6,6,10,10,14,16],
    'Ex-showroom Price (approx.)': [1200000,2300000,2500000,3300000,3500000,4000000, 4400000]
}

bulker_data = {
    'Payload Capacity (Tons)': [42],
    'Number of Tires': [18],
    'Ex-showroom Price (approx.)': [6000000]
}


Truckdf = pd.DataFrame(truck_data)
Bulkerdf = pd.DataFrame(bulker_data)
Trailerdf = pd.DataFrame(trailer_data)

mapping = {"Truck":Truckdf,"Bulker":Bulkerdf,"Trailer":Trailerdf}

def get_truck_details(weight,truck_type):
    df = mapping[truck_type]
    for index, row in df.iterrows():
        if weight <= row['Payload Capacity (Tons)']:
            return row['Number of Tires'], row['Ex-showroom Price (approx.)']
    # If weight exceeds the highest payload capacity, return the details for the highest capacity
    return df.iloc[-1]['Number of Tires'], df.iloc[-1]['Ex-showroom Price (approx.)']


def new_calculator(distance,weight,truck_type,is_bulk_cement,reverse_logistics,mileage):
    
    no_of_days = math.ceil(distance/avg_distance_trabelled_per_day)
    fuel_cost = distance*fuel_price/mileage
    toll_cost = distance * toll_per_km
    days_for_trip = math.ceil(distance/avg_distance_trabelled_per_day)
    driver_and_helper_cost = (driver_monthly_salary + helper_monthly_salary)*math.ceil((no_of_days/no_of_days_driver_helper_work_in_a_month))
    no_of_tyres,truck_price = get_truck_details(weight,truck_type)
    emi = emi_calculator(truck_price,int_rate,loan_tenure_years)
    maintenance_cost = 10000*distance/distance_travelled_per_month
    permit_cost = 10000*distance/distance_travelled_per_month
    emi_cost = emi*distance/distance_travelled_per_month
    driver_helper_food_cost = 400*days_for_trip
    driver_and_helper_cost = (driver_monthly_salary + helper_monthly_salary)*distance/distance_travelled_per_month
    admin_cost = 0
    tyre_cost = distance*(tyre_price/tyre_life)*no_of_tyres
    if(is_bulk_cement == "No"):
        loading_unloading_cost = 2*loading_unloading_cost_per_bag*weight*1000/weight_of_single_bag
        packaging_cost = weight*1000*packaging_cost_per_bag/weight_of_single_bag
    else:
        loading_unloading_cost = 0
        packaging_cost = 0

    
    total_cost = (1+ transporter_margin) * (admin_cost + \
            loading_unloading_cost + \
            driver_helper_food_cost + \
            emi_cost + \
            permit_cost + \
            maintenance_cost + \
            tyre_cost + \
            driver_and_helper_cost + \
            toll_cost + \
            fuel_cost)
    
    if(reverse_logistics == "No"):
       
        total_cost = total_cost* 1.5* (1+ transporter_margin)
       
    return {"admin_cost":admin_cost,"loading_unloading_cost":loading_unloading_cost, \
            "driver_helper_food_cost":driver_helper_food_cost,\
        "emi_cost":emi_cost,"permit_cost":permit_cost,"maintenance_cost":maintenance_cost,\
        "tyre_cost":tyre_cost,"driver_and_helper_cost":driver_and_helper_cost, \
        "toll_cost":toll_cost,"fuel_cost":fuel_cost},total_cost




    

    
    



# def calculate(distance,fuel_price,mileage_with_load,mileage_without_load,weight,bulk,no_of_tyres,emi):
#     fuel_cost = distance*fuel_price/mileage_with_load + distance*fuel_price/mileage_without_load
#     toll_cost = distance * 2 * toll_per_km
#     days_for_trip = math.ceil(distance/avg_distance_trabelled_per_day)*2
#     driver_and_helper_cost = (driver_monthly_salary + helper_monthly_salary)*days_for_trip/30
#     tyre_cost = distance*2*(tyre_price/tyre_life)*no_of_tyres
#     maintenance_cost = 10000*days_for_trip/30
#     permit_cost = 10000*days_for_trip/30
#     emi_cost = emi*days_for_trip/30
#     driver_helper_food_cost = 400*days_for_trip*2
#     if(bulk == "No"):
#         loading_unloading_cost = 2*loading_unloading_cost_per_bag*weight_in_ton*1000/weight_of_single_bag
#         packaging_cost = weight_in_ton*1000*packaging_cost_per_bag/weight_of_single_bag
#     else:
#         loading_unloading_cost = 0
#         packaging_cost = 0

#     admin_cost = 1
#     total_cost = admin_cost + \
#                 loading_unloading_cost + \
#                 packaging_cost + \
#                 driver_helper_food_cost + \
#                 emi_cost + \
#                 permit_cost + \
#                 maintenance_cost + \
#                 tyre_cost + \
#                 driver_and_helper_cost + \
#                 toll_cost + \
#                 fuel_cost
    
#     # print(total_cost)
#     return {"admin_cost":admin_cost,"loading_unloading_cost":loading_unloading_cost, \
#             "packaging_cost":packaging_cost \
#             ,"driver_helper_food_cost":driver_helper_food_cost,\
#         "emi_cost":emi_cost,"permit_cost":permit_cost,"maintenance_cost":maintenance_cost,\
#         "tyre_cost":tyre_cost,"driver_and_helper_cost":driver_and_helper_cost, \
#         "toll_cost":toll_cost,"fuel_cost":fuel_cost}
                
                


    








#     return False




    




    