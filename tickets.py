import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


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

    ticketstatusframe = StructurizeTickets(tickets, techs)

    ticketstatusframe["total"] = [(row["New"] + row["On hold"] + row["In progress"]) for index, row in ticketstatusframe.iterrows()]

    return ticketstatusframe

if __name__ == "__main__":
    Main()