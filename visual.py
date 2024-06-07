

import plotly.express as px
import pandas as pd
from random import randint
import matplotlib.pyplot as plt

import decimal




# def make_graph(cost_headers,values):
#     n = len(cost_headers)
    
#     colors = ['#%06X' % randint(0, 0xFFFFFF) for _ in range(n)]
#     df = pd.DataFrame({'Cost Header': cost_headers, 'Value': values})
#     # fig = px.bar(df, x='Value', y='Cost Header', orientation='h', title='Cost Headers vs. Values', color = (cost_headers))
#     fig = px.bar(df, x='Value', y='Cost Header', orientation='h', color = (cost_headers))


#     return fig



import pandas as pd
import plotly.express as px
from random import randint

def make_graph(cost_headers, values):
    n = len(cost_headers)
    
    colors = ['#%06X' % randint(0, 0xFFFFFF) for _ in range(n)]
    df = pd.DataFrame({'Cost Header': cost_headers, 'Value': values})
    fig = px.bar(df, x='Value', y='Cost Header', orientation='h', color=cost_headers)



    # Add value labels to the bars
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['Value'],
            y=row['Cost Header'],
            text=str(round(row['Value'],0)),  # Display the value as text
            showarrow=False,
            font=dict(size=12, color='black'),  # Customize font size and color
        )

    return fig










def stacked_bar_graph(cost_headers,values):
    n = len(cost_headers)
    colors = ['#%06X' % randint(0, 0xFFFFFF) for _ in range(n)]
    x= ["Total Cost"]
    plt.bar(x, [values[0]], color=colors[0],label = cost_headers[0])
    for i in range(1,len(values)):
        plt.bar(x,[values[i]],color = colors[i],bottom=[values[i-1]],label = cost_headers[i])
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Stacked Bar Chart')
    plt.legend(fontsize = 7 )
    return plt
    

# stacked_bar_graph(["a","b"],[1,2]).show()


  




