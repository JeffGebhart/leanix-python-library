import requests
import json


class Graph:
    def __init__(self,lix):
        
        self.header = lix.header
        self.lix = lix
        self.baseurl = lix.baseurl
        self.service = 'services/pathfinder/v1/'
        self.method = 'graphql'
        self.url = self.baseurl+self.service+self.method

    def __repr__(self):
        return f"GraphQL wrapper for {self.lix}"

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