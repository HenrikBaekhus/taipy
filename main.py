import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import cos, exp
import json
import requests
from requests.auth import HTTPBasicAuth
import string

def Plot(page):

    pass
#    tgb.chart("{data}", selected="{selected_indices}", layout="{layout}", plot_config="{config}")

def JitBit():

#    pd.set_option('future.no_silent_downcasting', True)

    authentication = HTTPBasicAuth('support@prediktor.com', 'LHi1XHSJgCEs')

    url = "https://support.prediktor.com/helpdesk/api/users?listMode=techs"
    responsetechs = requests.get(url, auth=authentication)
    url = "https://support.prediktor.com/helpdesk/api/Stats?forCurrentUser=false"
    state = requests.get(url, auth=authentication)
    url = "https://support.prediktor.com/helpdesk/api/Tickets?mode=unclosed&count=300"
    responsetickets = requests.get(url, auth=authentication)

    techresult = json.loads(responsetechs.content)
    ticketresult = json.loads(responsetickets.content)
    stateresult = json.loads(state.content)
    pdtechs = pd.json_normalize(techresult)
    pdtickets = pd.json_normalize(ticketresult)
    pdstate = pd.json_normalize(stateresult)

    grouped = pdtickets["AssignedToUserID"].value_counts()   
    grouped.to_frame
 
    statuses = ["New", "On hold", "In progress"]
    ticketcolumn = ["tech", "New", "On hold", "In progress"]
    ticketstatus = []

    for key in grouped.keys():
        person = pdtechs.loc[pdtechs["UserID"] == key]["FullName"].squeeze()

        newframe = (pdtickets.loc[pdtickets["AssignedToUserID"] == key][["IssueID", "Status", "UpdatedByUser"]])        
        newtickets = newframe["Status"].value_counts()

        entrylist = []
        entrylist.append(person)

        for stat in statuses:
            try:
                entrylist.append(newtickets[stat].squeeze())
            except:
                entrylist.append(0)

        ticketstatus.append(tuple(entrylist))

    ticketstatusframe = pd.DataFrame(ticketstatus, columns=ticketcolumn)

    Barcharts(ticketstatusframe) 

def Barcharts(data):

    def change_category(state):
        # Do nothing for now, we will implement this later
        return None

    data = pd.read_csv("data.csv")
    categories = list(data["Category"].unique())
    selected_category = categories[1]


    chart_data = (
        data.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
    )

    layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}

    with tgb.Page() as page:
        tgb.selector(value="{selected_category}", lov="{categories}", on_change=change_category)
        tgb.chart(
            data="{chart_data}",
            x="Sales",
            y="State",
            type="bar",
            layout="{layout}",
            orientation='h'
            
        )
        tgb.table(data="{data}")

    Gui(page=page).run(title="Barchart example")

def Graph():

    

    value = 10

    def compute_data(decay:int)->list:
        return [cos(i/6) * exp(-i*decay/600) for i in range(10)]
    #    return [1, 3, 5, 3, 1]

    def slider_moved(state):
        state.data = compute_data(state.value)

    value = 0

    with tgb.Page() as page:
        tgb.text(value="# Taipy Graph example", mode="md")
        tgb.text(value="Value: {value}")
        tgb.slider(value="{value}", min=-100, max=100, on_change=slider_moved)
        tgb.chart(data="{data}")

    data = compute_data(value)

    Gui(page=page).run(title="Dynamic chart example")

def Main():

    def on_button_action(state):
        notify(state, 'info', f'The text is: {state.text}')
        state.text = "Button pressed"

    def on_change(state, var_name, var_value):
        if var_name == "text" and var_value == "Reset":
            state.text = ""
            return


    text = "Original text"
    slidenumber = 5
    
    with tgb.Page() as page:
        
        tgb.text("# *24/7 support*", mode="md")
        tgb.text("My text: {text}")
        tgb.slider("{slidenumber}", min=1, max=10)
        tgb.text("Your current number is: {slidenumber}") 
        tgb.input("{slidenumber}")
        tgb.button("Run local", on_action=on_button_action)

        Plot(page)

    Gui(page).run(
            debug=True, 
            port=5002, 
            use_reloader=True, 
            dark_mode=False, 
            title="27/7 Support",
            margin="4em",
            watermark="Henrik"
            ) # use_reloader=True

if __name__ == "__main__":
    JitBit()
#    Barcharts()
#    Graph()
#    Main()

    