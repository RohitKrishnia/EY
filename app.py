import streamlit as st
from calculator import new_calculator
from visual import make_graph, stacked_bar_graph
import pandas as pd



def main():
    st.title("Freight Assessment Tool")
    distance = st.number_input("Distance (in kilometers)", min_value=0, step=1)
    weight = st.number_input("Weight in metric ton (in 1000 Kg)", min_value=0, step=1)
    truck_types = ['Trailer', 'Bulker', 'Truck']
    truck_type = st.selectbox('Select Vehicle Type', truck_types)
    if(truck_type == "Bulker"):
        is_bulk_cement = "Yes"
    else:
        is_bulk_cement = "No"
    reverse_logistics = st.radio("Reverse Haulage applicable? (Will be pulled from purchase register) ", ["Yes", "No"])
    submit_button = st.button('Submit')
    if submit_button:
       
        cost_headers_values_dict, total_cost= new_calculator(distance,weight,truck_type,is_bulk_cement,reverse_logistics)
        temp = sorted(cost_headers_values_dict.items(),key=lambda item: item[1])
        keys = []
        values = []
        for key,value in temp:
            keys.append(key)
            values.append(value)     
        # st.write(f" Total cost for transportation =  {toal_cost}")
        # st.write (f"PTPK price = {toal_cost/(distance*weight)}")
        final_data = {'Total Price ': f"₹ {round(total_cost,2)}",'PTPK' : f" ₹ {round(total_cost/(distance*weight))}"}
        # final_data = {'Total Price ': f"₹ {toal_cost}"}
        dct = {k:[v] for k,v in final_data.items()}  # WORKAROUND
        new_dict = {}
        for key,value in cost_headers_values_dict.items():
            new_dict[key] = value*100 / total_cost
        
        finaldf = pd.DataFrame(dct)
        st.dataframe(finaldf,hide_index=True)
        # st.dataframe(percentage_df,hide_index=True)
        # st.write(finaldf.style.hide())
        
        st.plotly_chart(make_graph(keys,values))







        
  
    

if __name__ == "__main__":
    main()


 



