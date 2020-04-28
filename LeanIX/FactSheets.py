import requests
import json

class FactSheets:
    def __init__(self,lix):
        """ Pass in the parent LeanIX object to have access to all of the methods and data
        """
        self.lix = lix
    
    def __repr__(self):
        return f"Factsheets wrapper for {self.lix}"

    def delete(self,fsid,comment="No Comment Provided",validateOnly=False):
        gql = """mutation ($fsid: ID!,$patches:[Patch]!,$validateOnly: Boolean!,$comment: String!)
                    {
                        updateFactSheet(id:$fsid, patches:$patches,validateOnly:$validateOnly,comment:$comment)
                        {
                            factSheet
                            {
                                name
                                id
                                status
                            }
                        }
                    }"""

        gvars = {
                    "fsid": fsid,
                    "patches": [
                        {
                            "op":"add",
                            "path": "/status",
                            "value": "ARCHIVED"
                        }
                    ]
                    ,"validateOnly": validateOnly,
                    "comment": comment
                }
        delfs = self.lix.graph.execGraphQLTrimmed(gql,gvars)
        return delfs

        
        

    def create(self,name,fstype,attributes={},validateOnly=False):
        """ Creates a fact sheet based on name and type, and applies the Key/Value pairs in attributes to it """

        gqlvar = {"validateOnly":validateOnly}

        patches = []
        gqlvar['input'] = {
            "name": name,
            "type": fstype
        }

        for key,value in attributes.items():
            patches.append({
                "op": "add",
                "path": key,
                "value": value
            })
        gqlvar['patches'] = patches

        gquery = """mutation ($input:BaseFactSheetInput!, $patches:[Patch],$validateOnly: Boolean)
                    {
                        createFactSheet(input: $input,patches:$patches,validateOnly:$validateOnly)
                        {
                            factSheet 
                            {
                                id
                                name
                            }
                        }
                    }"""

        newfs = self.lix.graph.execGraphQLTrimmed(gquery,gqlvar)

        return newfs




    
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
                                            status
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
