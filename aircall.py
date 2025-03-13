from base64 import b64encode
from http.client import HTTPSConnection
import json
import pandas as pd

class Connect:
    def __init__(self):
        username = "10dac6e933c08fa904244284616d86c1"
        password = "d6b54750f0b525236a5813441fd92c8d"
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        token = f"Basic {token}"
        self.apiconnect = HTTPSConnection("api.aircall.io")
        self.headers = { 'Authorization' : token, 'Connection' : 'close' } 

    def Query(self, query):
        self.apiconnect.request('GET', '/v1/' + query, headers=self.headers)
        result = self.apiconnect.getresponse()
        self.data = result.read()

    def JsonToPanda(self):
        jsonfile = json.loads(self.data)
        return jsonfile

def GetAvailable():
    connect = Connect()
    connect.Query("teams")    
    result = connect.JsonToPanda()
    jsonfile = json.dumps(result["teams"][0]["users"])        
    teams = pd.read_json(jsonfile)

    connect.Query("users")
    result = connect.JsonToPanda()
    jsonfile = json.dumps(result["users"])
    users = pd.read_json(jsonfile)

    available = (users.loc[users["available"] == True])
    available247 = teams.loc[teams["id"].isin(available["id"].tolist())]
    
    return (available247[["id", "name"]])

if __name__ == "__main__":
    Main()