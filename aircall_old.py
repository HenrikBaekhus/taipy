from http.client import HTTPSConnection
from base64 import b64encode
import json
import sys
from plyer.utils import platform
from plyer import notification

username = "10dac6e933c08fa904244284616d86c1"
password = "d6b54750f0b525236a5813441fd92c8d"
defaultteam = "Daytime CET"

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def APIQuery(query, c, headers):
    c.request('GET', '/v1/' + query, headers=headers)
    return c.getresponse()

def Query(query):
    c = HTTPSConnection("api.aircall.io")
    #then connect
    headers = { 'Authorization' : basic_auth(username, password) } 
    return APIQuery(query, c, headers)

def GetTeamMembers(teamname):
    print("hello")

def Main(teamsearch=defaultteam):
    
    #get the response back
    res = Query("teams")
    # at this point you could check the status etc
    # this gets the page text
    data = res.read()
    jsonfile = json.loads(data)
    validteam = False
    teamlist = []
    for team in jsonfile["teams"]: 
        if (team["name"] == teamsearch):
            validteam = True
            teammatch = team
        teamlist.append(team["name"])

    if not(validteam):
        print("Team \"" + teamsearch + "\" not found. You can choose from these teams: ")
        for t in teamlist:
            print("- " + t)
    else:
        userlist = {}
        for u in teammatch["users"]:
            userlist[u["id"]] = u["name"]

        userres = Query("users")
        userdata = userres.read()
        jsonfile = json.loads(userdata)
        userstatus = {}
        for u in range(len(jsonfile["users"])):
            userstatus[(jsonfile["users"][u]["id"])] = str(jsonfile["users"][u]["availability_status"])

        availableuser = []

        for status in userlist:
            if (userstatus[status] == "available"): 
                availableuser.append(userlist[status])
        if (len(availableuser) > 0):
            msg = "These resources are currently available on the 24/7 support!\n"
            for avail in availableuser:
                msg += "- " + avail + "\n"
        else:
            msg = "WARNING! NO OPERATORS CURRENTLY ON THE 24/7 SUPPORT!"

        notification.notify(
        title='24/7 support',
        message=msg,
        app_name='Aircall',
        app_icon='C:/Git/Aircall/bulb.ico'.format(
            # On Windows, app_icon has to be a path to a file in .ICO format.
            'ico' if platform == 'win' else 'png'
            )
        )



if __name__ == "__main__":
    if (len(sys.argv) > 1):
        Main(sys.argv[1])
    else:
        Main()