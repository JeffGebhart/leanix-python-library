import requests
import json

class LeanIX:
    def __init__(self,api_token="",workspaceid="",baseurl="https://us.leanix.net"):
        """ Authenticates to LeanIX with the given API Token and returns the Authorization header for use in future calls """
        self.api_token = api_token
        self.workspaceid = workspaceid
        self.baseurl = baseurl

        self.auth()
        self.graph = Graph(self)
        self.factsheets = FactSheets(self)

    def auth(self):
        """Authenticate to LeanIX using the API token in the class"""

        auth_url = f"{self.baseurl}/services/mtm/v1/oauth2/token"

        response = requests.post(auth_url, auth=('apitoken', self.api_token),
                                data={'grant_type': 'client_credentials'})
        response.raise_for_status() 
        self.access_token = response.json()['access_token']
        
        self.auth_header = 'Bearer ' + self.access_token
        self.header = {'Authorization': self.auth_header}


class Graph:
    def __init__(self,lix):
        
        self.header = lix.header
        self.lix = lix
        self.baseurl = lix.baseurl
        self.service = 'services/pathfinder/v1/'
        self.method = 'graphql'
        self.url = self.baseurl+self.service+self.method

    def execGraphQL(self,query,variables={}):
        """Send the query and variables to the GQL endpoint
        Return the raw response"""

        # Remove \n's from Query:
        query = query.replace("\n"," ")
        req = {"query":query}
        req['variables'] = variables

        response = requests.post(self.url,headers=self.header,data=json.dumps(req))
        
        #response = requests.post(self.url,headers={},data=json.dumps(req))
        if response.status_code == 200:
            return response
        else:
            # Try reauthenticating if the token has expired
            self.lix.auth()
            self.header = self.lix.header
            response = requests.post(self.url,headers=self.header,data=json.dumps(req))
            response.raise_for_status()
            return response

    def execGraphQLParsed(self,query,variables={}):
        """Send the GQL to the endpoint.  Convert the response JSON to a dict"""

        response = self.execGraphQL(query,variables)
        
        return json.loads(response.text)
    
    def execGraphQLTrimmed(self,query,variables={}):
        """Send the GQL to the endpoint, convert to dict, trim the "edges" and "node" tags"""
        return self.trimResults(self.execGraphQLParsed(query,variables=variables))

    def trimResults(self,results):
        """Trims out all the "node" and "edge" keys from a graph resultset to make it a bit easier to work with the results.
        Works by recursively walking down the result dictionary and trimming out the extra levels, bringing the lower levels up.
        """
        if type(results) == type({}): # Drill down on Dicts
            resultdata = {}
            for i in results.keys():
                if i in ['edges','node']:
                    resultdata =  self.trimResults(results[i])
                else:
                    resultdata[i] = self.trimResults(results[i])
            return resultdata
        elif type(results) == type([]):
            resultdata = []
            for i in results:
                resultdata.append( self.trimResults(i))
            return resultdata

        else:
            return results

class FactSheets:
    def __init__(self,lix):
        """ Pass in the parent LeanIX object to have access to all of the methods and data
        """
        self.lix = lix
    
    def getByContainsName(self,name):
        """ Gets FactSheets by name, does a "contains" query of all factsheets """

        gquery = """query ($filter: FilterInput) 
                        {
                            allFactSheets(filter: $filter) 
                            {
                                totalCount
                                edges 
                                {
                                    node {
                                            id
                                            displayName
                                            name
                                            type
                                        }
                                }
                            }
                        }"""
                        
        gvars = {
            "filter": {"quickSearch": name}
        }

        return self.lix.graph.execGraphQLTrimmed(gquery,gvars)

    def getFactSheetByNameAndType(self,name,fstype):
        """ Returns the factsheet given a type and name """
        factsheets = self.getByContainsName(name)['data']['allFactSheets']

        for fs in factsheets:
            if fs['type'].lower() == fstype.lower():
                if fs['name'].lower() == name.lower():
                    return fs
        return None        

    def getIdByNameAndType(self,name,fstype):
        """ Returns the factsheet ID given a type and name """
        fs = self.getFactSheetByNameAndType(name,fstype)
        if fs:
            return fs['id']
        else:
            return None




