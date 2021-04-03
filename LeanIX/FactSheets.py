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
        self.businesscapabilities = BusinessCapability(self.lix)
        self.process = Process(self.lix)
        self.usergroup = UserGroup(self.lix)
        self.project = Project(self.lix)
        self.interface = Interface(self.lix)
        self.dataobject = DataObject(self.lix)
        self.itcomponent = ITComponent(self.lix)
        self.technicalstack = TechnicalStack(self.lix)
        self.taggroups = {}
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

    def getByID(self,fsid,attributes):
        """ gets individual FS by id """
        gquery = """query ($fsid: ID!) {
                        factSheet(id: $fsid) {
                            ##ADDITIONALATTRIBS##
                            id
                            displayName
                            name
                            type
                            status
                            category
                            tags {
                            id
                            name
                            tagGroup {
                                id
                                name
                            }
                            }
                        }
                        }
                                        """.replace("##ADDITIONALATTRIBS##",attributes)
        gvars = {
            "fsid": fsid
        }
        return self.lix.graph.execGraphQLTrimmed(gquery,gvars)    

    def getall(self,fstype,attributes=""):
        """ Gets FactSheets by type """

        gquery = """query ($fstype: [String]!) {
                    allFactSheets(filter: {facetFilters: [{facetKey: "FactSheetTypes", keys: $fstype}]}) {
                        totalCount
                        edges {
                        node {
                            ##ADDITIONALATTRIBS##
                            id
                            displayName
                            name
                            type
                            status
                            category
                            tags {
                            id
                            name
                            tagGroup{
                                id
                                name
                            }
                            }
                        }
                        }
                    }
                    }
                        """.replace("##ADDITIONALATTRIBS##",attributes)
                        
        gvars = {"fstype":[fstype] }

        return self.lix.graph.execGraphQLTrimmed(gquery,gvars)      

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
    
    def createTagInGroup(self,tagname,taggroup,validateOnly=False):
        if not self.taggroups:

            gql="""{
                        allTagGroups {
                        edges {
                        node {
                            id
                            name
                        }
                        }
                    }
                    }"""
            taggroups = self.lix.graph.execGraphQLTrimmed(gql)
            tglist = {}
            for tg in taggroups['data']['allTagGroups']:
                tglist[tg['name'].lower()] = tg
            
            self.taggroups = tglist
        
        tgid = self.taggroups[taggroup.lower()]['id']

        gql2 = """mutation ($name: String!, $tgid: ID!, $validateOnly: Boolean!) {
                    createTag(name: $name, tagGroupId: $tgid, validateOnly: $validateOnly) {
                        id
                        name
                    }
                    }"""
        gvars2 = {
            "name":tagname,
            "tgid": tgid,
            "validateOnly": validateOnly
        }
        return self.lix.graph.execGraphQLTrimmed(gql2,gvars2)['data']['createTag']['id']
        




    def addTagToFactsheet(self,fsid=None,fsname=None,fstype=None,tagname=None,taggroup=None,tagid=None,addIfNotExist=True,validateOnly=False,replaceIfExists=True):
        """Adds the specified tag to the deisgnated factsheet

        Keyword Arguments:
        fsid (guid) -- Factsheet ID of the factsheet to add tag to.  Either fsid or fsname and fstype must be specified
        fsname string -- Name of factsheet. Must also provide type
        fstype string -- Factsheet type, used with name, not used if fsid specified
        tagname string -- Name of Tag, used with taggroup, not used of tagid spefcified
        taggroup string -- Tag Group, used with name, not used of tagid spefcified
        tagid guid -- tagid to add
        addIfNotExist boolean -- Whether to create tag in taggroup if it doesn't exist
        """

        if not fsid:
            """ if fsid not specified, look up the id based on name and group """
            fsid = self.getIdByNameAndType(name=fsname,fstype=fstype)

        if not tagid:
            tagid = self.getTagIdByNameAndGroup(tagname,taggroup)
            if not tagid:   # No tag ID found
                if addIfNotExist:       # Add tag to group if it doesn't exist
                    tagid = self.createTagInGroup(tagname,taggroup)
        


        

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
        
        result = self.lix.graph.execGraphQLTrimmed(gql,gvars)
        if replaceIfExists:
            if result['errors']:
                if result['errors'][0]['errorType'] == 'CONSTRAINT_VIOLATION':
                    # Tag exists already, need to remove it and readd
                    fs = self.getByID(fsid,"")
                    taglist = []
                    for t in fs['data']['factSheet']['tags']:
                        if t['tagGroup']['name'].lower() == taggroup.lower():   # The one to replace
                            taglist.append({
                                "tagId": tagid

                            })
                        else:                                                      # Other tags, just retain them
                            taglist.append({
                                "tagId": t['id']
                            })
                    
                    gvars['patches'] = [
                        {
                            "op": "replace",
                            "path":"/tags",
                            "value": json.dumps(taglist)
                        }
                    ]
                    result = self.lix.graph.execGraphQLTrimmed(gql,gvars)
                    





                    aaa=1
        return result


        a=1

    def addDocumentToFactsheet(self,fsid,url,docname="",description="",validateOnly=False)                                             :

        gquery = """mutation ($fsid: ID!, $docname: String!, $url: String!,$desc: String!, $validateOnly: Boolean!){
                            createDocument(factSheetId: $fsid, name: $docname, url: $url, description: $desc, validateOnly: $validateOnly) {
                                id
                                name
                                description
                                factSheetId
                            }
                            }"""
        gqlvar = {
            "fsid": fsid,
            "docname": docname,
            "url": url,
            "desc": description,
            "validateOnly": validateOnly
        }

        return self.lix.graph.execGraphQLTrimmed(gquery,gqlvar)

    def addSubscription(fsid,email,rolename,roletype):
        gvars = {
                    "fsid": fsid,
                    "user": {
                        "email":email
                    },
                    "role": [
                        getIDforRole(roleName)
                    ],
                    "subtype": roletype
        }
        roletype = roletype.upper()
        gql = """mutation ($fsid: ID!,
                        $user: UserInput!,
                            $role: [ID!],$subtype: String!) {
                        createSubscription(factSheetId: $fsid, 
                                user: $user, 
                                type: $subtype, 
                                validateOnly: false, 
                                roleIds: $role) 
                        {
                            id
                        }

                        }"""

        return self.lix.graph.execGraphQLTrimmed(gql,gqlvars)

        pass


    # def addSubscriberToFactsheet(self,fsid=None,fsname=None,fstype=None,subscriber="",role=""):
    #     """Adds a subscriber to a factsheet """
    #     if not fsid:
    #         """ if fsid not specified, look up the id based on name and group """
    #         fsid = self.getIdByNameAndType(name=fsname,fstype=fstype)

    #     subs = """    subscriptions {
    #                         edges {
    #                             node {
    #                             id
    #                             user {
    #                                 email
    #                                 id
    #                             }
    #                             roles{
    #                                 id
    #                                 name
    #                             }
    #                             }
    #                         }
    #                         }
    #                         """

    #     fs = self.getByID(fsid,subs)['data']['factSheet']
        
    #     if not fs['subscriptions']:     # No subs, no need to check
    #         pass

    #     else:
    #         foundsub = False
    #         for sub in fs['subscriptions']:
    #             if sub['user']['email'].lower() == subscriber.lower():
    #                 foundsub = True
    #                 for rol in sub['roles']:
    #                     if not rol['name'].lower() == role.lower():

