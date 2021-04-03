import requests
import json

class FactSheets:
    def __init__(self,lix):
        """Base class for LeanIX Factsheet

        Arguments:
            lix LeaxIX Class -- instantiated from the overall class, receives the class for data passing
        """
        self.lix = lix
        self.applications = Applications(self.lix)
        self.providers = Providers(self.lix)
        self.factsheettypes = [
                            'BusinessCapability',
                            "Process",
                            "UserGroup",
                            "Project",
                            "Application",
                            "Interface",
                            "DataObject",
                            "ITComponent",
                            "Provider",
                            "TechnicalStack"
                        ]
    
    def __repr__(self):
        return f"Factsheets wrapper for {self.lix}"

    def deleteByNameAndType(self,name,fstype,comment,validateOnly=False):
        """Archives factsheet given the name and type

        Arguments:
            name {string} -- Fact Sheet Name
            fstype {string} -- Fact Sheet Type
            comment {string} -- Reason for deletion

        Keyword Arguments:
            validateOnly {bool} -- Set validateOnly flag on call for testing (default: {False})

        Returns:
            json -- Return status from delete request
        """
        fsid = self.getIdByNameAndType(name,fstype)
        if fsid:
            return self.delete(fsid,comment,validateOnly)
        else:
            return None

    def delete(self,fsid,comment="No Comment Provided",validateOnly=False):
        """Archives factsheet by ID """

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

    def update(self,fsid,attributes,comment,validateOnly=False):
        """ Apply the patches described in the "attributes" dict to the factsheet by the factsheetID """

        gql = """mutation (
                                $fsid: ID!, 
                                $patches: [Patch]!,
                                $comment:String!,
                                $validateOnly: Boolean
                            )
                            {
                                updateFactSheet(
                                    id:$fsid,
                                    patches:$patches,
                                    comment:$comment,
                                    validateOnly:$validateOnly
                                    )
                                {
                                    factSheet
                                    {
                                    id
                                    name
                                    updatedAt
                                    }
                                }
                            }
                            """
        gvars = {
                    "fsid": fsid,
                    "comment": comment,
                    "validateOnly": validateOnly,
                    "patches": []
                  
                }

        for key,value in attributes.items():
            patch ={
                        "op": attributes[key].get("op","add"),
                        "path": key,
                        "value": attributes[key].get("value","")
                    }
            gvars['patches'].append(patch)

        

        return self.lix.graph.execGraphQLTrimmed(gql,gvars)

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

    def getAllByType(self,fstype):
        """ Gets FactSheets by type """

        gquery = """query ($typename: FactSheetType!) {
                    allFactSheets(factSheetType: $typename) {
                        totalCount
                        edges {
                        node {
                            id
                            displayName
                            name
                            type
                            status
                        }
                        }
                    }
                    }        
        """
                        
        gvars = {
            "typename": fstype
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

    def getTagIdByNameAndGroup(self,tagname,taggroup):
        """Gets the TagID given the name and group.  For NoGroup, specify None as the taggroup

        Arguments:
        tagname string -- Name of tag
        taggroup string -- Name of tag group"""


        gql = """query ($tagfilter: TagQueryFilters!) {
                    allTags(filter: $tagfilter) {
                        edges {
                        node {
                            id
                            name
                            
                            }
                        }
                    }
                }"""

        gvars = {
                    "tagfilter": {
                        "tagGroupName": taggroup,
                        "nameSubstring": tagname
                    }
                }

        results = self.lix.graph.execGraphQLTrimmed(gql,gvars)
        for tag in results['data']['allTags']:
            if tag['name'] == tagname:
                return tag['id']

    def addTagToFactsheet(self,fsid=None,fsname=None,fstype=None,tagname=None,taggroup=None,tagid=None,validateOnly=False):
        """Adds the specified tag to the deisgnated factsheet

        Keyword Arguments:
        fsid (guid) -- Factsheet ID of the factsheet to add tag to.  Either fsid or fsname and fstype must be specified
        fsname string -- Name of factsheet. Must also provide type
        fstype string -- Factsheet type, used with name, not used if fsid specified
        tagname string -- Name of Tag, used with taggroup, not used of tagid spefcified
        taggroup string -- Tag Group, used with name, not used of tagid spefcified
        tagid guid -- tagid to add
        """

        if not fsid:
            """ if fsid not specified, look up the id based on name and group """
            fsid = self.getIdByNameAndType(name=fsname,fstype=fstype)

        if not tagid:
            tagid = self.getTagIdByNameAndGroup(tagname,taggroup)

        

        gql = """mutation ($patches: [Patch]!, $fsid: ID!, $validate: Boolean!) {
                    result: updateFactSheet(id: $fsid, patches: $patches, validateOnly: $validate) {
                        factSheet {
                        rev
                        name
                        tags {
                            id
                            name
                            color
                            description
                            tagGroup {
                            shortName
                            name
                            }
                        }
                        }
                    }
                    }"""
        tagpatch = {
            "tagId": tagid
        }

        gvars = {
                    "patches": [
                        {
                            "op":"add",
                            "path": "/tags",
                            "value": [json.dumps(tagpatch)]
                        }
                    ],
                    "fsid": fsid,
                    "validate": validateOnly
                }
        
        return self.lix.graph.execGraphQLTrimmed(gql,gvars)

        a=1
                                                

class Applications:

    def __init__(self,lix):
        """Base class for LeanIX Applications, inheriting from FactSheets

        Arguments:
            lix LeaxIX Class -- instantiated from the overall class, receives the class for data passing
        """
        self.lix = lix
        self.fstype = "Application"

    def __repr__(self):
        return f"Application wrapper for {self.lix}"

    def delete(self,fsname):
        """Archives the named Application Factsheet

        Arguments:
            fsname string
        """

        return self.lix.factsheets.deleteByNameAndType(name=fsname,type=self.fstype)

    def getByName(self,name):
        """Gets fact sheet by name

        Arguments:
            name {[type]} -- [description]
        """
        return self.lix.factsheets.getFactSheetByNameAndType(name=name,fstype=self.fstype)

    def getIdByName(self,name):
        return self.lix.factsheets.getIdByNameAndType(name=name, fstype=self.fstype)


class Providers(Applications):
    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Provider"