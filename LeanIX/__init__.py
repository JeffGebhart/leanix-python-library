import requests
import json
from .Graph import Graph
from .FactSheets import FactSheets

class LeanIX:
    def __init__(self,api_token="",workspaceid="",baseurl="https://us.leanix.net/"):
        """ Authenticates to LeanIX with the given API Token and returns the Authorization header for use in future calls """
        self.__api_token = api_token
        self.workspaceid = workspaceid
        self.baseurl = baseurl
        if not self.baseurl.endswith("/"):
            self.baseurl += "/"                 # If URL is not passed in with a trailing /, add it

        self.auth()
        self.graph = Graph(self)
        self.factsheets = FactSheets(self)

    def __repr__(self):
        return f"LeanIX Object for {self.workspaceid}"

    def auth(self):
        """Authenticate to LeanIX using the API token in the class"""

        auth_url = f"{self.baseurl}/services/mtm/v1/oauth2/token"

        response = requests.post(auth_url, auth=('apitoken', self.__api_token),
                                data={'grant_type': 'client_credentials'})
        response.raise_for_status() 
        self._access_token = response.json()['access_token']
        
        self._auth_header = 'Bearer ' + self._access_token
        self.header = {'Authorization': self._auth_header}