class Applications:

    def __init__(self,lix):
        """Base class for LeanIX Applications, inheriting from FactSheets
        Also acts as a base for all other fact sheet types

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

    def getAll(self,attributes=""):
        """ Get all fact sheets of the type """
        return self.lix.factsheets.getall(fstype=self.fstype,attributes=attributes)

    def getByName(self,name):
        """Gets fact sheet by name

        Arguments:
            name {[type]} -- [description]
        """
        return self.lix.factsheets.getFactSheetByNameAndType(name=name,fstype=self.fstype)

    def getIdByName(self,name):
        return self.lix.factsheets.getIdByNameAndType(name=name, fstype=self.fstype)

    def create(self,name,attributes={},validateOnly=False):
        """ Creates a new factsheet of the specified type """
        # def create(self,name,fstype,attributes={},validateOnly=False):

        return self.lix.factsheets.create(name=name,fstype=self.fstype,attributes=attributes,validateOnly=validateOnly)

class Providers(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Provider"

class BusinessCapability(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="BusinessCapability"

class Process(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Process"

class Providers(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Provider"

class UserGroup(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="UserGroup"

class Project(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Project"

class Interface(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="Interface"

class DataObject(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="DataObject"

class ITComponent(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="ITComponent"

    def create(self,name,attributes={},validateOnly=False,category="Hardware"):
        """ Special override to add the "Category" attribute to ITComponent adds """

        attributes['/category'] = category
        return self.lix.factsheets.create(name=name,fstype=self.fstype,attributes=attributes,validateOnly=validateOnly)

class TechnicalStack(Applications):

    def __init__(self,lix):
        super().__init__(lix)
        self.fstype="TechnicalStack"