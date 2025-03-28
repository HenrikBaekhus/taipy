import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import time
import os
import datetime

class JitBit:
    def __init__(self):
        self.authentication = HTTPBasicAuth('support@prediktor.com', 'LHi1XHSJgCEs')

    def apiquery(self, request):
        url = f"https://support.prediktor.com/helpdesk/api/{request}" 
        response = requests.get(url, auth=self.authentication)
        result = json.loads(response.content)
        result = pd.json_normalize(result)
        return result

def StructurizeTickets(pdtickets, pdtechs):

    grouped = pdtickets["AssignedToUserID"].value_counts()
    grouped.to_frame

    groupresponse = pdtickets.groupby(["AssignedToUserID"]).agg({
        'UpdatedByUser': 'sum'}).reset_index()

    statuses = ["New", "On hold", "In progress"]
    ticketcolumn = ["Technichian", "New", "On hold", "In progress", "Response"]
    ticketstatus = []

    for key in grouped.keys():
        person = pdtechs.loc[pdtechs["UserID"] == key]["FullName"].squeeze()
        response = groupresponse.loc[groupresponse["AssignedToUserID"] == key]["UpdatedByUser"].squeeze()

        newframe = (pdtickets.loc[pdtickets["AssignedToUserID"] == key][["IssueID", "Status", "UpdatedByUser"]])
        newtickets = newframe["Status"].value_counts()

        entrylist = []
        entrylist.append(person)

        for stat in statuses:
            try:
                entrylist.append(newtickets[stat].squeeze())
            except:
                entrylist.append(0)

        entrylist.append(response)
        ticketstatus.append(tuple(entrylist))

    ticketstatusframe = pd.DataFrame(ticketstatus, columns=ticketcolumn)

    return ticketstatusframe

def Structure():

    apiconnect = JitBit()
    tickets = apiconnect.apiquery("Tickets?mode=unclosed&count=300")    
    techs = apiconnect.apiquery("users?listMode=techs")

    unassigned = str(sum(tickets["Technician"].isnull()))

    ticketstatusframe = StructurizeTickets(tickets, techs)

    ticketstatusframe["total"] = [(row["New"] + row["On hold"] + row["In progress"]) for index, row in ticketstatusframe.iterrows()]

    if os.path.isfile("ticketstatus.xlsx"):
        checkfile = pd.read_excel("ticketstatus.xlsx")
        if (checkfile.to_string() == ticketstatusframe.to_string()):
            print(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: No changes to previous tickets!")
        else:
            ticketstatusframe.to_excel("ticketstatus.xlsx", index=False)
            print(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Ticket file has been updated!")
    else:
        ticketstatusframe.to_excel("ticketstatus.xlsx", index=False)

    if os.path.isfile("unassigned.txt"):
        with open("unassigned.txt", "r") as file:
            file = file.read()
        if (unassigned.strip() == file.strip()):
            print(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: No changes to unassigned tickets!")
        else:
            with open("unassigned.txt", "w") as file:
                file.write(unassigned)
            print(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Unassigned file updated!")
    else:
        with open("unassigned.txt", "w") as file:
            file.write(unassigned)

#    return ticketstatusframe

if __name__ == "__main__":
#    Structure()

    while(True):
        Structure()
        time.sleep(10)
